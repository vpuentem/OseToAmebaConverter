# coding=utf-8
"""OSE2Ameba_busbar: Script to convert an OSE2000 database into Ameba CSV format.
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
import itertools
import debugger

from ose2ameba_functions import *
from ose2ameba_parameters import *

DATE_FLAG = True

class Busbar(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba_busbar.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        @param model: string with value 'Ope' or Opt'
        """

        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model


    def __convert_busbars(self):
        """Reads busbars from OSE2000 format and write Ameba busbars."""
        # TODO: Replace directory and file name below with correct one
        """ read files y writer """
        busbar_OSE_SING = reader_csv (os.path.join(DIR_OSE_SING,DIR_OSE_BUSBAR),
        FILE_OSE_BUSBAR_SING, self._ose_dir)

        if self._model == 'Opt':
            busbar_OSE_SIC = reader_csv (os.path.join(DIR_OSE_SIC,DIR_OSE_BUSBAR),
                                            FILE_OSE_BUSBAR_SIC_OPT, self._ose_dir)
        elif self._model == 'Ope':
            busbar_OSE_SIC = reader_csv (os.path.join(DIR_OSE_SIC,DIR_OSE_BUSBAR),
                                            FILE_OSE_BUSBAR_SIC_OPE, self._ose_dir)

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_BUSBAR)
        check_directory(directory)

        COLUMNS_AMEBA = [ BUSBAR_NAME_AMEBA,
                          BUSBAR_START_TIME_AMEBA,
                          BUSBAR_END_TIME_AMEBA,
                          BUSBAR_VOLTAGE_AMEBA
                        ]

        writer = writer_csv (os.path.join(DIR_AMEBA_BUSBAR,FILE_AMEBA_BUSBAR), COLUMNS_AMEBA, self._ameba_dir)
        writer.writeheader()

        """ Main iteration"""
        busbar_ameba=[]
        for row in itertools.chain(busbar_OSE_SING,busbar_OSE_SIC):
            #if row[BUSBAR_OPE_OSE]=='T':
            #debugger.debugger()
            busbar_ameba.append({})
            name = remove(row[BUSBAR_NAME_OSE])

            if not DATE_FLAG:
                date_ini = date_ini_ose (row[BUSBAR_START_TIME_OSE])
            else:
                date_ini = date_ini_ose('*')
            date_end = date_end_ose (row[BUSBAR_END_TIME_OSE])
            voltage = row[BUSBAR_VOLTAGE_OSE]
            busbar_ameba[-1].update({
                    BUSBAR_NAME_AMEBA: name,
                    BUSBAR_START_TIME_AMEBA: date_ini,
                    BUSBAR_END_TIME_AMEBA: date_end,
                    BUSBAR_VOLTAGE_AMEBA: voltage
                    })
            writer.writerow(busbar_ameba[-1])


        print 'busbar ready'

    def run(self):
        """Main execution point."""
        self.__convert_busbars()


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
    Busbar(args.ose_dir, args.ameba_dir, args.model).run()

if __name__ == '__main__':
    main()
