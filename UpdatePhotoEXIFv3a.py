#This code was originally created by VeeAnn Cross (USGS)
#and is based on the code from the script MCZM_writeexif_2_readfile.py
#Portions of this script was derived Tkinter hints from: 
#Guilherme H. Polo Goncalves -- http://tkinter.unpythonic.net/wiki/GridLayout
#
#format of input information
#   the image filename (including extension) must be in a field by itself (no path)
#   lat and long are assumed to be floating point, numbers only
#   time is expected to be hh:mm:ss
#   date is expected to be either YYYYMMDD or YYYY:MM:DD
#   the text file containing the information can have a header line
#   works with python 2.7.3
#
#modified 12/31/13
#   trying to allow for multiple forms of the yeardate; YYYY:MM:DD or YYYYMMDD, but
#   still require year, month and day
#modified 1/9/14
#   copied grid_manager_veeann_b.py from D:\edrive\python\TKinter\test\jpeg_writeexif
#modified 2/24/15
#   modified the code so there is a check box to allow a header line. 
#   Also allows more date format options: YYYYMMDD, YYY:MM:DD, or MM/DD/YYYY
#modified 4/21/15
#   trying to get it to work with Mac OSX.  
#   set shell=True for Macs. found this on
#   http://stackoverflow.com/questions/23258660/subprocess-call-fails-on-mac-and-linux
#   still works on Windows. Will have to test it on  Mac.
#modified 5/22/15
#   trying to get it to read the "changing" elements from a parameters text file.
#modified 9/1/2016 - sda
#  cleaning up the code for methods doc to accompany the CMGP Vid/Photo Portal
#  origial script called MCZM_writeexif_2_readfile.py, 
#  cleaned script is called UpdatePhotoEXIFv2.py 
#  requires that exiftools be installed on the system
#  this script will look for a params file (specified in the GUI) that contains the exiftool commands
#     for the comment, keyword, Caption, Caption-Abstract, and ImageDescription exif tags
#  other exif tags such as Credit, Copyright, CopyrightNotice are hardcoded into the code below
#  exif tags for the date, time, and GPS data are populated from info in the EXIF csv file 
#     and defined in the GUI interface
#  this code was tested and worked on a Mac OSX 10.10 using Python 2.7.12
#modified 2/14/2017 -VeeAnn Cross
#   Fixed it so that selecting any date format would activate the submit button.
#   Previously, the submit button only activated if you selected the YYYMMDD radio button.
#   Added a fourth date format that allows a 2 digit year. I set the code so that if the year value
#   is less than 50, a "20" is prepended, otherwise a "19" is prepended. Not thoroughly tested - so
#   use caution and check EXIF results.
#   Tested on a windows machine, using Python 2.7.3  ## 2/15/2017 - sda - tested this on a Mac El Cap, Python 2.7.12

from Tkinter import Tk, Button, Checkbutton, Label, Entry, Frame, IntVar, StringVar, Text, Radiobutton, END
import tkFileDialog
import sys, glob, os
import string
#import subprocess to run an external command
import subprocess


