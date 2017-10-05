"""OSE2Ameba: Script to convert an OSE2000 database into Ameba CSV format.
_______________________________________________________________________________
Copyright (c) 2017 AMEBA-Dev - Consultora SPEC Limitada
This software cannot be distributed.
For more information, visit ameba.spec.cl
Current version developer: Ameba Team
_______________________________________________________________________________
"""
import argparse
# import csv
import os

from module import busbar, branch, generator, demandload, profiles_ERNC, fuel, inflow, profile_GNL, dam, irrigation
from module import demandload_block

parser = argparse.ArgumentParser(description='OSE2000 to Ameba converter')
parser.add_argument(
    'model', default='opt', type=str, help='select model to get data from (Opt or Ope)')
args = parser.parse_args()

print 'starting process..........'

#  - - - - - - LEER RUTAS DE DATOS Y RESULTADOS  - - - - - - #

config_rutas = open('config_rute.txt', 'r')
path_datos = ''
path_resultados = ''
tmp_line = ''

for line in config_rutas:
    if tmp_line == '[data]':
        path_datos = line.split()[0]
    elif tmp_line == '[output]':
        path_resultados = line.split()[0]
    tmp_line = line.split()[0]

if not os.path.exists(path_resultados):
    print "output directory: " + path_resultados + " does not exists. Creating..."
    os.mkdir(path_resultados)

# - - - - - - CONFIG PARAMETERS  - - - - - - #
BLOCK_RESOLUTION = False

#  - - - - - - BUSBAR  - - - - - - #
print '-- processing busbar data --'
busbar = busbar.Busbar(path_datos, path_resultados, args.model)
# busbar.run()

# - - - - - - BRANCH  - - - - - - #
print '-- processing branch data --'
branch = branch.Branch(path_datos, path_resultados, args.model)
# branch.run()
# - - - - - - GENERATOR  - - - - - - #
print '-- processing generator data --'
generator = generator.Generator(path_datos, path_resultados, args.model)
# generator.run()

# - - - - - - DEMAND  - - - - - - #
print '-- processing demand data --'
dem_year_ini='2017'
dem_year_end='2017'
dem_year_ose='2013'
# demand = demandload.DemandLoad(path_datos, path_resultados, args.model, dem_year_ini, dem_year_end, dem_year_ose)
demand_block = demandload_block.DemandLoadBlock(path_datos, path_resultados, args.model, dem_year_ini, dem_year_end, dem_year_ose)
# demand.run()
demand_block.run()

# - - - - - - DEMAND  - - - - - - #
print '-- processing profile data --'
profile_power_year_ini='2017'
profile_power_year_ose='2013'
profile_power = profiles_ERNC.ProfilePower(path_datos, path_resultados, args.model, profile_power_year_ini, profile_power_year_ose)
profile_power.run()

# - - - - - - FUEL - - - - - - #
print '-- processing fuel data --'
fuel = fuel.Fuel(path_datos, path_resultados, args.model)
# fuel.run()

# - - - - - - INFLOW - - - - - - #
print '-- processing inflow data --'
inflow = inflow.ProfileInflow(path_datos, path_resultados, args.model)
# inflow.run()

# - - - - - - GNL - - - - - - #
# print '-- processing GNL indexed data --'
gnl = profile_GNL.ProfileGnl(path_datos, path_resultados, args.model)
# gnl.run()

# - - - - - - DAM - - - - - - #
print '-- processing dam data --'
dam = dam.DamCot(path_datos, path_resultados, args.model)
# dam.run()

# - - - - - - IRRIGATION - - - - - - #
print '-- processing irrigation data --'
irrigation = irrigation.Irrigation(path_datos, path_resultados, args.model)
# irrigation.run()

# demand_block = DemandLoadBlock(self._ose_dir, self._ameba_dir, self._model)
# profile_power_block = ProfilesBlock(self._ose_dir, self._ameba_dir, self._model)
# profile_inflow_block = ProfileInflowBlock(self._ose_dir, self._ameba_dir, self._model)
# if BLOCK_RESOLUTION:
#     demand_block.run()
#     profile_power_block.run()
#     profile_inflow_block.run()

print "process finished"
