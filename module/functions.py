# -*- coding: utf-8 -*-

import argparse
import csv
import os
import unicodedata
import datetime
from datetime import timedelta
import itertools
import debugger

# from workalendar.america import Chile
# CAL = Chile()

meses = {'Ene': '01', 'Feb': '02', 'Mar': '03', 'Abr': '04', 'May': '05', 'Jun': '06',
'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12' }

dias  = {'Ene': '31', 'Feb': '28', 'Mar': '31', 'Abr': '30', 'May': '31', 'Jun': '30',
'Jul': '31', 'Ago': '31', 'Sep': '30', 'Oct': '31', 'Nov': '30', 'Dic': '31' }

def reader_csv(input_dir, input_file, _ose_dir):
    """Gets a CSV reader for given directory and file.
    @param input_dir: string directory within OSE2000 directories
    @param input_file: string file name to read
    """
    file_name = os.path.join(_ose_dir, input_dir, input_file)
    in_file = open(file_name, 'rb')
    # TODO: Check options below are correct
    return csv.DictReader(
    in_file, delimiter=',', quotechar='"', skipinitialspace=True)

def writer_csv(output_file, fieldnames,_ameba_dir):
    """Gets a CSV writer for file.
    @param output_file: string file name to write
    @param fieldnames: list with string column names to write
    """
    out_file = open(os.path.join(_ameba_dir, output_file), 'wb')
    return csv.DictWriter(
    out_file, delimiter=',', fieldnames=fieldnames)
def check_directory(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

def date_ini_ose(date):
    if date == '*':
        return '1970-01-01-00:00'
    else:
        mes=date[3:6]
        return date[7:11]+'-'+meses[mes]+'-01-00:00'

def date_end_ose(date):
    """Fecha Fin | formato OSE a AMEBA"""
    if date == '*':
        return '3000-01-01-00:00'
    month = int(meses[date[3:6]])
    year = int(date[7:11])
    if month == 12:
        month=0
        year+=1
    return str(year)+'-'+str(month+1).zfill(2)+'-'+'01-00:00'

def DATE_TIME(date_time,year):
    month=date_time.month
    day=date_time.day
    hour=date_time.hour
    return str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'-'+str(hour).zfill(2)+':00'

def datetime_to_ameba(date_time):
    year = date_time.year
    month = date_time.month
    day = date_time.day
    return str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'-'+'00:00'
def datetime_to_ameba2(date_time):
    year = date_time.year
    month = date_time.month
    day = date_time.day
    hour = date_time.hour
    return str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'-'+str(hour).zfill(2)+':00'
def t_true(te):
    if te == 'T':
        return 'true'
    elif te == 'F':
        return 'false'
    return 'None'


def remove(name):
    name=str(name).replace('\xf1','n')
    name=str(name).replace('\xb0','')
    name=str(name).replace("'",'')

    name=''.join((c for c in unicodedata.normalize('NFD', unicode(name, 'unicode-escape')) if unicodedata.category(c) != 'Mn'))
    return str(name.strip())

def select_max_flow(maxf_AB,maxf_BA, maxf_ABN,maxf_BAN,flag):

    if flag == 'T':
        if maxf_ABN == '*' or maxf_BAN == '*':
            return (max([float(maxf_AB),float(maxf_BA)]))
        else:
            return (max([float(maxf_ABN),float(maxf_BAN)]))
    elif flag == 'F':
        if maxf_AB == '*' or maxf_BA == '*':
            return (max([float(maxf_ABN),float(maxf_BAN)]))
        else:
            return (max([float(maxf_AB),float(maxf_BA)]))
def max_flow_true(maxf_AB,maxf_BA, maxf_ABN,maxf_BAN):
    if maxf_AB=='*' and maxf_BA=='*' and maxf_ABN=='*' and maxf_BAN=='*':
        return False
    else:
        return True

def ameba_to_datetime(date_ameba):
    year = int(date_ameba[0:4])
    month = int(date_ameba[5:7])
    day = int(date_ameba[8:10])
    hour = int(date_ameba[11:13])
    return datetime.datetime(year, month, day, hour, 00)
def get_block(tablaAsign, hour, month):
    for element in tablaAsign:
        if str(element['hora']) == hour:
            return str(element[month])
