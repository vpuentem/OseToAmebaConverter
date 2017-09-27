#!/usr/bin/env python
# -*- coding: latin-1 -*-


"""OSE2Ameba_branch: Script to convert an OSE2000 database into Ameba CSV format.
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
import string
import itertools

from ose2ameba_functions import *
from ose2ameba_parameters import *

COLUMNS_AMEBA = [BRANCH_NAME_AMEBA,
BRANCH_START_TIME_AMEBA,
BRANCH_END_TIME_AMEBA,
BRANCH_VOLTAGE_AMEBA,
BRANCH_MAXFLOW_AMEBA,
BRANCH_R_AMEBA,
BRANCH_X_AMEBA,
BRANCH_LOSSES_AMEBA,
BRANCH_LIFETIME_AMEBA,
BRANCH_INV_COST_AMEBA,
BRANCH_COMA_COST_AMEBA,
BRANCH_BUSBARI_AMEBA,
BRANCH_BUSBARF_AMEBA,
BRANCH_CONNECTED_AMEBA,
BRANCH_REPORT_AMEBA]

DATE_FLAG = False
#potencia base para pasar de ohm a °/1
S_BASE=100

class Branch(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba__branch.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def __convert_branch(self):
        """Reads branch from OSE2000 format and write Ameba branch."""

        branch_OSE_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_BRANCH), FILE_OSE_BRANCH_SING, self._ose_dir))
        branch_OSE_SIX = list(reader_csv(os.path.join(DIR_OSE_SIX,DIR_OSE_BRANCH), FILE_OSE_BRANCH_SIX, self._ose_dir))

        if self._model == 'Opt':
            branch_OSE_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_BRANCH), FILE_OSE_BRANCH_SIC_OPT, self._ose_dir))
        elif self._model == 'Ope':
            branch_OSE_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_BRANCH), FILE_OSE_BRANCH_SIC_OPE, self._ose_dir))

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_BRANCH)
        check_directory(directory)

        writer = writer_csv(os.path.join(DIR_AMEBA_BRANCH,FILE_AMEBA_BRANCH), COLUMNS_AMEBA, self._ameba_dir)
        writer.writeheader()

        branch_ameba = []
        for row in itertools.chain(branch_OSE_SING,branch_OSE_SIC,branch_OSE_SIX):
            branch_ameba.append({})
            name = remove(row[BRANCH_NAME_OSE])
            busbari = remove(row[BRANCH_BUSBARI_OSE])
            busbarf = remove(row[BRANCH_BUSBARF_OSE])
            connected = t_true(row[BRANCH_CONNECTED_OSE])
            report = t_true(row[BRANCH_CONNECTED_OSE])

            if not DATE_FLAG:
                date_ini = date_ini_ose(row[BRANCH_START_TIME_OSE])
            else:
                date_ini = date_ini_ose('*')

            date_end = date_end_ose(row[BRANCH_END_TIME_OSE])
            voltage = row[BRANCH_VOLTAGE_OSE]
            max_flow = select_max_flow(row[BRANCH_MAXFLOW_AB_OSE],
                                row[BRANCH_MAXFLOW_BA_OSE],
                                row[BRANCH_MAXFLOW_ABN1_OSE],
                                row[BRANCH_MAXFLOW_BAN1_OSE],
                                row[BRANCH_FLAG_N1_OSE]
                                )
            r = round(float(row[BRANCH_R_OSE])/(float(row[BRANCH_VOLTAGE_OSE])**2/S_BASE),3)
            x = round(float(row[BRANCH_X_OSE])/(float(row[BRANCH_VOLTAGE_OSE])**2/S_BASE),3)
            if x < 0.001:
                x=0.001
            if r < 0.001 and r != 0:
                r=0.000
            losses = t_true(row[BRANCH_LOSSES_OSE])
            lifetime = row[BRANCH_LIFETIME_OSE]
            inv_cost = row[BRANCH_INV_COST_OSE]
            coma_cost = row[BRANCH_COMA_COST_OSE]
            branch_ameba[-1].update({
                BRANCH_NAME_AMEBA : name,
                BRANCH_START_TIME_AMEBA : date_ini,
                BRANCH_END_TIME_AMEBA : date_end,
                BRANCH_BUSBARI_AMEBA : busbari,
                BRANCH_BUSBARF_AMEBA : busbarf,
                BRANCH_VOLTAGE_AMEBA : voltage,
                BRANCH_CONNECTED_AMEBA : connected,
                BRANCH_REPORT_AMEBA : report,
                BRANCH_MAXFLOW_AMEBA : max_flow,
                BRANCH_R_AMEBA : r,
                BRANCH_X_AMEBA : x,
                BRANCH_LOSSES_AMEBA : losses,
                BRANCH_LIFETIME_AMEBA : lifetime,
                BRANCH_INV_COST_AMEBA : inv_cost,
                BRANCH_COMA_COST_AMEBA : coma_cost
                })
            writer.writerow(branch_ameba[-1])

    def run(self):
        """Main execution point."""
        self.__convert_branch()
        print 'branch ready'

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
    Branch(args.ose_dir, args.ameba_dir, args.model).run()


if __name__ == '__main__':
    main()
