#!/usr/bin/env python
# -*- coding: latin-1 -*-


"""ose2ameba_emb: Script to convert an OSE2000 database into Ameba CSV format.
_______________________________________________________________________________
Copyright (c) 2017 AMEBA-Dev - Consultora SPEC Limitada
This software cannot be distributed.
For more information, visit ameba.spec.cl
Current version developer: Ameba Team
_______________________________________________________________________________
"""
#unicode (['UTF-8]')
import argparse
import csv
import os
import string
import itertools

from functions import *
from parameters import *

FILE_OSE_OPT_1='EmbDatParOpt.csv'
FILE_OSE_OPE_1='EmbDatParOpe.csv'

FILE_OSE_2='EmbDatEtaCot.csv'

FILE_AMEBA_1='ele-embPar-SIC_Cot.csv'
FILE_AMEBA_2='ele-embMax-SIC_Cot.csv'
FILE_AMEBA_3='ele-embMin-SIC_Cot.csv'

COLUMNS_AMEBA_1=['name','start_time','end_time','vmax','vmin','vini','vend']
COLUMNS_AMEBA_2=['name','time','value']

#columas OSE
COLUMNS_OSE_1=['EmbINum','EmbNom','EmbFOpe','EmbFecOpeIni','EmbFecOpeFin','EmbFRegEta','EmbFRegBlo','EmbKRegBlo','EmbConQGen',
'EmbConQVer','EmbConQFil','EmbCotIni','EmbCotFin','EmbCotMax','EmbCotMin','EmbCotMed','EmbRenSerCen','EmbRenSerVer','EmbConEva',
'EmbVolExp','EmbNwtFV2C','EmbNwtErr','EmbNwtNIte','EmbFFilMod','EmbFFilSim','EmbFFilOpt','EmbFEvaMod','EmbFEvaSim',
'EmbFEvaOpt','EmbCosQDef','EmbFInv','EmbFecInv','EmbVI','EmbCOMA','EmbVidUti','EmbSis','EmbEmp','EmbAux']
COLUMNS_OSE_2=['EmbINum','EmbA\xf1oFRlt','EmbA\xf1oIni','EmbA\xf1oFin','EmbNom','EmbDatTip',
'EmbDatIHid','EmbEtaTip','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']

MONTH_NUM = {'Ene': '01', 'Feb': '02', 'Mar': '03', 'Abr': '04', 'May': '05', 'Jun': '06',
'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12' }

class DamCot(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of ose2ameba_emb.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def _date_emb(self, date, F):
        if date =='*':
            if F is True:
                return '1970-01-01-00:00'
            else:
                return '3000-01-01-00:00'
        else:
            return'date'
    def _time_emb(self, month, year):
        month=MONTH_NUM[month]
        return year+'-'+month+'-'+'01-00:00'

    def _year_ini(self, year_ini, year_num):
        if year_num == '*':
            return int(year_ini)
        else:
            return int(year_ini)+int(year_num)-1
    def _year_end(self, year_ini,year_end, year_num):
        if year_num == '*':
            return int(year_end)
        else:
            return int(year_ini)+1
    def _convert_emb(self):
        """Reads emb from OSE2000 format and write Ameba emb."""
        if self._model in ['Ope','ope','OPE']:
            dic_EmbPar = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DAM), FILE_OSE_OPE_1, self._ose_dir))
        else: #if self._model in ['Opt','opt','OPT']:
            dic_EmbPar = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DAM), FILE_OSE_OPT_1, self._ose_dir))


        dic_EmbEta = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DAM), FILE_OSE_2, self._ose_dir))
        # TODO: Replace parameters list below with right list
        # If we integrate Ameba code we can import libraries with correct names

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_DAM)
        check_directory(directory)

        writer_1 = writer_csv(os.path.join(DIR_AMEBA_DAM,FILE_AMEBA_1), COLUMNS_AMEBA_1, self._ameba_dir)
        writer_max = writer_csv(os.path.join(DIR_AMEBA_DAM,FILE_AMEBA_2), COLUMNS_AMEBA_2, self._ameba_dir)
        writer_min = writer_csv(os.path.join(DIR_AMEBA_DAM,FILE_AMEBA_3), COLUMNS_AMEBA_2, self._ameba_dir)


        # TODO: Replace below correct column values
        """escribe la primera fila en formato Ameba"""
        writer_1.writeheader()
        writer_max.writeheader()
        writer_min.writeheader()
        """escribe el resto de las filas"""
        for emb in dic_EmbPar:

            writer_1.writerow({
            COLUMNS_AMEBA_1[0]:emb[COLUMNS_OSE_1[1]],
            COLUMNS_AMEBA_1[1]:self._date_emb(emb[COLUMNS_OSE_1[3]], True),
            COLUMNS_AMEBA_1[2]:self._date_emb(emb[COLUMNS_OSE_1[4]], False),
            COLUMNS_AMEBA_1[3]:'',
            COLUMNS_AMEBA_1[4]:'',
            COLUMNS_AMEBA_1[5]:'',
            COLUMNS_AMEBA_1[6]:'',
            })
        year_ini='2017'
        year_end='2030'

        for emb in dic_EmbEta:

            for j in range(self._year_ini(year_ini,emb[COLUMNS_OSE_2[2]]),
                    self._year_end(self._year_ini(year_ini,emb[COLUMNS_OSE_2[2]]),
                    year_end,emb[COLUMNS_OSE_2[2]])):
                if emb[COLUMNS_OSE_2[5]] == 'EmbCotMax':
                    for i in range(8,len(COLUMNS_OSE_2)):
                        if emb[COLUMNS_OSE_2[i]] != emb[COLUMNS_OSE_2[i-1]] or i==17:
                            writer_max.writerow({
                            COLUMNS_AMEBA_2[0]:remove(emb[COLUMNS_OSE_2[4]]),
                            COLUMNS_AMEBA_2[1]:self._time_emb(COLUMNS_OSE_2[i],str(j)),
                            COLUMNS_AMEBA_2[2]:emb[COLUMNS_OSE_2[i]],
                            })
                elif emb[COLUMNS_OSE_2[5]] == 'EmbCotMin':
                    for i in range(8,len(COLUMNS_OSE_2)):
                        if emb[COLUMNS_OSE_2[i]] != emb[COLUMNS_OSE_2[i-1]] or i==17:
                            writer_min.writerow({
                            COLUMNS_AMEBA_2[0]:remove(emb[COLUMNS_OSE_2[4]]),
                            COLUMNS_AMEBA_2[1]:self._time_emb(COLUMNS_OSE_2[i],str(j)),
                            COLUMNS_AMEBA_2[2]:emb[COLUMNS_OSE_2[i]],
                            })

    def run(self):
        """Main execution point."""
        self._convert_emb()
        print 'dam ready'


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
    DamCot(args.ose_dir, args.ameba_dir, args.model).run()


if __name__ == '__main__':
    main()
