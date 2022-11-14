import tkinter as tk
from tkinter import *
from tkinter import ttk
from turtle import right
import numpy as np
from PIL import Image, ImageTk


gravityVector = np.array([])
massTypeInt = 1
forceTypeInt = 2
loadList = []
displayLoadList = []
accelList = []
accelVector = np.array([])
accelVectorList = np.array([])
directionArray = [[1, 1, 1],
                [1, 1, -1],
                [1, -1, 1],
                [1, -1, -1],
                [-1, 1, 1],
                [-1, 1, -1],
                [-1, -1, 1],
                [-1, -1, -1]]
ownAccelBase = [[1, 0, 0],
                [-1, 0, 0]]
ownAccel = 0

class actuatorLoad:
    name = ""
    xPos = 0
    yPos = 0
    zPos = 0 
    forceVector = np.array([0, 0, 0])
    momentVector = np.array([0, 0, 0])
    type = 0
    def __init__(self, name, xPosition, yPosition, zPosition, type):
        self.name = name
        self.xPos = xPosition
        self.yPos = yPosition
        self.zPos = zPosition 
        self.type = int(type)
    def getLoadType(self):
        return self.type

class massLoad(actuatorLoad):
    mass = 0
    def __init__(self, name, xPosition, yPosition, zPosition, mass):
        actuatorLoad.__init__(self, name, xPosition, yPosition, zPosition, massTypeInt)
        self.mass = mass
    def getForceVector (self, accelVector):
        self.forceVector = self.mass * accelVector
        return self.forceVector

    def getPosVectorMeters(self):
        comList = [self.xPos, self.yPos, self.zPos]
        comVector = np.array(comList)
        comVectorMeters = comVector / 1000
        return comVectorMeters

    def getMomentVector(self, accelVector):
        force = self.getForceVector(accelVector)
        radius = self.getPosVectorMeters()
        moment = np.cross(radius, force)
        return moment

    def toString(self):
        retString = f"(mass load) {self.name}, mass: {self.mass}, x: {self.xPos}, y: {self.yPos}, z: {self.zPos}"
        return retString

class forceLoad(actuatorLoad):
    xForce = 0
    yForce = 0
    zForce = 0

    def __init__(self, name, xPosition, yPosition, zPosition, xForce, yForce, zForce):
        actuatorLoad.__init__(self, name, xPosition, yPosition, zPosition, forceTypeInt)
        self.xForce = xForce
        self.yForce = yForce
        self.zForce = zForce
        self.forceVector = np.array([xForce, yForce, zForce])
    def getForceVector(self, accelVector):
        return self.forceVector

    def getPosVectorMeters(self):
        comList = [self.xPos, self.yPos, self.zPos]
        comVector = np.array(comList)
        comVectorMeters = comVector / 1000
        return comVectorMeters
    
    def getMomentVector(self, accelVector):
        force = self.getForceVector(accelVector)
        radius = self.getPosVectorMeters()
        moment = np.cross(radius, force)
        return moment
    
    def toString(self):
        retString = f"(Force load) {self.name}, x: {self.xPos}, y: {self.yPos}, z: {self.zPos} force{self.forceVector}"
        return retString

