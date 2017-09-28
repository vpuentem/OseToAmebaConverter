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
DIR_OSE_DAM='Emb'

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
DIR_OSE_THERMAL='Termica'
DIR_OSE_PAS='Pasada'
DIR_OSE_EMB='Embalse'
DIR_OSE_SER='Serie'
DIR_OSE_VIRTUAL = 'Virtual'
#DIR_OSE_EMB='Emb'

DIR_OSE_IND = 'Industrial'
DIR_OSE_VEG = 'Vegetativa'

""" GENERAL FILES"""

TABLA_HABIL='Asignaciondiahabil.csv'
TABLA_NO_HABIL='Asignaciondianohabil.csv'
BLOCK_LENGTH = 'tabla_duracion.csv'

"""_______________________________________________________________________________"""
""" BUSBAR PARAMETERS """

""" FILE NAMES """
FILE_OSE_BUSBAR_SIC_OPT = 'BarDatParOpt.csv'
FILE_OSE_BUSBAR_SIC_OPE = 'BarDatParOpe.csv'
FILE_OSE_BUSBAR_SING = 'BarDatPar.csv'
FILE_AMEBA_BUSBAR = 'ele-busbar.csv'
""" OSE & AMEBA COLUMN NAMES """
BUSBAR_NAME_OSE = 'BarNom'
BUSBAR_START_TIME_OSE = 'BarFecOpeIni'
BUSBAR_END_TIME_OSE = 'BarFecOpeFin'
BUSBAR_VOLTAGE_OSE = 'BarVtjBas'
BUSBAR_NAME_AMEBA = 'name'
BUSBAR_START_TIME_AMEBA = 'start_time'
BUSBAR_END_TIME_AMEBA = 'end_time'
BUSBAR_VOLTAGE_AMEBA = 'voltage'
BUSBAR_OPE_OSE='BarFOpe'


"""_______________________________________________________________________________"""
""" BRANCH PARAMETERS """

""" FILE NAMES """
FILE_OSE_BRANCH_SIC_OPT = 'LinDatParOpt.csv'
FILE_OSE_BRANCH_SIC_OPE = 'LinDatParOpe.csv'
FILE_OSE_BRANCH_SING = 'LinDatPar.csv'
FILE_OSE_BRANCH_SIX = 'LinDatPar1500Lat.csv'
FILE_AMEBA_BRANCH = 'ele-branch.csv'
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

"""_______________________________________________________________________________"""
""" BRANCH MAXFLOW PARAMETERS """

FILE_OSE_BRANCH_MAXFLOW_SIC_OPT = 'LinDatManOpt.csv'
FILE_OSE_BRANCH_MAXFLOW_SIC_OPE = 'LinDatManOpe.csv'
FILE_OSE_BRANCH_MAXFLOW_SING = 'LinDatMan.csv'
FILE_AMEBA_BRANCH_MAXFLOW = 'ele-branch-maxflow.csv'

BRANCH_MAXFLOW_START_TIME_OSE = 'LinFecIni'
BRANCH_MAXFLOW_END_TIME_OSE = 'LinFecFin'
BRANCH_FLAG_MAXFLOW_OSE = 'LinFMan'

BRANCH_TIME_AMEBA = 'time'

"""_______________________________________________________________________________"""
""" GENERATOR PARAMETERS """

NAME_PV=['PV','Solar']
NAME_WIND=['Eolica']
NAME_THERMAL=['Petróleo Diesel', 'Carbón', 'Petróleo IFO-180', 'Biomasa']
NAME_HYDRO=['Pasada','Embalse','Serie']

