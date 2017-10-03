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
import copy
import itertools
from workalendar.america import Chile

CAL = Chile()

from parameters import *
from functions import *

"""_______________________________________________________________________________"""
""" DEMAND LOAD PARAMETERS """

FILE_OSE_IND_1_SING = 'DemIndBloOpt_16_SIMP_SING.csv'
FILE_OSE_IND_2_SING = 'DemIndDat.csv'
FILE_OSE_VEG_1_SING = 'DemVegBloOpt_16_SIMP_SING.csv'
FILE_OSE_VEG_2_SING = 'DemVegBar.csv'
FILE_OSE_VEG_3_SING = 'DemVegDat.csv'
FILE_OSE_IND_OPT_1_SIC = 'DemIndBloOpt_16_SIMP_SIC.csv'
FILE_OSE_IND_OPT_2_SIC = 'DemIndDatOpt.csv'
FILE_OSE_VEG_OPT_1_SIC = 'DemVegBlo_16_SIMP_Opt.csv'
FILE_OSE_VEG_OPT_2_SIC = 'DemVegBarOpt.csv'
FILE_OSE_VEG_OPT_3_SIC = 'DemVegDatOpt.csv'
FILE_OSE_IND_OPE_1_SIC = 'DemIndBloOpe_16_SIMP_SIC.csv'
FILE_OSE_IND_OPE_2_SIC = 'DemIndDatOpe.csv'
FILE_OSE_VEG_OPE_1_SIC = 'DemVegBlo_16_SIMP_Ope.csv'
FILE_OSE_VEG_OPE_2_SIC = 'DemVegBarOpe.csv'
FILE_OSE_VEG_OPE_3_SIC = 'DemVegDatOpe.csv'

OSE_IND_YEAR = 'DemIndA\xf1oIni'
OSE_IND_BAR = 'DemIndBar'
OSE_IND_BLOCK = 'DemIndIBlo'
OSE_VEG_YEAR = 'DemVegA\xf1oIni'
OSE_VEG_BAR = 'DemVegBar'
OSE_VEG_BLOCK = 'DemVegIBlo'
OSE_MONTHS_1 = ['Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic', 'Ene', 'Feb', 'Mar']
OSE_MONTHS_2 = ['MesAbr', 'MesMay', 'MesJun', 'MesJul', 'MesAgo', 'MesSep', 'MesOct', 'MesNov', 'MesDic', 'MesEne',
                'MesFeb', 'MesMar']

FILE_DEM_AMEBA = 'ele-demand-load.csv'
FILE_BLOCK_AMEBA = 'TIME-BLOCK-STAGE.csv'

DEM_TIME_AMEBA = 'time'
DEM_NAME_AMEBA = 'name'
DEM_SCENARIO_AMEBA = 'scenario'
DEM_BLOCK_AMEBA = 'block'
DEM_STAGE_AMEBA = 'stage'
DEM_BUSBAR_AMEBA = 'busbar'

MONTH_INDEX = {1: 9, 2: 10, 3: 11, 4: 0, 5: 1, 6: 2,
               7: 3, 8: 4, 9: 5, 10: 6, 11: 7, 12: 8}
MONTH_HRS = {9: 744, 10: 672, 11: 744, 0: 720, 1: 744, 2: 720,
             3: 744, 4: 744, 5: 720, 6: 744, 7: 720, 8: 744}

HRS_REDUCED = True

MAX_BLOCK = 16
DEC_NUM = 1


