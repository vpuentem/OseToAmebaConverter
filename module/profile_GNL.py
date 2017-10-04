# coding=utf-8
"""OSE2Ameba_demand: Script to convert an OSE2000 database into Ameba CSV format.
_______________________________________________________________________________
Copyright (c) 2017 AMEBA-Dev - Consultora SPEC Limitada
This software cannot be distributed.
For more information, visit ameba.spec.cl
Current version developer: Ameba Team
_______________________________________________________________________________
"""
from parameters import *
from functions import *
from generator import *
from workalendar.america import Chile


COLUMNS_OSE_GNL = ['CenINum', 'CenA\xf1oFRlt', 'CenA\xf1oIni', 'CenA\xf1oFin', 'CenIBlo', 'CenNom', 'CenDatTip',
                   'CenEtaTip', 'SemAbr01', 'SemAbr02', 'SemAbr03',
                   'SemAbr04', 'SemMay01', 'SemMay02', 'SemMay03', 'SemMay04', 'SemJun01', 'SemJun02', 'SemJun03',
                   'SemJun04', 'SemJul01', 'SemJul02', 'SemJul03',
                   'SemJul04', 'SemAgo01', 'SemAgo02', 'SemAgo03', 'SemAgo04', 'SemSep01', 'SemSep02', 'SemSep03',
                   'SemSep04', 'SemOct01', 'SemOct02', 'SemOct03',
                   'SemOct04', 'SemNov01', 'SemNov02', 'SemNov03', 'SemNov04', 'SemDic01', 'SemDic02', 'SemDic03',
                   'SemDic04', 'SemEne01', 'SemEne02', 'SemEne03',
                   'SemEne04', 'SemFeb01', 'SemFeb02', 'SemFeb03', 'SemFeb04', 'SemMar01', 'SemMar02', 'SemMar03',
                   'SemMar04']

# Diccionarios de OSE a Ameba
MONTH_NUM = {'Ene': '01', 'Feb': '02', 'Mar': '03', 'Abr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12'}

CAL = Chile()

TIME_AMEBA = 'time'
BLOCK_AMEBA = 'block'
STAGE_AMEBA = 'stage'
SCENARIO_AMEBA = 'scenario'
NAME_AMEBA = 'name'
VALUE_AMEBA = 'value'

# columnas ameba
COLUMNS_AMEBA = [NAME_AMEBA, TIME_AMEBA, VALUE_AMEBA]

YEAR_END_SIM = 2031
YEAR_OSE = '2013'