def updateForm():
    #print(accelVector)
    #print("")
    allDirectionAccel = np.multiply(accelVector, directionArray)
    ownAccelArray = np.multiply(ownAccel, ownAccelBase)
    print(ownAccelArray)
    print(allDirectionAccel)
    allForceArray = np.zeros((16,3))
    allMomentArray = np.zeros((16,3))
    actuatorAccelAdder = 0;
    for j in range (2):
        loopOwnAccel = ownAccelArray[j]
        #print(loopOwnAccel)
        for i in range(8):
            loopForceVector = np.array([0, 0, 0])
            loopMomentVector = np.array([0, 0, 0])
            loopAccel = allDirectionAccel[i]
            #print(loopAccel)
            global gravityVector 
            loopAccel = loopAccel + gravityVector + loopOwnAccel
            #print(loopAccel)
            #print(loopAccel)
            #print("_____________")
            for load in loadList:
                #print(loopAccel)
                loopForceVector = loopForceVector + load.getForceVector(loopAccel)
                #print(forceVector)
                loopMomentVector = loopMomentVector + load.getMomentVector(loopAccel)
                #print(momentVector)
                #print("")
            allForceArray[i + actuatorAccelAdder] = loopForceVector
            allMomentArray[i + actuatorAccelAdder] = loopMomentVector
        actuatorAccelAdder = 8
    #print(allForceArray)
    #print(allMomentArray)
    xForceList = allForceArray[:,0]
    #print(xForceList)
    absoluteXforceList = np.absolute(xForceList)
    #print(absoluteXforceList)
    xForceMax = absoluteXforceList.max()
    #print(xForceMax)
    yForceList = allForceArray[:,1]
    #print(xForceList)
    absoluteYforceList = np.absolute(yForceList)
    #print(absoluteXforceList)
    yForceMax = absoluteYforceList.max()
    #print(xForceMax)
    zForceList = allForceArray[:,2]
    #print(xForceList)
    absoluteZforceList = np.absolute(zForceList)
    #print(absoluteXforceList)
    zForceMax = absoluteZforceList.max()
    #print(xForceMax)

    xMomentList = allMomentArray[:,0]
    xMomentAbsolute = np.absolute(xMomentList)
    xMaxMoment = xMomentAbsolute.max();
    yMomentList = allMomentArray[:,1]
    yMomentAbsolute = np.absolute(yMomentList)
    yMaxMoment = yMomentAbsolute.max();
    zMomentList = allMomentArray[:,2]
    zMomentAbsolute = np.absolute(zMomentList)
    zMaxMoment = zMomentAbsolute.max();

    forceResult["text"] = f"Force (N): Fx: {xForceMax:.1f}, Fy: {yForceMax:.1f}, Fz: {zForceMax:.1f}"
    momentResult["text"] = f"Moment (N*m): Mx: {xMaxMoment:.1f}, My: {yMaxMoment:.1f}, Mz: {zMaxMoment:.1f}"

def addMass():
    name = nameEntry.get()
    mass = float(massEntry.get())
    xCom = float(xComEntry.get())
    yCom = float(yComEntry.get())
    zCom = float(zComEntry.get())
    newMassLoad = massLoad(name, xCom, yCom, zCom, mass)
    loadList.append(newMassLoad)
    updateLoadListBox()

def addForce():
    name = forceNameEntry.get()
    xForce = float(xForceEntry.get())
    yForce = float(yForceEntry.get())
    zForce = float(zForceEntry.get())
    xPos = float(xPosEntry.get())
    yPos = float(yPosEntry.get())
    zPos = float(zPosEntry.get())
    newForceLoad = forceLoad(name, xPos, yPos, zPos, xForce, yForce, zForce)
    loadList.append(newForceLoad)
    updateLoadListBox()

def updateAccel():
    xAccel = float(xAccelEntry.get())
    yAccel = float(yAccelEntry.get())
    zAccel = float(zAccelEntry.get())
    global ownAccel 
    ownAccel = float(ownAccelEntry.get())
    accelList = np.array([xAccel, yAccel, zAccel])
    global accelVector
    global gravityVector

    accelVector= np.array(accelList)
    if verticalOrHorizontal.get() == "gravity pulling in -Z direction":
        gravityVector = np.array([0, 0, 9.81])
    elif verticalOrHorizontal.get() == "gravity pulling in -X direction":
        gravityVector = np.array([9.81, 0, 0])
    elif verticalOrHorizontal.get() == "gravity pulling in -Y direction":
        gravityVector = np.array([0, 9.81, 0]) 
    accelResult["text"] = f"Base Accel(m/s^2): {accelVector}"
    ownAccelResult["text"] = f"actuator accel(m/s^2): {ownAccel}"

def updateLoadListBox():
    displayLoadList = []
    for load in loadList:
        displayLoadList.append(load.toString())
    loadListBox.delete(0, tk.END)
    loadListBox.insert(0, *displayLoadList)

