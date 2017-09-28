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
from functions import *
from parameters import *

"""_______________________________________________________________________________"""
""" BRANCH PARAMETERS """

""" FILE NAMES """
FILE_OSE_BRANCH_SIC_OPT = 'LinDatParOpt.csv'
FILE_OSE_BRANCH_SIC_OPE = 'LinDatParOpe.csv'
FILE_OSE_BRANCH_SING = 'LinDatPar.csv'
FILE_OSE_BRANCH_SIX = 'LinDatPar1500Lat.csv'
FILE_AMEBA_BRANCH = 'ele-branch.csv'

FILE_OSE_BRANCH_MAXFLOW_SIC_OPT = 'LinDatManOpt.csv'
FILE_OSE_BRANCH_MAXFLOW_SIC_OPE = 'LinDatManOpe.csv'
FILE_OSE_BRANCH_MAXFLOW_SING = 'LinDatMan.csv'
FILE_AMEBA_BRANCH_MAXFLOW = 'ele-branch-maxflow.csv'

""" OSE COLUMN NAMES """
BRANCH_NAME_OSE = 'LinNom'
BRANCH_START_TIME_OSE = 'LinFecOpeIni'
BRANCH_END_TIME_OSE = 'LinFecOpeFin'
BRANCH_CONNECTED_OSE = 'LinFOpe'
BRANCH_VOLTAGE_OSE = 'LinVolt'
BRANCH_MAXFLOW_AB_OSE = 'LinPotMaxA->B'
BRANCH_MAXFLOW_BA_OSE = 'LinPotMaxB->A'
BRANCH_MAXFLOW_ABN1_OSE = 'LinPotN-1A->B'
BRANCH_MAXFLOW_BAN1_OSE = 'LinPotN-1B->A'
BRANCH_FLAG_N1_OSE = 'LinFN-1'
BRANCH_R_OSE = 'LinR'
BRANCH_X_OSE = 'LinX'
BRANCH_LOSSES_OSE = 'LinFPer'
BRANCH_LIFETIME_OSE = 'LinVidUti'
BRANCH_INV_COST_OSE = 'LinVI'
BRANCH_COMA_COST_OSE = 'LinCOMA'
BRANCH_BUSBARI_OSE = 'LinBarA'
BRANCH_BUSBARF_OSE = 'LinBarB'

BRANCH_MAXFLOW_START_TIME_OSE = 'LinFecIni'
BRANCH_MAXFLOW_END_TIME_OSE = 'LinFecFin'
BRANCH_MAXFLOW_FLAG_OSE = 'LinFMan'

""" AMEBA COLUMN NAMES """
BRANCH_NAME_AMEBA = 'name'
BRANCH_START_TIME_AMEBA = 'start_time'
BRANCH_END_TIME_AMEBA = 'end_time'
BRANCH_CONNECTED_AMEBA = 'connected'
BRANCH_REPORT_AMEBA = 'report'
BRANCH_VOLTAGE_AMEBA = 'voltage'
BRANCH_MAXFLOW_AMEBA = 'max_flow'
BRANCH_R_AMEBA = 'r'
BRANCH_X_AMEBA = 'x'
BRANCH_LOSSES_AMEBA = 'losses'
BRANCH_LIFETIME_AMEBA = 'lifetime'
BRANCH_INV_COST_AMEBA = 'inv_cost'
BRANCH_COMA_COST_AMEBA = 'coma_cost'
BRANCH_BUSBARI_AMEBA = 'busbari'
BRANCH_BUSBARF_AMEBA = 'busbarf'
BRANCH_TIME_AMEBA = 'time'

COLUMNS_AMEBA = [BRANCH_NAME_AMEBA, BRANCH_BUSBARI_AMEBA, BRANCH_BUSBARF_AMEBA, BRANCH_CONNECTED_AMEBA,
                 BRANCH_REPORT_AMEBA, BRANCH_START_TIME_AMEBA, BRANCH_END_TIME_AMEBA, BRANCH_VOLTAGE_AMEBA,
                 BRANCH_MAXFLOW_AMEBA, BRANCH_R_AMEBA, BRANCH_X_AMEBA, BRANCH_LOSSES_AMEBA, BRANCH_LIFETIME_AMEBA,
                 BRANCH_INV_COST_AMEBA, BRANCH_COMA_COST_AMEBA]

