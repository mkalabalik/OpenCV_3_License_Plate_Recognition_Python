# -*- coding: utf-8 -*-

from tkinter import *
from PIL import ImageTk, Image
import os, time, sys
import Main
import picamera
import serial

strLicense = "<PLAKA>"
##hiz = 0.01
hizLimiti = 999

WINDOWWIDTH = 972 #324*3
WINDOWHEIGHT = 486


class Gui(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        self.title("Plaka Tanıma")
        self.geometry("{}x{}+100+100".format(WINDOWWIDTH, WINDOWHEIGHT))

        self.strLicense = strLicense
        self.speed = 0
        self.speedLimit = hizLimiti

        #Camera
        self.camera = picamera.PiCamera()
        self.camera.close()

                       

        #Left frame
        self.frameLeft = Frame(self)
        self.frameLeft.place(x = 0, y = 0, height = 486, width = 324)
        self.frameRight = Frame(self)
        self.frameRight.place(x = WINDOWWIDTH/3, y = 0)
        #self.frameRight.pack(side = "right")

        ##Entry for License
        self.entryLicense = Entry(self.frameLeft, width = len(strLicense), font=("Calibri", 40))
        self.entryLicense.insert(0, strLicense)
        self.entryLicense.place(x = 0, y = 5*WINDOWHEIGHT/6)

        self.imgOriginalSceneGui = "imgOriginalSceneGui.png"
        self.imgLicenseGui = "imgLicenseGui.png"
        self.imgLicenseCharsGui = "imgLicenseCharsGui.png"
        self.imgNotFoundGui = "imgNotFoundGui.png"
        
        #Read images
        self.readImages()
        self.imgNotFound = ImageTk.PhotoImage(Image.open(self.imgNotFoundGui))

        #Entry of Speed
        self.entrySpeed = Entry(self.frameLeft, width = 4, font=("Calibri",40))
        self.entrySpeed.insert(0, self.speed)
        self.entrySpeed.place(x = 2*WINDOWWIDTH/20, y = 1*WINDOWHEIGHT/6)
        #entryLicense.grid(column=1, row=3, padx=20, pady=20)

        #Buttons
        self.var = IntVar()
        self.Button1 = Radiobutton(self.frameLeft, text = "Mod 1: Radar ",
                                   variable = self.var, value = 1, command = self.fromRadar)
        self.Button2 = Radiobutton(self.frameLeft, text = "Mod 2: Kamera",
                                   variable = self.var, value = 2, command = self.fromCamera)
        self.Button3 = Radiobutton(self.frameLeft, text = "Mod 3: Dosya",
                                   variable = self.var, value = 3, command = self.fromDirectory)
        self.Button1.place(x = 0, y = 0*WINDOWHEIGHT/18)
        self.Button2.place(x = 0, y = 1*WINDOWHEIGHT/18)
        self.Button3.place(x = 0, y = 2*WINDOWHEIGHT/18)

        #When close the window, run exit function
        self.protocol('WM_DELETE_WINDOW', self.exitFunction)

        #Start main function
        self.main()
        
        #Serial connection
        try:
            self.serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
            self.writeSpeed()
        except:
            self.serial = None
            
        

    def putImages(self):
        """
        Put the images on GUI
        """

        ##Put images into left frame
        self.labelLicense = Label(self.frameLeft, image = self.imgLicense)
        self.labelLicense.place(x = WINDOWWIDTH/25, y = 3*WINDOWHEIGHT/6)
        #self.labelLicense.grid(column=1, row=1)

        self.labelLicenseThresh = Label(self.frameLeft, image = self.imgLicenseChars)
        self.labelLicenseThresh.place(x = WINDOWWIDTH/25, y = 4*WINDOWHEIGHT/6)
        #self.labelLicenseThresh.grid(column=1, row=2, padx=20, pady=20)

        
        ##Put images into right frame
        self.labelImageOriginal = Label(self.frameRight, image = self.imgOriginalScene)
        self.labelImageOriginal.pack(side = "left") #, fill = "both", expand = "yes"

    def placeStrLicense(self):
        if self.strLicense == None:
            self.strLicense = "Bulunamadı"
            
        self.entryLicense.configure(width = len(self.strLicense))
        self.entryLicense.delete(0, END)
        self.entryLicense.insert(0, self.strLicense)
##        self.entryLicense.place(x = WINDOWWIDTH/20, y = 5*WINDOWHEIGHT/6)
        #self.entryLicense.grid(column=1, row=3, padx=20, pady=20)
        
    def cameraClose(self):
        self.camera.close()
        
    def cameraOpen(self):
        if self.camera.closed:
            self.camera = picamera.PiCamera()
            time.sleep(1)
        
    def takePhoto(self):
        self.camera.capture("imgOriginalScene.png")

    def readImages(self):
        self.imgOriginalScene = ImageTk.PhotoImage(Image.open(self.imgOriginalSceneGui))
        if self.strLicense == None:
            self.imgLicense = self.imgLicenseChars = self.imgNotFound
        else:
            self.imgLicense = ImageTk.PhotoImage(Image.open(self.imgLicenseGui))
            self.imgLicenseChars = ImageTk.PhotoImage(Image.open(self.imgLicenseCharsGui))
        
    def refresh(self):
        self.labelLicense.destroy()
        self.labelLicenseThresh.destroy()
        self.labelImageOriginal.destroy()
        self.readImages()
##        self.imgOriginalScene = ImageTk.PhotoImage(Image.open("imgOriginalSceneGui.png"))
##        self.imgLicense = ImageTk.PhotoImage(Image.open("imgLicenseGui.png"))
##        self.imgLicenseChars = ImageTk.PhotoImage(Image.open("imgLicenseCharsGui.png"))

        
    def speedFromSerial(self):
        try:
            bytesDataFromSerial = self.serial.readline()
            strSpeedFromData = str(bytesDataFromSerial)[2:-5]
            intSpeed = int(strSpeedFromData)
        except:
            intSpeed = -1
        return intSpeed

    def writeSpeed(self):
        try:
            while True:
                self.speed = self.speedFromSerial()
                self.entrySpeed.delete(0, END)
                #self.entrySpeed.insert(0, self.speed)
                self.entrySpeed.insert(0, "0")
                self.entrySpeed.update()
        except:
            pass
            
    def fromRadar(self):
        print("Reading speed from radar...")
        while self.var.get() == 1:
            self.speed = self.speedFromSerial()
            self.entrySpeed.delete(0, END)
            self.entrySpeed.insert(0, self.speed)
            self.entrySpeed.update()
##            print(self.speed)
            if self.speed > self.speedLimit:
                print("OVERSPEED")
                self.fromCamera()
    
    def fromDirectory(self):
        self.cameraClose()
        print("Reading file from directory")
        self.strLicense = Main.main("test.jpg")
        self.refresh()
        self.main()
        
    def fromCamera(self):
        print("Reading file from camera")
        self.cameraOpen()
        self.takePhoto()
        self.strLicense = Main.main()
        self.refresh()
        self.main()
        
    def exitFunction(self):
        self.cameraClose()
        self.destroy()
##        self.after(1250, self.destroy)
        print("exit function running")
        
    def main(self):
        self.putImages()
        self.placeStrLicense()
        
gui = Gui()
gui.mainloop()

