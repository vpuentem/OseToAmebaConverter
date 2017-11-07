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
import itertools
import copy
from operator import itemgetter
from workalendar.america import Chile

from functions import *
from parameters import *
from inflow import *

FILE_AMEBA_EMB = 'ele-profile_emb_block.csv'
FILE_AMEBA_EMB_2 = 'ele-profile_emb_block_length.csv'


TIME_AMEBA = 'time'
BLOCK_AMEBA = 'block'

CAL = Chile()

NAME_OSE = 'AflNom'
HID_NUM_OSE = 'AflHid'

WEEK_EMB = ['Sem01','Sem02','Sem03','Sem04','Sem05','Sem06','Sem07','Sem08','Sem09','Sem10',
'Sem11','Sem12','Sem13','Sem14','Sem15','Sem16','Sem17','Sem18','Sem19','Sem20',
'Sem21','Sem22','Sem23','Sem24','Sem25','Sem26','Sem27','Sem28','Sem29','Sem30',
'Sem31','Sem32','Sem33','Sem34','Sem35','Sem36','Sem37','Sem38','Sem39','Sem40',
'Sem41','Sem42','Sem43','Sem44','Sem45','Sem46','Sem47','Sem48']

#Diccionarios de OSE a Ameba
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

MONTH_WEEK_INDEX = {4:0,5:4,6:8,7:12,8:16,9:20,10:24,11:28,12:32,1:36,2:40,3:44}

MONTH_NUM={'ABR':4,'MAY':5,'JUN':6,'JUL':7,'AGO':8,'SEP':9,'OCT':10,'NOV':11,'DIC':12,'ENE':1,'FEB':2,'MAR':3}

year_OSE = '2013'
year_ini = '2017'
hid_number = 59
DEC_NUM = 1