class App:
    def __init__(self, master):
        self.master = master
        column0_padx = 24
        row_pady = 40
        self.imgck = IntVar()
        self.latck = IntVar()
        self.lonck = IntVar()
        self.timeck = IntVar()
        self.dateck = IntVar()
        self.datestate = int()
        self.imgval = StringVar()
        self.latval = StringVar()
        self.lonval = StringVar()
        self.timeval = StringVar()
        self.dateval = StringVar()
        self.headerVal = IntVar()
        self.rbv = IntVar()
        vcmd = (master.register(self.validate), '%d', '%i', '%P', '%s',
                '%S', '%v', '%V', '%W')

        self.entryExif = Entry(master, relief="sunken")
        self.entryExif.insert(0, "EXIF csv file")
        self.entryExif.grid(row=0,columnspan=4, sticky='EW',padx=5, pady=10)
        exifbtn = Button(master, text="OPEN CSV file", command=self.getEXIFfile)
        exifbtn.grid(row=1, column=0, padx=5, sticky='w')

        ##added to allow header line
        self.headerOpt = Checkbutton(master, text="Select if CSV file has header line", variable=self.headerVal)
        self.headerOpt.grid(row=2, column=0, padx=5, sticky='w')

        self.entryJPGS = Entry(master, relief="sunken")
        self.entryJPGS.insert(0, "JPEG folder")
        self.entryJPGS.grid(row=3,columnspan=4, sticky='EW',padx=5, pady=10)
        JPGbtn = Button(master, text="OPEN JPEG folder", command=self.getJPEGFolder)
        JPGbtn.grid(row=4, column=0, padx=5, sticky='w')

        self.paramFile = Entry(master, relief="sunken")
        self.paramFile.insert(0, "Param file")
        self.paramFile.grid(row=5, columnspan=4, sticky='EW', padx=5, pady=10)
        parambtn = Button(master, text="OPEN PARAM file", command=self.getParamfile)
        parambtn.grid(row=6, column=0, padx=5, sticky='w')

        
        lbl_exiftag = Label(master, text="EXIF tag", wraplength=100,
                            anchor='w', justify='left')
        lbl_column = Label(master, text="CSV column (zero based)", wraplength=100,
                           anchor='w', justify='left')
        cbImage = Checkbutton(master, text='Image name', variable=self.imgck,
                              command=self.imgcheck)
        cbLatitude = Checkbutton(master, text='Latitude', variable=self.latck,
                                 command=self.latcheck)
        cbLongitude = Checkbutton(master, text='Longitude', variable=self.lonck,
                                  command=self.loncheck)
        cbTime = Checkbutton(master, text='GPSTime', variable=self.timeck,
                             command=self.timecheck)
        cbDate = Checkbutton(master, text='GPSDate', variable=self.dateck,
                             command=self.datecheck)
        lblText =Label(master, text="Free text fields:")
        lblArtist = Label(master, text="Artist:")
        
##        lbl_analysis = Label(master, text="Analysis Library")
        self.entryImage = Entry(master, validate = 'key', validatecommand = vcmd,
                                width=5, state='disabled')
        self.entryLat = Entry(master, validate = 'key', validatecommand = vcmd,
                              width=5, state='disabled')
        self.entryLon = Entry(master, validate = 'key', validatecommand = vcmd,
                              width=5, state='disabled')
        self.entryTime = Entry(master, validate = 'key', validatecommand = vcmd,
                               width=5, state='disabled')
        self.entryDate = Entry(master, validate = 'key', validatecommand = vcmd,
                               width=5, state='disabled')
        self.entryArtist = Entry(master, width=40)

        #lbl_testcase_exec.grid(row=0, column=2, padx=20, pady=12, sticky='w')
        lbl_exiftag.grid(row=7, column=0, padx=20, pady=12, sticky='w')
        lbl_column.grid(row=7, column=1, padx=10, pady=12, sticky='w')
        cbImage.grid(row=8, column=0, padx=20, sticky='w')
        cbLatitude.grid(row=9, column=0, padx=20, sticky='w')
        cbLongitude.grid(row=10, column=0, padx=20, sticky='w')
        cbTime.grid(row=11, column=0, padx=20, sticky='w')
        cbDate.grid(row=12, column=0, padx=20, sticky='w')
        lblText.grid(row=13, column=0, padx=30, sticky='w')
        lblArtist.grid(row=14, column=0, padx=20, sticky='w')
        self.entryImage.grid(row=8, column=1, padx=10, sticky='w')
        self.entryLat.grid(row=9, column=1, padx=10, sticky='w')
        self.entryLon.grid(row=10, column=1, padx=10, sticky='w')
        self.entryTime.grid(row=11, column=1, padx=10, sticky='w')
        self.entryDate.grid(row=12, column=1, padx=10, sticky='w')
        lbl_datefmt = Label(master, text="Select date format:", wraplength=500,
                           anchor='w', justify='left')
        lbl_datefmt.grid(row=12, column=1, padx=50, sticky='w')
        self.entryArtist.grid(row=14, column=1, padx=10, sticky='w')
