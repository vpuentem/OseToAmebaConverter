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

from functions import *
from parameters import *
from profiles_ERNC import *

FILE_AMEBA_WIND = 'ele-profile_wind_blocks.csv'
FILE_AMEBA_SOLAR = 'ele-profile_solar_blocks.csv'

COLUMNS_OSE_PMAX = ['CenPotMax','CenAux','CenNom']

TIME_AMEBA = 'time'
NAME_AMEBA = 'name'
SCENARIO_AMEBA = 'scenario'
PMAX_AMEBA = 'Pmax'
BLOCK_AMEBA = 'block'
STAGE_AMEBA = 'stage'

WIND_OSE = 'Eolica'
SOLAR_OSE = 'Solar'
MONTHS_OSE = ['abr','may','jun','jul','ago','sep','oct','nov','dic','ene','feb','mar']
BLOCK_OSE = 'CenIBlo'
NAME_OSE = 'CenNom'

MONTH_INDEX = {1:9, 2:10, 3:11, 4:0, 5:1, 6:2 ,
7:3, 8:4, 9:5, 10:6, 11:7 , 12:8}

DEC_NUM = 3
BLOCK_NUM = 16
MONTH_NUM = 12

year_OSE = '2013'
year_ini = '2017'

class ProfilesBlock(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba_demand.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def __block_length_dates(self, year, block_length):
        """
        @param block_length: list
        @param year: int
        """
        dates = []
        for month_num in range(1,MONTH_NUM+1):
            for block_num in range(1,BLOCK_NUM+1):
                if block_num == 1:
                    dates.append({ TIME_AMEBA : datetime.datetime(year, month_num, 01, 00, 00, 00),
                                   BLOCK_AMEBA : block_num,
                                   SCENARIO_AMEBA : 'profile_OSE'
                                 })

                else:
                    block_hours = int(block_length[month_num-1][str(block_num-1)])
                    dates.append({ TIME_AMEBA : dates[-1][TIME_AMEBA]+datetime.timedelta(hours=block_hours),
                                   BLOCK_AMEBA : block_num,
                                   SCENARIO_AMEBA : 'profile_OSE'
                                 })
        return dates


    def __get_block(self, tablaAsign, hour, month):

        for element in tablaAsign:
            if str(element['hora']) == hour:
                return str(element[month])

    def __update_value(self, gen_list, block_value_list_name, block_num, month_num, profile, gen_type):
        for gen in gen_list:

            gen_name = qwerty(gen[NAME_AMEBA])
            block_value_list = block_value_list_name.get_profile_value2(block_num,gen_name)
            if block_value_list is None:
                profile_value = 1
            else:

                profile_value = (
                    float(block_value_list[month_num]) /
                    float(gen[PMAX_AMEBA])
                )
            if profile_value > 1:
                profile_value = 1

            profile.update({remove(gen[NAME_AMEBA])+'_'+gen_type: round(profile_value,DEC_NUM)})

    def __convert_profile_wind(self):
        """Reads profiles from OSE2000 format and write Ameba profiles."""

        dic_tabla_habil = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))
        dic_tabla_duracion = list(reader_csv('', BLOCK_LENGTH, self._ose_dir))

        dic_wind_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_WIND_SIC, self._ose_dir))
        dic_Pmax_SIC_1 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_2, self._ose_dir))
        dic_Pmax_SIC_2 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_1, self._ose_dir))

        dic_wind_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_WIND_SING, self._ose_dir))
        dic_Pmax_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SING_1, self._ose_dir))

        block_value_SIC = SearchProfile(BLOCK_NUM, dic_wind_SIC, NAME_OSE, BLOCK_OSE, MONTHS_OSE)
        block_value_SING = SearchProfile(BLOCK_NUM, dic_wind_SING, NAME_OSE, BLOCK_OSE, MONTHS_OSE)

        profile_wind=self.__block_length_dates(int(year_OSE), dic_tabla_duracion)

        """ LIST OF GEN NAMES AND PMAX"""
        Gen_wind_SIC = []
        for gen_pmax in itertools.chain(dic_Pmax_SIC_1,dic_Pmax_SIC_2):
                if gen_pmax[COLUMNS_OSE_PMAX[1]] == WIND_OSE:
                    Gen_wind_SIC.append({NAME_AMEBA : gen_pmax[COLUMNS_OSE_PMAX[2]], PMAX_AMEBA:gen_pmax[COLUMNS_OSE_PMAX[0]]})
        Gen_wind_SING = []
        for gen_pmax in itertools.chain(dic_Pmax_SING):
                if gen_pmax[COLUMNS_OSE_PMAX[1]] == WIND_OSE:
                    Gen_wind_SING.append({NAME_AMEBA : gen_pmax[COLUMNS_OSE_PMAX[2]], PMAX_AMEBA:gen_pmax[COLUMNS_OSE_PMAX[0]]})

        for profile in profile_wind:
            block_num = int(profile[BLOCK_AMEBA])
            month_num = MONTH_INDEX[int(profile[TIME_AMEBA].month)]

            for gen in Gen_wind_SIC:
                gen_name = qwerty(gen[NAME_AMEBA])
                value = float(block_value_SIC.get_profile_value(block_num,gen_name)[month_num])/float(gen[PMAX_AMEBA])
                profile.update({remove(gen[NAME_AMEBA])+'_wind': round(value,DEC_NUM)})
            for gen in Gen_wind_SING:
                gen_name = qwerty(gen[NAME_AMEBA])
                value = float(block_value_SING.get_profile_value(block_num,gen_name)[month_num])/float(gen[PMAX_AMEBA])
                profile.update({remove(gen[NAME_AMEBA])+'_wind': round(value,DEC_NUM)})
            profile.update({TIME_AMEBA : profile[TIME_AMEBA].replace(year=int(year_ini))})
            profile.update({TIME_AMEBA: datetime_to_ameba2(profile[TIME_AMEBA],profile[TIME_AMEBA].year)})

        Columns=profile_wind[0].keys()
        Columns.insert(0, Columns.pop(Columns.index(TIME_AMEBA)))
        Columns.insert(1, Columns.pop(Columns.index('scenario')))

        Columns.pop(Columns.index('block'))

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_PROFILE)
        check_directory(directory)

        writer = writer_csv(FILE_AMEBA_WIND, Columns, os.path.join(self._ameba_dir,DIR_AMEBA_PROFILE))
        writer.writeheader()

        for profile in profile_wind:
            profile.pop('block')
            writer.writerow(profile)

    def __convert_profile_solar(self):
        """Reads profiles from OSE2000 format and write Ameba profiles."""

        dic_tabla_habil = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))
        dic_tabla_duracion = list(reader_csv('', BLOCK_LENGTH, self._ose_dir))

        # TODO: Replace directory and file name below with correct one
        dic_solar_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_SOLAR_SIC, self._ose_dir))
        dic_Pmax_SIC_1 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_2, self._ose_dir))
        dic_Pmax_SIC_2 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SIC_OPT_1, self._ose_dir))

        dic_solar_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_SOLAR_SING, self._ose_dir))
        dic_Pmax_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_GENERATOR,DIR_OSE_THERMAL), FILE_OSE_THERMAL_SING_1, self._ose_dir))

        block_value_SIC = SearchProfile(BLOCK_NUM, dic_solar_SIC, NAME_OSE, BLOCK_OSE, MONTHS_OSE)
        block_value_SING = SearchProfile(BLOCK_NUM, dic_solar_SING, NAME_OSE, BLOCK_OSE, MONTHS_OSE)

        profile_solar=self.__block_length_dates(int(year_OSE), dic_tabla_duracion)

        """ LIST OF GEN NAMES AND PMAX"""
        Gen_solar_SIC = []
        for gen_pmax in itertools.chain(dic_Pmax_SIC_1,dic_Pmax_SIC_2):
                if gen_pmax[COLUMNS_OSE_PMAX[1]] == SOLAR_OSE:
                    Gen_solar_SIC.append({NAME_AMEBA : gen_pmax[COLUMNS_OSE_PMAX[2]], PMAX_AMEBA:gen_pmax[COLUMNS_OSE_PMAX[0]]})
        Gen_solar_SING = []
        for gen_pmax in itertools.chain(dic_Pmax_SING):
                if gen_pmax[COLUMNS_OSE_PMAX[1]] == SOLAR_OSE:
                    Gen_solar_SING.append({NAME_AMEBA : gen_pmax[COLUMNS_OSE_PMAX[2]], PMAX_AMEBA:gen_pmax[COLUMNS_OSE_PMAX[0]]})

        for profile in profile_solar:

            block_num = int(profile[BLOCK_AMEBA])
            month_num = MONTH_INDEX[int(profile[TIME_AMEBA].month)]
            self.__update_value(Gen_solar_SIC, block_value_SIC, block_num, month_num, profile, 'solar')

            self.__update_value(Gen_solar_SING, block_value_SING, block_num, month_num, profile, 'solar')
            profile.update({TIME_AMEBA : profile[TIME_AMEBA].replace(year=int(year_ini))})
            profile.update({TIME_AMEBA: datetime_to_ameba2(profile[TIME_AMEBA],profile[TIME_AMEBA].year)})

        Columns=profile_solar[0].keys()
        Columns.insert(0, Columns.pop(Columns.index(TIME_AMEBA)))
        Columns.insert(1, Columns.pop(Columns.index('scenario')))

        Columns.pop(Columns.index('block'))

        writer = writer_csv(FILE_AMEBA_SOLAR, Columns, os.path.join(self._ameba_dir,DIR_AMEBA_PROFILE))
        writer.writeheader()

        for profile in profile_solar:
            profile.pop('block')
            writer.writerow(profile)

    def run(self):
        """Main execution point."""
        self.__convert_profile_wind()
        self.__convert_profile_solar()
        print 'profile_power_block ready'

def qwerty(name):
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

            list_profile[self.__get_index( int(row[self.__block_OSE]))][qwerty(row[self.__name_OSE])] = [row[month] for month in self.__months]

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
    Profiles(args.ose_dir, args.ameba_dir, args.model).run()


if __name__ == '__main__':
    main()
