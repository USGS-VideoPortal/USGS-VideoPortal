#This code was originally written by VeeAnn Cross (USGS)
#and is based on the SEABOSS tool parse_hypack_folder.py
#The GUI code based on the Tkinter tutorial from: http://www.zetcode.com/gui/tkinter/layout/
#modified 7/30/2013 
#to sort the output and closed a file that was left open
#removed the intialdir so the code starts where the code is located.
#modified 8/27/13
#-this modification is to allow it to process all files in a folder
#-the user needs to make sure all the files are actually HYPACK files
#-it will run a whole folder if file extensions is written as *
#-note: julian day comes from TND calculation, not filename. 
#modified 8/22/2016 - sda
#cleaning up the code for methods doc to accompany the CMGP Vid/Photo Portal
#this code was tested and worked on a Mac OSX 10.10 using Python 2.7.12

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
        self.pack(fill=BOTH, expand=1)

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

        junk = "HYPACK folder"
        junk2 = "output file"                     
        
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
        #HYPfolder = tkFileDialog.askdirectory(initialdir="C:/", title='Pick HYPACK folder')
        #by not specifying an intial directory, it starts where the script is located.
        HYPfolder = tkFileDialog.askdirectory(title='Pick HYPACK folder')

        self.entryLabel2.delete(0,END)
        if len(HYPfolder) > 0:
            print "now read HYPACK folder %s" % HYPfolder

            #for entry widget
            self.entryLabel2.insert(0,HYPfolder)

    def saveHYPtext(self):
        HYPtext = tkFileDialog.asksaveasfilename(initialfile="parsedHYP.txt", title='Save HYPACK Parsed file')
        print HYPtext
        self.outLabel2.delete(0,END)

        self.outLabel2.insert(0,HYPtext)


    def ParseHYPACK(self):
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

        output = open(parsefile,"w")
        tempfolder = "c:/temp/"
        if os.path.exists(tempfolder):
            usetmpfolder = tempfolder
        else:
            usetmpfolder = tkFileDialog.askdirectory(initialdir="C:/", title='Pick temporary folder')
        tmpfile = "hypjunk.txt"
        skpfile = "skippedfiles.txt"

        #to make a normal windows path with all the slashes going the same way
        tempfile = os.path.normpath(os.path.join(usetmpfolder, tmpfile))
        skipfile = os.path.normpath(os.path.join(usetmpfolder, skpfile))
        print tempfile
        outtemp = open(tempfile, "w")
        outskip = open(skipfile,"w")
        
        newline = "\n"
        #output.writelines("Latitude, Longitude, Hours, Minutes, Seconds, JulianDay, Year, CruiseID")
        #modified 8/27/13 to add prefix filename
        output.writelines("Latitude, Longitude, Hours, Minutes, Seconds, JulianDay, Year, CruiseID, file")
        output.writelines(newline)

        for infile in glob.glob(os.path.join(navfolder,inputext)): # in navfolder:
            dir_name, file_name=os.path.split(infile)
            nav_name, nav_ext=os.path.splitext(file_name)
            file=open(infile,"r")
            #print file
            count = 0
            while 1:
                line = file.readline()
                count = count + 1
                word = line.split()
                if not line: break
                if count == 1:
                    if line[0:3] <> "FTP":
                        print line[0:3]
                        print "not a hypack file"
                        outskip.write("%s%s" % (file_name, newline))
                        break        

                #grab TND to calculate Julian day
                if line[0:3] == "TND":
                    month = string.atoi(word[2][0:2])
                    day = string.atoi(word[2][3:5])
                    year = string.atoi(word[2][6:10])
                    epochtime = (time.mktime((year,month,day,0,0,0,0,0,0)))
                    time2 = time.strftime("%j", time.gmtime(epochtime))

                #the next if clause will grab lat, long, and time from the RAW string
                #have to account for different longitude character length
                #also had to modify this to take RAW as input as this
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
                     #output.write("%f, %f, %i, %i, %i, %s, %i, %s%s" % (latdeg3, longdeg3, hour, minute, sec, time2, year, cruiseID, newline))
                     #writing to a temporary file that I will then sort based on julian day and time
                     #outtemp.write("%f, %f, %i, %i, %i, %s, %i, %s%s" % (latdeg3, longdeg3, hour, minute, sec, time2, year, cruiseID, newline))
                     #added 8/27/13 to write filename
                     outtemp.write("%f, %f, %i, %i, %i, %s, %i, %s, %s%s" % (latdeg3, longdeg3, hour, minute, sec, time2, year, cruiseID, file_name, newline))
                     #print nav_name
            #this is the break line, so I want to reset my counter since the whole file has been read
            count = 0         
        outtemp.close()
        #outtemp.open('r')
        #with open(outtemp) as info:
        #    file_sorted = sorted((ast.literal_eval(x) for x in f), key=lambda z:(int(z[5]),z[2],z[3],z[4]))
        #the sorting based on:
        #http://www.daniweb.com/software-development/python/threads/142829/sort-by-column-im-stumped
        unsorted_data = open(tempfile,'r')
        data_list = []
        data_list = [line.strip() for line in open(tempfile)]

        data_list.sort(key=lambda line: (int(line.split(",")[5]),int(line.split(",")[2]),int(line.split(",")[3]),int(line.split(",")[4])))

        #output.write(file_sorted)
        #output.write('\n'.join(data_list))
        #the list writing based on:
        #http://stackoverflow.com/questions/899103/python-write-a-list-to-a-file
        output.writelines( "%s\n" % item for item in data_list )
        #output.write("testing writing")
        output.close()
        unsorted_data.close()
        tkMessageBox.showinfo("HYPACK Parse", "Done")

def main():
  
    root = Tk()
    root.geometry("550x400+300+300")
    app = Example(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()