MONTH_NUM_INT = {'Ene': 1, 'Feb': 2, 'Mar': 3, 'Abr': 4, 'May': 5, 'Jun': 6,
'Jul': 7, 'Ago': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12 }

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

        self._branch_par_OSE_SING = list(reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_BRANCH),
                                               FILE_OSE_BRANCH_SING, ose_dir))
        self._branch_maxflow_OSE_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_BRANCH), FILE_OSE_BRANCH_MAXFLOW_SING, self._ose_dir))
        self._branch_par_OSE_SIX = list(reader_csv(os.path.join(DIR_OSE_SIX, DIR_OSE_BRANCH),
                                               FILE_OSE_BRANCH_SIX, ose_dir))
        if model in ['Ope','ope','OPE']:
            self._branch_par_OSE_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_BRANCH),
                                               FILE_OSE_BRANCH_SIC_OPE, ose_dir))
            self._branch_maxflow_OSE_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_BRANCH),
                                               FILE_OSE_BRANCH_MAXFLOW_SIC_OPE, self._ose_dir))
        else: #if model in ['Opt','opt','OPT']:
            self._branch_par_OSE_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_BRANCH), FILE_OSE_BRANCH_SIC_OPT, ose_dir))
            self._branch_maxflow_OSE_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_BRANCH),
                                               FILE_OSE_BRANCH_MAXFLOW_SIC_OPT, self._ose_dir))
    def __datetime_to_ameba(self,date_time):
        return str(date_time.year) + '-' + str(date_time.month).zfill(2) + '-' + str(date_time.day).zfill(2) + '-' + '00:00'

    def __month_list(self, year_ini,year_end):
        dates=[]
        for year in range(year_ini,year_end+1):
            for month in range(1,13):
                dates.append({
                BRANCH_TIME_AMEBA : self.__datetime_to_ameba(datetime.datetime(year, month, 1, 00, 00, 00)),
                'index' : self.__get_month_list_index(month, year_ini, year),
                'scenario': 'branch_OSE'
                })
        return dates

    def __get_month_list_index(self, month_num, year_ini, year_end):
        return (year_end - year_ini) * 12 + (month_num -1)

    def __max_flow_true(self, maxf_AB,maxf_BA, maxf_ABN,maxf_BAN):
        if maxf_AB=='*' and maxf_BA=='*' and maxf_ABN=='*' and maxf_BAN=='*':
            return False
        else:
            return True

    def __parameters(self):
        """@Reads branch from OSE2000 format and write Ameba branch."""

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_BRANCH)
        check_directory(directory)

        writer = writer_csv(os.path.join(DIR_AMEBA_BRANCH,FILE_AMEBA_BRANCH), COLUMNS_AMEBA, self._ameba_dir)
        writer.writeheader()

        branch_ameba = []
        for row in itertools.chain(self._branch_par_OSE_SING,self._branch_par_OSE_SIC,self._branch_par_OSE_SIX):
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

    def __max_flow(self):
        """Reads max flow from OSE2000 format and write Ameba max flow."""
        dic_maxflow_AB_nominal = {}
        dic_maxflow_AB_N_nominal = {}
        dic_flag_n_nominal = {}
        for branch in itertools.chain(self._branch_par_OSE_SIC, self._branch_par_OSE_SING):
            max_flow_AB = max([float(branch[BRANCH_MAXFLOW_AB_OSE]),float(branch[BRANCH_MAXFLOW_BA_OSE])])
            max_flow_AB_N = max([float(branch[BRANCH_MAXFLOW_ABN1_OSE]),float(branch[BRANCH_MAXFLOW_BAN1_OSE])])

            dic_maxflow_AB_nominal.update({branch[BRANCH_NAME_OSE] : max_flow_AB})
            dic_maxflow_AB_N_nominal.update({branch[BRANCH_NAME_OSE] : max_flow_AB_N})
            dic_flag_n_nominal.update({branch[BRANCH_NAME_OSE] : branch[BRANCH_FLAG_N1_OSE]})

        #GET MIN & MAX YEAR
        dic_maxflow = {}
        max_year = 0
        min_year = 3000
        for branch in itertools.chain(self._branch_maxflow_OSE_SIC, self._branch_maxflow_OSE_SING):
            if branch[BRANCH_NAME_OSE] not in dic_maxflow:
                if dic_flag_n_nominal[branch[BRANCH_NAME_OSE]] == 'T':
                    max_flow = dic_maxflow_AB_N_nominal[branch[BRANCH_NAME_OSE]]
                else:
                    max_flow = dic_maxflow_AB_nominal[branch[BRANCH_NAME_OSE]]

                dic_maxflow.update({
                branch[BRANCH_NAME_OSE] : max_flow
                })
            if int(branch[BRANCH_MAXFLOW_START_TIME_OSE][7:]) < min_year:
                min_year = int(branch[BRANCH_MAXFLOW_START_TIME_OSE][7:])
            if int(branch[BRANCH_MAXFLOW_START_TIME_OSE][7:]) > max_year:
                max_year = int(branch[BRANCH_MAXFLOW_START_TIME_OSE][7:])
            if branch[BRANCH_MAXFLOW_END_TIME_OSE] is not '*':
                if int(branch[BRANCH_MAXFLOW_END_TIME_OSE][7:]) > max_year:
                    max_year = int(branch[BRANCH_MAXFLOW_END_TIME_OSE][7:])

        # LIST OF MONTH DATES FROM MIN YEAR TO MAX YEAR
        dates = self.__month_list(min_year,max_year)
        for date in dates:
            date.update(dic_maxflow)

        for branch in itertools.chain(self._branch_maxflow_OSE_SIC, self._branch_maxflow_OSE_SING):
            if branch[BRANCH_MAXFLOW_FLAG_OSE] == 'T':
                year_ini = int(branch[BRANCH_MAXFLOW_START_TIME_OSE][7:])
                month_ini = MONTH_NUM_INT[branch[BRANCH_MAXFLOW_START_TIME_OSE][3:6]]
                index_ini = self.__get_month_list_index(month_ini, min_year, year_ini)
                name = branch[BRANCH_NAME_OSE]

                if branch[BRANCH_MAXFLOW_END_TIME_OSE] != '*':
                    year_end = int(branch[BRANCH_MAXFLOW_END_TIME_OSE][7:])
                    month_end = MONTH_NUM_INT[branch[BRANCH_MAXFLOW_END_TIME_OSE][3:6]]
                    index_end = self.__get_month_list_index(month_end, min_year, year_end)
                else:
                    index_end = self.__get_month_list_index(12, min_year, max_year)

                if  not max_flow_true(
                    branch[BRANCH_MAXFLOW_AB_OSE],
                    branch[BRANCH_MAXFLOW_BA_OSE],
                    branch[BRANCH_MAXFLOW_ABN1_OSE],
                    branch[BRANCH_MAXFLOW_BAN1_OSE]):

                    if branch[BRANCH_FLAG_N1_OSE] == '*':
                        continue
                    else:
                        if branch[BRANCH_FLAG_N1_OSE] == 'F':
                            maxflow = dic_maxflow_AB_nominal[name]
                        else:
                            maxflow = dic_maxflow_AB_N_nominal[name]
                else:
                    if branch[BRANCH_FLAG_N1_OSE] == '*':
                        flag_n = dic_flag_n_nominal[name]
                    else:
                        flag_n = branch[BRANCH_FLAG_N1_OSE]
                    maxflow = select_max_flow(
                        branch[BRANCH_MAXFLOW_AB_OSE],
                        branch[BRANCH_MAXFLOW_BA_OSE],
                        branch[BRANCH_MAXFLOW_ABN1_OSE],
                        branch[BRANCH_MAXFLOW_BAN1_OSE],
                        flag_n
                        )

                while index_ini <= index_end:
                    dates[index_ini][name] = maxflow
                    index_ini += 1

        columns = dates[0].keys()
        columns.insert(0, columns.pop(columns.index(BRANCH_TIME_AMEBA)))
        columns.insert(1, columns.pop(columns.index('scenario')))
        columns.pop(columns.index('index'))

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_BRANCH)
        check_directory(directory)

        writer = writer_csv(os.path.join(DIR_AMEBA_BRANCH, FILE_AMEBA_BRANCH_MAXFLOW), columns, self._ameba_dir)
        writer.writeheader()
        for date in dates:
            date.pop('index')
            writer.writerow(date)

    def run(self):
        """Main execution point."""
        self.__parameters()
        print 'branch parameters ready'
        self.__max_flow()
        print 'branch max flow ready'

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