class DemandLoad(object):
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

    def _time_year(self, year):
        dates = []
        for i in range(0, 8760, 1):
            dates.append({DEM_TIME_AMEBA: datetime.datetime(year, 01, 01, 00, 00, 00) + datetime.timedelta(hours=i)})
        return dates

    # def _get_block(self, tablaAsign, hour, month):
    #     for element in tablaAsign:
    #         if str(element['hora']) == hour:
    #             return str(element[month])

    def _date_time(self, date_time, year):
        month = date_time.month
        day = date_time.day
        hour = date_time.hour
        return str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2) + '-' + str(hour).zfill(2) + ':00'

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

        dic_tabla_habil = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))

        """ READER SING"""
        dic_ind_1_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_DEM, DIR_OSE_IND), FILE_OSE_IND_1_SING, self._ose_dir))
        dic_ind_2_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_DEM, DIR_OSE_IND), FILE_OSE_IND_2_SING, self._ose_dir))

        dic_veg_1_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_1_SING, self._ose_dir))
        dic_veg_2_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_2_SING, self._ose_dir))
        dic_veg_3_SING = list(
            reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_3_SING, self._ose_dir))
        """ READER SIC"""
        if self._model in ['Ope', 'ope', 'OPE']:
            dic_ind_1_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_IND), FILE_OSE_IND_OPE_1_SIC, self._ose_dir))
            dic_ind_2_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_IND), FILE_OSE_IND_OPE_2_SIC, self._ose_dir))

            dic_veg_1_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_OPE_1_SIC, self._ose_dir))
            dic_veg_2_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_OPE_2_SIC, self._ose_dir))
            dic_veg_3_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_OPE_3_SIC, self._ose_dir))
        else:  # if self._model in ['Opt','opt','OPT']:
            dic_ind_1_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_IND), FILE_OSE_IND_OPT_1_SIC, self._ose_dir))
            dic_ind_2_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_IND), FILE_OSE_IND_OPT_2_SIC, self._ose_dir))

            dic_veg_1_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_OPT_1_SIC, self._ose_dir))
            dic_veg_2_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_OPT_2_SIC, self._ose_dir))
            dic_veg_3_SIC = list(
                reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_DEM, DIR_OSE_VEG), FILE_OSE_VEG_OPT_3_SIC, self._ose_dir))

        """ Find the initial and last year of every file"""
        dic_ind_1_SING_max_year = self._get_max_year(dic_ind_1_SING, OSE_IND_YEAR)
        dic_ind_2_SING_max_year = self._get_max_year(dic_ind_2_SING, OSE_IND_YEAR)
        dic_veg_1_SING_max_year = self._get_max_year(dic_veg_1_SING, OSE_VEG_YEAR)
        dic_veg_2_SING_max_year = self._get_max_year(dic_veg_2_SING, OSE_VEG_YEAR)
        dic_veg_3_SING_max_year = self._get_max_year(dic_veg_3_SING, OSE_VEG_YEAR)

        dic_ind_1_SING_min_year = self._get_min_year(dic_ind_1_SING, OSE_IND_YEAR)
        dic_ind_2_SING_min_year = self._get_min_year(dic_ind_2_SING, OSE_IND_YEAR)
        dic_veg_1_SING_min_year = self._get_min_year(dic_veg_1_SING, OSE_VEG_YEAR)
        dic_veg_2_SING_min_year = self._get_min_year(dic_veg_2_SING, OSE_VEG_YEAR)
        dic_veg_3_SING_min_year = self._get_min_year(dic_veg_3_SING, OSE_VEG_YEAR)

        dic_ind_1_SIC_max_year = self._get_max_year(dic_ind_1_SIC, OSE_IND_YEAR)
        dic_ind_2_SIC_max_year = self._get_max_year(dic_ind_2_SIC, OSE_IND_YEAR)
        dic_veg_1_SIC_max_year = self._get_max_year(dic_veg_1_SIC, OSE_VEG_YEAR)
        dic_veg_2_SIC_max_year = self._get_max_year(dic_veg_2_SIC, OSE_VEG_YEAR)
        dic_veg_3_SIC_max_year = self._get_max_year(dic_veg_3_SIC, OSE_VEG_YEAR)

        dic_ind_1_SIC_min_year = self._get_min_year(dic_ind_1_SIC, OSE_IND_YEAR)
        dic_ind_2_SIC_min_year = self._get_min_year(dic_ind_2_SIC, OSE_IND_YEAR)
        dic_veg_1_SIC_min_year = self._get_min_year(dic_veg_1_SIC, OSE_VEG_YEAR)
        dic_veg_2_SIC_min_year = self._get_min_year(dic_veg_2_SIC, OSE_VEG_YEAR)
        dic_veg_3_SIC_min_year = self._get_min_year(dic_veg_3_SIC, OSE_VEG_YEAR)

        dem_factor_ind_SING = SearchDemandFactor(MAX_BLOCK, dic_ind_1_SING_min_year, dic_ind_1_SING_max_year,
                                                 dic_ind_1_SING, [OSE_IND_YEAR, OSE_IND_BAR, OSE_IND_BLOCK],
                                                 OSE_MONTHS_1)
        energy_ind_SING = SearchEnergy(dic_ind_2_SING_min_year, dic_ind_2_SING_max_year, dic_ind_2_SING,
                                       [OSE_IND_YEAR, OSE_IND_BAR], OSE_MONTHS_1)

        dem_factor_veg_SING = SearchDemandFactor(MAX_BLOCK, dic_veg_1_SING_min_year, dic_veg_1_SING_max_year,
                                                 dic_veg_1_SING, [OSE_VEG_YEAR, OSE_VEG_BAR, OSE_VEG_BLOCK],
                                                 OSE_MONTHS_1)
        energy_factor_veg_SING = SearchEnergy(dic_veg_2_SING_min_year, dic_veg_2_SING_max_year, dic_veg_2_SING,
                                              [OSE_VEG_YEAR, OSE_VEG_BAR], OSE_MONTHS_1)
        energy_veg_SING = SearchYearEnergy(dic_veg_3_SING_min_year, dic_veg_3_SING_max_year, dic_veg_3_SING,
                                           OSE_MONTHS_1)

        dem_factor_ind_SIC = SearchDemandFactor(MAX_BLOCK, dic_ind_1_SIC_min_year, dic_ind_1_SIC_max_year,
                                                dic_ind_1_SIC, [OSE_IND_YEAR, OSE_IND_BAR, OSE_IND_BLOCK], OSE_MONTHS_2)
        energy_ind_SIC = SearchEnergy(dic_ind_2_SIC_min_year, dic_ind_2_SIC_max_year, dic_ind_2_SIC,
                                      [OSE_IND_YEAR, OSE_IND_BAR], OSE_MONTHS_1)

        dem_factor_veg_SIC = SearchDemandFactor(MAX_BLOCK, dic_veg_1_SIC_min_year, dic_veg_1_SIC_max_year,
                                                dic_veg_1_SIC, [OSE_VEG_YEAR, OSE_VEG_BAR, OSE_VEG_BLOCK], OSE_MONTHS_2)
        energy_factor_veg_SIC = SearchEnergy(dic_veg_2_SIC_min_year, dic_veg_2_SIC_max_year, dic_veg_2_SIC,
                                             [OSE_VEG_YEAR, OSE_VEG_BAR], OSE_MONTHS_1)
        energy_veg_SIC = SearchYearEnergy(dic_veg_3_SIC_min_year, dic_veg_3_SIC_max_year, dic_veg_3_SIC, OSE_MONTHS_1)

        """ demand profile duration"""
        # TODO: Replace below correct column values
        demand = self._time_year(int(self._year_ose))

        """ SIC & SING BAR LIST"""
        bar_ind_SING = []
        for row in dic_ind_2_SING:
            if row[OSE_IND_YEAR] == self._year_ini:
                bar_ind_SING.append({DEM_NAME_AMEBA: row[OSE_IND_BAR]})
        bar_veg_SING = []
        for row in dic_veg_2_SING:
            if row[OSE_VEG_YEAR] == self._year_ini:
                bar_veg_SING.append({DEM_NAME_AMEBA: row[OSE_VEG_BAR]})
        bar_ind_SIC = []
        for row in dic_ind_2_SIC:
            if row[OSE_IND_YEAR] == self._year_ini:
                bar_ind_SIC.append({DEM_NAME_AMEBA: row[OSE_IND_BAR]})
        bar_veg_SIC = []
        for row in dic_veg_2_SIC:
            if row[OSE_VEG_YEAR] == self._year_ini:
                bar_veg_SIC.append({DEM_NAME_AMEBA: row[OSE_VEG_BAR]})

        """ DATES OF 1 YEAR & RESPECTIVE BLOCK LIST """
        demand_reduced = []
        for i in range(0, len(demand)):
            if demand[i][DEM_TIME_AMEBA].weekday() == 6 or demand[i][
                DEM_TIME_AMEBA].weekday() == 5 or CAL.is_working_day(demand[i][DEM_TIME_AMEBA]) is False:
                block = get_block(dic_tabla_no_habil, str(demand[i][DEM_TIME_AMEBA].hour + 1),
                                  str(demand[i][DEM_TIME_AMEBA].month))
            else:
                block = get_block(dic_tabla_habil, str(demand[i][DEM_TIME_AMEBA].hour + 1),
                                  str(demand[i][DEM_TIME_AMEBA].month))

            demand[i].update({DEM_BLOCK_AMEBA: block})
            demand[i].update({DEM_SCENARIO_AMEBA: 'demanda_OSE'})
            demand[i].update({DEM_STAGE_AMEBA: demand[i][DEM_TIME_AMEBA].month})

            if i == 0:
                demand_reduced.append(demand[i])
                continue
            if demand[i][DEM_BLOCK_AMEBA] != demand[i - 1][DEM_BLOCK_AMEBA]:
                demand_reduced.append(demand[i])
            elif demand[i][DEM_BLOCK_AMEBA] == demand[i - 1][DEM_BLOCK_AMEBA] and demand[i][DEM_TIME_AMEBA].month != \
                    demand[i - 1][DEM_TIME_AMEBA].month:
                demand_reduced.append(demand[i])

        """ DATES FOR ALL YEARS"""
        indexed_parameter = []
        i = 0
        profile_demand_iter = demand_reduced if HRS_REDUCED is True else demand

        for years in range(int(self._year_ini), int(self._year_end) + 1):
            for element in (profile_demand_iter):
                indexed_parameter.append(copy.deepcopy(element))
                indexed_parameter[i].update({DEM_TIME_AMEBA: element.copy()[DEM_TIME_AMEBA].replace(year=years)})
                i += 1

        """ BLOCK & STAGE GENERATOR"""
        dem1 = []
        i = 0
        for years in range(int(self._year_ini), int(self._year_end) + 1):
            for element in (demand):
                if years == int(self._year_ini):
                    dem1.append(copy.deepcopy(element))
                    dem1[i].update({DEM_TIME_AMEBA: element.copy()[DEM_TIME_AMEBA].replace(year=years)})
                else:
                    dem1.append(copy.deepcopy(element))
                    dem1[i].update({DEM_TIME_AMEBA: element.copy()[DEM_TIME_AMEBA].replace(year=years)})
                    delta = years - int(self._year_ini)
                    dem1[i].update({DEM_STAGE_AMEBA: int(element.copy()[DEM_STAGE_AMEBA]) + (12 * delta)})
                i += 1
        # - - - - - STAGE-BLOCK STRUCTURE FILE - - - - - #
        """ CHECK IF DIRECTORY EXIST """
        directory = os.path.join(self._ameba_dir, DIR_AMEBA_DEM)
        check_directory(directory)

        writer_block = writer_csv(FILE_BLOCK_AMEBA, ['time', DEM_STAGE_AMEBA, DEM_BLOCK_AMEBA],
                                  os.path.join(self._ameba_dir, DIR_AMEBA_DEM))
        writer_block.writeheader()

        for element in dem1:
            element.update({'time': self._date_time(element['time'], element['time'].year)})
            element.pop(DEM_SCENARIO_AMEBA)
            writer_block.writerow(element)

        # - - - - - INDEXED PARAMETERS FILE - - - - - #
        """ ASSIGN VALUE FOR RESPECTIVE DATE AND BLOCK"""
        for element in indexed_parameter:
            year = int(element[DEM_TIME_AMEBA].year)
            block = int(element[DEM_BLOCK_AMEBA])
            month = MONTH_INDEX[int(element[DEM_TIME_AMEBA].month)]

            """ check year of every file to search"""
            if month > 8 and year != 2017:
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

            """ assing values from name and date"""
            for name_ind in bar_ind_SING:
                name = name_ind[DEM_NAME_AMEBA]
                value_dem_factor = float(dem_factor_ind_SING.get_demand_factor(year_ind1_sing, block, name)[month])
                value_ene = float(energy_ind_SING.get_energy(year_ind2_sing, name)[month])
                value = value_dem_factor * value_ene * 1000 / MONTH_HRS[month]
                element.update({str(remove(name_ind[DEM_NAME_AMEBA])) + '_ind': round(value, DEC_NUM)})
            for name_veg in bar_veg_SING:
                name = name_veg[DEM_NAME_AMEBA]
                value_dem_factor = float(dem_factor_veg_SING.get_demand_factor(year_veg1_sing, block, name)[month])
                value_ene_factor = float(energy_factor_veg_SING.get_energy(year_veg2_sing, name)[month])
                value_ene = float(energy_veg_SING.get_energy(year_veg3_sing)[month])
                value = (value_dem_factor * value_ene_factor * 1000 / MONTH_HRS[month]) * value_ene
                element.update({str(remove(name_veg[DEM_NAME_AMEBA])) + '_veg': round(value, DEC_NUM)})
            for name_ind in bar_ind_SIC:
                name = name_ind[DEM_NAME_AMEBA]
                value_dem_factor = float(dem_factor_ind_SIC.get_demand_factor(year_ind1_sic, block, name)[month])
                value_ene = float(energy_ind_SIC.get_energy(year_ind2_sic, name)[month])
                value = value_dem_factor * value_ene * 1000 / MONTH_HRS[month]
                element.update({str(remove(name_ind[DEM_NAME_AMEBA])) + '_ind': round(value, DEC_NUM)})
            for name_veg in bar_veg_SIC:
                name = name_veg[DEM_NAME_AMEBA]

                value_dem_factor = float(dem_factor_veg_SIC.get_demand_factor(year_veg1_sic, block, name)[month])
                value_ene_factor = float(energy_factor_veg_SIC.get_energy(year_veg2_sic, name)[month])
                value_ene = float(energy_veg_SIC.get_energy(year_veg3_sic)[month])
                value = (value_dem_factor * value_ene_factor * 1000 / MONTH_HRS[month]) * value_ene
                element.update({str(remove(name_veg[DEM_NAME_AMEBA])) + '_veg': round(value, DEC_NUM)})

            element.update({DEM_TIME_AMEBA: self._date_time(element[DEM_TIME_AMEBA], element[DEM_TIME_AMEBA].year)})

        # ESCRIBE ARCHIVO Y ELIMINA VALORES REPETIDOS
        directory = os.path.join(self._ameba_dir, DIR_AMEBA_GENERATOR)
        check_directory(directory)

        header = indexed_parameter[0].keys()
        header.remove('time')
        header.remove('scenario')
        header.remove('block')
        header.remove('stage')

        output_file = writer_csv(FILE_DEM_AMEBA, ['name', 'time', 'scenario', 'value'],
                                     os.path.join(self._ameba_dir, DIR_AMEBA_DEM))
        output_file.writeheader()
        # REMOVER VALORES REPETIDOS
        for h in header:
            for i in range(0, len(indexed_parameter)):
                if indexed_parameter[i][h] == indexed_parameter[i - 1][h] and i > 0 and HRS_REDUCED:
                    continue
                output_file.writerow(
                    dict(name=h, time=indexed_parameter[i]['time'], scenario=indexed_parameter[i]['scenario'],
                         value=indexed_parameter[i][h]))

        # - - - - - PARAMETERS FILE - - - - - #
        writer_par = writer_csv('ele-demand_par.csv', [DEM_NAME_AMEBA, DEM_BUSBAR_AMEBA],
                                os.path.join(self._ameba_dir, DIR_AMEBA_DEM))
        writer_par.writeheader()
        for bar in itertools.chain(bar_veg_SIC, bar_veg_SING):
            writer_par.writerow({
                DEM_NAME_AMEBA : remove(bar[DEM_NAME_AMEBA]) + '_veg',
                DEM_BUSBAR_AMEBA : remove(bar[DEM_NAME_AMEBA])
            })
        for bar in itertools.chain(bar_ind_SIC, bar_ind_SING):
            writer_par.writerow({
                DEM_NAME_AMEBA : remove(bar[DEM_NAME_AMEBA]) + '_ind',
                DEM_BUSBAR_AMEBA : remove(bar[DEM_NAME_AMEBA])
            })

    def run(self):
        """Main execution point."""
        self._convert_demand()

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
        list_ind_1 = [dict() for _ in range(dim)]

        for row in self.__reader:
            list_ind_1[self.__get_index(int(row[self.__columns[0]]), int(row[self.__columns[2]]))][
                row[self.__columns[1]]] = [row[month] for month in self.__months]
        return list_ind_1

    def get_demand_factor(self, year, block, bar_name):
        return list(self.__list_ind[self.__get_index(year, block)][bar_name])


