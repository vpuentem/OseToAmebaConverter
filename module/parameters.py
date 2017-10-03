#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""_______________________________________________________________________________"""
""" GENERAL PARAMETERS """

""" DIR NAMES """
DIR_OSE_SIC = 'SIC'
DIR_OSE_SING = 'SING'
DIR_OSE_SIX = 'SIX'

""" SUB DIR NAMES """
DIR_OSE_BUSBAR = 'Bar'
DIR_OSE_BRANCH = 'Lin'
DIR_OSE_GENERATOR = 'Cen'
DIR_OSE_INFLOW = 'Afl'
DIR_OSE_DEM = 'Dem'
DIR_OSE_DAM = 'Emb'

DIR_AMEBA_BUSBAR = 'busbar'
DIR_AMEBA_BRANCH = 'branch'
DIR_AMEBA_GENERATOR = 'generator'
DIR_AMEBA_FUEL = 'fuel'
DIR_AMEBA_INFLOW = 'inflow'
DIR_AMEBA_PROFILE = 'profile'
DIR_AMEBA_IRRIGATION = 'irrigation'
DIR_AMEBA_DEM = 'demandload'
DIR_AMEBA_DAM = 'dam'

""" SUB SUB DIR NAMES"""
DIR_OSE_THERMAL = 'Termica'
DIR_OSE_PAS = 'Pasada'
DIR_OSE_EMB = 'Embalse'
DIR_OSE_SER = 'Serie'
DIR_OSE_VIRTUAL = 'Virtual'
# DIR_OSE_EMB='Emb'

DIR_OSE_IND = 'Industrial'
DIR_OSE_VEG = 'Vegetativa'

""" GENERAL FILES"""

TABLA_HABIL = 'Asignaciondiahabil.csv'
TABLA_NO_HABIL = 'Asignaciondianohabil.csv'
BLOCK_LENGTH = 'tabla_duracion.csv'

"""_______________________________________________________________________________"""
""" GNL PROFILE PARAMETERS """
FILE_AMEBA_PROFILE_GNL_MAX_SIC = 'ele-profile_gnl_max_SIC.csv'
FILE_AMEBA_PROFILE_GNL_MIN_SIC = 'ele-profile_gnl_min_SIC.csv'

FILE_OSE_GNL_PROFILE_SIC1 = 'CenTerEtaPMax_GNL_SIC.csv'
FILE_OSE_GNL_PROFILE_SIC2 = 'CenTerEtaPMax_TERMICAS.csv'
FILE_OSE_GNL_PROFILE_SING = 'CenTerEtaPMax_GNL_SING.csv'

GEN_TIME_AMEBA = 'time'
GEN_VALUE_AMEBA = 'value'

"""_______________________________________________________________________________"""
""" FUEL PARAMETERS """

FILE_OSE_FUEL_SIC = 'CenTerEtaCVar.csv'
FILE_OSE_FUEL_SING = 'CenTerEtaCVar.csv'

FILE_AMEBA_FUEL = 'ele-fuel.csv'
FILE_AMEBA_FUEL_PROFILE = 'ele-fuel_profile.csv'

"""_______________________________________________________________________________"""
""" POWER PARAMETERS """

FILE_AMEBA_WIND = 'ele-profile_wind.csv'
FILE_AMEBA_SOLAR = 'ele-profile_solar.csv'

FILE_OSE_WIND_SIC = 'CenTerEtaPMax_EOLICA_16blo_SIC.csv'
FILE_OSE_SOLAR_SIC = 'CenTerEtaPMax_SOLAR_16blo_SIC.csv'
FILE_OSE_WIND_SING = 'CenTerEtaPMax SING_Eolico.csv'
FILE_OSE_SOLAR_SING = 'CenTerEtaPMax SING_Solar.csv'

GEN_SCENARIO_AMEBA = 'scenario'
GEN_BLOCK_AMEBA = 'block'

WIND_OSE = 'Eolica'
SOLAR_OSE = 'Solar'
GEN_BLOCK_OSE = 'CenIBlo'

MONTHS_OSE = ['abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic', 'ene', 'feb', 'mar']

"""_______________________________________________________________________________"""
""" VIRTUAL PARAMETERS """

FILE_OSE_VIRTUAL_SIC_OPT = 'CenVirParOpt.csv'
FILE_OSE_VIRTUAL_SIC_OPE = 'CenVirParOpe.csv'
FILE_OSE_IRRIGATION = 'cenvireta.csv'

FILE_AMEBA_HYDRO_CONNECTION = 'ele-hydro-connection.csv'
FILE_AMEBA_IRRIGATION = 'ele-irrigation.csv'

"""_______________________________________________________________________________"""
""" DICTIONARY OSE2AMEBA PARAMETERS """

MONTH_NUM = {'ABR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DIC': 12, 'ENE': 1,
             'FEB': 2, 'MAR': 3}
MONTH_HRS = {'ENE': 744, 'FEB': 672, 'MAR': 744, 'ABR': 720, 'MAY': 744, 'JUN': 720,
             'JUL': 744, 'AGO': 744, 'SEP': 720, 'OCT': 744, 'NOV': 720, 'DIC': 744}

WEEK_TO_MONTH = {1: 4, 2: 4, 3: 4, 4: 4,
                 5: 5, 6: 5, 7: 5, 8: 5,
                 9: 6, 10: 6, 11: 6, 12: 6,
                 13: 7, 14: 7, 15: 7, 16: 7,
                 17: 8, 18: 8, 19: 8, 20: 8,
                 21: 9, 22: 9, 23: 9, 24: 9,
                 25: 10, 26: 10, 27: 10, 28: 10,
                 29: 11, 30: 11, 31: 11, 32: 11,
                 33: 12, 34: 12, 35: 12, 36: 12,
                 37: 1, 38: 1, 39: 1, 40: 1,
                 41: 2, 42: 2, 43: 2, 44: 2,
                 45: 3, 46: 3, 47: 3, 48: 3}
