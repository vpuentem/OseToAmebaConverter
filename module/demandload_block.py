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
import copy
from workalendar.america import Chile
import debugger
from operator import itemgetter
from parameters import *
from functions import *
from demandload import *

FILE_AMEBA='ele-demand-load-blocks.csv'

COLUMNS_OSE_IND_2 = ['DemIndA\xf1oIni','DemIndBar','Abr','May','Jun','Jul',
                    'Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']

#columas ArchivoOSE_veg_2
COLUMNS_OSE_VEG_2 = ['DemVegA\xf1oIni','DemVegBar','Abr','May','Jun','Jul','Ago',
                    'Sep','Oct','Nov','Dic','Ene','Feb','Mar']

TIME_AMEBA = 'time'
NAME_AMEBA = 'name'
BLOCK_AMEBA = 'block'
STAGE_AMEBA = 'stage'
SCENARIO_AMEBA = 'scenario'
COLUMNS_BLOCK=[TIME_AMEBA,STAGE_AMEBA,BLOCK_AMEBA]

MONTH_INDEX = {1:9, 2:10, 3:11, 4:0, 5:1, 6:2 ,
7:3, 8:4, 9:5, 10:6, 11:7 , 12:8}

MONTH_HRS = {9: 744, 10: 672, 11: 744, 0: 720, 1: 744, 2: 720,
3: 744, 4: 744, 5: 720, 6: 744, 7: 720, 8: 744 }

OSE_IND_YEAR = 'DemIndA\xf1oIni'
OSE_IND_BAR = 'DemIndBar'
OSE_IND_BLOCK = 'DemIndIBlo'
OSE_VEG_YEAR = 'DemVegA\xf1oIni'
OSE_VEG_BAR = 'DemVegBar'
OSE_VEG_BLOCK = 'DemVegIBlo'
OSE_MONTHS_1 = ['Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']
OSE_MONTHS_2 = ['MesAbr','MesMay','MesJun','MesJul','MesAgo','MesSep','MesOct','MesNov','MesDic','MesEne','MesFeb','MesMar']

MAX_BLOCK = 16
MONTH_NUM = 12

