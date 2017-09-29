# coding=utf-8
"""ose2ameba_profiles_ERNC: Script to convert an OSE2000 database into Ameba CSV format.
_______________________________________________________________________________
Copyright (c) 2017 AMEBA-Dev - Consultora SPEC Limitada
This software cannot be distributed.
For more information, visit ameba.spec.cl
Current version developer: Ameba Team
_______________________________________________________________________________
"""
import argparse
import os

import datetime
# from datetime import timedelta
import itertools

from workalendar.america import Chile

from parameters import *
from functions import *
from generator import*

MONTH_INDEX = {1: 9, 2: 10, 3: 11, 4: 0, 5: 1, 6: 2,
               7: 3, 8: 4, 9: 5, 10: 6, 11: 7, 12: 8}

CAL = Chile()

MONTH_NAME = {1: 'ene', 2: 'feb', 3: 'mar', 4: 'abr', 5: 'may', 6: 'jun',
              7: 'jul', 8: 'ago', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dic'}

HRS_REDUCED = True
DEC_NUM = 3

YEAR_OSE = '2013'
YEAR_INI = '2017'

MAX_BLOCK = 16


class ProfilePower(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba_demand.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        @param model:
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def __time_year(self, year):
        dates = []
        for i in range(0, 8760, 1):
            dates.append({GEN_TIME_AMEBA: (datetime.datetime(year, 01, 01, 00, 00, 00) + datetime.timedelta(hours=i))})
        return dates

    def __get_block(self, tablaAsign, hour, month):
        for element in tablaAsign:
            if str(element['hora']) == hour:
                return str(element[month])

    def __update_value(self, gen_list, block_value_list_name, block_num, month_num, profile, gen_type):
        for gen in gen_list:
            gen_name = remove_upper(gen[GEN_NAME_AMEBA])
            block_value_list = block_value_list_name.get_profile_value2(block_num, gen_name)
            if block_value_list is None:
                profile_value = 1
            else:
                profile_value = (
                    float(block_value_list[month_num]) /
                    float(gen[GEN_PMAX_AMEBA])
                )
            if profile_value > 1:
                profile_value = 1
            profile.update({remove(gen[GEN_NAME_AMEBA]) + '_' + gen_type: round(profile_value, DEC_NUM)})

    def __convert_profile_wind(self):
        """Reads profiles from OSE2000 format and write Ameba profiles."""

        dic_tabla_habil = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))

        dic_wind_SIC = list(
            reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_WIND_SIC, self._ose_dir))

        if self._model in ['Ope', 'ope', 'OPE']:
            dic_Pmax_SIC_1 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPE_2,
                           self._ose_dir))
            dic_Pmax_SIC_2 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPE_1,
                           self._ose_dir))

        else:  # if self._model in ['Opt', 'opt', 'OPT']:
            dic_Pmax_SIC_1 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_2,
                           self._ose_dir))
            dic_Pmax_SIC_2 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_1,
                           self._ose_dir))

        dic_wind_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_WIND_SING,
                       self._ose_dir))
        dic_Pmax_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SING_1,
                       self._ose_dir))

        block_value_SIC = SearchProfile(MAX_BLOCK, dic_wind_SIC, GEN_NAME_OSE, GEN_BLOCK_OSE, MONTHS_OSE)
        block_value_SING = SearchProfile(MAX_BLOCK, dic_wind_SING, GEN_NAME_OSE, GEN_BLOCK_OSE, MONTHS_OSE)

        profile_wind = self.__time_year(int(YEAR_OSE))

        """ LIST OF GEN NAMES AND PMAX"""
        Gen_wind_SIC = []
        for gen_pmax in itertools.chain(dic_Pmax_SIC_1, dic_Pmax_SIC_2):
            if gen_pmax[GEN_TYPE_OSE] == WIND_OSE:
                Gen_wind_SIC.append({GEN_NAME_AMEBA: gen_pmax[GEN_NAME_OSE], GEN_PMAX_AMEBA: gen_pmax[GEN_PMAX_OSE]})
        Gen_wind_SING = []
        for gen_pmax in itertools.chain(dic_Pmax_SING):
            if gen_pmax[GEN_TYPE_OSE] == WIND_OSE:
                Gen_wind_SING.append({GEN_NAME_AMEBA: gen_pmax[GEN_NAME_OSE], GEN_PMAX_AMEBA: gen_pmax[GEN_PMAX_OSE]})

        """ LIST OF DATES, SCENARIO AND BLOCK """
        profile_wind_reduced = []
        for i in range(0, len(profile_wind)):
            if profile_wind[i][GEN_TIME_AMEBA].weekday() == 6 or profile_wind[i][
                GEN_TIME_AMEBA].weekday() == 5 or CAL.is_working_day(profile_wind[i][GEN_TIME_AMEBA]) is False:
                block = self.__get_block(dic_tabla_no_habil, str(profile_wind[i][GEN_TIME_AMEBA].hour + 1),
                                         str(profile_wind[i][GEN_TIME_AMEBA].month))
            else:
                block = self.__get_block(dic_tabla_habil, str(profile_wind[i][GEN_TIME_AMEBA].hour + 1),
                                         str(profile_wind[i][GEN_TIME_AMEBA].month))
            profile_wind[i].update({GEN_TIME_AMEBA: profile_wind[i][GEN_TIME_AMEBA].replace(year=int(YEAR_INI))})
            profile_wind[i].update({GEN_BLOCK_AMEBA: block})
            profile_wind[i].update({GEN_SCENARIO_AMEBA: 'profile_OSE'})
            if i == 0:
                profile_wind_reduced.append(profile_wind[i])
            elif profile_wind[i][GEN_BLOCK_AMEBA] != profile_wind[i - 1][GEN_BLOCK_AMEBA]:
                profile_wind_reduced.append(profile_wind[i])
            elif profile_wind[i][GEN_BLOCK_AMEBA] == profile_wind[i - 1][GEN_BLOCK_AMEBA] and profile_wind[i][
                GEN_TIME_AMEBA].month != profile_wind[i - 1][GEN_TIME_AMEBA].month:
                profile_wind_reduced.append(profile_wind[i])

        profile_wind_iter = profile_wind_reduced if HRS_REDUCED is True else profile_wind

        for profile in profile_wind_iter:
            block_num = int(profile[GEN_BLOCK_AMEBA])
            month_num = MONTH_INDEX[int(profile[GEN_TIME_AMEBA].month)]

            for gen in Gen_wind_SIC:
                gen_name = remove_upper(gen[GEN_NAME_AMEBA])
                value = float(block_value_SIC.get_profile_value(block_num, gen_name)[month_num]) / float(
                    gen[GEN_PMAX_AMEBA])
                profile.update({remove(gen[GEN_NAME_AMEBA]) + '_wind': round(value, DEC_NUM)})
            for gen in Gen_wind_SING:
                gen_name = remove_upper(gen[GEN_NAME_AMEBA])
                value = float(block_value_SING.get_profile_value(block_num, gen_name)[month_num]) / float(
                    gen[GEN_PMAX_AMEBA])
                profile.update({remove(gen[GEN_NAME_AMEBA]) + '_wind': round(value, DEC_NUM)})
            profile.update({GEN_TIME_AMEBA: datetime_to_ameba2(profile[GEN_TIME_AMEBA], profile[GEN_TIME_AMEBA].year)})

        # CHECK IF DIRECTORY EXIST
        directory = os.path.join(self._ameba_dir, DIR_AMEBA_PROFILE)
        check_directory(directory)

        names = profile_wind_iter[0].keys()
        names.remove('time')
        names.remove('scenario')
        names.remove('block')

        output_file = writer_csv(FILE_AMEBA_WIND, ['name', 'time', 'scenario', 'value'],
                                 os.path.join(self._ameba_dir, DIR_AMEBA_PROFILE))
        output_file.writeheader()
        # REMOVER VALORES REPETIDOS
        for name in names:
            for i in range(0, len(profile_wind_iter)):
                if profile_wind_iter[i][name] == profile_wind_iter[i - 1][name] and i > 0:
                    continue
                output_file.writerow(
                    dict(name=name, time=profile_wind_iter[i]['time'], scenario=profile_wind_iter[i]['scenario'],
                         value=profile_wind_iter[i][name]))

    def __convert_profile_solar(self):
        """Reads profiles from OSE2000 format and write Ameba profiles."""

        dic_tabla_habil = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))

        # TODO: Replace directory and file name below with correct one
        dic_solar_SIC = list(
            reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_SOLAR_SIC,
                       self._ose_dir))

        if self._model in ['Ope', 'ope', 'OPE']:
            dic_Pmax_SIC_1 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_2,
                           self._ose_dir))
            dic_Pmax_SIC_2 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_1,
                           self._ose_dir))
        else:  # if self._model in ['Opt', 'opt', 'OPT']:
            dic_Pmax_SIC_1 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_2,
                           self._ose_dir))
            dic_Pmax_SIC_2 = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_1,
                           self._ose_dir))

        dic_solar_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_SOLAR_SING,
                       self._ose_dir))
        dic_Pmax_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_GENERATOR, DIR_OSE_THERMAL), FILE_OSE_THERMAL_SING_1,
                       self._ose_dir))

        block_value_SIC = SearchProfile(MAX_BLOCK, dic_solar_SIC, GEN_NAME_OSE, GEN_BLOCK_OSE, MONTHS_OSE)
        block_value_SING = SearchProfile(MAX_BLOCK, dic_solar_SING, GEN_NAME_OSE, GEN_BLOCK_OSE, MONTHS_OSE)

        profile_solar = self.__time_year(int(YEAR_OSE))

        """ LIST OF GEN NAMES AND PMAX"""
        Gen_solar_SIC = []
        for gen_pmax in itertools.chain(dic_Pmax_SIC_1, dic_Pmax_SIC_2):
            if gen_pmax[GEN_TYPE_OSE] == SOLAR_OSE:
                Gen_solar_SIC.append({GEN_NAME_AMEBA: gen_pmax[GEN_NAME_OSE], GEN_PMAX_AMEBA: gen_pmax[GEN_PMAX_OSE]})
        Gen_solar_SING = []
        for gen_pmax in itertools.chain(dic_Pmax_SING):
            if gen_pmax[GEN_TYPE_OSE] == SOLAR_OSE:
                Gen_solar_SING.append({GEN_NAME_AMEBA: gen_pmax[GEN_NAME_OSE], GEN_PMAX_AMEBA: gen_pmax[GEN_PMAX_OSE]})

        """ LIST OF DATES, SCENARIO AND BLOCK """
        profile_solar_reduced = []
        for i in range(0, len(profile_solar)):
            if profile_solar[i][GEN_TIME_AMEBA].weekday() == 6 or profile_solar[i][
                GEN_TIME_AMEBA].weekday() == 5 or CAL.is_working_day(profile_solar[i][GEN_TIME_AMEBA]) is False:
                block = self.__get_block(dic_tabla_no_habil, str(profile_solar[i][GEN_TIME_AMEBA].hour + 1),
                                         str(profile_solar[i][GEN_TIME_AMEBA].month))
            else:
                block = self.__get_block(dic_tabla_habil, str(profile_solar[i][GEN_TIME_AMEBA].hour + 1),
                                         str(profile_solar[i][GEN_TIME_AMEBA].month))
            profile_solar[i].update({GEN_TIME_AMEBA: profile_solar[i][GEN_TIME_AMEBA].replace(year=int(YEAR_INI))})
            profile_solar[i].update({GEN_BLOCK_AMEBA: block})
            profile_solar[i].update({GEN_SCENARIO_AMEBA: 'profile_OSE'})
            if i == 0:
                profile_solar_reduced.append(profile_solar[i])
            elif profile_solar[i][GEN_BLOCK_AMEBA] != profile_solar[i - 1][GEN_BLOCK_AMEBA]:
                profile_solar_reduced.append(profile_solar[i])
            elif profile_solar[i][GEN_BLOCK_AMEBA] == profile_solar[i - 1][GEN_BLOCK_AMEBA] and profile_solar[i][
                GEN_TIME_AMEBA].month != profile_solar[i - 1][GEN_TIME_AMEBA].month:
                profile_solar_reduced.append(profile_solar[i])

        profile_solar_iter = profile_solar_reduced if HRS_REDUCED is True else profile_solar

        for profile in profile_solar_iter:
            block_num = int(profile[GEN_BLOCK_AMEBA])
            month_num = MONTH_INDEX[int(profile[GEN_TIME_AMEBA].month)]
            self.__update_value(Gen_solar_SIC, block_value_SIC, block_num, month_num, profile, 'solar')
            self.__update_value(Gen_solar_SING, block_value_SING, block_num, month_num, profile, 'solar')
            profile.update({GEN_TIME_AMEBA: datetime_to_ameba2(profile[GEN_TIME_AMEBA], profile[GEN_TIME_AMEBA].year)})

        directory = os.path.join(self._ameba_dir, DIR_AMEBA_PROFILE)
        check_directory(directory)

        names = profile_solar_iter[0].keys()
        names.remove('time')
        names.remove('scenario')
        names.remove('block')

        output_file = writer_csv(FILE_AMEBA_SOLAR, ['name', 'time', 'scenario', 'value'], os.path.join(self._ameba_dir, DIR_AMEBA_PROFILE))
        output_file.writeheader()
        # REMOVER VALORES REPETIDOS
        for name in names:
            for i in range(0, len(profile_solar_iter)):
                if profile_solar_iter[i][name] == profile_solar_iter[i - 1][name] and i > 0:
                    continue
                output_file.writerow(
                    dict(name=name, time=profile_solar_iter[i]['time'], scenario=profile_solar_iter[i]['scenario'],
                         value=profile_solar_iter[i][name]))

    def run(self):
        """Main execution point."""
        self.__convert_profile_wind()
        print 'profile wind ready'
        self.__convert_profile_solar()
        print 'profile solar ready'

def remove_upper(name):
    return remove(name).upper()

class SearchProfile(object):
    """ """

    def __init__(self, max_block, reader, name_OSE, block_OSE, months):
        """
        @param max_block : {int}
        @param reader : {csv.DictReader or list}
        @param name_OSE : {string}
        @param block_OSE : {string}
        @param months : {list of string}
        """
        self.__months = months
        self.__name_OSE = name_OSE
        self.__block_OSE = block_OSE
        self.__max_block = max_block
        self.__reader = reader
        self.__list_profile = self.__load_data(self.__max_block)

    def __get_index(self, block):
        return block - 1

    def __load_data(self, dim):
        list_profile = [dict() for _ in range(dim)]
        for row in self.__reader:
            list_profile[self.__get_index(int(row[self.__block_OSE]))][remove_upper(row[self.__name_OSE])] = \
                                                                                [row[month] for month in self.__months]
        return list_profile

    def get_profile_value(self, block, gen_name):
        return self.__list_profile[self.__get_index(block)][gen_name]

    def get_profile_value2(self, block, gen_name):
        return self.__list_profile[self.__get_index(block)].get(gen_name)


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
    ProfilePower(args.ose_dir, args.ameba_dir, args.model).run()


if __name__ == '__main__':
    main()
