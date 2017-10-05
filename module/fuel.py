# coding=utf-8
"""OSE2Ameba_fuel: Script to convert an OSE2000 database into Ameba CSV format.
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
from generator import *

from parameters import *
from functions import *

COLUMNS_OSE_FUEL_SIC=['CenNom','CenA\xf1oIni','CenA\xf1oFin','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']
COLUMNS_OSE_FUEL_SING=['CenNom','CenA\xf1oIni','CenA\xf1oFin','1','2','3','4','5','6','7','8','9','10','11','12']
COLUMNS_OSE_FUEL_TYPE=['CenEtaCVar','CenAux']

MONTH_NUM = {'Abr':4,'May':5,'Jun':6,'Jul':7,'Ago':8,'Sep':9,'Oct':10,'Nov':11,'Dic':12,'Ene':1,'Feb':2,'Mar':3}

COLUMNS_AMEBA=['name','start_time','end_time','fuel_type','fuel_price','scenario']
COLUMNS_AMEBA_2=['name','time','scenario','value']

YEAR_FLAG = False

FUEL_TYPE={
'Biomasa':'biomass',
'Biomasa-Licor Negro-Petroleo N6':'biomass',
'Biomasa-Petroleo N6':'biomass',
'Carbon':'coal',
'Desechos Forestales':'biomass',
'GNL':'gnl',
'Licor Negro-Petroleo N6':'biomass',
'Petroleo Diesel':'diesel',
'Petroleo IFO-180':'diesel',
'Gas Natural':'gas',
}

class Fuel(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba_fuel.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

        self._dic_fuel_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_FUEL_SIC,self._ose_dir))
        if self._model in ['Ope','ope','OPE']:
            self._dic_fuel_type_SIC_1 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPE_1, self._ose_dir))
            self._dic_fuel_type_SIC_2 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPE_2, self._ose_dir))
            self._dic_fuel_type_SIC_3 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPE_3, self._ose_dir))
        else: #if self._model in ['Opt','opt','OPT']:
            self._dic_fuel_type_SIC_1 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_1, self._ose_dir))
            self._dic_fuel_type_SIC_2 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_2, self._ose_dir))
            self._dic_fuel_type_SIC_3 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_3, self._ose_dir))

        self._dic_fuel_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_FUEL_SING, self._ose_dir))
        self._dic_fuel_type_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SING_1, self._ose_dir))

    def _dateIniOSE_fuel(self, year):
        """Fecha Inicio | formato OSE a AMEBA"""
        if year == '*':
            return '1970-01-01-00:00'
        elif YEAR_FLAG:
            return str(year)+'-01-01-00:00'
        return '1970-01-01-00:00'
    def _dateFinOSE_fuel(self, year):
        """Fecha Fin | formato OSE a AMEBA"""
        if year == '*':
            return '3000-01-01-00:00'
        else:
            return '3000-01-01-00:00'

    def _get_fuel_type(self, name, fuel_list):
        "@fuel_list: list of list of fueltypes"
        joined_fuel_list = [item for sublist in fuel_list for item in sublist]
        for fuel_type in joined_fuel_list:
            if name == remove(fuel_type[COLUMNS_OSE_FUEL_TYPE[0]]):
                return remove(fuel_type[COLUMNS_OSE_FUEL_TYPE[1]])
    def _get_month(self, month_OSE):
        return MONTH_NUM[month_OSE]

    def _date_ameba(self, year, month):
        if month==1 or month==2 or month==3:
            year=year+1
        return str(year)+'-'+str(month).zfill(2)+'-01-00:00'
    def _mes(self,i):
        if i == 12:
            return str(1).zfill(2)
        elif i == 13:
            return str(2).zfill(2)
        elif i == 14:
            return str(3).zfill(2)
        else:
            return str(i+1).zfill(2)

    def _convert_fuel(self):
        """Reads fuel from OSE2000 format and write Ameba fuel."""

        # If we integrate Ameba code we can import libraries with correct names
        directory = os.path.join(self._ameba_dir,DIR_AMEBA_FUEL)
        check_directory(directory)

        writer = writer_csv(os.path.join(DIR_AMEBA_FUEL, FILE_AMEBA_FUEL), COLUMNS_AMEBA, self._ameba_dir)
        writer.writeheader()
        year_ini = '2017'

        #Obtener lista con barras y fechas para año 2017
        for fuel in self._dic_fuel_SIC:
                if fuel[COLUMNS_OSE_FUEL_SIC[1]] == year_ini:
                    fuel_type = self._get_fuel_type(remove(fuel[COLUMNS_OSE_FUEL_SIC[0]]),
                                                    [self._dic_fuel_type_SIC_1, self._dic_fuel_type_SIC_2,
                                                    self._dic_fuel_type_SIC_3])
                    # debugger.debugger()
                    if fuel_type is not None:
                        writer.writerow({
                            COLUMNS_AMEBA[0]: 'fuel_'+remove(fuel[COLUMNS_OSE_FUEL_SIC[0]]),
                            COLUMNS_AMEBA[1]: self._dateIniOSE_fuel(fuel[COLUMNS_OSE_FUEL_SIC[1]]),
                            COLUMNS_AMEBA[2]: self._dateFinOSE_fuel(fuel[COLUMNS_OSE_FUEL_SIC[2]]),
                            COLUMNS_AMEBA[3]: FUEL_TYPE[fuel_type],
                            COLUMNS_AMEBA[4]: fuel[COLUMNS_OSE_FUEL_SIC[3]],
                            COLUMNS_AMEBA[5]: 'fuel_OSE'
                            })
                    else:
                        print ".. fuel " + remove(fuel[COLUMNS_OSE_FUEL_SIC[0]])+" is not asociated to any generator .."

        for fuel in self._dic_fuel_SING:
                if fuel[COLUMNS_OSE_FUEL_SING[1]] == year_ini:
                    fuel_type = self._get_fuel_type(remove(fuel[COLUMNS_OSE_FUEL_SING[0]]), [self._dic_fuel_type_SING])
                    if fuel_type is not None:
                        writer.writerow({
                            COLUMNS_AMEBA[0]: 'fuel_'+remove(fuel[COLUMNS_OSE_FUEL_SING[0]]),
                            COLUMNS_AMEBA[1]: self._dateIniOSE_fuel(fuel[COLUMNS_OSE_FUEL_SING[1]]),
                            COLUMNS_AMEBA[2]: self._dateFinOSE_fuel(fuel[COLUMNS_OSE_FUEL_SING[2]]),
                            COLUMNS_AMEBA[3]: FUEL_TYPE[fuel_type],
                            COLUMNS_AMEBA[4]: fuel[COLUMNS_OSE_FUEL_SING[3]],
                            COLUMNS_AMEBA[5]: 'fuel_OSE'
                            })
                    else:
                        print ".. fuel " + remove(fuel[COLUMNS_OSE_FUEL_SING[0]])+" is not asociated to any generator .."

    def _convert_fuel_profile(self):
        """Reads fuel profile from OSE2000 format and write Ameba fuel profile."""

        writer = writer_csv(os.path.join(DIR_AMEBA_FUEL, FILE_AMEBA_FUEL_PROFILE), COLUMNS_AMEBA_2, self._ameba_dir)
        writer.writeheader()

        #obtener lista con barras y fechas para año 2017
        for i in range(0,len(self._dic_fuel_SIC)):
            fuel_type = self._get_fuel_type(remove(self._dic_fuel_SIC[i][COLUMNS_OSE_FUEL_SIC[0]]),
                                                    [self._dic_fuel_type_SIC_1,self._dic_fuel_type_SIC_2,
                                                    self._dic_fuel_type_SIC_3])
            if fuel_type is not None:
                for j in range(3,15):
                    value = self._dic_fuel_SIC[i][COLUMNS_OSE_FUEL_SIC[j]]
                    if j>3 and value == self._dic_fuel_SIC[i][COLUMNS_OSE_FUEL_SIC[j-1]]:
                        continue
                    writer.writerow({
                        COLUMNS_AMEBA_2[0]: 'fuel_'+remove(self._dic_fuel_SIC[i][COLUMNS_OSE_FUEL_SIC[0]]),
                        COLUMNS_AMEBA_2[1]: self._date_ameba(int(self._dic_fuel_SIC[i][COLUMNS_OSE_FUEL_SIC[1]]), int(self._mes(j))),
                        COLUMNS_AMEBA_2[2]: 'fuel_OSE',
                        COLUMNS_AMEBA_2[3]: value
                        })

        for i in range(0,len(self._dic_fuel_SING)):
            fuel_type = self._get_fuel_type(remove(self._dic_fuel_SING[i][COLUMNS_OSE_FUEL_SING[0]]), [self._dic_fuel_type_SING])
            if fuel_type is not None:
                for j in range(3,15):
                    value = self._dic_fuel_SING[i][COLUMNS_OSE_FUEL_SING[j]]
                    if j>3 and value == self._dic_fuel_SING[i][COLUMNS_OSE_FUEL_SING[j-1]]:
                        continue
                    writer.writerow({
                        COLUMNS_AMEBA_2[0]: 'fuel_'+remove(self._dic_fuel_SING[i][COLUMNS_OSE_FUEL_SING[0]]),
                        COLUMNS_AMEBA_2[1]: self._date_ameba(int(self._dic_fuel_SING[i][COLUMNS_OSE_FUEL_SING[1]]), int(self._mes(j))),
                        COLUMNS_AMEBA_2[2]: 'fuel_OSE',
                        COLUMNS_AMEBA_2[3]: value
                        })

    def run(self):
        """Main execution point."""
        self._convert_fuel()
        self._convert_fuel_profile()


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
    Fuel(args.ose_dir, args.ameba_dir, args.model).run()


if __name__ == '__main__':
    main()