def deleteLoad():
    loadIndex = loadListBox.curselection()[0]
    print(loadIndex)
    loadList.pop(loadIndex)
    updateLoadListBox()



#Set up window
window = tk.Tk()
window.title("Vertical Actuator Calculator")
massEntryNoteBook = ttk.Notebook(window)
#set up entry

#mass entry
frm_entry = tk.Frame(master=massEntryNoteBook)
nameEntry = tk.Entry(master=frm_entry, width=10)
nameLabel = tk.Label(master=frm_entry, text="Name:")
massEntry = tk.Entry(master=frm_entry, width=10)
massEntry.insert(END, "0")
massLabel = tk.Label(master=frm_entry, text="Load mass (kg):")
xComEntry = tk.Entry(master=frm_entry, width=10)
xComEntry.insert(END, "0")
xComLabel = tk.Label(master=frm_entry, text="X com position (mm)")
yComEntry = tk.Entry(master=frm_entry, width=10)
yComEntry.insert(END, "0")
yComLabel = tk.Label(master=frm_entry, text="Y com position (mm)")
zComEntry = tk.Entry(master=frm_entry, width=10)
zComEntry.insert(END, "0")
zComLabel = tk.Label(master=frm_entry, text="Z com position (mm)")
nameLabel.grid(row = 0, column = 0)
nameEntry.grid(row=0, column=1)
massLabel.grid(row=1, column=0)
massEntry.grid(row=1, column=1)
xComEntry.grid(row=2, column=1)
xComLabel.grid(row=2, column=0)
yComEntry.grid(row=3, column=1)
yComLabel.grid(row=3, column=0)
zComEntry.grid(row=4, column=1)
zComLabel.grid(row=4, column=0)
btnAddMass = tk.Button(
    master=frm_entry,
    text ="Add Mass",
    command = addMass
)
btnAddMass.grid(row=5, column=1, padx=10)
frm_entry.grid(row=0, column=0, padx=10)

#accel entry
frm_accel = tk.Frame(master=massEntryNoteBook)
xAccelEntry = tk.Entry(master=frm_accel, width=10)
xAccelEntry.insert(END, "0")
xAccelLabel = tk.Label(master=frm_accel, text="X base acceleration (m/s^2)")
yAccelEntry = tk.Entry(master=frm_accel, width=10)
yAccelEntry.insert(END, "0")
yAccelLabel = tk.Label(master=frm_accel, text="Y base acceleration (m/s^2)")
zAccelEntry = tk.Entry(master=frm_accel, width=10)
zAccelEntry.insert(END, "0")
zAccelLabel = tk.Label(master=frm_accel, text="Z base acceleration (m/s^2)")
ownAccelEntry = tk.Entry(master=frm_accel, width=10)
ownAccelEntry.insert(END, "0")
ownAccelLabel = tk.Label(master=frm_accel, text="Actuator acceleration (m/s^2)")
xAccelEntry.grid(row=0, column=1)
xAccelLabel.grid(row=0, column=0)
yAccelEntry.grid(row=1, column=1)
yAccelLabel.grid(row=1, column=0)
zAccelEntry.grid(row=2, column=1)
zAccelLabel.grid(row=2, column=0)
ownAccelEntry.grid(row=3, column=1)
ownAccelLabel.grid(row=3, column=0)
frm_accel.grid(row=0, column=0, padx=10)
btnUpdateAccel = tk.Button(
    master=frm_accel,
    text ="Update Accel",
    command = updateAccel
)