FILE_OSE_THERMAL_SING_1='CenTerPar_SING.csv'
FILE_OSE_THERMAL_SIC_OPT_1='CenTerPar_Esc_SIC_Opt.csv'
FILE_OSE_THERMAL_SIC_OPT_2='CenTerPar_Exist+Const_SIC_Opt.csv'
FILE_OSE_THERMAL_SIC_OPT_3='CenTerPar_GNL_SIC_Opt.csv'
FILE_OSE_THERMAL_SIC_OPE_1='CenTerPar_Esc_SIC_Ope.csv'
FILE_OSE_THERMAL_SIC_OPE_2='CenTerPar_Exist+Const_SIC_Ope.csv'
FILE_OSE_THERMAL_SIC_OPE_3='CenTerPar_GNL_SIC_Ope.csv'
FILE_OSE_PAS_SIC_OPT_1='cenpaspar_Exis+Const_Opt.csv'
FILE_OSE_PAS_SIC_OPT_2='cenpaspar_Esc_Opt.csv'
FILE_OSE_PAS_SIC_OPE_1='cenpaspar_Exis+Const_Ope.csv'
FILE_OSE_PAS_SIC_OPE_2='cenpaspar_Esc_Ope.csv'
FILE_OSE_EMB_SIC_OPT_1='cenembparOpt.csv'
FILE_OSE_EMB_SIC_OPE_1='cenembparOpe.csv'
FILE_OSE_SER_SIC_OPT_1='censerparOpt.csv'
FILE_OSE_SER_SIC_OPE_1='censerparOpe.csv'

FILE_AMEBA_HYDRO='ele-hydro.csv'
FILE_AMEBA_THERMAL='ele-thermal.csv'
FILE_AMEBA_PV='ele-pv.csv'
FILE_AMEBA_CEN_WIND='ele-wind.csv'
""" OSE GENERATOR COLUMNS"""
GEN_NAME_OSE = 'CenNom'
GEN_START_TIME_OSE = 'CenFecOpeIni'
GEN_END_TIME_OSE = 'CenFecOpeFin'
GEN_LIFETIME_OSE = 'CenVidUti'
GEN_TYPE_OSE = 'CenAux'
GEN_CONNECTED_OSE = 'CenFOpe'
GEN_CO2_EMISSION_OSE = 'CenEmiDpz [tCO2e/GWh]'
GEN_CONTROL_AREAS_OSE = 'CenUbc'
GEN_IS_NCRE_OSE = 'CenFERNC'
GEN_PMAX_OSE = 'CenPotMax'
GEN_PMAX_OSE_PAS = 'CenPMax'
GEN_EFF_OSE = 'CenTurRen'
GEN_PMIN_OSE = 'CenPotMin'
GEN_HEATRATE_AVG_OSE = 'CenRenTer'
GEN_VOMC_AVG_OSE = 'CenCosOpe'
GEN_FORCED_OUTAGE_RATE_OSE = 'CenDisEne'
GEN_FUELNAME_OSE = 'CenEtaCVar'
GEN_AUXSERV_OSE = 'CenConPro%'
GEN_CANDIDATE_OSE = 'CenFInv'
GEN_INV_COST_OSE = 'CenVI'
GEN_FOM_COST_OSE = 'CenCOMA'
GEN_OWNER_OSE = 'CenCmr'
GEN_BUSBAR_OSE = 'CenBar'

GEN_NAME_AMEBA = 'name'
GEN_START_TIME_AMEBA = 'start_time'
GEN_END_TIME_AMEBA = 'end_time'
GEN_LIFETIME_AMEBA = 'lifetime'
GEN_TYPE_AMEBA = 'gtype'
GEN_CONNECTED_AMEBA = 'connected'
GEN_CO2_EMISSION_AMEBA = 'co2_emission'
GEN_CONTROL_AREAS_AMEBA = 'control_areas'
GEN_IS_NCRE_AMEBA = 'is_ncre'
GEN_PMAX_AMEBA = 'pmax'
GEN_EFF_AMEBA = 'eff'
GEN_PMIN_AMEBA = 'pmin'
GEN_HEATRATE_AVG_AMEBA = 'heatrate_avg'
GEN_VOMC_AVG_AMEBA = 'vomc_avg'
GEN_FORCED_OUTAGE_RATE_AMEBA = 'forced_outage_rate'
GEN_FUELNAME_AMEBA = 'fuel_name'
GEN_AUXSERV_AMEBA = 'auxserv'
GEN_CANDIDATE_AMEBA = 'candidate'
GEN_INV_COST_AMEBA = 'inv_cost'
GEN_FOM_COST_AMEBA = 'fom_cost'
GEN_OWNER_AMEBA = 'owner'
GEN_INITIAL_INVESTMENT_AMEBA = 'initial_investment'
GEN_ZONE_AMEBA = 'zone'
GEN_BUSBAR_AMEBA = 'busbar'

