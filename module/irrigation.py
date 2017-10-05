#!/usr/bin/env python
# -*- coding: latin-1 -*-


"""ose2ameba_virtual: Script to convert an OSE2000 database into Ameba CSV format.
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
import debugger
import itertools

from parameters import *
from functions import *

#COLUMNS_ AMEBA
COLUMNS_AMEBA_1=['name','h_max_flow','h_min_flow','eff']
COLUMNS_AMEBA_2=['name','time','scenario','value']

#columas OSE
COLUMNS_OSE_1=['CenNom','CenPotMax','CenPotMin','CenTurRen','CenTip']
COLUMNS_OSE_2=['CenNom','CenFunEta','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']

#Diccionario para pasar fechas de OSE a AMEBA
MONTH_NUM = {'Ene': '01', 'Feb': '02', 'Mar': '03', 'Abr': '04', 'May': '05', 'Jun': '06',
'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12' }

YEAR_INI=2017
YEAR_END=2031

class Irrigation(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of ose2ameba_virtual.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def _date_virt(self, year, month):
        return year+'-'+MONTH_NUM[month]+'-01-00:00'

    def _convert_virtual(self):
        """Reads virtual from OSE2000 format and write Ameba virtual."""
        if self._model in ['Ope','ope','OPE']:
            dic_VirPar = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_VIRTUAL), FILE_OSE_VIRTUAL_SIC_OPE, self._ose_dir))
        else: # self._model in ['Opt','opt','OPT']:
            dic_VirPar = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_VIRTUAL), FILE_OSE_VIRTUAL_SIC_OPT, self._ose_dir))


        dic_VirEta = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_VIRTUAL), FILE_OSE_IRRIGATION, self._ose_dir))

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_IRRIGATION)
        check_directory(directory)

        writer = writer_csv(os.path.join(DIR_AMEBA_IRRIGATION,FILE_AMEBA_HYDRO_CONNECTION), COLUMNS_AMEBA_1, self._ameba_dir)
        writer_max = writer_csv(os.path.join(DIR_AMEBA_IRRIGATION,FILE_AMEBA_IRRIGATION), COLUMNS_AMEBA_2, self._ameba_dir)

        writer.writeheader()
        writer_max.writeheader()

        for virt in dic_VirPar:
            if virt[COLUMNS_OSE_1[4]] == 'BocCap':
                writer.writerow({
                COLUMNS_AMEBA_1[0] : 'generacion '+remove(virt[COLUMNS_OSE_1[0]]),
                COLUMNS_AMEBA_1[1] : virt[COLUMNS_OSE_1[1]],
                COLUMNS_AMEBA_1[2] : virt[COLUMNS_OSE_1[2]],
                COLUMNS_AMEBA_1[3] : virt[COLUMNS_OSE_1[3]],
                })

        for virt in dic_VirEta:
            for year in range(YEAR_INI,YEAR_END):
                for i in range(2,len(COLUMNS_OSE_2)):
                    if virt[COLUMNS_OSE_2[1]] == 'CenQMax':
                        writer_max.writerow({
                        COLUMNS_AMEBA_2[0]:'irrig_'+remove(virt[COLUMNS_OSE_2[0]]),
                        COLUMNS_AMEBA_2[1]:self._date_virt(str(year), COLUMNS_OSE_2[i]),
                        COLUMNS_AMEBA_2[2]:'irrigation_OSE',
                        COLUMNS_AMEBA_2[3]:virt[COLUMNS_OSE_2[i]],
                        })

    def run(self):
        """Main execution point."""
        self._convert_virtual()

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
    Irrigation(args.ose_dir, args.ameba_dir, args.model).run()

if __name__ == '__main__':
    main()
