#This code was originally written by VeeAnn Cross (USGS)
#and is based on the SEABOSS tool photo_locations.py
#The GUI code based on the Tkinter tutorial from: http://www.zetcode.com/gui/tkinter/layout/

#The purpose of this script is to combine the navigation parsed
#from HYPACK files with the information stripped from the EXIF headers
#of SEABOSS JPEG images.
#Time is the common factor - and the result is a shapefile
#of photo locations.
#added timeoffset as an attribute so I can keep track of what the user enters.
#modified 12/11/13
#trenamed that variable originally called datetime to datetimeval, because this script is
#now using the module datetime
#modified 8/22/2016 - sda
#cleaning up the code for methods doc to accompany the CMGP Vid/Photo Portal
#this code was tested and worked on a Mac OSX 10.10 using Python 2.7.12

import sys, os, string
import time
from Tkinter import *
import tkFileDialog
import tkMessageBox
import datetime

#this next two are special and does not ship with Python
#from dbfpy import dbf
#modified 8/1/2013
#   minor text mods
#modified 8/5/2013
#   set it to strip the leading and trailing spaces from the hotlink text field. Otherwise, the hotlinks won't work.
#modified 12/31/13 version 3
#   needed to add the year to the shapefile output.
#   I also fixed the datum and projection to match exactly what ArcGIS 9.3.1 and 10.1 use.
#modified 1/10/14 version 4
#   changing the output slightly for the csv output (that will then be brought back in to the JPEG header
#   I don't need certain information because my exif header software takes care of it.
#modified 1/30/14 version 5
#   fixed the projection again...copied directly from the spatialreference.org site
import shapefile

