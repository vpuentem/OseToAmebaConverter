# coding=utf-8
"""OSE2Ameba_demand: Script to convert an OSE2000 database into Ameba CSV format.
_______________________________________________________________________________
Copyright (c) 2017 AMEBA-Dev - Consultora SPEC Limitada
This software cannot be distributed.
For more information, visit ameba.spec.cl
Current version developer: Ameba Team
_______________________________________________________________________________
"""
import argparse
import csv
import os
import datetime
from datetime import timedelta
import itertools
from operator import itemgetter

from generator import *
from parameters import *
from functions import *

"""_______________________________________________________________________________"""
""" INFLOW PARAMETERS """

FILE_OSE_EMB_1 = 'AflBioBioEtaSemRal.csv'
FILE_OSE_EMB_2 = 'AflChapoEtaSem.csv'
FILE_OSE_EMB_3 = 'AflLajaEtaSem.csv'
FILE_OSE_EMB_4 = 'AflMauleEtaSem.csv'
FILE_OSE_EMB_5 = 'AflRapelEtaSem.csv'
FILE_OSE_PAS = 'EnePasEtaMen.csv'

FILE_AMEBA_EMB = 'ele-profile_emb.csv'
FILE_AMEBA_PAS = 'ele-profile_pas.csv'

COLUMNS_OSE_EMB = ['AflNum', 'AflNom', 'AflAnoIni', 'AflAnoFin', 'AflIBlo', 'AflHid', 'AflEtaTip', 'AflDatTip', 'Sem01',
                   'Sem02', 'Sem03',
                   'Sem04', 'Sem05', 'Sem06', 'Sem07', 'Sem08', 'Sem09', 'Sem10', 'Sem11', 'Sem12', 'Sem13', 'Sem14',
                   'Sem15', 'Sem16', 'Sem17', 'Sem18', 'Sem19', 'Sem20',
                   'Sem21', 'Sem22', 'Sem23', 'Sem24', 'Sem25', 'Sem26', 'Sem27', 'Sem28', 'Sem29', 'Sem30', 'Sem31',
                   'Sem32', 'Sem33', 'Sem34', 'Sem35', 'Sem36', 'Sem37',
                   'Sem38', 'Sem39', 'Sem40', 'Sem41', 'Sem42', 'Sem43', 'Sem44', 'Sem45', 'Sem46', 'Sem47', 'Sem48']

