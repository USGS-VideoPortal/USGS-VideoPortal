#Python script written by Evan Dailey, July 2015.
#Reformats navigation data from USGS's infobank website to match desired format; changes a .txt file to .csv.  
#New .csv files formatted to read as date (mm/dd/yyyy), time, lat. and long.
#Copy and paste nav data from infobank into text file, then select folder with text files to reformat.
#This version of the script runs on all files in a folder, for a single file version, see 'infobank2csv_single.py'
import os
import os.path
import datetime
import fileinput
wd = raw_input("Enter folder path with navigation txt files: \n")
os.chdir(wd)
for file in os.listdir(os.getcwd()):
    file_read = open(file, 'r')
    print "Input file:" + file
    file = os.path.splitext(file)[0]    #Separates file name root from extension for use in next line
    csvfile = file + '.csv'             #Adds csv extension to new file
    print "Output file:" + csvfile
    file_write = open(csvfile, 'w')
    for line in file_read:
      year = int(line [0:4])
      day = int(line [4:7])
      d = datetime.timedelta(day - 1) + datetime.date(year,1,1)  #Module to convert julian day to year, month, day #This converts the day of year into calendar date
      d = d.strftime("%m/%d/%Y")        #Restructure date.time object to desired format
      hour = line [7:9]                 #These four lines grab values for time out of txt file
      min = line [9:11]
      sec = line [11:13]
      tenth = line [13]
      lat = line[16:24]                 #These two lines grab the latitude and longitude values from txt file
      long = line[25:36]
      line = str(d) + "," + str(hour) + ":" + str(min) + ":" + str(sec) + "," + str(lat) + "," + str(long) + "\n"
      file_write.write(line)
    file_write.close()                   #Closes new file
    file_read.close()                    #Closes original read file
    for line in fileinput.input(files = [csvfile], inplace = True):
      if fileinput.isfirstline():
        print "Date,Time,Latitude,Longitude"    #'Prints' to file (basically writes header to file)
      print line,                       #Comma keeps new file from having additional blank lines
fileinput.close()                       #Closes final csv file