class PhotoLocs(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
      
        self.parent.title("Merge Navigation with Image Info")

        self.pack(fill=BOTH, expand=1)

        #my attempts
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.rowconfigure(13, weight=1)
        self.rowconfigure(14, weight=1)
        self.rowconfigure(15, weight=1)
        self.rowconfigure(16, weight=1)
        self.rowconfigure(17, weight=1)
        self.rowconfigure(18, weight=1)
        self.rowconfigure(19, weight=1)
        self.rowconfigure(20, weight=1)

        self.columnconfigure(0, weight=1, pad=1)
        self.columnconfigure(1, weight=1, pad=1)
        self.columnconfigure(2, weight=1, pad=1)


        junk = "EXIF info file"
        junkb = "parsed HYPACK file"
        junk2 = "output shapefile"
        junk3 = "output EXIF csv"
        self.projType = IntVar()
        
        lbl = Label(self, text="Input")
        lbl.grid(sticky=W, pady=4, padx=5)

        #input image file
        entryLabel = Label(self, text="EXIF info file: ", fg="red")
        entryLabel.grid(row=1, sticky=W, column=0, padx=5)

        #as entry line
        self.entryLabel2 = Entry(self, relief="sunken")
        self.entryLabel2.insert(0, junk)
        self.entryLabel2.grid(row=2, padx=5,columnspan=3, sticky=W+E)
        
        abtn = Button(self, text="OPEN IMAGE file", command=self.getIMGfile)
        abtn.grid(row=3, column=0, padx=5, sticky=W)

        #input navigation file
        entryNavLbl = Label(self, text="Parsed HYPACK file: ", )
        entryNavLbl.grid(row=4, sticky=W, column=0, padx=5)

        self.entryNav = Entry(self, relief="sunken")
        self.entryNav.insert(0, junkb)
        self.entryNav.grid(row=5, padx=5, columnspan=3, sticky=W+E)

        navbtn = Button(self, text="OPEN NAV file", command=self.getNAVfile)
        navbtn.grid(row=6, column=0, padx=5, sticky=W)

        #output shapefile
        outLabel = Label(self, text="Output file: ")
        outLabel.grid(row=7,padx=5, sticky=W)

        #output filename as entry line
        self.outLabel2 = Entry(self, relief="sunken")
        self.outLabel2.insert(0, junk2)
        self.outLabel2.grid(row=8, padx=5, columnspan=3,sticky=W+E)

        filebtn = Button(self, text="Output shapefile", command=self.saveSHPtext)
        filebtn.grid(row=9,column=0, padx=5, sticky=W)

        #projection radio buttons
        prjLabel = Label(self, text="Shapefile projection: ", font='bold')
        prjLabel.grid(row=10, padx=5, sticky=W)
        self.projOpt = Radiobutton(self, text="Geographic, WGS 84", variable=self.projType, value=1)
        self.projOpt.grid(row=11, column=0, sticky=W)
        self.projOpt = Radiobutton(self, text="Geographic NAD 83", variable=self.projType, value=2)
        self.projOpt.grid(row=12, column=0, sticky=W)
        self.projOpt = Radiobutton(self, text="Other", variable=self.projType, value=3)
        self.projOpt.grid(row=13, column=0, sticky=W)
        

        #time offset
        lblTimeOffset = Label(self, text="Time offset (use negative to shift image time earlier): ")
        lblTimeOffset.grid(row=15, column=0, sticky=W, padx=5)

        self.txtTimeOffset = Entry(self)
        self.txtTimeOffset.insert(0,"00:00:00")
        self.txtTimeOffset.grid(row=16, column=0, sticky=W, padx=12)

        #write exif
        lblExifOut = Label(self, text="write EXIF tags: ")
        lblExifOut.grid(row=20, column=0, sticky=W, padx=5)
        
        self.outExif = Entry(self, relief="sunken")
        self.outExif.insert(0, junk3)
        self.outExif.grid(row=21, padx=5, columnspan=3,sticky=W+E)

        filebtnexif = Button(self, text="Output EXIF csv", command=self.saveEXIFtext)
        filebtnexif.grid(row=23,column=0, padx=5, sticky=W)
        

        #submit and close buttons
        hbtn = Button(self, text="Submit", command=self.MergeNav)
        #hbtn = Button(self, text="Submit")
        hbtn.grid(row=30, column=0, padx=5)
        
        cbtn = Button(self, text="Close", command=self.cbtnClick)
        cbtn.grid(row=30, column=2)


    def cbtnClick(self):
        print "close button event handler"
        self.parent.destroy()

    def getHYPACKFolder(self):
        HYPfolder = tkFileDialog.askdirectory(initialdir="C:/", title='Pick HYPACK folder')
        self.entryLabel2.delete(0,END)
        if len(HYPfolder) > 0:
            print "now read HYPACK folder %s" % HYPfolder
            self.entryLabel2.insert(0,HYPfolder)

    def getIMGfile(self):
        IMGfile = tkFileDialog.askopenfilename(initialdir="C:/", title='Image EXIF info')
        print IMGfile
        self.entryLabel2.delete(0,END)
        self.entryLabel2.insert(0, IMGfile)

    def getNAVfile(self):
        NAVfile = tkFileDialog.askopenfilename(initialdir="C:/", title='Parsed HYPACK Nav file')
        print NAVfile
        self.entryNav.delete(0,END)
        self.entryNav.insert(0, NAVfile)

    def saveSHPtext(self):
        SHPtext = tkFileDialog.asksaveasfilename(filetypes=[('Shapefile','.shp')], title='Save Shapefile')
        print SHPtext
        self.outLabel2.delete(0,END)
        self.outLabel2.insert(0,SHPtext)

    def saveEXIFtext(self):
        EXIFtext = tkFileDialog.asksaveasfilename(filetypes=[('CSV','.csv')], title='Save Exif CSV')
        print EXIFtext
        self.outExif.delete(0,END)
        self.outExif.insert(0,EXIFtext)        


    def MergeNav(self):
        try:
            #gather variables.
            #print "gather variables"
            navfile = self.entryNav.get()
            #print "got nav file"
            inputfile = open(navfile,"r")
            #print "open nav file for reading"
            exiffile = self.entryLabel2.get()
            #print "got exiffile"
            #print exiffile
            outshp = self.outLabel2.get()
            #print "got output shape"
            sTimeOffset = self.txtTimeOffset.get()
            #print "got time offset"
            toffset = string.split(sTimeOffset,":")
            #print "split time offset"
            toffhr = string.atoi(toffset[0])
            #print "offset hr"
            toffmin = string.atoi(toffset[1])
            #print "offset minutes"
            toffsec = string.atoi(toffset[2])
            #print "offset seconds"
            tofftotsecs = (toffhr*3600)+(toffmin*60)+toffsec
            #print "finished time section"
            #output exif info
            outexifcsv = self.outExif.get()

            #create feature class
            #print "create feature class"
            wshp = shapefile.Writer(shapefile.POINT)
            wshp.field('TIME', 'C',8)
            wshp.field('TIMEOFFSET', 'C', 10)
            wshp.field('LONG', 'F', 16, 7)
            wshp.field('LAT', 'F', 17, 7)
            wshp.field('JD','N', 3, 0)
            wshp.field('YEAR', 'N', 4, 0)
            wshp.field('PICNAME','C', 254)
            wshp.field('HOTLINK','C', 254)
            wshp.field('GPSTIME','C', 16)
            wshp.field('DIFFTIME','F', 16)
            print "finished creating feature class"
            #writing projection

            projPrefix = os.path.splitext(outshp)[0]
            if self.projType.get() == 1:
                print "projection wgs84"
                #based on: http://spatialreference.org/ref/epsg/4326/
                epsg = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
                prjpoint = open("%s.prj" % projPrefix, "w")
                prjpoint.write(epsg)
                prjpoint.close()
                print "finished writing projection file %s" % prjpoint
            elif self.projType.get() == 2:
                print "projection nad83"
                #based on: http://spatialreference.org/ref/sr-org/7169/
                epsg = 'GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.017453292519943295]]'
                
                prjpoint = open("%s.prj" % projPrefix, "w")
                prjpoint.write(epsg)
                prjpoint.close()
            else:
                print "projection other"
            
            if toffset[0][0:1] == "-":
                tofftotsecs = -1*abs(tofftotsecs)
            count = 0
            #for startinfo in fileinput.input(exiffile):
            writecsv = open(outexifcsv, "w")
            for startinfo in open(exiffile):
                #print "starting to read exiffile"
                if startinfo in ("__DATA__", "__END__"):
                    fileinput.close(exiffile)
                    print "close exiffile"
                    break
                starts = string.split(startinfo,",")
                lineid = starts[0]
                hotlinkread = starts[1]
                #to be safe, I need to strip the leading space, so I strip leading and trailing.
                hotlink = hotlinkread.strip()
                datetimeval = starts[2]
                datetimestuff = string.split(datetimeval, " ")
                datestr = (datetimestuff[1])
                timestr = (datetimestuff[2])
                #print "read row of exiffile"
                #print datestr
                #print timestr

                datestuff = string.split(datestr,":")
                yearid = string.atoi(datestuff[0])
                month = string.atoi(datestuff[1])
                day = string.atoi(datestuff[2])

                timestuff = string.split(timestr,":")
                timehr = string.atoi(timestuff[0])
                timemin = string.atoi(timestuff[1])
                timesec = string.atoi(timestuff[2])
                timeepoch = (time.mktime((yearid,month,day,timehr,timemin,timesec,0,0,0)))
                timepadj = timeepoch + tofftotsecs
                #print timepadj

                firstpass = 0
                collect = 0
                while 1:
                    #print "in the while loop"
                    #now I should be opening the nav file
                    line = inputfile.readline()
                    #print "got first row of nav file"
                    values = string.split(line,",")
                    lat = values[0].strip()
                    longi = values[1].strip()
                    #print lat
                    #print longi
                    if self.isNumber(lat):
                        #print "seeing if it's a number"
                        navyear = eval(values[6])
                        navjd = string.atoi(values[5])
                        navhr = string.atoi(values[2])
                        navmin = string.atoi(values[3])
                        navsec = string.atoi(values[4])
                        #gpstime = values[2] + ":" + values[3] + ":" + values[4]
                        gpstime = '%02d:%02d:%02d' % (navhr,navmin,navsec)
                        #print gpstime
                        #print "up to navepoch"
                        navepoch = (time.mktime((navyear,1,navjd,navhr,navmin,navsec,0,0,0)))
                        #print "navepoch"
                        test1 = navepoch
                        #print test1
                        test2 = timepadj
                        #print test1
                        #print test2
                        difftime = abs(test1 - test2)
                        #print "finished doing number stuff"
                        #getting stuff ready for GPSDateStamp
                        jdfill = str(navjd).zfill(3)
                        #print "filled julian day"
                        #print jdfill
                        yrjd = str(navyear)+jdfill
                        #print "combined jd and year"
                        #print yrjd
                        gpsvdate = datetime.datetime.strptime(yrjd,'%Y%j').strftime('%Y:%m:%d')
                        #print "formatted gpsdate"
                        #print gpsvdate

                        if test1 == test2:
                            collect = 1

                            #do shapefile stuff
                            
                            wshp.point(float(longi), float(lat))
                            wshp.record(timestr, sTimeOffset, float(longi), float(lat), long(navjd),long(navyear), lineid, hotlink, gpstime, long(difftime))
                            if float(lat) > 0:
                                latref = "N"
                            else:
                                latref = "S"
                            if float(longi) > 0:
                                lonref = "E"
                            else:
                                lonref = "W"
                            writecsv.write(lineid+', ' + gpsvdate + ', ' + gpstime + ', ' + lat + ', '+longi+'\n')
                            #
                            count = count + 1
                            holdid = lineid
                            firstpass = 1
                            break

                        if (firstpass == 1 and holddiffstart <= difftime):

                            if float(holdy) > 0:
                                latref = "N"
                            else:
                                latref = "S"
                            if float(holdx) > 0:
                                lonref = "E"
                            else:
                                lonref = "W"
                                
                            wshp.point(float(holdx), float(holdy))
                            wshp.record(timestr, sTimeOffset, float(holdx), float(holdy), long(navjd), long(navyear), lineid, hotlink, holdgpstime, long(holddiffstart))
                            writecsv.write(lineid + ', ' + gpsvdate + ', ' + holdgpstime + ', ' + holdy +', '+holdx+'\n')
                            #

                            count = count + 1

                            break
                        holddiffstart = difftime
                        holdx = values[1].strip()
                        holdy = values[0].strip()
                        holdhr = navhr
                        holdmin = navmin
                        holdsec = navsec
                        holdgpstime = gpstime
                        firstpass = 1
                    else:
                        print "not a number"
        except:
            print "booboo"

        inputfile.close()
        wshp.save(outshp)
        writecsv.close()
        #prjpoint.write(epsg)
        #prjpoint.close()
        print "done"
                    
        

    def isNumber(self, s):
        #print "in isNumber"
        try:
            float(s)
            return 1 #no exception, must be a number
        except:
            print "header line"
            
def main():
  
    root = Tk()
    root.geometry("550x550+300+300")
    app = PhotoLocs(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()