"""_______________________________________________________________________________"""
""" GENERATOR UNAVAILABILITY PARAMETERS """

FILE_OSE_THERMAL_SIC_UNAV='CenTerMan.csv'
FILE_OSE_THERMAL_SING_UNAV='CenTerMan.csv'
FILE_OSE_SER_SIC_UNAV='censerman.csv'
FILE_OSE_PAS_SIC_UNAV='cenpasman.csv'
FILE_OSE_EMB_SIC_UNAV='cenembman.csv'

FILE_AMEBA_GEN_UNAV='ele-gen-unavailability.csv'
"""_______________________________________________________________________________"""
""" GNL PROFILE PARAMETERS """
FILE_AMEBA_PROFILE_GNL_MAX_SIC = 'ele-profile_gnl_max_SIC.csv'
FILE_AMEBA_PROFILE_GNL_MIN_SIC = 'ele-profile_gnl_min_SIC.csv'

FILE_OSE_GNL_PROFILE_SIC1='CenTerEtaPMax_GNL_SIC.csv'
FILE_OSE_GNL_PROFILE_SIC2='CenTerEtaPMax_TERMICAS.csv'
FILE_OSE_GNL_PROFILE_SING='CenTerEtaPMax_GNL_SING.csv'

GEN_TIME_AMEBA = 'time'
GEN_NAME_AMEBA = 'name'
GEN_VALUE_AMEBA = 'value'

"""_______________________________________________________________________________"""
""" FUEL PARAMETERS """

FILE_OSE_FUEL_SIC = 'CenTerEtaCVar.csv'
FILE_OSE_FUEL_SING = 'CenTerEtaCVar.csv'

FILE_AMEBA_FUEL='ele-fuel.csv'
FILE_AMEBA_FUEL_PROFILE='ele-fuel_profile.csv'
"""_______________________________________________________________________________"""
""" INFLOW PARAMETERS """

FILE_OSE_EMB_1='AflBioBioEtaSemRal.csv'
FILE_OSE_EMB_2='AflChapoEtaSem.csv'
FILE_OSE_EMB_3='AflLajaEtaSem.csv'
FILE_OSE_EMB_4='AflMauleEtaSem.csv'
FILE_OSE_EMB_5='AflRapelEtaSem.csv'
FILE_OSE_PAS='EnePasEtaMen.csv'

FILE_AMEBA_EMB = 'ele-profile_emb.csv'
FILE_AMEBA_PAS = 'ele-profile_pas.csv'

COLUMNS_OSE_EMB=['AflNum','AflNom','AflAnoIni','AflAnoFin','AflIBlo','AflHid','AflEtaTip','AflDatTip','Sem01','Sem02','Sem03',
'Sem04','Sem05','Sem06','Sem07','Sem08','Sem09','Sem10','Sem11','Sem12','Sem13','Sem14','Sem15','Sem16','Sem17','Sem18','Sem19','Sem20',
'Sem21','Sem22','Sem23','Sem24','Sem25','Sem26','Sem27','Sem28','Sem29','Sem30','Sem31','Sem32','Sem33','Sem34','Sem35','Sem36','Sem37',
'Sem38','Sem39','Sem40','Sem41','Sem42','Sem43','Sem44','Sem45','Sem46','Sem47','Sem48']

COLUMNS_OSE_PAS=['AflNum','AflNom','AflAnoIni','AflAnoFin','AflIBlo','AflHid','AflEtaTip',
'AflDatTip','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC','ENE','FEB','MAR']

INFLOW_NAME_AMEBA = 'name'
INFLOW_TIME_AMEBA = 'time'
INFLOW_SCENARIO_AMEBA = 'scenario'
INFLOW_VALUE_AMEBA = 'value'

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

MONTHS_OSE = ['abr','may','jun','jul','ago','sep','oct','nov','dic','ene','feb','mar']

"""_______________________________________________________________________________"""
""" VIRTUAL PARAMETERS """