class DemandLoadBlock(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model, year_ini, year_end, year_ose):
        """Constructor of OSE2Ameba_demand.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        @param model: string
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model
        self._year_ini = year_ini
        self._year_end = year_end
        self._year_ose = year_ose

    def __block_length_dates(self, year, block_length):
        """
        @param block_length: list
        @param year: int
        """
        dates = []
        for month_num in range(1,MONTH_NUM+1):
            for block_num in range(1,MAX_BLOCK+1):
                if block_num == 1:
                    dates.append({ TIME_AMEBA : datetime.datetime(year, month_num, 01, 00, 00, 00),
                                   BLOCK_AMEBA : block_num,
                                   STAGE_AMEBA : month_num,
                                   SCENARIO_AMEBA : 'demanda_OSE'
                                 })

                else:
                    block_hours = int(block_length[month_num-1][str(block_num-1)])
                    dates.append({ TIME_AMEBA : dates[-1][TIME_AMEBA]+datetime.timedelta(hours=block_hours),
                                   BLOCK_AMEBA : block_num,
                                   STAGE_AMEBA : month_num,
                                   SCENARIO_AMEBA : 'demanda_OSE'
                                 })
        return dates

    def __block_distribution(self, block_length_dates):
        all_dates = []

        block_length_dates.append(copy.deepcopy(block_length_dates[0]))
        year_at = block_length_dates[-1][TIME_AMEBA].year
        block_length_dates[-1].update({TIME_AMEBA : block_length_dates[-1][TIME_AMEBA].replace(year=year_at+1)})

        for date in range(0,len(block_length_dates)-1):
            all_dates.append(copy.deepcopy(block_length_dates[date]))

            while  all_dates[-1][TIME_AMEBA] < block_length_dates[date+1][TIME_AMEBA]-datetime.timedelta(hours=1):
                all_dates.append(copy.deepcopy(all_dates[-1]))
                all_dates[-1].update({TIME_AMEBA : all_dates[-1][TIME_AMEBA]+datetime.timedelta(hours=1)})
        del block_length_dates[-1]

        return all_dates

    def _date_time(self,date_time,year):
        month=date_time.month
        day=date_time.day
        hour=date_time.hour
        return str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'-'+str(hour).zfill(2)+':00'
    def _get_max_year(self, dic, year_column_name):
        max_year = 0
        for row in dic:
            year = int(row[year_column_name])
            if year > max_year:
                max_year = year
        return max_year

    def _get_min_year(self, dic, year_column_name):
        min_year = 3000
        for row in dic:
            year = int(row[year_column_name])
            if year < min_year:
                min_year = year
        return min_year


    def _convert_demand(self):
        """Reads demand from OSE2000 format and write Ameba demand."""

        dic_TABLA_HABIL = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))
        dic_tabla_duracion = list(reader_csv('', BLOCK_LENGTH, self._ose_dir))

        # TODO: Replace directory and file name below with correct one
        # If we integrate Ameba code we can import libraries with correct names
        """ READER SING"""
        dic_ind_1_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_DEM,DIR_OSE_IND), FILE_OSE_IND_1_SING, self._ose_dir))
        dic_ind_2_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_DEM,DIR_OSE_IND), FILE_OSE_IND_2_SING, self._ose_dir))

        dic_veg_1_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_1_SING, self._ose_dir))
        dic_veg_2_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_2_SING, self._ose_dir))
        dic_veg_3_SING = list(reader_csv(os.path.join(DIR_OSE_SING,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_3_SING, self._ose_dir))
        """ READER SIC"""
        if self._model in ['Ope','ope','OPE']:
            dic_ind_1_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_IND), FILE_OSE_IND_OPE_1_SIC, self._ose_dir))
            dic_ind_2_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_IND), FILE_OSE_IND_OPE_2_SIC, self._ose_dir))

            dic_veg_1_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_OPE_1_SIC, self._ose_dir))
            dic_veg_2_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_OPE_2_SIC, self._ose_dir))
            dic_veg_3_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_OPE_3_SIC, self._ose_dir))
        else: # if self._model in ['Opt','opt','OPT']:
            dic_ind_1_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_IND), FILE_OSE_IND_OPT_1_SIC, self._ose_dir))
            dic_ind_2_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_IND), FILE_OSE_IND_OPT_2_SIC, self._ose_dir))

            dic_veg_1_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_OPT_1_SIC, self._ose_dir))
            dic_veg_2_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_OPT_2_SIC, self._ose_dir))
            dic_veg_3_SIC = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_DEM,DIR_OSE_VEG), FILE_OSE_VEG_OPT_3_SIC, self._ose_dir))

        """ """

        """ Find the initial and last year of every file"""
        dic_ind_1_SING_max_year = self._get_max_year(dic_ind_1_SING,OSE_IND_YEAR)
        dic_ind_2_SING_max_year = self._get_max_year(dic_ind_2_SING,OSE_IND_YEAR)
        dic_veg_1_SING_max_year = self._get_max_year(dic_veg_1_SING,OSE_VEG_YEAR)
        dic_veg_2_SING_max_year = self._get_max_year(dic_veg_2_SING,OSE_VEG_YEAR)
        dic_veg_3_SING_max_year = self._get_max_year(dic_veg_3_SING,OSE_VEG_YEAR)

        dic_ind_1_SING_min_year = self._get_min_year(dic_ind_1_SING,OSE_IND_YEAR)
        dic_ind_2_SING_min_year = self._get_min_year(dic_ind_2_SING,OSE_IND_YEAR)
        dic_veg_1_SING_min_year = self._get_min_year(dic_veg_1_SING,OSE_VEG_YEAR)
        dic_veg_2_SING_min_year = self._get_min_year(dic_veg_2_SING,OSE_VEG_YEAR)
        dic_veg_3_SING_min_year = self._get_min_year(dic_veg_3_SING,OSE_VEG_YEAR)

        dic_ind_1_SIC_max_year = self._get_max_year(dic_ind_1_SIC,OSE_IND_YEAR)
        dic_ind_2_SIC_max_year = self._get_max_year(dic_ind_2_SIC,OSE_IND_YEAR)
        dic_veg_1_SIC_max_year = self._get_max_year(dic_veg_1_SIC,OSE_VEG_YEAR)
        dic_veg_2_SIC_max_year = self._get_max_year(dic_veg_2_SIC,OSE_VEG_YEAR)
        dic_veg_3_SIC_max_year = self._get_max_year(dic_veg_3_SIC,OSE_VEG_YEAR)

        dic_ind_1_SIC_min_year = self._get_min_year(dic_ind_1_SIC,OSE_IND_YEAR)
        dic_ind_2_SIC_min_year = self._get_min_year(dic_ind_2_SIC,OSE_IND_YEAR)
        dic_veg_1_SIC_min_year = self._get_min_year(dic_veg_1_SIC,OSE_VEG_YEAR)
        dic_veg_2_SIC_min_year = self._get_min_year(dic_veg_2_SIC,OSE_VEG_YEAR)
        dic_veg_3_SIC_min_year = self._get_min_year(dic_veg_3_SIC,OSE_VEG_YEAR)


        dem_factor_ind_SING = SearchDemandFactor(MAX_BLOCK, dic_ind_1_SING_min_year, dic_ind_1_SING_max_year, dic_ind_1_SING, [OSE_IND_YEAR, OSE_IND_BAR, OSE_IND_BLOCK], OSE_MONTHS_1)
        energy_ind_SING     = SearchEnergy(dic_ind_2_SING_min_year,dic_ind_2_SING_max_year, dic_ind_2_SING, [OSE_IND_YEAR, OSE_IND_BAR], OSE_MONTHS_1)

        dem_factor_veg_SING    = SearchDemandFactor(MAX_BLOCK, dic_veg_1_SING_min_year, dic_veg_1_SING_max_year, dic_veg_1_SING, [OSE_VEG_YEAR, OSE_VEG_BAR, OSE_VEG_BLOCK], OSE_MONTHS_1)
        energy_factor_veg_SING = SearchEnergy(dic_veg_2_SING_min_year,dic_veg_2_SING_max_year, dic_veg_2_SING, [OSE_VEG_YEAR, OSE_VEG_BAR], OSE_MONTHS_1)
        energy_veg_SING        = SearchYearEnergy(dic_veg_3_SING_min_year, dic_veg_3_SING_max_year, dic_veg_3_SING, OSE_MONTHS_1)

        dem_factor_ind_SIC = SearchDemandFactor(MAX_BLOCK, dic_ind_1_SIC_min_year, dic_ind_1_SIC_max_year, dic_ind_1_SIC, [OSE_IND_YEAR, OSE_IND_BAR, OSE_IND_BLOCK], OSE_MONTHS_2)
        energy_ind_SIC     = SearchEnergy(dic_ind_2_SIC_min_year,dic_ind_2_SIC_max_year, dic_ind_2_SIC, [OSE_IND_YEAR, OSE_IND_BAR], OSE_MONTHS_1)

        dem_factor_veg_SIC    = SearchDemandFactor(MAX_BLOCK, dic_veg_1_SIC_min_year, dic_veg_1_SIC_max_year, dic_veg_1_SIC, [OSE_VEG_YEAR, OSE_VEG_BAR, OSE_VEG_BLOCK], OSE_MONTHS_2)
        energy_factor_veg_SIC = SearchEnergy(dic_veg_2_SIC_min_year,dic_veg_2_SIC_max_year, dic_veg_2_SIC, [OSE_VEG_YEAR, OSE_VEG_BAR], OSE_MONTHS_1)
        energy_veg_SIC        = SearchYearEnergy(dic_veg_3_SIC_min_year, dic_veg_3_SIC_max_year, dic_veg_3_SIC, OSE_MONTHS_1)


        """ demand profile duration"""
        demand = self.__block_length_dates(int(self._year_ose), dic_tabla_duracion)

        """ STAGE & BLOCK GENERATOR"""
        block_distribution_year = self.__block_distribution(demand)
        block_distribution = []
        for years in range(int(self._year_ini),int(self._year_end)+1):
            for block in block_distribution_year:
                block_distribution.append(copy.deepcopy(block))

                block_distribution[-1].update({TIME_AMEBA : block_distribution[-1][TIME_AMEBA].replace(year=years)})
                delta = years-int(self._year_ini)
                block_distribution[-1].update({STAGE_AMEBA : int(block_distribution[-1][STAGE_AMEBA])+(12*delta)})

        """ CHECK IF DIRECTORY EXIST """
        directory = os.path.join(self._ameba_dir,DIR_AMEBA_DEM)
        check_directory(directory)

        writer_block = writer_csv('block_distribution.csv', COLUMNS_BLOCK, os.path.join(self._ameba_dir,DIR_AMEBA_DEM))
        writer_block.writeheader()

        for block in block_distribution:
            block.update({TIME_AMEBA: self._date_time(block[TIME_AMEBA],block[TIME_AMEBA].year)})
            block.pop(SCENARIO_AMEBA)

            writer_block.writerow(block)

        """ SIC AND SING BAR LIST"""
        bar_ind_SING=[]
        for row in dic_ind_2_SING:
            if row[COLUMNS_OSE_IND_2[0]]==self._year_ini:
                bar_ind_SING.append({NAME_AMEBA:row[COLUMNS_OSE_IND_2[1]]})
        bar_veg_SING=[]
        for row in dic_veg_2_SING:
            if row[COLUMNS_OSE_VEG_2[0]]==self._year_ini:
                bar_veg_SING.append({NAME_AMEBA:row[COLUMNS_OSE_VEG_2[1]]})
        bar_ind_SIC=[]
        for row in dic_ind_2_SIC:
            if row[COLUMNS_OSE_IND_2[0]]==self._year_ini:
                bar_ind_SIC.append({NAME_AMEBA:row[COLUMNS_OSE_IND_2[1]]})
        bar_veg_SIC=[]
        for row in dic_veg_2_SIC:
            if row[COLUMNS_OSE_VEG_2[0]]==self._year_ini:
                bar_veg_SIC.append({NAME_AMEBA:row[COLUMNS_OSE_VEG_2[1]]})

        """ genera lista para todos los años"""
        dem=[]
        i=0
        for years in range(int(self._year_ini),int(self._year_end)+1):
            for element in demand:
                dem.append(copy.deepcopy(element))
                dem[i].update({ TIME_AMEBA:element.copy()[TIME_AMEBA].replace(year=years )})
                i+=1


        """ MAIN PART"""
        dec_num = 1

        for element in dem:
            year = int(element[TIME_AMEBA].year)
            block = int(element[BLOCK_AMEBA])
            month = MONTH_INDEX[int(element[STAGE_AMEBA])]

            if month > 8:
                year = year - 1

            year_ind1_sic = year
            year_ind2_sic = year
            year_ind1_sing = year
            year_ind2_sing = year
            year_veg1_sic = year
            year_veg2_sic = year
            year_veg3_sic = year
            year_veg1_sing = year
            year_veg2_sing = year
            year_veg3_sing = year

            if year_ind1_sing < dic_ind_1_SING_min_year:
                year_ind1_sing = dic_ind_1_SING_min_year
            if year_ind2_sing < dic_ind_2_SING_min_year:
                year_ind2_sing = dic_ind_2_SING_min_year

            if year_veg1_sing < dic_veg_1_SING_min_year:
                year_veg1_sing = dic_veg_1_SING_min_year
            if year_veg2_sing < dic_veg_2_SING_min_year:
                year_veg2_sing = dic_veg_2_SING_min_year
            if year_veg3_sing < dic_veg_3_SING_min_year:
                year_veg3_sing = dic_veg_3_SING_min_year

            if year_ind1_sic < dic_ind_1_SIC_min_year:
                year_ind1_sic = dic_ind_1_SIC_min_year
            if year_ind2_sic < dic_ind_2_SIC_min_year:
                year_ind2_sic = dic_ind_2_SIC_min_year

            if year_veg1_sic < dic_veg_1_SIC_min_year:
                year_veg1_sic = dic_veg_1_SIC_min_year
            if year_veg2_sic < dic_veg_2_SIC_min_year:
                year_veg2_sic = dic_veg_2_SIC_min_year
            if year_veg3_sic < dic_veg_3_SIC_min_year:
                year_veg3_sic = dic_veg_3_SIC_min_year

            for name_ind in bar_ind_SING:
                name = name_ind[NAME_AMEBA]
                value_dem_factor = float(dem_factor_ind_SING.get_demand_factor(year_ind1_sing, block, name)[month])
                value_ene = float(energy_ind_SING.get_energy(year_ind2_sing, name)[month])
                value = value_dem_factor*value_ene*1000/MONTH_HRS[month]

                element.update({str(remove(name_ind[NAME_AMEBA]))+'_ind': round(value,dec_num)})
            for name_veg in bar_veg_SING:
                name = name_veg[NAME_AMEBA]
                value_dem_factor = float(dem_factor_veg_SING.get_demand_factor(year_veg1_sing, block, name)[month])
                value_ene_factor = float(energy_factor_veg_SING.get_energy(year_veg2_sing, name)[month])
                value_ene = float(energy_veg_SING.get_energy(year_veg3_sing)[month])
                value = (value_dem_factor*value_ene_factor*1000/MONTH_HRS[month])*value_ene
                element.update({str(remove(name_veg['name']))+'_veg': round(value,dec_num)})

            for name_ind in bar_ind_SIC:
                name = name_ind[NAME_AMEBA]
                value_dem_factor = float(dem_factor_ind_SIC.get_demand_factor(year_ind1_sic, block, name)[month])
                value_ene = float(energy_ind_SIC.get_energy(year_ind2_sic, name)[month])
                value = value_dem_factor*value_ene*1000/MONTH_HRS[month]

                element.update({str(remove(name_ind[NAME_AMEBA]))+'_ind': round(value,dec_num)})
            for name_veg in bar_veg_SIC:
                name = name_veg[NAME_AMEBA]

                value_dem_factor = float(dem_factor_veg_SIC.get_demand_factor(year_veg1_sic, block, name)[month])
                value_ene_factor = float(energy_factor_veg_SIC.get_energy(year_veg2_sic, name)[month])
                value_ene = float(energy_veg_SIC.get_energy(year_veg3_sic)[month])

                value = (value_dem_factor*value_ene_factor*1000/MONTH_HRS[month])*value_ene
                element.update({str(remove(name_veg['name']))+'_veg': round(value,dec_num)})
            element.update({TIME_AMEBA: self._date_time(element[TIME_AMEBA],element[TIME_AMEBA].year)})

        columns=dem[0].keys()
        columns.insert(0, columns.pop(columns.index(TIME_AMEBA)))
        columns.insert(1, columns.pop(columns.index('scenario')))

        columns.pop(columns.index('block'))
        columns.pop(columns.index(STAGE_AMEBA))

        """ CHECK IF DIRECTORY EXIST """
        directory = os.path.join(self._ameba_dir,DIR_AMEBA_DEM)
        check_directory(directory)

        writer = writer_csv(FILE_AMEBA, columns, os.path.join(self._ameba_dir,DIR_AMEBA_DEM))
        writer.writeheader()

        for element in dem:
            element.pop(BLOCK_AMEBA)
            element.pop(STAGE_AMEBA)
            writer.writerow(element)

    def run(self):
        """Main execution point."""
        self._convert_demand()
        print 'demandload_block ready'


class SearchDemandFactor(object):
    """ """
    def __init__(self, max_block, ini_year, last_year, reader, columns, months):
        """
        @param max_block : {int}
        @param ini_year : {int}
        @param last_year : {int}
        @param reader : {csv.DictReader}
        @param columns : {list of string}
        @param months : {list of string}
        """
        self.__months = months
        self.__columns = columns
        self.__max_block = max_block
        self.__ini_year = ini_year
        self.__reader = reader
        self.__list_ind = self.__load_data(
            (last_year - ini_year + 1) * max_block
        )
    def __get_index(self, year, block):
        return (year - self.__ini_year) * self.__max_block + block - 1
    def __load_data(self, dim):
        list_ind_1=[dict() for _ in range(dim)]

        for row in self.__reader:
            list_ind_1[self.__get_index(int(row[self.__columns[0]]), int(row[self.__columns[2]]))][row[self.__columns[1]]] = [row[month] for month in self.__months]
        return list_ind_1
    def get_demand_factor(self, year, block, bar_name):
        return list(self.__list_ind[self.__get_index(year, block)][bar_name])

class SearchEnergy(object):
    def __init__(self, ini_year, last_year, reader, columns, months):
        self.__months = months
        self.__columns = columns
        self.__ini_year = ini_year
        self.__reader = reader
        self.__list_ind = self.__load_data((last_year - ini_year + 1) )
    def __get_index(self, year):
        return (year - self.__ini_year)
    def __load_data(self, dim):
        list_ind_1=[dict() for _ in range(dim)]

        for row in self.__reader:
            list_ind_1[self.__get_index(int(row[self.__columns[0]]))][row[self.__columns[1]]] = [row[month] for month in self.__months]
        return list_ind_1
    def get_energy(self, year, bar_name):
        return list(self.__list_ind[self.__get_index(year)][bar_name])

class SearchYearEnergy(object):
    def __init__(self, ini_year, last_year, reader, months):
        self.__months = months
        self.__ini_year = ini_year
        self.__reader = reader
        self.__list_ind = self.__load_data((last_year - ini_year + 1) )
    def __get_index(self, year):
        return (year - self.__ini_year)
    def __load_data(self, dim):
        list_ind_1=[dict() for _ in range(dim)]

        for row in self.__reader:
            list_ind_1[self.__get_index(int(row[OSE_VEG_YEAR]))] = [row[month] for month in self.__months]
        return list_ind_1
    def get_energy(self, year):
        return list(self.__list_ind[self.__get_index(year)])


def main():
    """Main program."""
    parser = argparse.ArgumentParser(description='OSE2000 to Ameba converter')
    parser.add_argument(
        'ose_dir', type=str, help='directory to read OSE2000 files from')
    parser.add_argument(
        'ameba_dir', type=str, help='directory to write Ameba files to')
    parser.add_argument(
        'model', type=str, help='select model to get data from (Opt or Ope)')
    parser.add_argument(
        'year_ini', type=str, help='initial year to generate indexed demandload')
    parser.add_argument(
        'year_end', type=str, help='final year to generate indexed demandload')
    parser.add_argument(
        'year_ose', type=str, help='year take dates from')
    args = parser.parse_args()
    DemandLoadBlock(args.ose_dir, args.ameba_dir, args.model, args.year_ini, args.year_end, args.year_ose).run()

if __name__ == '__main__':
    main()
