#This code was originally written by VeeAnn Cross (USGS)
#and is based on the SEABOSS tool JPEG_exifextract.py
#The GUI code based on the Tkinter tutorial from: http://www.zetcode.com/gui/tkinter/layout/
#modified 7/30/2013
#added the capability to sort the output EXIF information chronologically
#modified 8/1/2013
#removed the initialdir references to file location
#added check on temporary folder
#modified 8/5/2013
#in the template format statement, removed the space before the pathname. This was causing problems
#when this turns into a shapefile.
#modified 8/22/2016 - sda
#cleaning up the code for methods doc to accompany the CMGP Vid/Photo Portal
#this code was tested and worked on a Mac OSX 10.10 using Python 2.7.12


from Tkinter import *
import tkFileDialog
import tkMessageBox
import sys, glob, os
import EXIF
import string, time

# default template
template="""%(Filename)s,%(Pathname)s, %(EXIF DateTimeOriginal)s, %(EXIF ExposureTime)s, f/%(EXIF FNumber)s, %(EXIF FocalLength)s, %(Image ImageDescription)s, %(Image Model)s"""
class PrintMap:
    def __init__(self, map):
        self.map=map
        
    def __getitem__(self, key):
    	return self.map.get(key, '???')

class VACEXIFextract(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
      
        self.parent.title("Extract JPEG EXIF headers")
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

        junk = "JPEG image folder"
        junk2 = "output file"                     
        
        lbl = Label(self, text="Input")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        entryLabel = Label(self, text="JPEG image folder: ")
        entryLabel.grid(row=1, sticky=W, column=0, padx=5)
        
        self.entryLabel2 = Entry(self, relief="sunken")
        self.entryLabel2.insert(0, junk)
        self.entryLabel2.grid(padx=5,columnspan=3, sticky=W+E, row=2)
        
        abtn = Button(self, text="OPEN folder", command=self.getHYPACKFolder)
        abtn.grid(row=3, column=0, padx=5, sticky=W)

        outLabel = Label(self, text="Output file: ")
        outLabel.grid(row=6,padx=5, sticky=W)

        self.outLabel2 = Entry(self, relief="sunken")
        self.outLabel2.insert(0, junk2)
        self.outLabel2.grid(padx=5, columnspan=3,sticky=W+E, row=7)

        filebtn = Button(self, text="Output file", command=self.saveHYPtext)
        filebtn.grid(row=8,column=0, padx=5, sticky=W)
        
        hbtn = Button(self, text="Submit", command=self.ParseHYPACK)
        hbtn.grid(row=15, column=0, padx=5)

        cbtn = Button(self, text="Close", command=self.cbtnClick)
        cbtn.grid(row=15, column=2)



    def cbtnClick(self):
        print "close button event handler"
        self.parent.destroy()

    def getHYPACKFolder(self):
        HYPfolder = tkFileDialog.askdirectory(title='Pick Image Folder')
        self.entryLabel2.delete(0,END)
        if len(HYPfolder) > 0:
            print "now read JPEG folder %s" % HYPfolder
            self.entryLabel2.insert(0,HYPfolder)

    def saveHYPtext(self):
        HYPtext = tkFileDialog.asksaveasfilename(initialfile="parsedEXIF.txt", title='Save EXIF info file')
        print HYPtext
        self.outLabel2.delete(0,END)
        self.outLabel2.insert(0,HYPtext)


    def ParseHYPACK(self):
        jpegfolder = self.entryLabel2.get()
        parsefile = self.outLabel2.get()
        tempfolder = "c:/temp/"
        if os.path.exists(tempfolder):
            usetmpfolder = tempfolder
        else:
            usetmpfolder = tkFileDialog.askdirectory(initialdir="C:/", title='Pick temporary folder')
        tmpfile = "exifjunk.txt"
        #the normpath makes it look right for windows.
        tempfile = os.path.normpath(os.path.join(usetmpfolder, tmpfile))
        print tempfile
        output = open(tempfile,"w")
        for infile in glob.glob(os.path.join(jpegfolder,'*.JPG')): # in navfolder:
            dir_name, file_name=os.path.split(infile)
            photo_name, photo_ext=os.path.splitext(file_name)
            f=open(infile,"rb")
            tags=EXIF.process_file(f)
            tags['Filename']=file_name
            tags['Dirname']=dir_name
            imgtime=tags['EXIF DateTimeOriginal']
            #taking the image time, parsing it and creating the epoch time to use for sorting
            imgstring = str(imgtime)
            datetimestuff = string.split(imgstring, " ")
            datestr = (datetimestuff[0])
            timestr = (datetimestuff[1])
            datestuff = string.split(datestr,":")
            yearid = string.atoi(datestuff[0])
            month = string.atoi(datestuff[1])
            day = string.atoi(datestuff[2])
            timestuff = string.split(timestr,":")
            timehr = string.atoi(timestuff[0])
            timemin = string.atoi(timestuff[1])
            timesec = string.atoi(timestuff[2])
            timeepoch = (time.mktime((yearid,month,day,timehr,timemin,timesec,0,0,0)))

            #this next line takes the path name and normalizes the case of a pathname
            #on Windows, it converts forward slashes to backward slashes.
            tags['Pathname']=os.path.normpath(infile)
            #print info using template
            #add epoch time to the output so I can use it in the sort
            #this output actually writes to the temporary file - should overwrite if it exists
            output.write( template % PrintMap(tags) + ', ' + str(timeepoch)  + '\n')


        output.close()
        unsorted_data = open(tempfile,'r')
        data_list = []
        data_list = [line.strip() for line in open(tempfile)]
        data_list.sort(key=lambda line: float(line.split(",")[8]))
        outputsort=open(parsefile,"w")
        outputsort.writelines( "%s\n" % item for item in data_list )
        outputsort.close()
        unsorted_data.close()
        tkMessageBox.showinfo("JPEG Parse", "Done")

def main():
  
    root = Tk()
    root.geometry("550x400+300+300")
    app = VACEXIFextract(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()