class InflowBlock(object):
    """Script to convert an OSE2000 database into Ameba CSV format."""
    def __init__(self, ose_dir, ameba_dir, model):
        """Constructor of OSE2Ameba_demand.
        @param ose_dir: string directory to read OSE2000 files from
        @param ameba_dir: string directory to write Ameba files to
        """
        self._ose_dir = ose_dir
        self._ameba_dir = ameba_dir
        self._model = model

    def __date_emb(self, date,year):
        week=int(date[3:5])
        month=WEEK_TO_MONTH[int(week)]
        if int(week)>=37:
            #year=str(int(year)+1)
            day=(week-36)-4*(month-1)
        else:
            day=week-(month-4)*4
        return year+'-'+str(WEEK_TO_MONTH[week]).zfill(2)+'-'+str((day-1)*7+1).zfill(2)+'-'+'00:00'

    def __time_year(self, year):
        dates=[]
        for i in range (0,8760,1):
            dates.append({'time':(datetime.datetime(year, 01, 01, 00, 00, 00)+datetime.timedelta(hours=i))})
        return dates
    def __get_block(self, tablaAsign, hour, month):

        for element in tablaAsign:
            if str(element['hora']) == hour:
                return str(element[month])
    def __block_length_dates(self, year, block_length):
        """
        @param block_length: list
        @param year: int
        """
        dates = []
        for month_num in range(1,12+1):
            for block_num in range(1,16+1):
                if block_num == 1:
                    dates.append({ TIME_AMEBA : datetime.datetime(year, month_num, 01, 00, 00, 00),
                                   BLOCK_AMEBA : block_num,
                                 })
                else:
                    block_hours = int(block_length[month_num-1][str(block_num-1)])
                    dates.append({ TIME_AMEBA : dates[-1][TIME_AMEBA]+datetime.timedelta(hours=block_hours),
                                   BLOCK_AMEBA : block_num,
                                 })
        return dates
    def __get_week_block_length(self, dic, month, week, block):
        for row in dic:
            if row['month'] == str(month) and row['week'] == str(week):
                return int(row[str(block)])
    def _date_time(self,date_time,year):
        month=date_time.month
        day=date_time.day
        hour=date_time.hour
        return str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'-'+str(hour).zfill(2)+':00'

    def __convert_profile_emb(self):
        """Reads profiles from OSE2000 format and write Ameba profiles."""

        dic_tabla_habil = list(reader_csv('', TABLA_HABIL, self._ose_dir))
        dic_tabla_no_habil = list(reader_csv('', TABLA_NO_HABIL, self._ose_dir))
        dic_tabla_duracion = list(reader_csv('', BLOCK_LENGTH, self._ose_dir))
        dic_duracion_bloque_semana = list(reader_csv('', 'duracion_bloque_semana.csv', self._ose_dir))

        # TODO: Replace directory and file name below with correct one
        dic_emb_1 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_INFLOW), FILE_OSE_EMB_1, self._ose_dir))
        dic_emb_2 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_INFLOW), FILE_OSE_EMB_2, self._ose_dir))
        dic_emb_3 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_INFLOW), FILE_OSE_EMB_3, self._ose_dir))
        dic_emb_4 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_INFLOW), FILE_OSE_EMB_4, self._ose_dir))
        dic_emb_5 = list(reader_csv(os.path.join(DIR_OSE_SIC,DIR_OSE_INFLOW), FILE_OSE_EMB_5, self._ose_dir))

        dic_emb=dic_emb_1+dic_emb_2+dic_emb_3+dic_emb_4+dic_emb_5

        inflow_value = SearchInflow(1, 59, dic_emb, WEEK_EMB)

        directory = os.path.join(self._ameba_dir,DIR_AMEBA_INFLOW)
        check_directory(directory)

        inflow_date_hourly=self.__time_year(int(year_OSE))
        inflow_date_block=self.__block_length_dates(int(year_ini), dic_tabla_duracion)

        for i in range(0,len(inflow_date_hourly)):
            time = inflow_date_hourly[i][TIME_AMEBA]
            if time.weekday() == 6 or time.weekday() == 5 or CAL.is_working_day(time) is False:
                block=self.__get_block(dic_tabla_no_habil,str(time.hour+1),str(time.month))
            else:
                block=self.__get_block(dic_tabla_habil,str(time.hour+1),str(time.month))
            inflow_date_hourly[i].update({TIME_AMEBA : time.replace(year=int(year_ini))})
            inflow_date_hourly[i].update({'month' : time.month})
            inflow_date_hourly[i].update({BLOCK_AMEBA : block})
            if time.day < 8:
                inflow_date_hourly[i].update({'week' : 1})
            elif time.day >= 8 and time.day < 15 :
                inflow_date_hourly[i].update({'week' : 2})
            elif time.day >= 15 and time.day < 22 :
                inflow_date_hourly[i].update({'week' : 3})
            elif time.day >= 22:
                inflow_date_hourly[i].update({'week' : 4})

        """ INFLOW NAMES"""
        inflow_name = []
        for inflow in dic_emb:
            if inflow[HID_NUM_OSE] == '1':
                inflow_name.append('Aflu_'+inflow[NAME_OSE])
        for inflow in inflow_date_block:
            for name in inflow_name:
                inflow.update({name: ''})

        """ DATES FOR ALL HIDROLOGIES"""
        inflow_blocks_emb = []

        for hid_num in range(2,hid_number+1):
            for date in inflow_date_block:
                inflow_blocks_emb.append(copy.deepcopy(date))
                inflow_blocks_emb[-1].update({'hid_num': hid_num})

        for inflow in inflow_blocks_emb:
            month = inflow[TIME_AMEBA].month
            block = inflow[BLOCK_AMEBA]

            if month == 1 or month == 2 or month == 3 and inflow['hid_num'] != 57 and inflow['hid_num'] != 58 and inflow['hid_num'] != 59:
                hid_num = inflow['hid_num']-1
            else:
                hid_num = inflow['hid_num']

            block_length_1 = self.__get_week_block_length(dic_duracion_bloque_semana,month,1,block)
            block_length_2 = self.__get_week_block_length(dic_duracion_bloque_semana,month,2,block)
            block_length_3 = self.__get_week_block_length(dic_duracion_bloque_semana,month,3,block)
            block_length_4 = self.__get_week_block_length(dic_duracion_bloque_semana,month,4,block)

            sum_block = block_length_1+block_length_2+block_length_3+block_length_4
            for names in inflow_name:
                name = names[5:]
                value1 = float(inflow_value.get_inflow(hid_num,name)[MONTH_WEEK_INDEX[month]])
                value2 = float(inflow_value.get_inflow(hid_num,name)[MONTH_WEEK_INDEX[month]+1])
                value3 = float(inflow_value.get_inflow(hid_num,name)[MONTH_WEEK_INDEX[month]+2])
                value4 = float(inflow_value.get_inflow(hid_num,name)[MONTH_WEEK_INDEX[month]+3])

                value = (value1*block_length_1+value2*block_length_2+value3*block_length_3+value4*block_length_4)/sum_block

                inflow.update({names : value})
            if inflow['hid_num'] != 57 and inflow['hid_num'] != 58 and inflow['hid_num'] != 59:
                inflow.update({'scenario': 'hidrologia_'+str(1959+inflow['hid_num'])})
            elif inflow['hid_num'] == 57:
                inflow.update({'scenario': 'hidrologia_'+str(5000)})
            elif inflow['hid_num'] == 58:
                inflow.update({'scenario': 'hidrologia_'+str(6000)})
            elif inflow['hid_num'] == 59:
                inflow.update({'scenario': 'hidrologia_'+str(7000)})

        """ WRITE FILE 2"""
        columns=inflow_date_hourly[0].keys()
        writer_emb_2 = writer_csv(os.path.join(DIR_AMEBA_INFLOW,FILE_AMEBA_EMB_2), columns, self._ameba_dir)
        # TODO: Replace below correct column values
        writer_emb_2.writeheader()

        for element in inflow_date_hourly:
            element.update({TIME_AMEBA: self._date_time(element[TIME_AMEBA],element[TIME_AMEBA].year)})
            writer_emb_2.writerow(element)

        """ WRITE FILE 1"""
        columns=inflow_blocks_emb[0].keys()
        columns.insert(0, columns.pop(columns.index(TIME_AMEBA)))
        columns.insert(1, columns.pop(columns.index('scenario')))
        #columns.insert(1, columns.pop(columns.index('block')))
        #columns.insert(2, columns.pop(columns.index('hid_num')))
        columns.pop(columns.index('block'))
        columns.pop(columns.index('hid_num'))

        writer_emb = writer_csv(os.path.join(DIR_AMEBA_INFLOW,FILE_AMEBA_EMB), columns, self._ameba_dir)
        writer_emb.writeheader()

        for element in inflow_blocks_emb:
            element.pop('block')
            element.pop('hid_num')
            element.update({TIME_AMEBA: self._date_time(element[TIME_AMEBA],element[TIME_AMEBA].year)})
            writer_emb.writerow(element)

    def run(self):
        """Main execution point."""
        self.__convert_profile_emb()
        print 'profile_inflow_block ready'

class SearchInflow(object):
    def __init__(self, ini_hid_num, last_hid_num, reader, week):
        self.__week = week
        self.__ini_hid_num = ini_hid_num
        self.__reader = reader
        self.__list_emb = self.__load_data((last_hid_num - ini_hid_num + 1) )
    def __get_index(self, hid_num):
        return (hid_num - self.__ini_hid_num)
    def __load_data(self, dim):
        list_emb_1=[dict() for _ in range(dim)]
        for row in self.__reader:
            list_emb_1[self.__get_index(int(row['AflHid']))][row['AflNom']] = [row[week] for week in self.__week]
        return list_emb_1
    def get_inflow(self, hid_num, inflow_name):
        return list(self.__list_emb[self.__get_index(hid_num)][inflow_name])

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
    InflowBlock(args.ose_dir, args.ameba_dir, args.model).run()

if __name__ == '__main__':
    main()
