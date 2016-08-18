#from http://www.zetcode.com/gui/tkinter/layout/
#making mods to attach commands to button
#right now this won't work in Python 2.5 because of ttk
#but I think I can get rid of that
#v2
#starting to zero in on some formatting, so I need
#to delete some comments because it's confusing me.
#this is the equivalent of parse_hypack_folder.py
#in D:\edrive\python\SEABOSS_june2009
#original working filename:
#tkinter_grid2_vac_v4.py
#in: D:\edrive\python\TKinter\test\grid
"""
ZetCode Tkinter tutorial

In this script, we use the grid
manager to create a more complicated
layout.

author: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

#from Tkinter import Tk, Text, BOTH, W, N, E, S
#from ttk import Frame, Button, Label, Style
from Tkinter import *
import tkFileDialog
import tkMessageBox
import sys, string, time
import glob, os


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
      
        self.parent.title("Parse HYPACK Navigation Folder")
        #commented out next two lines because no ttk in python 2.5
        #self.style = Style()
        #self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        #next 4 lines are the original coding
        #self.columnconfigure(1, weight=1)
        #self.columnconfigure(4, pad=7)
        #self.rowconfigure(3, weight=1)
        #self.rowconfigure(5, pad=1)
        #self.rowconfigure(9, pad=1)
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

        self.columnconfigure(0, weight=1, pad=1)
        self.columnconfigure(1, weight=1, pad=1)
        self.columnconfigure(2, weight=1, pad=1)
        #self.columnconfigure(3, weight=1, pad=5)
        #self.columnconfigure(4, weight=1, pad=5)

        junk = "junk test"
        junk2 = "Junk test 2"                     
        
        lbl = Label(self, text="Input")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        entryLabel = Label(self, text="Navigation folder: ", fg="red")
        entryLabel.grid(row=1, sticky=W, column=0, padx=5)
        #as label
        #self.entryLabel2 = Label(self, relief="sunken", width=75)
        #self.entryLabel2.config(text=junk)
        #self.entryLabel2.grid(padx=5)
        #as entry line
        self.entryLabel2 = Entry(self, relief="sunken")
        self.entryLabel2.insert(0, junk)
        self.entryLabel2.grid(padx=5,columnspan=3, sticky=W+E, row=2)
        
        abtn = Button(self, text="OPEN folder", command=self.getHYPACKFolder)
        abtn.grid(row=3, column=0, padx=5, sticky=W)
        

        lblFileExtension = Label(self, text="File extension: ")
        lblFileExtension.grid(row=4, column=0, sticky=W, padx=5)

        self.txtFileExtension = Entry(self)
        self.txtFileExtension.grid(row=5, column=0, sticky=W, padx=12)

        outLabel = Label(self, text="Output file: ")
        outLabel.grid(row=6,padx=5, sticky=W)

        #output filename as label
        #self.outLabel2 = Label(self, relief="sunken", width=75)
        #self.outLabel2.configure(text=junk2)
        #self.outLabel2.grid(row=6, padx=5)
        #output filename as entry line
        self.outLabel2 = Entry(self, relief="sunken")
        self.outLabel2.insert(0, junk2)
        self.outLabel2.grid(padx=5, columnspan=3,sticky=W+E, row=7)

        filebtn = Button(self, text="Output file", command=self.saveHYPtext)
        filebtn.grid(row=8,column=0, padx=5, sticky=W)

        lblCruise = Label(self, text="Cruise ID: ")
        lblCruise.grid(row=11, column=0, sticky=W, padx=5)

        self.txtCruise = Entry(self)
        self.txtCruise.grid(row=12, column=0, sticky=W, padx=12)

        lblDevice = Label(self, text="Device ID: ")
        lblDevice.grid(row=13, column=0, sticky=W, padx=5)

        self.txtDevice = Entry(self)
        self.txtDevice.grid(row=14, column=0, sticky=W, padx=12)

        cbtn = Button(self, text="Close", command=self.cbtnClick)
        cbtn.grid(row=15, column=2)
        
        hbtn = Button(self, text="Submit", command=self.ParseHYPACK)
        hbtn.grid(row=15, column=0, padx=5)


    def cbtnClick(self):
        print "close button event handler"
        self.parent.destroy()

    def getHYPACKFolder(self):
        #HYPfolder = tkFileDialog.askdirectory(initialdir="F:/", title='PickHYPACK')
        HYPfolder = tkFileDialog.askdirectory(initialdir="C:/", title='PickHYPACK')
        #need to clear anything that's there
        self.entryLabel2.delete(0,END)
        if len(HYPfolder) > 0:
            print "now read HYPACK folder %s" % HYPfolder
            #self.entryLabel2.config(text=HYPfolder)
            #this took forever to get to work. I had to add the self. to the entryLabel2
            #and then the self here. without it in both places - no go.
            #for entry widget
            self.entryLabel2.insert(0,HYPfolder)

    def saveHYPtext(self):
        HYPtext = tkFileDialog.asksaveasfilename(initialfile="parsed.txt", title='Save HYPACK Parsed file')
        print HYPtext
        #need to clear anything that's there
        self.outLabel2.delete(0,END)
        #from when it was just a lable
        #self.outLabel2.config(text=HYPtext)
        self.outLabel2.insert(0,HYPtext)
        #if HYPtext:
            #print "now writing file %" % str(HYPtext)
            #self.outLabel2.config(str(HYPtext))
            #return open(filename, 'w')
            #return HYPtext

    def ParseHYPACK(self):
        #first think I need to do is make sure nothing is blank, but haven't coded that yet
        navfolder = self.entryLabel2.get()
        fileext = self.txtFileExtension.get()
        parsefile = self.outLabel2.get()
        cruiseID = self.txtCruise.get()
        inputext = "*." + fileext
        rawline = self.txtDevice.get()
        rawtext = "RAW " + rawline
        print navfolder
        print fileext
        print parsefile
        print cruiseID
        print inputext
        print rawtext
        #listing = os.listdir(navfolder)
        #for infile in glob.glob(os.path.join(navfolder,inputext)):
        #    print "current file is: " + infile
        #now that I've populated my variables, I'm pretty much just going to grab from my other code.
        output = open(parsefile,"w")
        newline = "\n"
        output.writelines("Latitude, Longitude, Hours, Minutes, Seconds, JulianDay, Year, CruiseID")
        output.writelines(newline)
        #had to completely redo this next part about getting the files
        #list. I have no idea why what I have in the other program
        #works at all - in ArcGIS or otherwise.
        for infile in glob.glob(os.path.join(navfolder,inputext)): # in navfolder:
            dir_name, file_name=os.path.split(infile)
            nav_name, nav_ext=os.path.splitext(file_name)
            file=open(infile,"r")
            #print file
            while 1:
                line = file.readline()
                word = line.split()
                if not line: break

                #grab TND to calculate Julian day
                if line[0:3] == "TND":
                    month = string.atoi(word[2][0:2])
                    day = string.atoi(word[2][3:5])
                    year = string.atoi(word[2][6:10])
                    epochtime = (time.mktime((year,month,day,0,0,0,0,0,0)))
                    time2 = time.strftime("%j", time.gmtime(epochtime))

                #the next if clause will grab lat, long, and time from the RAW string
                #have to account for different longitude character length
                #alo had to modify this to take RAW as input as this
                    #cruise had 2 gps systems on board
                if line[0:5] == rawtext:
                     latitude = word[4]
                     longitude = word[5]
                     navstime = string.split(word[7],".")
                     navlength = len(navstime[0])

                     #on the RAW line, time does not contain a uniform number of characters.
                     #So, I have to see how many numbers there are, and split the string
                     #into it's time pieces accordingly

                     if navlength < 3:
                         hour = 0
                         minute = 0
                         sec = string.atoi(navstime[0])
                     elif navlength < 5:
                         hour = 0
                         minute = string.atoi(navstime[0][0:navlength-2])
                         sec = string.atoi(navstime[0][navlength-2:navlength])
                     else:
                         hour = string.atoi(navstime[0][0:navlength-4])
                         minute = string.atoi(navstime[0][navlength-4:navlength-2])
                         sec = string.atoi(navstime[0][navlength-2:navlength])
                     if latitude[0:1] == "-":
                         if len(latitude) == 12:
                             lat = string.atof(word[4][0:2])
                             latdeg = string.atof(word[4][2:12])
                             latdeg2 = latdeg/6000
                             latdeg3 = lat - latdeg2
                         elif len(latitude) == 13:
                             lat = string.atof(word[4][0:3])
                             latdeg = string.atof(word[4][3:13])
                             latdeg2 = latdeg/6000
                             latdeg3 = lat - latdeg2
                     elif latitude[0:1] != "-":
                         if len(latitude) == 11:
                             lat = string.atof(word[4][0:1])
                             latdeg = string.atof(word[4][1:11])
                             latdeg2 = latdeg/6000
                             latdeg3 = lat + latdeg2
                         elif len(latitude) == 12:
                             lat = string.atof(word[4][0:2])
                             latdeg = string.atof(word[4][2:12])
                             latdeg2 = latdeg/6000
                             latdeg3 = lat + latdeg2
                     if longitude[0:1] == "-":
                         if len(longitude) == 12:
                             longi =  string.atof(word[5][0:2])
                             longdeg = string.atof(word[5][2:12])
                             longdeg2 = longdeg/6000
                             longdeg3 = longi - longdeg2
                         elif len(longitude) == 13:
                             longi =  string.atof(word[5][0:3])
                             longdeg = string.atof(word[5][3:13])
                             longdeg2 = longdeg/6000
                             longdeg3 = longi - longdeg2
                         elif len(longitude) == 14:
                             longi = string.atof(word[5][0:4])
                             longdeg = string.atof(word[5][4:14])
                             longdeg2 = longdeg/6000
                             longdeg3 = longi - longdeg2
                     if longitude[0:1] != "-":
                         if len(longitude) == 11:
                             longi =  string.atof(word[5][0:1])
                             longdeg = string.atof(word[5][1:11])
                             longdeg2 = longdeg/6000
                             longdeg3 = longi + longdeg2
                         elif len(longitude) == 12:
                             longi =  string.atof(word[5][0:2])
                             longdeg = string.atof(word[5][2:12])
                             longdeg2 = longdeg/6000
                             longdeg3 = longi + longdeg2
                         elif len(longitude) == 13:
                             longi = string.atof(word[5][0:3])
                             longdeg = string.atof(word[5][3:13])
                             longdeg2 = longdeg/6000
                             longdeg3 = longi + longdeg2
                     output.write("%f, %f, %i, %i, %i, %s, %i, %s%s" % (latdeg3, longdeg3, hour, minute, sec, time2, year, cruiseID, newline))
                     #print nav_name
        output.close()
        tkMessageBox.showinfo("HYPACK Parse", "Done")

def main():
  
    root = Tk()
    root.geometry("550x400+300+300")
    app = Example(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()