class SearchEnergy(object):
    def __init__(self, ini_year, last_year, reader, columns, months):
        self.__months = months
        self.__columns = columns
        self.__ini_year = ini_year
        self.__reader = reader
        self.__list_ind = self.__load_data((last_year - ini_year + 1))

    def __get_index(self, year):
        return (year - self.__ini_year)

    def __load_data(self, dim):
        list_ind_1 = [dict() for _ in range(dim)]

        for row in self.__reader:
            list_ind_1[self.__get_index(int(row[self.__columns[0]]))][row[self.__columns[1]]] = [row[month] for month in
                                                                                                 self.__months]
        return list_ind_1

    def get_energy(self, year, bar_name):
        return list(self.__list_ind[self.__get_index(year)][bar_name])


class SearchYearEnergy(object):
    def __init__(self, ini_year, last_year, reader, months):
        self.__months = months
        self.__ini_year = ini_year
        self.__reader = reader
        self.__list_ind = self.__load_data((last_year - ini_year + 1))

    def __get_index(self, year):
        return (year - self.__ini_year)

    def __load_data(self, dim):
        list_ind_1 = [dict() for _ in range(dim)]

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
    DemandLoad(args.ose_dir, args.ameba_dir, args.model, args.year_ini, args.year_end, args.year_ose).run()


if __name__ == '__main__':
    main()