FILE_OSE_VIRTUAL_SIC_OPT='CenVirParOpt.csv'
FILE_OSE_VIRTUAL_SIC_OPE='CenVirParOpe.csv'
FILE_OSE_IRRIGATION='cenvireta.csv'

FILE_AMEBA_HYDRO_CONNECTION = 'ele-hydro-connection.csv'
FILE_AMEBA_IRRIGATION = 'ele-irrigation.csv'

"""_______________________________________________________________________________"""
""" DEMAND LOAD PARAMETERS """

FILE_OSE_IND_1_SING='DemIndBloOpt_16_SIMP_SING.csv'
FILE_OSE_IND_2_SING='DemIndDat.csv'
FILE_OSE_VEG_1_SING='DemVegBloOpt_16_SIMP_SING.csv'
FILE_OSE_VEG_2_SING='DemVegBar.csv'
FILE_OSE_VEG_3_SING='DemVegDat.csv'
FILE_OSE_IND_OPT_1_SIC='DemIndBloOpt_16_SIMP_SIC.csv'
FILE_OSE_IND_OPT_2_SIC='DemIndDatOpt.csv'
FILE_OSE_VEG_OPT_1_SIC='DemVegBlo_16_SIMP_Opt.csv'
FILE_OSE_VEG_OPT_2_SIC='DemVegBarOpt.csv'
FILE_OSE_VEG_OPT_3_SIC='DemVegDatOpt.csv'
FILE_OSE_IND_OPE_1_SIC='DemIndBloOpe_16_SIMP_SIC.csv'
FILE_OSE_IND_OPE_2_SIC='DemIndDatOpe.csv'
FILE_OSE_VEG_OPE_1_SIC='DemVegBlo_16_SIMP_Ope.csv'
FILE_OSE_VEG_OPE_2_SIC='DemVegBarOpe.csv'
FILE_OSE_VEG_OPE_3_SIC='DemVegDatOpe.csv'

OSE_IND_YEAR = 'DemIndA\xf1oIni'
OSE_IND_BAR = 'DemIndBar'
OSE_IND_BLOCK = 'DemIndIBlo'
OSE_VEG_YEAR = 'DemVegA\xf1oIni'
OSE_VEG_BAR = 'DemVegBar'
OSE_VEG_BLOCK = 'DemVegIBlo'
OSE_MONTHS_1 = ['Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']
OSE_MONTHS_2 = ['MesAbr','MesMay','MesJun','MesJul','MesAgo','MesSep','MesOct','MesNov','MesDic','MesEne','MesFeb','MesMar']

FILE_DEM_AMEBA = 'ele-demand-load.csv'
FILE_BLOCK_AMEBA = 'TIME-BLOCK-STAGE.csv'

DEM_TIME_AMEBA = 'time'
DEM_NAME_AMEBA = 'name'
DEM_SCENARIO_AMEBA = 'scenario'
DEM_BLOCK_AMEBA = 'block'
DEM_STAGE_AMEBA = 'stage'


"""_______________________________________________________________________________"""
""" DICTIONARY OSE2AMEBA PARAMETERS """

MONTH_NUM={'ABR':4,'MAY':5,'JUN':6,'JUL':7,'AGO':8,'SEP':9,'OCT':10,'NOV':11,'DIC':12,'ENE':1,'FEB':2,'MAR':3}
MONTH_HRS = {'ENE': 744, 'FEB': 672, 'MAR': 744, 'ABR': 720, 'MAY': 744, 'JUN': 720,
'JUL': 744, 'AGO': 744, 'SEP': 720, 'OCT': 744, 'NOV': 720, 'DIC': 744 }

WEEK_TO_MONTH={1:4,2:4,3:4,4:4,
5:5,6:5,7:5,8:5,
9:6,10:6,11:6,12:6,
13:7,14:7,15:7,16:7,
17:8,18:8,19:8,20:8,
21:9,22:9,23:9,24:9,
25:10,26:10,27:10,28:10,
29:11,30:11,31:11,32:11,
33:12,34:12,35:12,36:12,
37:1,38:1,39:1,40:1,
41:2,42:2,43:2,44:2,
45:3,46:3,47:3,48:3}
