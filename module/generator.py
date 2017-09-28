# !/usr/bin/env python
# -*- coding: latin-1 -*-


"""OSE2Ameba_generator: Script to convert an OSE2000 database into Ameba CSV format.
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


COLUMNS_AMEBA_HYDRO = [GEN_NAME_AMEBA, GEN_START_TIME_AMEBA, GEN_END_TIME_AMEBA,
                GEN_LIFETIME_AMEBA, GEN_TYPE_AMEBA, GEN_CONNECTED_AMEBA,
                GEN_CO2_EMISSION_AMEBA, GEN_CONTROL_AREAS_AMEBA,
                GEN_IS_NCRE_AMEBA, GEN_PMAX_AMEBA, GEN_EFF_AMEBA,
                GEN_FORCED_OUTAGE_RATE_AMEBA,
                GEN_AUXSERV_AMEBA, GEN_CANDIDATE_AMEBA, GEN_INV_COST_AMEBA,
                GEN_FOM_COST_AMEBA, GEN_OWNER_AMEBA, GEN_INITIAL_INVESTMENT_AMEBA,
                GEN_BUSBAR_AMEBA]
COLUMNS_AMEBA_THERMAL = [GEN_NAME_AMEBA, GEN_START_TIME_AMEBA, GEN_END_TIME_AMEBA,
                GEN_LIFETIME_AMEBA, GEN_TYPE_AMEBA, GEN_CONNECTED_AMEBA,
                GEN_CO2_EMISSION_AMEBA, GEN_CONTROL_AREAS_AMEBA,
                GEN_IS_NCRE_AMEBA, GEN_PMAX_AMEBA,
                GEN_PMIN_AMEBA, GEN_HEATRATE_AVG_AMEBA, GEN_VOMC_AVG_AMEBA,
                GEN_FORCED_OUTAGE_RATE_AMEBA, GEN_FUELNAME_AMEBA,
                GEN_AUXSERV_AMEBA, GEN_CANDIDATE_AMEBA, GEN_INV_COST_AMEBA,
                GEN_FOM_COST_AMEBA, GEN_OWNER_AMEBA, GEN_INITIAL_INVESTMENT_AMEBA,
                GEN_BUSBAR_AMEBA]
COLUMNS_AMEBA_ERNC= [GEN_NAME_AMEBA, GEN_START_TIME_AMEBA, GEN_END_TIME_AMEBA,
                GEN_LIFETIME_AMEBA, GEN_TYPE_AMEBA, GEN_CONNECTED_AMEBA,
                GEN_CO2_EMISSION_AMEBA, GEN_CONTROL_AREAS_AMEBA,
                GEN_IS_NCRE_AMEBA, GEN_PMAX_AMEBA,
                GEN_PMIN_AMEBA, GEN_VOMC_AVG_AMEBA,
                GEN_FORCED_OUTAGE_RATE_AMEBA,GEN_AUXSERV_AMEBA,
                GEN_CANDIDATE_AMEBA, GEN_INV_COST_AMEBA,
                GEN_FOM_COST_AMEBA, GEN_OWNER_AMEBA, GEN_INITIAL_INVESTMENT_AMEBA,
                GEN_ZONE_AMEBA,GEN_BUSBAR_AMEBA]

class Generator(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""
    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba__generator.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ameba_dir = ameba_dir
        # READS FILES FROM DIR 'Termica'
        self._reader_thermal_SING_1 = reader_csv(os.path.join(DIR_OSE_SING, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                           FILE_OSE_THERMAL_SING_1, ose_dir)
        if model in ['Ope', 'ope', 'OPE']:
            # READS FILES FROM DIR 'Termica'
            self._reader_thermal_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                              FILE_OSE_THERMAL_SIC_OPE_1, ose_dir)
            self._reader_thermal_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                              FILE_OSE_THERMAL_SIC_OPE_2, ose_dir)
            self._reader_thermal_SIC_3 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                              FILE_OSE_THERMAL_SIC_OPE_3, ose_dir)
            # READS FILES FROM DIR 'Pasada'
            self._reader_pas_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                          FILE_OSE_PAS_SIC_OPE_1, ose_dir)
            self._reader_pas_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                          FILE_OSE_PAS_SIC_OPE_2, ose_dir)
            # READS FILES FROM DIR 'Embalse'
            self._reader_emb_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_EMB),
                                          FILE_OSE_EMB_SIC_OPE_1, ose_dir)
            # READS FILES FROM DIR 'Serie'
            self._reader_ser_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_SER),
                                          FILE_OSE_SER_SIC_OPE_1, ose_dir)
        else:  # if model in ['Opt','opt','OPT']:
            self._reader_thermal_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                              FILE_OSE_THERMAL_SIC_OPT_1, ose_dir)
            self._reader_thermal_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                              FILE_OSE_THERMAL_SIC_OPT_2, ose_dir)
            self._reader_thermal_SIC_3 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_THERMAL),
                                              FILE_OSE_THERMAL_SIC_OPT_3, ose_dir)
            # READS FILES FROM DIR 'Pasada'
            self._reader_pas_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                          FILE_OSE_PAS_SIC_OPT_1, ose_dir)
            self._reader_pas_SIC_2 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_PAS),
                                          FILE_OSE_PAS_SIC_OPT_2, ose_dir)
            # READS FILES FROM DIR 'Embalse'
            self._reader_emb_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_EMB),
                                          FILE_OSE_EMB_SIC_OPT_1, ose_dir)
            # READS FILES FROM DIR 'Serie'
            self._reader_ser_SIC_1 = reader_csv(os.path.join(DIR_OSE_SIC, DIR_OSE_GENERATOR, DIR_OSE_SER),
                                          FILE_OSE_SER_SIC_OPT_1, ose_dir)

    def __flag_invest(self, candidate):
        if candidate == 'T':
            return 1
        else:
            return 0

    def __parameters(self):
        # CREATE WRITER
        directory = os.path.join(self._ameba_dir,DIR_AMEBA_GENERATOR)
        check_directory(directory)

        writer_pv      = writer_csv(os.path.join(DIR_AMEBA_GENERATOR, FILE_AMEBA_PV),
                                    COLUMNS_AMEBA_ERNC, self._ameba_dir)
        writer_wind    = writer_csv(os.path.join(DIR_AMEBA_GENERATOR, FILE_AMEBA_CEN_WIND),
                                    COLUMNS_AMEBA_ERNC, self._ameba_dir)
        writer_thermal = writer_csv(os.path.join(DIR_AMEBA_GENERATOR, FILE_AMEBA_THERMAL),
                                    COLUMNS_AMEBA_THERMAL, self._ameba_dir)
        writer_hydro   = writer_csv(os.path.join(DIR_AMEBA_GENERATOR, FILE_AMEBA_HYDRO),
                                    COLUMNS_AMEBA_HYDRO, self._ameba_dir)

        """escribe la primera fila en formato Ameba"""
        writer_hydro.writeheader()
        writer_thermal.writeheader()
        writer_pv.writeheader()
        writer_wind.writeheader()
        """escribe el resto de las filas"""
        #recorre los archivos de la carpeta 'Termica'
        dic_gen = []
        for generator in itertools.chain(self._reader_thermal_SING_1,self._reader_thermal_SIC_1,
                                         self._reader_thermal_SIC_2,self._reader_thermal_SIC_3):
            dic_gen.append ({
            GEN_NAME_AMEBA : remove(generator[GEN_NAME_OSE]),
            GEN_START_TIME_AMEBA : date_ini_ose(generator[GEN_START_TIME_OSE]),
            GEN_END_TIME_AMEBA : date_end_ose(generator[GEN_END_TIME_OSE]),
            GEN_LIFETIME_AMEBA : generator[GEN_LIFETIME_OSE],
            GEN_TYPE_AMEBA : remove(generator[GEN_TYPE_OSE]),
            GEN_CONNECTED_AMEBA : t_true(generator[GEN_CONNECTED_OSE]),
            GEN_CO2_EMISSION_AMEBA : float(generator[GEN_CO2_EMISSION_OSE])*1000,
            GEN_CONTROL_AREAS_AMEBA : generator[GEN_CONTROL_AREAS_OSE],
            GEN_IS_NCRE_AMEBA : t_true(generator[GEN_IS_NCRE_OSE]),
            GEN_PMAX_AMEBA : generator[GEN_PMAX_OSE],
            GEN_PMIN_AMEBA : generator[GEN_PMIN_OSE],
            #GEN_HEATRATE_AVG_AMEBA : generator[GEN_HEATRATE_AVG_OSE],
            GEN_VOMC_AVG_AMEBA : generator[GEN_VOMC_AVG_OSE],
            GEN_FORCED_OUTAGE_RATE_AMEBA : 1-float(generator[GEN_FORCED_OUTAGE_RATE_OSE]),
            #GEN_FUELNAME_AMEBA : 'fuel_'+remove(generator[GEN_FUELNAME_OSE]),
            GEN_AUXSERV_AMEBA : float(generator[GEN_AUXSERV_OSE])*float(generator[GEN_PMAX_OSE]),
            GEN_CANDIDATE_AMEBA : t_true(generator[GEN_CANDIDATE_OSE]),
            GEN_INV_COST_AMEBA : generator[GEN_INV_COST_OSE],
            GEN_FOM_COST_AMEBA : generator[GEN_FOM_COST_OSE],
            GEN_OWNER_AMEBA : remove(generator[GEN_OWNER_OSE]),
            GEN_INITIAL_INVESTMENT_AMEBA : self.__flag_invest(generator[GEN_CANDIDATE_OSE]),
            GEN_BUSBAR_AMEBA : remove(generator[GEN_BUSBAR_OSE])
            })
            if str(generator[GEN_TYPE_OSE]) in NAME_HYDRO:
                dic_gen[-1].pop(GEN_HEATRATE_AVG_AMEBA, None)
                dic_gen[-1].pop(GEN_FUELNAME_AMEBA, None)
                dic_gen[-1].pop(GEN_VOMC_AVG_AMEBA, None)
                dic_gen[-1].pop(GEN_PMIN_AMEBA, None)
                dic_gen[-1].update({GEN_EFF_AMEBA : generator[GEN_HEATRATE_AVG_OSE],
                                    GEN_TYPE_AMEBA : 'HydroGenerator' })
                writer_hydro.writerow(dic_gen[-1])

            elif str(generator[GEN_TYPE_OSE]) in NAME_PV:
                dic_gen[-1].update({GEN_ZONE_AMEBA : remove(generator[GEN_NAME_OSE])+'_solar',
                                    GEN_TYPE_AMEBA : 'PvGenerator'})
                dic_gen[-1].pop(GEN_HEATRATE_AVG_AMEBA, None)
                dic_gen[-1].pop(GEN_FUELNAME_AMEBA, None)
                writer_pv.writerow(dic_gen[-1])

            elif str(generator[GEN_TYPE_OSE]) in NAME_WIND:
                dic_gen[-1].update({GEN_ZONE_AMEBA : remove(generator[GEN_NAME_OSE])+'_wind',
                                    GEN_TYPE_AMEBA : 'WindGenerator'})
                dic_gen[-1].pop(GEN_HEATRATE_AVG_AMEBA, None)
                dic_gen[-1].pop(GEN_FUELNAME_AMEBA, None)
                writer_wind.writerow(dic_gen[-1])
            else:
                if remove(generator[GEN_FUELNAME_OSE]) == '*':
                    fuel_name = ''
                else:
                    fuel_name = 'fuel_'+remove(generator[GEN_FUELNAME_OSE])
                dic_gen[-1].update  ({
                    GEN_FUELNAME_AMEBA : fuel_name,
                    GEN_HEATRATE_AVG_AMEBA : generator[GEN_HEATRATE_AVG_OSE],
                    GEN_TYPE_AMEBA : 'ThermalGenerator'
                    })
                writer_thermal.writerow(dic_gen[-1])
        #recorre los arvchivos en la carpeta 'Pasada','Embalse' y 'Serie'
        dic_gen_2 = []
        for generator in itertools.chain(self._reader_pas_SIC_1,self._reader_pas_SIC_2,
                                         self._reader_emb_SIC_1,self._reader_ser_SIC_1):
            if generator[GEN_TYPE_OSE] == NAME_HYDRO[0]:
                pmax = generator[GEN_PMAX_OSE_PAS]
            else:
                pmax = generator[GEN_PMAX_OSE]

            dic_gen_2.append({
            GEN_NAME_AMEBA : remove(generator[GEN_NAME_OSE]),
            GEN_START_TIME_AMEBA : date_ini_ose(generator[GEN_START_TIME_OSE]),
            GEN_END_TIME_AMEBA : date_end_ose(generator[GEN_END_TIME_OSE]),
            GEN_LIFETIME_AMEBA : generator[GEN_LIFETIME_OSE],
            GEN_TYPE_AMEBA : 'HydroGenerator',
            GEN_CONNECTED_AMEBA : t_true(generator[GEN_CONNECTED_OSE]),
            GEN_CO2_EMISSION_AMEBA : float(generator[GEN_CO2_EMISSION_OSE])*1000,
            GEN_CONTROL_AREAS_AMEBA : generator[GEN_CONTROL_AREAS_OSE],
            GEN_IS_NCRE_AMEBA : t_true(generator[GEN_IS_NCRE_OSE]),
            GEN_PMAX_AMEBA : pmax,
            GEN_EFF_AMEBA : generator[GEN_EFF_OSE],
            GEN_FORCED_OUTAGE_RATE_AMEBA : 1-float(generator[GEN_FORCED_OUTAGE_RATE_OSE]),
            GEN_AUXSERV_AMEBA : float(generator[GEN_AUXSERV_OSE])*float(pmax),
            GEN_CANDIDATE_AMEBA : t_true(generator[GEN_CANDIDATE_OSE]),
            GEN_INV_COST_AMEBA : generator[GEN_INV_COST_OSE],
            GEN_FOM_COST_AMEBA : generator[GEN_FOM_COST_OSE],
            GEN_OWNER_AMEBA : remove(generator[GEN_OWNER_OSE]),
            GEN_INITIAL_INVESTMENT_AMEBA : self.__flag_invest(generator[GEN_CANDIDATE_OSE]),
            GEN_BUSBAR_AMEBA : remove(generator[GEN_BUSBAR_OSE])
            })
            writer_hydro.writerow(dic_gen_2[-1])

    def run(self):
        """Main execution point."""
        self.__parameters()
        print 'generator parameters ready'

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
    Generator(args.ose_dir, args.ameba_dir, args.model).run()

if __name__ == '__main__':
    main()