##        ##added to allow header line
##        self.dateOpt1 = Checkbutton(master, text="YYYYMMDD", variable=self.headerVal)
##        self.dateOpt1.grid(row=10, column=1, padx=160, sticky='w')
##        self.dateOpt2 = Checkbutton(master, text="YYYY:MM:DD", variable=self.headerVal)
##        self.dateOpt2.grid(row=10, column=1, padx=260, sticky='w')
##        self.dateOpt3 = Checkbutton(master, text="MM/DD/YYYY", variable=self.headerVal)
##        self.dateOpt3.grid(row=10, column=1, padx=360, sticky='w')        

        #try radio buttons
        Radiobutton(master, text="YYYYMMDD", variable=self.rbv, value=1, command=self.rdioInvoke).grid(row=10, column=1, padx=190, sticky='w')
        Radiobutton(master, text="YYYY:MM:DD", variable=self.rbv, value=2, command=self.rdioInvoke).grid(row=11, column=1, padx=190, sticky='w')
        Radiobutton(master, text="MM/DD/YYYY", variable=self.rbv, value=3, command=self.rdioInvoke).grid(row=12, column=1, padx=190, sticky='w')
        Radiobutton(master, text="MM/DD/YY", variable=self.rbv, value=4, command=self.rdioInvoke).grid(row=13, column=1, padx=190, sticky='w')

        # buttons
        bottom_frame = Frame(master)
        bottom_frame.grid(row=30, column=1, columnspan=3, sticky='w')

        #I had to add the self to the prefix, otherwise my rdioInvoke wouldn't work.
        #I'm guessing the self is sort of the global aspect.
        #temporarily commenting this out so I can just test reading the param file
        self.btn_start = Button(bottom_frame, text = "Submit", width=7, command=self.MergeExif)
        #self.btn_start = Button(bottom_frame, text = "Submit", width=7, command=self.readParamfile)
        self.btn_start.pack(side='left', pady=20)
        self.btn_start.config(state='disabled')
##        btn_commit = Button(bottom_frame, text="Commit", width=7)
##        btn_commit.pack(side='left', padx=80)
        btn_exit = Button(bottom_frame, text="Exit", width=7, command=self.cbtnClick)
        btn_exit.pack(side='left', padx=10)

    def rdioInvoke(self):
        print "rdioInvoke"
        self.btn_start.configure(state='normal')
        
    def cbtnClick(self):
        print "close button event handler"
        self.master.destroy()

    def imgcheck(self):
        print "check"
        if self.imgck.get() == 0:
            self.entryImage.configure(state='disabled')
        else:
            self.entryImage.configure(state='normal')
    def latcheck(self):
        print "check"
        if self.latck.get() == 0:
            self.entryLat.configure(state='disabled')
        else:
            self.entryLat.configure(state='normal')            
    def loncheck(self):
        print "check"
        if self.lonck.get() == 0:
            self.entryLon.configure(state='disabled')
        else:
            self.entryLon.configure(state='normal')
    def timecheck(self):
        print "check"
        if self.timeck.get() == 0:
            self.entryTime.configure(state='disabled')
        else:
            self.entryTime.configure(state='normal')
    def datecheck(self):
        print "check"
        if self.dateck.get() == 0:
            self.entryDate.configure(state='disabled')
        else:
            self.entryDate.configure(state='normal')
            #self.datestate == 1
    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            return True
        else:
            return False
    def getEXIFfile(self):
        EXIFcsvfile = tkFileDialog.askopenfilename(title='Image EXIF CSV file')
        #need to fix the next line
        self.entryExif.delete(0,END)
        if len(EXIFcsvfile) > 0:
            self.entryExif.insert(0,EXIFcsvfile)
            
    def getJPEGFolder(self):
        #by not specifying an intial directory, it starts where the script is located.
        JPGfolder = tkFileDialog.askdirectory(title='Pick JPEG folder')
        #need to clear anything that's there
        self.entryJPGS.delete(0,END)
        if len(JPGfolder) > 0:
            #print "now read JPEG folder %s" % JPGfolder
            #for entry widget
            self.entryJPGS.insert(0,JPGfolder)

    def getParamfile(self):
        PARAMtxtfile = tkFileDialog.askopenfilename(title='Paramter text file')
        self.paramFile.delete(0,END)
        if len(PARAMtxtfile) > 0:
            self.paramFile.insert(0,PARAMtxtfile)

    def readParamfile(self):
        params = self.paramFile.get()
        inputparams = open(params, "r")
        allparams = inputparams.read()
        for cmd3 in allparams.splitlines():
            if "-comment" in cmd3:
