"""OSE2Ameba: Script to convert an OSE2000 database into Ameba CSV format.
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

from module import busbar
from module import branch
from module import generator
from module import demandload

# from ose2ameba_profile_GNLv2 import *

# from ose2ameba_fuel import *
# from ose2ameba_profile_inflow import *
# from ose2ameba_profiles_ERNC import *
# from ose2ameba_irrigation import *
# from ose2ameba_dam import *
# from ose2ameba_demand_load_blocks import *
# from ose2ameba_profile_inflow_block import *
# from ose2ameba_profiles_ERNC_blocks import *


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
print '|------------------------|'
print '| generating busbar data |'
print '|------------------------|'
print ''
busbar = busbar.Busbar(path_datos, path_resultados, args.model)
busbar.run()
# - - - - - - BRANCH  - - - - - - #
print '|------------------------|'
print '| generating branch data |'
print '|------------------------|'
print ''
branch = branch.Branch(path_datos, path_resultados, args.model)
branch.run()
# - - - - - - GENERATOR  - - - - - - #
print '|---------------------------|'
print '| generating generator data |'
print '|---------------------------|'
print ''
generator = generator.Generator(path_datos, path_resultados, args.model)
generator.run()

# - - - - - - DEMAND  - - - - - - #
print '|------------------------|'
print '| generating demand data |'
print '|------------------------|'
print ''
year_ini='2017'
year_end='2018'
year_ose='2013'
demand = demandload.DemandLoad(path_datos, path_resultados, args.model, year_ini, year_end, year_ose)
demand.run()

# gen_unav = GenUnav(self._ose_dir, self._ameba_dir, self._model)
# fuel = Fuel(self._ose_dir, self._ameba_dir, self._model)
# profile_gnl = ProfileGnl(self._ose_dir, self._ameba_dir, self._model)
# profile_inflow = ProfileInflow(self._ose_dir, self._ameba_dir, self._model)
# profile_power = ProfilePower(self._ose_dir, self._ameba_dir, self._model)
# irrigation = Irrigation(self._ose_dir, self._ameba_dir, self._model)

# dam = DamCot(self._ose_dir, self._ameba_dir, self._model)

# gen_unav.run()
# fuel.run()
# profile_gnl.run()
# profile_inflow.run()
# profile_power.run()
# irrigation.run()

# dam.run()

# demand_block = DemandLoadBlock(self._ose_dir, self._ameba_dir, self._model)
# profile_power_block = ProfilesBlock(self._ose_dir, self._ameba_dir, self._model)
# profile_inflow_block = ProfileInflowBlock(self._ose_dir, self._ameba_dir, self._model)
# if BLOCK_RESOLUTION:
#     demand_block.run()
#     profile_power_block.run()
#     profile_inflow_block.run()

print "process finished"
