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

from ose2ameba_busbar import *
from ose2ameba_branch import *
# from ose2ameba_branch_maxflow import *
# from ose2ameba_generator import *
# from ose2ameba_gen_unavailability import *
# from ose2ameba_profile_GNLv2 import *
# from ose2ameba_demand_load import *
# from ose2ameba_fuel import *
# from ose2ameba_profile_inflow import *
# from ose2ameba_profiles_ERNC import *
# from ose2ameba_irrigation import *
# from ose2ameba_dam import *

# from ose2ameba_demand_load_blocks import *
# from ose2ameba_profile_inflow_block import *
# from ose2ameba_profiles_ERNC_blocks import *

# import debugger

BLOCK_RESOLUTION = False

class OSE2Ameba(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""

    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba.
        @param ose_dir: string directory to read OSE2000 files from (dat)
        @param ameba_dir: string directory to write Ameba files to
        @param model: string with value 'Ope' or Opt'
        """

        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def __ose2ameba(self):

        busbar = Busbar(self._ose_dir, self._ameba_dir, self._model)
        branch = Branch(self._ose_dir, self._ameba_dir, self._model)
        # branch_maxflow = BranchMaxflow(self._ose_dir, self._ameba_dir, self._model)
        # generator = Generator(self._ose_dir, self._ameba_dir, self._model)
        # gen_unav = GenUnav(self._ose_dir, self._ameba_dir, self._model)
        # fuel = Fuel(self._ose_dir, self._ameba_dir, self._model)
        # profile_gnl = ProfileGnl(self._ose_dir, self._ameba_dir, self._model)
        # profile_inflow = ProfileInflow(self._ose_dir, self._ameba_dir, self._model)
        # profile_power = ProfilePower(self._ose_dir, self._ameba_dir, self._model)
        # irrigation = Irrigation(self._ose_dir, self._ameba_dir, self._model)
        # demand = DemandLoad(self._ose_dir, self._ameba_dir, self._model)
        # dam = DamCot(self._ose_dir, self._ameba_dir, self._model)

        #busbar.run()
        #branch.run()

        #branch_maxflow.run()
        # generator.run()

        # gen_unav.run()
        #fuel.run()
        # profile_gnl.run()
        #profile_inflow.run()
        #profile_power.run()
        #irrigation.run()
        #demand.run()
        #dam.run()

        # demand_block = DemandLoadBlock(self._ose_dir, self._ameba_dir, self._model)
        # profile_power_block = ProfilesBlock(self._ose_dir, self._ameba_dir, self._model)
        # profile_inflow_block = ProfileInflowBlock(self._ose_dir, self._ameba_dir, self._model)
        # if BLOCK_RESOLUTION:
        #     demand_block.run()
        #     profile_power_block.run()
        #     profile_inflow_block.run()

    def run(self):
        """Main execution point."""
        self.__ose2ameba()

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
    OSE2Ameba(args.ose_dir, args.ameba_dir, args.model).run()


if __name__ == '__main__':
    main()
