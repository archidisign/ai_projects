#!/usr/bin/python

import time
import datetime
from datetime import timedelta as td
import holidays
import pickle
import json

def DayDifference(start_date, end_date, Province):
    if not start_date or not end_date:
        return None
    else:
        start_time = time.time( )
        d2 = end_date
        d1 = start_date
        count = (d2.hour - d1.hour) / 24 + (d2.minute - d1.minute) / 1440

        if d1.date( ) == d2.date( ):
            pass
        elif d1.date( ) > d2.date( ):
            delta = d1.date( ) - d2.date( )
            for i in range( delta.days ):
                day = d2 + td( days=(i + 1) )
                if not (day.isoweekday( ) in [6, 7]) and not (day in holidays.Canada( prov=Province )):
                    count -= 1
        else:
            delta = d2.date( ) - d1.date( )
            for i in range( delta.days ):
                day = d1 + td( days=(i + 1) )
                if not (day.isoweekday( ) in [6, 7]) and not (day in holidays.Canada( prov='QC' )):
                    count += 1

        end_time = time.time( )
        return count

def strToDate(string_date):
    if string_date==None:
        return None
    else:
        string_date.split("'")
        return datetime.datetime.strptime(string_date, "'%Y-%m-%d %H:%M:%S'")

#open file to be written to
finalf =open("prediction2_10.sql", "w")

with open( "prediction2_10.json", "r" ) as f:
    for line in f:
        # initialize my values
        newLine = [None] * 35 # IMPORTANT!! notice how None has to be replaced by NULL and " by ' in SQL Form
        data = json.loads( line )

        # input values into newLine array
        newLine[0] =data['PatientAriaSer']
        newLine[1] = '\''+data['response']+'\''
        if 'SGASDueDate' in data:
            newLine[2] = '\''+data['SGASDueDate']+'\''
        newLine[3] = '\''+data['prediction']+'\''
        for element in data['steps']:
            if element['stage'] == 'Ct-Sim':
                i = 3
            if element['stage'] == 'READY FOR MD CONTOUR':
                i = 9
            if element['stage'] == 'READY FOR DOSE CALCULATION':
                i = 15
            if element['stage'] == 'READY FOR PHYSICS QA':
                i = 21
            if element['stage'] == 'READY FOR TREATMENT':
                i = 27
            newLine[i + 1] = '\''+element['stage']+'\''
            newLine[i + 2] = element['AriaSerNum']
            newLine[i + 3] = '\''+element['cancer']+'\''
            newLine[i + 4] = '\''+element['priority']+'\''
            newLine[i + 5] = '\''+element['appointment/task']+'\''
            newLine[i + 6] = '\''+element['date']+'\''
        newLine[34]=DayDifference(strToDate(newLine[9]), strToDate(newLine[3]), 'QC')
        officialNewLine = '(' + ','.join( str( x ) for x in newLine ) + '),'
        finalf.write(officialNewLine+'\n')
finalf.close()
f.close()