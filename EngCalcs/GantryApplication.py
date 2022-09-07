import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

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
        self.type = type

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
        actuatorLoad.__init__(self, name, xPosition, yPosition, zPosition, massTypeInt)
        self.xForce = xForce
        self.yForce = yForce
        self.zForce = zForce
        self.forceVector = np.array[xForce, yForce, zForce]
    def getForceVector(self, accelVector):
        return self.forceVector

    def getPosVectorMeters(self):
        comList = [self.xPos, self.yPos, self.zPos]
        comVector = np.array(comList)
        comVectorMeters = comVector / 1000
        return comVectorMeters
    
    def getMomentVector(self):
        force = self.getForceVector(accelVector)
        radius = self.getPosVectorMeters()
        moment = np.cross(radius, force)
        return moment
    def toString(self):
        retString = f"(Force load) {self.name}, mass: {self.mass}, x: {self.xPos}, y: {self.yPos}, z: {self.zPos} force{self.forceVector}"
        return retString

def updateForm():
    #print(accelVector)
    #print("")
    allDirectionAccel = np.multiply(accelVector, directionArray)
    #print(allDirectionAccel)
    allForceArray = np.zeros((8,3))
    allMomentArray = np.zeros((8,3))
    for i in range(8):
        loopForceVector = np.array([0, 0, 0])
        loopMomentVector = np.array([0, 0, 0])
        loopAccel = allDirectionAccel[i]
        for load in loadList:
            #print(loopAccel)
            loopForceVector = loopForceVector + load.getForceVector(loopAccel)
            #print(forceVector)
            loopMomentVector = loopMomentVector + load.getMomentVector(loopAccel)
            #print(momentVector)
            #print("")
        allForceArray[i] = loopForceVector
        allMomentArray[i] = loopMomentVector
    print(allForceArray)
    
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

    forceResult["text"] = f"Force: {[xForceMax, yForceMax, zForceMax ]}"
    momentResult["text"] = f"Moment: {[xMaxMoment, yMaxMoment,zMaxMoment]}"

def addMass():
    name = nameEntry.get()
    mass = float(massEntry.get())
    xCom = float(xComEntry.get())
    yCom = float(yComEntry.get())
    zCom = float(zComEntry.get())
    newMassLoad = massLoad(name, xCom, yCom, zCom, mass)
    loadList.append(newMassLoad)
    updateLoadListBox()

def updateAccel():
    xAccel = float(xAccelEntry.get())
    yAccel = float(yAccelEntry.get())
    zAccel = float(zAccelEntry.get())
    accelList = [xAccel, yAccel, zAccel]
    global accelVector 
    accelVector= np.array(accelList)
    
    accelResult["text"] = f"Accel: {accelVector}"

def updateLoadListBox():
    displayLoadList = []
    for load in loadList:
        displayLoadList.append(load.toString())
    loadListBox.delete(0, tk.END)
    loadListBox.insert(0, *displayLoadList)

#Set up window
window = tk.Tk()
window.title("Vertical Actuator Calculator")

#set up entry
frm_entry = tk.Frame(master=window)
frm_entryForce = tk.Frame(master=window)
frm_accel = tk.Frame(master=window)
frm_results = tk.Frame(master=window)

nameEntry = tk.Entry(master=frm_entry, width=10)
nameLabel = tk.Label(master=frm_entry, text="Name:")
massEntry = tk.Entry(master=frm_entry, width=10)
massLabel = tk.Label(master=frm_entry, text="Load mass (kg):")
xComEntry = tk.Entry(master=frm_entry, width=10)
xComLabel = tk.Label(master=frm_entry, text="X com position (mm)")
yComEntry = tk.Entry(master=frm_entry, width=10)
yComLabel = tk.Label(master=frm_entry, text="Y com position (mm)")
zComEntry = tk.Entry(master=frm_entry, width=10)
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

xAccelEntry = tk.Entry(master=frm_accel, width=10)
xAccelLabel = tk.Label(master=frm_accel, text="X acceleration (m/s^2)")
yAccelEntry = tk.Entry(master=frm_accel, width=10)
yAccelLabel = tk.Label(master=frm_accel, text="Y acceleration (m/s^2)")
zAccelEntry = tk.Entry(master=frm_accel, width=10)
zAccelLabel = tk.Label(master=frm_accel, text="Z acceleration (m/s^2)")
xAccelEntry.grid(row=0, column=1)
xAccelLabel.grid(row=0, column=0)
yAccelEntry.grid(row=1, column=1)
yAccelLabel.grid(row=1, column=0)
zAccelEntry.grid(row=2, column=1)
zAccelLabel.grid(row=2, column=0)

forceNameEntry = tk.Entry(master=frm_entryForce, width=10)
forceNameLabel = tk.Label(master=frm_entryForce, text="Name:")
xForceEntry = tk.Entry(master=frm_entryForce, width=10)
xForceLabel = tk.Label(master=frm_entryForce, text="X force component (mm)")
yForceEntry = tk.Entry(master=frm_entryForce, width=10)
yForceLabel = tk.Label(master=frm_entryForce, text="Y force component (mm)")
zForceEntry = tk.Entry(master=frm_entryForce, width=10)
zForceLabel = tk.Label(master=frm_entryForce, text="Z force component (mm)")
xPosEntry = tk.Entry(master=frm_entryForce, width=10)
xPosLabel = tk.Label(master=frm_entryForce, text="X application point (mm)")
yPosEntry = tk.Entry(master=frm_entryForce, width=10)
yPosLabel = tk.Label(master=frm_entryForce, text="Y application point (mm)")
zPosEntry = tk.Entry(master=frm_entryForce, width=10)
zPosLabel = tk.Label(master=frm_entryForce, text="Z application point (mm)")
forceNameEntry.grid(row=0, column=1)
forceNameLabel.grid(row=0, column=0)
xForceEntry.grid(row=1, column=1)
xForceLabel.grid(row=1, column=0)

#place components in frame




loadListBox = tk.Listbox(window, width= 50)

#set up button
btnCalc = tk.Button(
    master=window,
    text ="calc",
    command = updateForm
)

btnAddMass = tk.Button(
    master=frm_entry,
    text ="Add Mass",
    command = addMass
)

btnUpdateAccel = tk.Button(
    master=frm_accel,
    text ="Update Accel",
    command = updateAccel
)

accelResult =tk.Label(master=frm_results, text="Accel (m/s^2):")
forceResult = tk.Label(master=frm_results, text="Force (N):")
momentResult = tk.Label(master=frm_results, text="Moment (N*m):")
accelResult.grid(row=0, column=0, padx=10)
forceResult.grid(row=1 , column=0, padx=10)
momentResult.grid(row=2, column=0, padx=10)

#place frame in window
frm_entry.grid(row=0, column=0, padx=10)
frm_entryForce.grid(row=6)
frm_accel.grid(row=0, column=3, padx=10)
btnCalc.grid(row=2, column=3, padx=10)
btnAddMass.grid(row=5, column=1, padx=10)
btnUpdateAccel.grid(row=3, column=1, padx=10)

loadListBox.grid(row=0, column=2, padx=10)
frm_results.grid(row=1, column=3, padx=10)
window.mainloop()