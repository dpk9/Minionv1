from __future__ import print_function
from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

import Tkinter
import serial
import time

#from IPython.html import widgets
#from IPython.display import display, clear_output, HTML

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
# devices = [('/dev/tty0', '')]
device_dict = dict(devices)

#valve_control = widgets.Dropdown(options=[str(x) for x in range(1,10)])
#port_control = widgets.Dropdown(options=[x[0] for x in devices])
#pull_volume_control = widgets.BoundedIntText(min=0, max=1000, value=0)
#push_volume_control = widgets.BoundedIntText(min=0, max=1000, value=0)
#notification_area = widgets.HTML("")

def update_notification(val):
    notification_area.value = val

def call_button(button, f):
    button.disabled = True

    button.disabled = False

#pull_button = widgets.Button(description="Extract")
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

#pull_button.on_click(extract)
#pull_button.disabled = False

#push_button = widgets.Button(description="Dispense")
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

#findSerialPumps()

root = Tkinter.Tk()
root.wm_title("Microscope-pump GUI test")

#log = Tkinter.Text(root, width=23, height=1, takefocus=0)
#log.grid(row=0, column=1)

#Tkinter.Label(root, text="Command:").grid(row=0, column=0)

port ="/dev/ttyUSB0"
rate = 9600
timeout = 1
ser = serial.Serial(port, rate, timeout=timeout, writeTimeout=0)

pump = device_dict.get("/dev/ttyUSB0")

frame1 = Tkinter.Frame(root)
frame1.pack()


protocollabelframe = Tkinter.LabelFrame(frame1, text="Protocol", width=800, height=400)
protocollabelframe.grid(row=0, column=0, padx=5, pady=5)

#protocolframe = Tkinter.Frame(protocollabelframe)
#protocolframe.pack()

Tkinter.Label(protocollabelframe, text="Add").grid(row=0, column=0)
Tkinter.Entry(protocollabelframe, width=2).grid(row=0, column=1)
Tkinter.Label(protocollabelframe, text="fields").grid(row=0, column=2)
Tkinter.Button(protocollabelframe, text="Add").grid(row=0, column=3)

loglabelframe = Tkinter.LabelFrame(frame1, text="Log", width=800, height=200)
loglabelframe.grid(row=1, column=0, padx=5, pady=5)

Tkinter.Text(loglabelframe).pack(padx=5, pady=5)

#Tkinter.Label(frame1, text="Hello").pack()

root.mainloop()

def readSerial():
	while True:
		global pump
		cmd = ser.read(20)
		#cmd.split()
		#print(cmd)
		if len(cmd) == 0:
			break
		else:
			log.delete("0.0", "end")
			log.insert("end", cmd)
			if cmd == "dispense":
				pump.dispense(1, 200, execute=True)
			elif cmd == "extract":
				pump.extract(1, 200, execute=True)
	root.after(10, readSerial)

#root.after(100, readSerial)
#pump.setStartSpeed(200, execute=True)
#pump.setSpeed(4)
#pump.dispense(1, 900, execute=True)

#root.mainloop()

#pump = device_dict.get("/dev/ttyUSB0")

#pump.extract(2, 100, execute=True)
#time.sleep(6)
#pump.dispense(5, 600, execute=True)

#device_dict["/dev/ttyUSB0"].extractToWaste(2, 800, flush=True)
#device_dict["/dev/ttyUSB0"].init()
#device_dict["/dev/ttyUSB0"].dispenseToWaste()
#device_dict["/dev/ttyUSB0"].movePlungerAbs(800)

#pump = getSerialPumps()[0]

#print(pump)























#push_button.on_click(dispense)
#push_button.disabled = False


#hbox0 = widgets.HBox()
#sp_label = widgets.HTML("Serial Port: ")
#sp_label.width = 100
#hbox0.children = [sp_label, port_control]


#hbox1 = widgets.HBox()
#valve_label = widgets.HTML("Valve: ")
#valve_label.width = 100
#hbox1.children = [valve_label, valve_control]

#hbox2 = widgets.HBox()
#pull_button.width = 100
#hbox2.children = [pull_button, pull_volume_control]

#hbox3 = widgets.HBox()
#push_button.width = 100
#hbox3.children = [push_button, push_volume_control]

#hbox4 = widgets.HBox()
#notification_label = widgets.HTML("Notifications: ")
#notification_label.width = 100
#hbox4.children = [notification_label, notification_area]
#notification_area.width = 600

#vbox = widgets.VBox()
#vbox.width = 600
#vbox.children = [hbox0, hbox1, hbox2, hbox3, hbox4]

#display(vbox)

# checkout 
# https://github.com/ipython/ipython/blob/master/IPython/html/widgets/interaction.py
# if you want to create your own interaction situation