class ProfileGnl(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba_demand.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def _date_gnl(self, date, year):
        month = date[3:6]
        if int(MONTH_NUM[month]) < 4:
            year = str(int(year) + 1)
        week = date[6:8]
        return year + '-' + MONTH_NUM[month] + '-' + str((int(week) - 1) * 7 + 1).zfill(2) + '-' + '00:00'

    def _time_year(self, year):
        dates = []
        for i in range(0, 8760, 1):
            dates.append({TIME_AMEBA: datetime.datetime(year, 01, 01, 00, 00, 00) + datetime.timedelta(hours=i)})
        return dates

    def _date_gnl_min(self, date, year):
        month = date[3:6]
        week = date[6:8]
        return year + '-' + MONTH_NUM[month] + '-' + str((int(week) - 1) * 7 + 1).zfill(2) + '-' + '00:00'

    def _get_year_list_index(self, hour_num, year_ini, year):
        index_ini = (year - year_ini) * hour_num
        index_end = (year - year_ini) * hour_num + hour_num
        return [index_ini, index_end]

    def _datetime_index(self, datetime):
        month = datetime.month
        day = datetime.day
        if day < 8:
            week = 1
        elif day >= 8 and day < 15:
            week = 2
        elif day >= 15 and day < 22:
            week = 3
        else:
            week = 4
        return [month, week]

    def _get_gnl_date(self, column):
        month = int(column / 4) - 1
        week = (float(column) / float(4) - 1 - month) * 4 + 1
        return [int(month), int(week)]

    def _get_gnl_value(self, month, week):
        if month < 4:
            return int((month + 1) * 4 + week - 1 + 36)
        else:
            return int((month + 1) * 4 + week - 1 - 12)

    def _convert_profile_gnl(self):
        """Reads GNL profiles from OSE2000 format and write Ameba profiles."""
        pmax_thermal_SING_1 = reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                         FILE_OSE_THERMAL_SING_1, self._ose_dir)
        if self._model in ['Ope', 'ope', 'OPE']:
            pmax_thermal_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                            FILE_OSE_THERMAL_SIC_OPE_1, self._ose_dir)
            pmax_thermal_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                            FILE_OSE_THERMAL_SIC_OPE_2, self._ose_dir)
            pmax_thermal_SIC_3 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                            FILE_OSE_THERMAL_SIC_OPE_3, self._ose_dir)
            pmax_pas_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                        FILE_OSE_PAS_SIC_OPE_1, self._ose_dir)
            pmax_pas_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                        FILE_OSE_PAS_SIC_OPE_2, self._ose_dir)
            pmax_ser_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_SER),
                                        FILE_OSE_SER_SIC_OPE_1, self._ose_dir)
            pmax_emb_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_EMB),
                                        FILE_OSE_EMB_SIC_OPE_1, self._ose_dir)
        else: #if self._model in ['Opt', 'opt', 'OPT']:
            pmax_thermal_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                            FILE_OSE_THERMAL_SIC_OPT_1, self._ose_dir)
            pmax_thermal_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                            FILE_OSE_THERMAL_SIC_OPT_2, self._ose_dir)
            pmax_thermal_SIC_3 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                            FILE_OSE_THERMAL_SIC_OPT_3, self._ose_dir)
            pmax_pas_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                        FILE_OSE_PAS_SIC_OPT_1, self._ose_dir)
            pmax_pas_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                        FILE_OSE_PAS_SIC_OPT_2, self._ose_dir)
            pmax_ser_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_SER),
                                        FILE_OSE_SER_SIC_OPT_1, self._ose_dir)
            pmax_emb_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_EMB),
                                        FILE_OSE_EMB_SIC_OPT_1, self._ose_dir)

        """  DIC WITH NAMES AND RESPECTIVE NOMINAL PMAX & PMIN """
        dic_pmin = {}
        for generator in itertools.chain(pmax_thermal_SIC_1, pmax_thermal_SING_1, pmax_thermal_SIC_2,
                                         pmax_thermal_SIC_3):
            dic_pmin.update({remove(generator[GEN_NAME_OSE]): float(generator[GEN_PMIN_OSE])})

        dic_gnl_1 = list(
            reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_GNL_PROFILE_SIC1,
                       self._ose_dir))
        dic_gnl_2 = list(
            reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_GNL_PROFILE_SIC2,
                       self._ose_dir))
        dic_gnl_3 = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_GNL_PROFILE_SING,
                       self._ose_dir))

        dic_tabla_habil = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))

        directory = os.path.join(self._ameba_dir, DIR_AMEBA_GENERATOR)
        check_directory(directory)
        """ PART 1"""
        time_hourly = self._time_year(int(YEAR_OSE))

        """ DATES OF 1 YEAR & RESPECTIVE BLOCK LIST """
        time_reduced = []
        for i in range(0, len(time_hourly)):
            if time_hourly[i][TIME_AMEBA].weekday() == 6 or time_hourly[i][
                TIME_AMEBA].weekday() == 5 or CAL.is_working_day(time_hourly[i][TIME_AMEBA]) is False:
                block = get_block(dic_tabla_no_habil, str(time_hourly[i][TIME_AMEBA].hour + 1),
                                  str(time_hourly[i][TIME_AMEBA].month))
            else:
                block = get_block(dic_tabla_habil, str(time_hourly[i][TIME_AMEBA].hour + 1),
                                  str(time_hourly[i][TIME_AMEBA].month))
            time_hourly[i].update({BLOCK_AMEBA: block})
            time_hourly[i].update({SCENARIO_AMEBA: 'GNL_profile_OSE'})
            time_hourly[i].update({STAGE_AMEBA: time_hourly[i][TIME_AMEBA].month})
            if i == 0:
                time_reduced.append(time_hourly[i])
                continue
            if time_hourly[i][BLOCK_AMEBA] != time_hourly[i - 1][BLOCK_AMEBA]:
                time_reduced.append(time_hourly[i])
            elif time_hourly[i][BLOCK_AMEBA] == time_hourly[i - 1][BLOCK_AMEBA] and time_hourly[i][
                TIME_AMEBA].month != time_hourly[i - 1][TIME_AMEBA].month:
                time_reduced.append(time_hourly[i])
        """ DATES FOR ALL YEARS"""
        min_year = 3000
        max_year = 0
        for gnl in itertools.chain(dic_gnl_1, dic_gnl_2, dic_gnl_3):
            if gnl[COLUMNS_OSE_GNL[4]] != '*' and gnl[COLUMNS_OSE_GNL[6]] == 'CenPotMin':
                name = remove(gnl[COLUMNS_OSE_GNL[5]])
                ini_year = int(gnl[COLUMNS_OSE_GNL[2]])
                if gnl[COLUMNS_OSE_GNL[3]] == '*':
                    end_year = YEAR_END_SIM
                else:
                    end_year = int(gnl[COLUMNS_OSE_GNL[3]])
                if ini_year < min_year:
                    min_year = ini_year
                if end_year > max_year:
                    max_year = end_year
        index = 0
        time_reduced_allyears = []
        for years in range(min_year, max_year + 1, 1):
            for time in time_reduced:
                time_reduced_allyears.append(time.copy())
                time_reduced_allyears[-1].update(
                    {TIME_AMEBA: time_reduced_allyears[-1][TIME_AMEBA].replace(year=years)})
                time_reduced_allyears[-1].update({'index': index})
                index += 1

        gnl_ele = []
        """ main iteration 1 (creates list with dates, element -> Pmin)"""
        for time_element in time_reduced_allyears:
            gnl_ele.append(time_element.copy())

            for gnl in itertools.chain(dic_gnl_1, dic_gnl_2, dic_gnl_3):
                name = remove(gnl[COLUMNS_OSE_GNL[5]])
                year_ini = gnl[COLUMNS_OSE_GNL[2]]
                if gnl[COLUMNS_OSE_GNL[4]] != '*' and gnl[COLUMNS_OSE_GNL[6]] == 'CenPotMin':
                    gnl_ele[-1].update({name: int(dic_pmin[name])})
            [month, week] = self._datetime_index(gnl_ele[-1][TIME_AMEBA])
            year = gnl_ele[-1][TIME_AMEBA].year
            for gnl in itertools.chain(dic_gnl_1, dic_gnl_2, dic_gnl_3):

                if gnl[COLUMNS_OSE_GNL[4]] != '*' and gnl[COLUMNS_OSE_GNL[6]] == 'CenPotMin':
                    year_ini = int(gnl[COLUMNS_OSE_GNL[2]])
                    if gnl[COLUMNS_OSE_GNL[3]] == '*':
                        year_end = YEAR_END_SIM
                    else:
                        year_end = int(gnl[COLUMNS_OSE_GNL[3]])
                    name = remove(gnl[COLUMNS_OSE_GNL[5]])
                    block = int(gnl[COLUMNS_OSE_GNL[4]])
                    if year_ini <= year and year_end >= year:
                        column = self._get_gnl_value(month, week)
                        value = int(gnl[COLUMNS_OSE_GNL[column]])
                        if block == int(gnl_ele[-1][BLOCK_AMEBA]):
                            gnl_ele[-1].update({name: int(value)})

        # OBTIENE COLUMNAS
        header = gnl_ele[0].keys()
        header.remove(TIME_AMEBA)
        header.remove(BLOCK_AMEBA)
        header.remove(STAGE_AMEBA)
        header.remove('index')
        header.remove(SCENARIO_AMEBA)

        output_file = writer_csv('ele-gnl-profile_min2.csv', [NAME_AMEBA, TIME_AMEBA, VALUE_AMEBA],
                                 os.path.join(self._ameba_dir, DIR_AMEBA_GENERATOR))
        output_file.writeheader()
        # REMOVER VALORES REPETIDOS
        for h in header:
            for i in range(0, len(gnl_ele)):
                if gnl_ele[i][h] == gnl_ele[i - 1][h] and i > 0:
                    continue
                output_file.writerow(
                    dict(name=h, time=datetime_to_ameba2(gnl_ele[i]['time']), value=gnl_ele[i][h]))

        """ PART 2 """
        writer_gnl_max = writer_csv(os.path.join(DIR_AMEBA_GENERATOR, FILE_AMEBA_PROFILE_GNL_MAX_SIC), COLUMNS_AMEBA,
                                    self._ameba_dir)
        writer_gnl_min = writer_csv(os.path.join(DIR_AMEBA_GENERATOR, FILE_AMEBA_PROFILE_GNL_MIN_SIC), COLUMNS_AMEBA,
                                    self._ameba_dir)
        writer_gnl_max.writeheader()
        writer_gnl_min.writeheader()

        """ main iteration 2"""
        for gnl in itertools.chain(dic_gnl_1, dic_gnl_2, dic_gnl_3):
            name = remove(gnl[COLUMNS_OSE_GNL[5]])
            if gnl[COLUMNS_OSE_GNL[4]] == '*':
                if gnl[COLUMNS_OSE_GNL[3]] == '*':
                    if gnl[COLUMNS_OSE_GNL[6]] == 'CenPotMax':
                        for j in range(int(gnl[COLUMNS_OSE_GNL[2]]), YEAR_END_SIM + 1):
                            for i in range(8, len(COLUMNS_OSE_GNL)):
                                if gnl[COLUMNS_OSE_GNL[i]] != gnl[COLUMNS_OSE_GNL[i - 1]] or i == 8:
                                    writer_gnl_max.writerow({
                                        NAME_AMEBA: name,
                                        TIME_AMEBA: self._date_gnl_min(COLUMNS_OSE_GNL[i], str(j)),
                                        VALUE_AMEBA: gnl[COLUMNS_OSE_GNL[i]],
                                    })
                    elif gnl[COLUMNS_OSE_GNL[6]] == 'CenPotMin':
                        for j in range(int(gnl[COLUMNS_OSE_GNL[2]]), YEAR_END_SIM + 1):
                            for i in range(8, len(COLUMNS_OSE_GNL)):
                                if gnl[COLUMNS_OSE_GNL[i]] != gnl[COLUMNS_OSE_GNL[i - 1]] or i == 8:
                                    writer_gnl_min.writerow({
                                        NAME_AMEBA: name,
                                        TIME_AMEBA: self._date_gnl_min(COLUMNS_OSE_GNL[i], str(j)),
                                        VALUE_AMEBA: gnl[COLUMNS_OSE_GNL[i]],
                                    })
                else:
                    if gnl[COLUMNS_OSE_GNL[6]] == 'CenPotMax':
                        for i in range(8, len(COLUMNS_OSE_GNL)):
                            if gnl[COLUMNS_OSE_GNL[i]] != gnl[COLUMNS_OSE_GNL[i - 1]] or i == 8:
                                writer_gnl_max.writerow({
                                    NAME_AMEBA: name,
                                    TIME_AMEBA: self._date_gnl(COLUMNS_OSE_GNL[i], gnl[COLUMNS_OSE_GNL[2]]),
                                    VALUE_AMEBA: gnl[COLUMNS_OSE_GNL[i]],
                                })

                    elif gnl[COLUMNS_OSE_GNL[6]] == 'CenPotMin':
                        for i in range(8, len(COLUMNS_OSE_GNL)):
                            if gnl[COLUMNS_OSE_GNL[i]] != gnl[COLUMNS_OSE_GNL[i - 1]] or i == 8:
                                writer_gnl_min.writerow({
                                    NAME_AMEBA: name,
                                    TIME_AMEBA: self._date_gnl(COLUMNS_OSE_GNL[i], gnl[COLUMNS_OSE_GNL[2]]),
                                    VALUE_AMEBA: gnl[COLUMNS_OSE_GNL[i]],
                                })

    def run(self):
        """Main execution point."""
        self._convert_profile_gnl()


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
    ProfileGnl(args.ose_dir, args.ameba_dir).run()


if __name__ == '__main__':
    main()