##                print cmd3
##                print " "
                val3 = cmd3
        for cmd4 in allparams.splitlines():
            if "-sep" in cmd4:
##                print cmd4
##                print " "
                #return cmd4
                val4 = cmd4

        for cmd6 in allparams.splitlines():
            if "-Caption=" in cmd6:
##                print cmd6
##                print " "
                #return cmd6
                val6=cmd6

        for cmd9 in allparams.splitlines():
            if "-Caption-Abstract" in cmd9:
##                print cmd9
##                print " "
                #return cmd9
                val9 = cmd9

        for cmd10 in allparams.splitlines():
            if "-ImageDescription=" in cmd10:
##                print cmd10
##                print " "
                #return cmd10
                val10 = cmd10
##        print "read params"
##        print "val3"
##        print val3
        return (val3, val4, val6, val9, val10)
    
        #self.MergeExif()
        
            
    def MergeExif(self):
        try:
            test = self.entryExif.get()
            print test

##            print "date format"
##            print str(self.rbv.get())
            inputfile = open(test, "r")
            #print "made it here 1"
            imgval = int(self.entryImage.get())
            #print self.entryImage.get()
            #print str(imgval)
            if self.latck.get() <> 0:
                latval = int(self.entryLat.get())
            #print "made it here 1a"
            if self.lonck.get() <> 0:
                lonval = int(self.entryLon.get())
            print "made it here 1b"
            if self.timeck.get() <> 0:
                timeval = int(self.entryTime.get())
            print "made it here 1c"
            if self.dateck.get() <> 0:
                dateval = int(self.entryDate.get())
                print "got date"
                print str(dateval)
            print "made it here 2"
            ##add this if statement to deal with header value
            if self.headerVal.get() == 1:
                print "have a header value"
                line = inputfile.readline()
            else:
                print "no header value"
            print "getting return"
##            retcmd3, retcmd4, retcmd6, retcmd9, retcmd10 = self.readParamfile()
##            print "just cmd3"
##            print retcmd3
            allreturns = self.readParamfile()
            print "allreturns"
            print allreturns
##            print "first return"
##            print allreturns[0]
            while 1:
                line = inputfile.readline()
                print "made it here 3"
                values = str.split(line,",")
##                print line
##                print "imgval"
##                print imgval
                ##if extension is included in text file
                img = values[imgval].strip()
                ##if extension is NOT included in text file
                ##img = values[imgval].strip() + '.JPG'
                vlat = values[latval].strip()
                vlon = values[lonval].strip()
                ingpsdate = values[dateval].strip()
##                #section to read date formats
                if self.rbv.get()==1:
                    vyr=str(ingpsdate)[0:4]
                    vmm=str(ingpsdate)[4:6]
                    vdd=str(ingpsdate)[6:8]
                    vgpsdate=vyr+":"+vmm+":"+vdd
                if self.rbv.get()==2:
                    vgpsdate=ingpsdate
                if self.rbv.get()==3:
                    vmm, vdd, vyr = ingpsdate.split("/")
                    if len(vmm)==1:
                        vmm="0"+vmm
                    if len(vdd)==1:
                        vdd="0"+vdd
                    vgpsdate=vyr+":"+vmm+":"+vdd
                if self.rbv.get()==4:
                    vmm, vdd, vyr = ingpsdate.split("/")
                    if len(vmm)==1:
                        vmm="0"+vmm
                    if len(vdd)==1:
                        vdd="0"+vdd
                    if int(vyr) < 50:
                        vyr="20"+vyr
                    else:
                        vyr="19"+vyr
                    vgpsdate=vyr+":"+vmm+":"+vdd
##                if ingpsdate.find(':')==-1:
##                    vyr=str(ingpsdate)[0:4]
##                    vmm=str(ingpsdate)[4:6]
####                    print ingpsdate
####                    print "year"
####                    print vyr
####                    print "month"
####                    print vmm
##                    vdd=ingpsdate[6:8]
##                    vgpsdate=vyr+":"+vmm+":"+vdd
##                else:
##                    vgpsdate=ingpsdate
                print vgpsdate
                vgpstime = values[timeval].strip()
                imagefolder = self.entryJPGS.get()
                fullimg = os.path.join(imagefolder, img)
                fullimg = fullimg.replace('\\','/')
                vartist = self.entryArtist.get()
                vartistquotes = '"'+vartist+'"'
