from __future__ import print_function
from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

from Tkinter import *
from serial import Serial
from time import sleep, time
import threading

try:
    from tecancavrotest.models import XCaliburD
    from tecancavrotest.transport import TecanAPISerial, TecanAPINode
except ImportError:  # Support direct import from package
    import sys
    import os
    dirn = os.path.dirname
    LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(dirn(dirn(LOCAL_DIR)))
    from tecancavrotest.models import XCaliburD
    from tecancavrotest.transport import TecanAPISerial, TecanAPINode

def findSerialPumps():
    return TecanAPISerial.findSerialPumps()


def getSerialPumps():
    ''' Assumes that the pumps are XCaliburD pumps and returns a list of
    (<serial port>, <instantiated XCaliburD>) tuples
    '''
    pump_list = findSerialPumps()
    return [(ser_port, XCaliburD(com_link=TecanAPISerial(0,
             ser_port, 9600))) for ser_port, _, _ in pump_list]

devices = getSerialPumps()
device_dict = dict(devices)

pump = device_dict.get("/dev/ttyUSB0")

readserial = True

def donothing():
	pass

def exit():
#	thread.stop()
	readserial = False
	root.destroy()
	root.quit()

root = Tk()
root.wm_title("Pump Control - Test")

frame1 = Frame(root)
frame1.pack()

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New protocol", command=donothing)
filemenu.add_command(label="Open protocol...", command=donothing)
filemenu.add_command(label="Save protocol...", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit)

menubar.add_cascade(menu=filemenu, label="File")

#def exit():
	#thread.stop()
	#root.exit()

root.config(menu=menubar)

port ="/dev/ttyAMA0"
baudrate = 9600
timeout = 1
ser = Serial(port, baudrate, timeout=timeout, writeTimeout=0)

protocollabelframe = LabelFrame(frame1, text="Protocol", width=1000, height=400)
protocollabelframe.grid(row=0, column=0, padx=5, pady=5)

#--------------Protocol Command Form
Label(protocollabelframe, text="From Port:").grid(row=0, column=0)
sb_fromport = Spinbox(protocollabelframe, from_=1, to=9, width=1)
sb_fromport.grid(row=0, column=1)

Label(protocollabelframe, text="To Port:").grid(row=0, column=2)
sb_toport = Spinbox(protocollabelframe, from_=1, to=9, width=1)
sb_toport.grid(row=0, column=3)

Label(protocollabelframe, text="Volume(uL):").grid(row=0, column=4)
sb_volume = Spinbox(protocollabelframe, from_=1, to=1000, width=4)
sb_volume.grid(row=0, column=5)

Label(protocollabelframe, text="Speed(0-40):").grid(row=0, column=6)
sb_speed = Spinbox(protocollabelframe, from_=0, to=40, width=2)
sb_speed.grid(row=0, column=7)

Label(protocollabelframe, text="Leave for:").grid(row=0, column=8)
sb_timemin = Spinbox(protocollabelframe, from_=0, to=600, width=3)
sb_timemin.grid(row=0, column=9)
Label(protocollabelframe, text="min").grid(row=0, column=10)
sb_timesec = Spinbox(protocollabelframe, from_=5, to=59, width=2)
sb_timesec.grid(row=0, column=11)
Label(protocollabelframe, text="sec").grid(row=0, column=12)

waste = IntVar()
Radiobutton(protocollabelframe, text="Return", variable=waste, value=0).grid(row=0, column=13)
Radiobutton(protocollabelframe, text="Waste", variable=waste, value=1).grid(row=0, column=14)
#-----------------------End

def executePump():
	log.delete("0.0", "end")
	#log.insert("0.0", pump.getEncoderPos())
	print(pump.getPlungerPos())
	#global pump
	toport = int(sb_toport.get())
	fromport = int(sb_fromport.get())
	volume = int(sb_volume.get())
	speed = int(sb_speed.get())
	
	timesleep = 45

	timewait = int(sb_timemin.get())*60+int(sb_timesec.get())
	
	wasteornot = waste.get()
	print(wasteornot)

	pump.setSpeed(speed)
	sleep(5)
	#pump.setMicrostep(True)
	#sleep(5)
	pump.extract(fromport, volume, execute=True)
	sleep(timesleep)
	pump.dispense(toport, volume, execute=True)

	sleep(timesleep)

	sleep(timewait)

	pump.extract(toport, volume, execute=True)

	sleep(timesleep)

	if wasteornot == 0:
		print("Dump to port: "+str(fromport))
		pump.dispense(fromport, volume, execute=True)
	elif wasteornot == 1:
		print("Dump to port: 9")
		pump.dispense(9, volume, execute=True)

	sleep(timesleep)
	if pump.getPlungerPos() != 0:
		print("Plunger didn't end up where it was supposed to be, resetting to 0")
		pump.movePlungerAbs(0, execute=True)

	sleep(5)	

def resetPump():
	pump.init()
	print(pump.getPlungerPos())

Button(protocollabelframe, text="Pump", command=executePump).grid(row=0, column=15)

Button(protocollabelframe, text="Reset pump", command=resetPump).grid(row=0, column=16)

loglabelframe = LabelFrame(frame1, text="Log", width=800, height=200)
loglabelframe.grid(row=1, column=0, padx=5, pady=5)

log = Text(loglabelframe, height=10)
log.pack(padx=5, pady=5)


def readSerial():
	while readserial:
		command = ser.read(20)
		print(command)

		if command == "pump":
			executePump()


#thread = threading.Thread(target=readSerial, args=())
#thread.start()

print(device_dict.get("/dev/ttyUSB0"))

#pump.setSpeed(33)
#sleep(5)
#timestart = time()
#timepump = pump.extractToWaste(1, 1000)
#timestop = time()

#--------------------------- @30 1000uL = 88sec
#--------------------------- @31 1000uL = 102sec
#--------------------------- @32 1000uL = 122sec
#--------------------------- @33 1000uL = 152sec

#print(timepump)

#pump.init()

#print("It took %s seconds for 1000uL at speed 30" %(timestop-timestart))

#pump.dispense(execute=True)
#pump.changePort(2, execute=True)
#sleep(5)
#pump.movePlungerAbs(2000, execute=True)

#pump.init()
#pump.dispenseToWaste(execute=True)
#pump.movePlungerRel(-400, execute=True)
#print(pump.getPlungerPos())




root.mainloop()