COLUMNS_OSE_PAS = ['AflNum', 'AflNom', 'AflAnoIni', 'AflAnoFin', 'AflIBlo', 'AflHid', 'AflEtaTip',
                   'AflDatTip', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC', 'ENE', 'FEB', 'MAR']

INFLOW_NAME_AMEBA = 'name'
INFLOW_TIME_AMEBA = 'time'
INFLOW_SCENARIO_AMEBA = 'scenario'
INFLOW_VALUE_AMEBA = 'value'

COLUMNS_AMEBA = [INFLOW_NAME_AMEBA,
                 INFLOW_TIME_AMEBA,
                 INFLOW_SCENARIO_AMEBA,
                 INFLOW_VALUE_AMEBA]

DEC_NUM = 1

YEAR_PROFILE = '2017'


class ProfileInflow(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba_demand.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def __date_emb(self, date, year):
        week = int(date[3:5])
        month = WEEK_TO_MONTH[int(week)]
        if int(week) >= 37:
            # year=str(int(year)+1)
            day = (week - 36) - 4 * (month - 1)
        else:
            day = week - (month - 4) * 4
        return year + '-' + str(WEEK_TO_MONTH[week]).zfill(2) + '-' + str((day - 1) * 7 + 1).zfill(2) + '-' + '00:00'

    def __date_pas(self, month, year):
        month = MONTH_NUM[month]
        # if month < 4:
        # year=str(int(year)+1)
        return year + '-' + str(month).zfill(2) + '-01-00:00'

    def __get_eff(self, name, Dic1, Dic2):
        for eff in itertools.chain(Dic1, Dic2):
            if remove(name).upper() == remove(eff[GEN_NAME_OSE]).upper():
                return float(eff[GEN_EFF_OSE])

    def __convert_profile_emb(self):
        """Reads profiles from OSE2000 format and write Ameba profiles."""
        dic_emb_1 = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_INFLOW), FILE_OSE_EMB_1, self._ose_dir))
        dic_emb_2 = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_INFLOW), FILE_OSE_EMB_2, self._ose_dir))
        dic_emb_3 = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_INFLOW), FILE_OSE_EMB_3, self._ose_dir))
        dic_emb_4 = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_INFLOW), FILE_OSE_EMB_4, self._ose_dir))
        dic_emb_5 = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_INFLOW), FILE_OSE_EMB_5, self._ose_dir))

        directory = os.path.join(self._ameba_dir, DIR_AMEBA_INFLOW)
        check_directory(directory)

        writer_emb = writer_csv(os.path.join(DIR_AMEBA_INFLOW, FILE_AMEBA_EMB), COLUMNS_AMEBA, self._ameba_dir)
        writer_emb.writeheader()

        dic_emb = dic_emb_1 + dic_emb_2 + dic_emb_3 + dic_emb_4 + dic_emb_5
        inflow_emb = []

        for j in range(0, len(dic_emb)):
            if dic_emb[j][COLUMNS_OSE_EMB[1]] == dic_emb[j - 1][COLUMNS_OSE_EMB[1]]:
                hid = dic_emb[j][COLUMNS_OSE_EMB[0]]
                for i in range(8, len(COLUMNS_OSE_EMB)):
                    if i < 44:
                        value = round(float(dic_emb[j][COLUMNS_OSE_EMB[i]]), DEC_NUM)
                    else:
                        if hid == '5000' or '6000' or '7000':
                            value = round(float(dic_emb[j][COLUMNS_OSE_EMB[i]]), DEC_NUM)
                        else:
                            value = round(float(dic_emb[j - 1][COLUMNS_OSE_EMB[i]]), DEC_NUM)

                    inflow_emb.append({
                        INFLOW_NAME_AMEBA: 'Aflu_' + remove(dic_emb[j][COLUMNS_OSE_EMB[1]]),
                        INFLOW_TIME_AMEBA: self.__date_emb(COLUMNS_OSE_EMB[i], YEAR_PROFILE),
                        INFLOW_SCENARIO_AMEBA: 'hidrologia_' + dic_emb[j][COLUMNS_OSE_EMB[0]],
                        INFLOW_VALUE_AMEBA: value,
                    })

        inflow_emb = sorted(inflow_emb, key=itemgetter('time', 'name'))

        for inflow in inflow_emb:
            writer_emb.writerow(inflow)

    def __convert_profile_pas(self):
        """Reads profiles from OSE2000 format and write Ameba profiles."""

        dic_pas = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_INFLOW), FILE_OSE_PAS, self._ose_dir))

        if self._model in ['Ope','ope','OPE']:
            dic_eff1 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS), FILE_OSE_PAS_SIC_OPE_1,
                           self._ose_dir))
            dic_eff2 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS), FILE_OSE_PAS_SIC_OPE_2,
                           self._ose_dir))
        else: #if self._model in ['Opt','opt','OPT']:
            dic_eff1 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS), FILE_OSE_PAS_SIC_OPT_1,
                           self._ose_dir))
            dic_eff2 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS), FILE_OSE_PAS_SIC_OPT_2,
                           self._ose_dir))


        writer_pas = writer_csv(os.path.join(DIR_AMEBA_INFLOW, FILE_AMEBA_PAS), COLUMNS_AMEBA, self._ameba_dir)
        writer_pas.writeheader()

        for j in range(0, len(dic_pas)):
            if dic_pas[j][COLUMNS_OSE_PAS[1]] == dic_pas[j - 1][COLUMNS_OSE_PAS[1]]:
                for i in range(8, len(COLUMNS_OSE_PAS)):
                    hid = dic_pas[j][COLUMNS_OSE_PAS[0]]

                    if dic_pas[j][COLUMNS_OSE_PAS[7]] == 'DatCau':
                        if i < 17:
                            value = round(float(dic_pas[j][COLUMNS_OSE_PAS[i]]), DEC_NUM)
                        else:
                            if hid == '5000' or '6000' or '7000':
                                value = round(float(dic_pas[j][COLUMNS_OSE_PAS[i]]), DEC_NUM)
                            else:
                                value = round(float(dic_pas[j - 1][COLUMNS_OSE_PAS[i]]), DEC_NUM)
                    elif dic_pas[j][COLUMNS_OSE_PAS[7]] == 'DatEne':
                        eff = self.__get_eff(dic_pas[j][COLUMNS_OSE_PAS[1]], dic_eff1, dic_eff2)
                        if i < 17:
                            value = round(
                                float(dic_pas[j][COLUMNS_OSE_PAS[i]]) * 1000 / (MONTH_HRS[COLUMNS_OSE_PAS[i]] * eff),
                                DEC_NUM)
                        else:
                            if hid == '5000' or '6000' or '7000':
                                value = round(float(dic_pas[j][COLUMNS_OSE_PAS[i]]) * 1000 / (
                                MONTH_HRS[COLUMNS_OSE_PAS[i]] * eff), DEC_NUM)
                            else:
                                value = round(float(dic_pas[j - 1][COLUMNS_OSE_PAS[i]]) * 1000 / (
                                MONTH_HRS[COLUMNS_OSE_PAS[i]] * eff), DEC_NUM)
                    writer_pas.writerow({
                        INFLOW_NAME_AMEBA: 'Aflu_' + remove(dic_pas[j][COLUMNS_OSE_PAS[1]]),
                        INFLOW_TIME_AMEBA: self.__date_pas(COLUMNS_OSE_PAS[i], YEAR_PROFILE),
                        INFLOW_SCENARIO_AMEBA: 'hidrologia_' + dic_pas[j][COLUMNS_OSE_PAS[0]],
                        INFLOW_VALUE_AMEBA: value,
                    })

    def run(self):
        """Main execution point."""
        self.__convert_profile_emb()
        self.__convert_profile_pas()


def main():
    """Main program."""
    parser = argparse.ArgumentParser(description='OSE2000 to Ameba converter')
    parser.add_argument(
        'ose_dir', type=str, help='directory to read OSE2000 files from')
    parser.add_argument(
        'ameba_dir', type=str, help='directory to write Ameba files to')
    parser.add_argument(
        'model', type=str, help='select model to get data from (Opt or Ope)')
    args = parser.parse_args()
    ProfileInflow(args.ose_dir, args.ameba_dir, args.model).run()


if __name__ == '__main__':
    main()