##                print str(fullimg)                
##                print str(vlat)
##                print str(vlon)
##                print str(vgpsdate)
##                print str(vgpstime)
                if (float(vlat)) > 0:
                    print "latref1"
                    vlatref = 'N'
                else:
                    print "latref2"
                    vlatref = 'S'
                if (float(vlon)) > 0:
                    vlonref = 'E'
                else:
                    vlonref = 'W'
##                print str(vlatref)
##                print str(vlonref)
                cmd = "exiftool -GPSDateStamp=" + vgpsdate + " -GPSTimeStamp="+vgpstime+" -GPSLatitude="+vlat+" -GPSLatitudeRef="+ vlatref+\
                      " -GPSLongitude="+vlon+" -GPSLongitudeRef="+vlonref+" "+ " -Artist=" +vartistquotes +" "+fullimg
                print cmd
                #print "made it past first os.system"
                subprocess.check_call(cmd, shell=True)
                print "executed"
                cmd2 = """exiftool -Credit="U.S. Geological Survey" -Contact="gs-g-spcmsc_data_inquiries@usgs.gov " """+ fullimg
                subprocess.check_call(cmd2, shell=True)

                #jpeg comment
                print "in command 3 section"
                cmd3=allreturns[0]
                cmd3new = cmd3+" "+fullimg
                print cmd3new
                #print cmd3
                #cmd3 = """exiftool -comment="Photo from down-looking camera on the USGS SEABOSS deployed from the R/V Rafael during survey 2012-003-FA (http://woodshole.er.usgs.gov/operations/ia/public_ds_info.php?fa=2012-003-FA). Released as part of publication DOI:10.3133/ds937. " """+ fullimg
                subprocess.check_call(cmd3new, shell=True)
                #iptc info
                #cmd4 = """exiftool -sep ", " -keywords="Barnegat Bay, New Jersey, 2012-003-FA, SEABOSS, sea floor, USGS " """+ fullimg
                cmd4=allreturns[1]
                cmd4new = cmd4+" "+fullimg
                #subprocess.check_call(cmd4, shell=True)
                subprocess.check_call(cmd4new, shell=True)
                #cmd5 unused and skipped

                #xmp info
                #cmd6 = """exiftool -Caption="Photograph of the sea floor in Barnegat Bay, New Jersey from survey 2012-003-FA " """+ fullimg
                cmd6=allreturns[2]
                cmd6new = cmd6+" "+fullimg                
                #subprocess.check_call(cmd6, shell=True)
                subprocess.check_call(cmd6new, shell=True)
                print "did caption"
                #EXIF info
                cmd7 = """exiftool -Copyright="Public Domain - please credit U.S. Geological Survey " """ + fullimg
                subprocess.check_call(cmd7, shell=True)
                print "did copyright"
                #iptc info
                cmd8 = """exiftool -CopyrightNotice="Public Domain - please credit U.S. Geological Survey " """ + fullimg
                subprocess.check_call(cmd8, shell=True)
                #iptc info
                #cmd9 = """exiftool -Caption-Abstract="Photograph of the sea floor in Barnegat Bay, New Jersey from survey 2012-003-FA " """+ fullimg
                cmd9=allreturns[3]
                cmd9new = cmd9+" "+fullimg                 
                #subprocess.check_call(cmd9, shell=True)
                subprocess.check_call(cmd9new, shell=True)
                #exif info - software such as Picasso use this as the caption
                #cmd10 = """exiftool -ImageDescription="Photograph of the sea floor in Barnegat Bay, New Jersey from survey 2012-003-FA " """+ fullimg                
                cmd10=allreturns[4]
                cmd10new = cmd10+" "+fullimg                
                #subprocess.check_call(cmd10, shell=True)
                subprocess.check_call(cmd10new, shell=True)
        except:
            print "booboo maybe?"
        inputfile.close()
        print "done"
root = Tk()
root.title("Test Automation")
root.minsize(800, 400)
app = App(root)
root.mainloop()
