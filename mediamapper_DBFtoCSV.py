#Code to convert Media Mapper DBF files to csv files.  Converts Excel's serial datetime to calendar date and standard time.
#Creates new csv file with only desired rows and columns (DBF file contains two rows for each time point, but the very first row
#gives the date the file was created, and this is not desired.  Also do not want to have two rows for each nav point.
#Created by Evan Dailey, 10-30-2015

import datetime
import time
from dateutil import parser
from datetime import timedelta
import xlrd
import os
import os.path
import arcpy
import glob
import fileinput

###################################################################################################
##########  Function to convert DBF files to CSV
def dbf2csv(dbfpath, csvpath):
    ''' To convert .dbf file or any shapefile/featureclass to csv file
    Inputs: 
        dbfpath: full path to .dbf file [input] or featureclass
        csvpath: full path to .csv file [output]

    '''
    import csv
    rows = arcpy.SearchCursor(dbfpath)
    csvFile = csv.writer(open(csvpath, 'wb')) #output csv
    fieldnames = [f.name for f in arcpy.ListFields(dbfpath)]

    allRows = []
    for row in rows:
        rowlist = []
        for field in fieldnames:
            rowlist.append(row.getValue(field))
        allRows.append(rowlist)

    csvFile.writerow(fieldnames)
    for row in allRows:
        csvFile.writerow(row)
    row = None
    rows = None
####################################################################################################

########This portion of code takes converts DBF files to CSV using the function:

wdDBF = raw_input("Enter directory path to input DBF folder: \n")
survey = raw_input("Enter survey ID: \n")
#wdDBF = ('D:/Temp/DBF')
os.chdir(wdDBF)

###wdCSV = raw_input("Enter directory path to output CSV folder: \n")
##wdCSV = ('D:/Temp/CSV')
newdir = wdDBF + '/Output'
if not os.path.exists(newdir):
    os.makedirs(newdir)
newfile = newdir + '/' + survey + '.csv'
file_write = open(newfile, 'a+')
path1 = os.getcwd() + '\\*.DBF'
for file in glob.glob(path1):
    DBFfile = file
    file_base = os.path.splitext(file)[0]
    CSVfile = file_base + '.csv'
    dbf2csv(DBFfile, CSVfile)
skipper = parser.parse(time.ctime(os.path.getmtime(DBFfile)))   #Gets modified date of dbf file, important further down (skipper)
path = os.getcwd() + '\\*.csv'                              #Creates wildcard path to get all csv files in directory
for CSVfile in glob.glob(path):
    cs = open(CSVfile, 'r')
    csname = os.path.splitext(CSVfile)[0]
    csname = csname.split("\\")[-1]
    itercs = iter(cs)                                       #Skips first line because it contains the date the MediaMapper file was created
    next(itercs)
    for line in cs:
        line = line.strip()
        cols = line.split(",")
        lon = cols[1]
        lat = cols[2]
        utc = float(cols[4])
        dt = datetime.datetime(*xlrd.xldate_as_tuple(utc,0))
        cal = dt.strftime("%m/%d/%Y")
        tm = dt.strftime("%H:%M:%S")
        fn = csname + '.mpg'
        #skipper = datetime.datetime.now() - timedelta(days = 30)
        #wrongcal = skipper.strftime("%m/%d/%Y")
        #wrongdate = datetime.datetime.strptime('10/01/2014', '%m/%d/%Y').date()
        #wrongcal = wrongdate.strftime('%m/%d/%Y')
        skipper2 = cols[6]
        if (dt > skipper or skipper2 == str('NoFix')):
            pass
        else:        
            newline = str(fn) + "," + str(cal) + "," + str(tm) + "," + str(lat) + "," + str(lon) + "," + str(survey) + "\n"
            #print newline
            file_write.write(newline)
    cs.close()
file_write.close()
for line in fileinput.input(files = [newfile], inplace = True):
    if fileinput.isfirstline():
        print "VideoFile,Date,Time,Latitude,Longitude,SurveyID"
    print line,
fileinput.close()

print "Finished.  Results are in: " + newfile
print 'Done'
