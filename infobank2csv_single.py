#Python script written by Evan Dailey, July 2015.
#Python script to change format of navigation data from USGS's infobank.
#Reads a single .txt file and outputs a .csv file.
#New .csv files formatted to read as date (mm/dd/yyyy), time, lat. and long.
#This script runs on a single file; for a script to run on a whole folder of files, see 'infobank2csv_folder.py'
import os
import datetime   #Allows the change directory command to work
import fileinput   #Append csv with header
wd = raw_input("Enter working directory path: \n")
print dir
#os.chdir(wd)
file_read = raw_input("Enter file to be read: \n")
f = open(file_read, "r")
#Create new empty file for properly formatted data
r_write = raw_input("Enter new filename for output: \n")
f2 = open(r_write, "w")
for line in f:
  year = int(line [0:4])
  day = int(line [4:7])
  d = datetime.timedelta(day - 1) + datetime.date(year,1,1)  #Module to convert julian day to year, month, day #This converts the day of year into calendar date
  d = d.strftime("%m/%d/%Y") #Restructure date.time object to desired format
  hour = line [7:9]   #These four lines grab values for time out of txt file
  min = line [9:11]
  sec = line [11:13]
  tenth = line [13]
  #print d
  lat = line[16:24]   #These two lines grab the latitude and longitude values from txt file
  long = line[25:36]
  line = str(d) + "," + str(hour) + ":" + str(min) + ":" + str(sec) + "," + str(lat) + "," + str(long) + "\n"
  f2.write(line)
  #print line
f2.close()    #Closes new file
for line in fileinput.input(files = [r_write], inplace = True):
  if fileinput.isfirstline():
    print "Date,Time,Latitude,Longitude"
  print line,  #Comma keeps new file from having additional blank lines
fileinput.close()