#force entry
frm_entryForce = tk.Frame(master=massEntryNoteBook)
forceNameEntry = tk.Entry(master=frm_entryForce, width=10)
forceNameLabel = tk.Label(master=frm_entryForce, text="Name:")
xForceEntry = tk.Entry(master=frm_entryForce, width=10)
xForceEntry.insert(END, "0")
xForceLabel = tk.Label(master=frm_entryForce, text="X force component (N)")
yForceEntry = tk.Entry(master=frm_entryForce, width=10)
yForceEntry.insert(END, "0")
yForceLabel = tk.Label(master=frm_entryForce, text="Y force component (N)")
zForceEntry = tk.Entry(master=frm_entryForce, width=10)
zForceEntry.insert(END, "0")
zForceLabel = tk.Label(master=frm_entryForce, text="Z force component (N)")
xPosEntry = tk.Entry(master=frm_entryForce, width=10)
xPosEntry.insert(END, "0")
xPosLabel = tk.Label(master=frm_entryForce, text="X application point (mm)")
yPosEntry = tk.Entry(master=frm_entryForce, width=10)
yPosEntry.insert(END, "0")
yPosLabel = tk.Label(master=frm_entryForce, text="Y application point (mm)")
zPosEntry = tk.Entry(master=frm_entryForce, width=10)
zPosEntry.insert(END, "0")
zPosLabel = tk.Label(master=frm_entryForce, text="Z application point (mm)")
forceNameEntry.grid(row=0, column=1)
forceNameLabel.grid(row=0, column=0)
xForceEntry.grid(row=1, column=1)
xForceLabel.grid(row=1, column=0)
yForceEntry.grid(row=2, column=1)
yForceLabel.grid(row=2, column=0)
zForceEntry.grid(row=3, column=1)
zForceLabel.grid(row=3, column=0)
xPosEntry.grid(row=4, column=1)
xPosLabel.grid(row=4, column=0)
yPosEntry.grid(row=5, column=1)
yPosLabel.grid(row=5, column=0)
zPosEntry.grid(row=6, column=1)
zPosLabel.grid(row=6, column=0)
btnAddForce = tk.Button(
    master=frm_entryForce,
    text ="Add Force",
    command = addForce
)
frm_entryForce.grid(row=0, column=0, padx=10)

#form results
frm_results = tk.Frame(master=window)
accelResult =tk.Label(master=frm_results, text="Accel (m/s^2):")
ownAccelResult =tk.Label(master=frm_results, text="actuator Accel (m/s^2):")
forceResult = tk.Label(master=frm_results, text="Force (N):")
momentResult = tk.Label(master=frm_results, text="Moment (N*m):")
accelResult.grid(row=1, column=0, padx=10)
ownAccelResult.grid(row=2, column=0, padx=10)
forceResult.grid(row=3 , column=0, padx=10)
momentResult.grid(row=4, column=0, padx=10)
btnCalc = tk.Button(
    master=frm_results,
    text ="calc",
    command = updateForm
)
frm_results.grid(row=1, column=0, padx=10)

loadListBox = tk.Listbox(window, width= 75)

#set up button

btnDeleteLoad = tk.Button(
    master=window,
    text ="Delete Load",
    command = deleteLoad
)


momentForceImage = Image.open("ForcesAndMoments.JPG")
momentForceImage = momentForceImage.resize((325, 200), Image.ANTIALIAS)
momentForceImage = ImageTk.PhotoImage(momentForceImage)
momentForcePanel = Label(window, image = momentForceImage)



n = tk.StringVar()
verticalOrHorizontal =ttk.Combobox(master=frm_accel, width = 30, textvariable = n)
verticalOrHorizontal['values'] = ("gravity pulling in -Z direction", "gravity pulling in -X direction", "gravity pulling in -Y direction")
verticalOrHorizontal.grid(row=4, column = 0, columnspan=2)
verticalOrHorizontal.current(0)


#place frame in window
frm_entryForce.grid(row=2, column = 0, padx =10)
frm_accel.grid(row=0, column=3, padx=10)
btnCalc.grid(row=3, column=3, padx=10)
btnAddForce.grid(row=7, column=1, padx=10)
btnUpdateAccel.grid(row=5, column=1, padx=10)
btnDeleteLoad.grid(row=4, column=2, padx=10)

momentForcePanel.grid(row=0, column=2, padx=10)
loadListBox.grid(row=1, column=2, padx=10)

massEntryNoteBook.add(frm_entry, text = "Add mass")
massEntryNoteBook.add(frm_accel, text = "Update accel")
massEntryNoteBook.add(frm_entryForce, text = "Add Force")
massEntryNoteBook.grid(row = 0, column =0, padx = 10)
window.mainloop()
