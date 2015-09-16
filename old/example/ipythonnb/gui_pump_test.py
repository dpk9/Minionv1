from __future__ import print_function
from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

import Tkinter
import serial
import time

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

def update_notification(val):
    notification_area.value = val

def call_button(button, f):
    button.disabled = True

    button.disabled = False

def extract(arg):
    global device_dict
    push_button.disabled = True
    serial_port = port_control.value
    valve = int(valve_control.value)
    volume = pull_volume_control.value
    update_notification("Received extract for: %d ul from port %d on serial port %s" % (volume,
          valve, serial_port))
    if len(sp) > 0:
        device_dict[serial_port].extract(valve, volume)
    pull_button.disabled = False

def dispense(arg):
    global device_dict
    push_button.disabled = True
    serial_port = port_control.value
    valve = int(valve_control.value)
    volume = push_volume_control.value
    update_notification("Received dispense for: %d ul from port %d on serial port %s" % (volume,
          valve, serial_port))
    if len(sp) > 0:
        device_dict[serial_port].dispense(valve, volume)
    push_button.disabled = False


root = Tkinter.Tk()

root.wm_title("Pump Control - Test")


port ="/dev/ttyAMA0"
rate = 9600
timeout = 1
ser = serial.Serial(port, rate, timeout=timeout, writeTimeout=0)

pump = device_dict.get("/dev/ttyUSB0")

frame1 = Tkinter.Frame(root)
frame1.pack()	


protocollabelframe = Tkinter.LabelFrame(frame1, text="Protocol", width=1000, height=400)
protocollabelframe.grid(row=0, column=0, padx=5, pady=5)

Tkinter.Label(protocollabelframe, text="From Port:").grid(row=0, column=0)
sb_fromport = Tkinter.Spinbox(protocollabelframe, from_=1, to=9, width=1)
sb_fromport.grid(row=0, column=1)

Tkinter.Label(protocollabelframe, text="To Port:").grid(row=0, column=2)
sb_toport = Tkinter.Spinbox(protocollabelframe, from_=1, to=9, width=1)
sb_toport.grid(row=0, column=3)

Tkinter.Label(protocollabelframe, text="Volume(uL):").grid(row=0, column=4)
sb_volume = Tkinter.Spinbox(protocollabelframe, from_=1, to=1000, width=4)
sb_volume.grid(row=0, column=5)

Tkinter.Label(protocollabelframe, text="Speed(0-40):").grid(row=0, column=6)
sb_speed = Tkinter.Spinbox(protocollabelframe, from_=0, to=40, width=2)
sb_speed.grid(row=0, column=7)

Tkinter.Label(protocollabelframe, text="Leave for:").grid(row=0, column=8)
sb_timemin = Tkinter.Spinbox(protocollabelframe, from_=0, to=600, width=3)
sb_timemin.grid(row=0, column=9)
Tkinter.Label(protocollabelframe, text="min").grid(row=0, column=10)
sb_timesec = Tkinter.Spinbox(protocollabelframe, from_=0, to=59, width=2)
sb_timesec.grid(row=0, column=11)
Tkinter.Label(protocollabelframe, text="sec").grid(row=0, column=12)

waste = Tkinter.IntVar()
Tkinter.Radiobutton(protocollabelframe, text="Return", variable=waste, value=0).grid(row=0, column=13)
Tkinter.Radiobutton(protocollabelframe, text="Waste", variable=waste, value=1).grid(row=0, column=14)

def executePump():
	log.delete("0.0", "end")
	log.insert("0.0", sb_volume.get())
	
	#global pump
	toport = int(sb_toport.get())
	fromport = int(sb_fromport.get())
	volume = int(sb_volume.get())
	speed = int(sb_speed.get())
	
	timesleep = 5

	timewait = int(sb_timemin.get())*60+int(sb_timesec.get())
	
	wasteornot = waste.get()
	print(wasteornot)

	pump.setSpeed(speed)
	pump.extract(fromport, volume, execute=True)
	time.sleep(timesleep)
	pump.dispense(toport, volume, execute=True)

	time.sleep(timewait)

	pump.extract(toport, volume, execute=True)
	time.sleep(timesleep)

	if wasteornot == 0:
		print("Dump to port: "+str(fromport))
		pump.dispense(fromport, volume, execute=True)
	elif wasteornot == 1:
		print("Dump to port: 9")
		pump.dispense(9, volume, execute=True)
	time.sleep(timesleep)	

def resetPump():
	pump.init()

Tkinter.Button(protocollabelframe, text="Pump", command=executePump).grid(row=0, column=15)

Tkinter.Button(protocollabelframe, text="Reset pump", command=resetPump).grid(row=0, column=16)

loglabelframe = Tkinter.LabelFrame(frame1, text="Log", width=800, height=200)
loglabelframe.grid(row=1, column=0, padx=5, pady=5)

log = Tkinter.Text(loglabelframe)
log.pack(padx=5, pady=5)


def readSerial():
	while True:
		command = ser.read(20)
		print(command)
		if len(command) == 0:
			break
		else:
			#log.delete("0.0", "end")
			#log.insert("end", cmd)
			#print("j: "+command)
			if command == "dispense":
				pump.dispense(1, 200, execute=True)
			elif command == "extract":
				pump.extract(1, 200, execute=True)
			elif command == "pump":
				executePump()

	root.after(10, readSerial)


#root.after(300, readSerial)
print(device_dict.get("/dev/ttyUSB0"))
root.mainloop()






# checkout 
# https://github.com/ipython/ipython/blob/master/IPython/html/widgets/interaction.py
# if you want to create your own interaction situation
