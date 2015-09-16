from __future__ import print_function
from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

import Tkinter as tk
import ttk
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

########################################################################################################################

class MainMenu(tk.Menu):

	def __init__(self, parent, *args, **kwargs):
		tk.Menu.__init__(self)

		self.parent = parent
	
		self.menubar = tk.Menu(parent)

		self.filemenu = tk.Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="New protocol", command=self.parent.donothing)
		self.filemenu.add_command(label="Open protocol...", command=self.parent.donothing)
		self.filemenu.add_command(label="Save protocol...", command=self.parent.donothing)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=parent.quit)

		self.menubar.add_cascade(menu=self.filemenu, label="File")

		self.parent.parent.config(menu=self.menubar)
		
########################################################################################################################

class Log(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent

		self.renderLog()

		self.pack()

	def addRecord(self, text):
		self.log.insert("0.0", text)


	def renderLog(self):
		self.loglabelframe = tk.LabelFrame(self.parent, text="Log", width=800, height=200)
		self.loglabelframe.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="ns")
		self.log = tk.Text(self.loglabelframe, height="20")
		self.log.pack(padx=5, pady=5, fill="both", expand=1)

########################################################################################################################

class ControlPanel(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent

		self.labelframe = tk.LabelFrame(self.parent, text="Control Panel")
		self.labelframe.grid(row=0, column=0, padx=5, pady=5, sticky="n")

		tk.Button(self.labelframe, text="Execute Commands", command=self.parent.protocol.updateProtocol).grid(row=0, column=0, padx=5, pady=5)

		#ttk.Separator(self.labelframe, orient='vertical').pack()

		pumps = [x[0] for x in self.parent.devices]
		self.selectedpump = tk.StringVar()
		self.selectedpump.set(pumps[0])
		option = tk.OptionMenu(self.labelframe, self.selectedpump, *pumps)
		option.grid(row=0, column=1, padx=5, pady=5)
		
		tk.Button(self.labelframe, text="Reset pump", command=self.parent.protocol.resetPump).grid(row=0, column=2, padx=5, pady=5)
		tk.Button(self.labelframe, text="Add command", command=self.parent.protocol.addCommand).grid(row=0, column=3, padx=5, pady=5)

		self.pack()

########################################################################################################################

class Protocol(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent
		self.command = {}
		self.protocol = []
		self.protocol.append(self.command)

		self.renderProtocol()
		
		self.pack()


	def updateProtocol(self):
		l = ['a', 'b']
		for i in range(len(self.protocol)):
			cmd = self.protocol[i]
			cmd['name'] = l[i]
		print("Updated command list: " + str(self.protocol))


	def addCommand(self):
		print("Previous command list: "+str(self.protocol))
		self.protocol.append({})
		print("Appended command list: "+str(self.protocol))

		self.renderCommand(len(self.protocol)-1)


	def renderCommand(self, i):
		tk.Label(self.labelframe, text=str(i+1)+") ").grid(row=i, column=0)

		tk.Label(self.labelframe, text="Name: ").grid(row=i, column=1)
		commandname = tk.StringVar()
		en_name = tk.Entry(self.labelframe, textvariable=commandname)
		en_name.grid(row=i, column=2)

		tk.Label(self.labelframe, text="Pump: ").grid(row=i, column=3)
		pumps = [x[0] for x in self.parent.devices]
		#print("List of pumps: " + str(pumps))
		self.selectedpump = tk.StringVar()
		self.selectedpump.set(pumps[0])
		#self.parent.setPump(self.selectedpump.get())
		#print("Selected pump: " + str(self.selectedpump.get()))
		self.option = tk.OptionMenu(self.labelframe, self.selectedpump, *pumps)
		self.option.grid(row=i, column=4)

		tk.Label(self.labelframe, text="From Port: ").grid(row=i, column=5)
		self.sb_fromport = tk.Spinbox(self.labelframe, from_=1, to=9, width=1)
		self.sb_fromport.grid(row=i, column=6)

		tk.Label(self.labelframe, text="To Port: ").grid(row=i, column=7)
		self.sb_toport = tk.Spinbox(self.labelframe, from_=1, to=9, width=1)
		self.sb_toport.grid(row=i, column=8)

		tk.Label(self.labelframe, text="Volume(uL): ").grid(row=i, column=9)
		self.sb_volume = tk.Spinbox(self.labelframe, from_=1, to=1000, width=4)
		self.sb_volume.grid(row=i, column=10)

		tk.Label(self.labelframe, text="Speed(0-40): ").grid(row=i, column=11)
		self.sb_speed = tk.Spinbox(self.labelframe, from_=0, to=40, width=2)
		self.sb_speed.grid(row=i, column=12)

		tk.Label(self.labelframe, text="Leave for: ").grid(row=i, column=13)
		self.sb_timemin = tk.Spinbox(self.labelframe, from_=0, to=600, width=3)
		self.sb_timemin.grid(row=i, column=14)
		tk.Label(self.labelframe, text="min").grid(row=i, column=15)
		self.sb_timesec = tk.Spinbox(self.labelframe, from_=5, to=59, width=2)
		self.sb_timesec.grid(row=i, column=16) 
		tk.Label(self.labelframe, text="sec").grid(row=i, column=17)

		self.waste = tk.IntVar()
		tk.Radiobutton(self.labelframe, text="Return", variable=self.waste, value=0).grid(row=i, column=18)
		tk.Radiobutton(self.labelframe, text="Waste", variable=self.waste, value=1).grid(row=i, column=19)


	def renderProtocol(self):
		self.labelframe = tk.LabelFrame(self.parent, text="Protocol", width=1000, height=20)
		self.labelframe.grid(row=1, column=0, padx=5, pady=5, sticky="n")

		for i in range(len(self.protocol)):
			self.renderCommand(i)

	def resetPump(self):
		port = self.parent.controlpanel.selectedpump.get()
		pump = self.parent.device_dict.get(port)
		pump.init()

########################################################################################################################

class SerialPort():

	def __init__(self, parent, port, baud, timeout):
		self.parent = parent
		self.portname = port
		self.baudrate = baud
		self.timeout = timeout

		self.read = True

		self.port = Serial(self.portname, self.baudrate, timeout=self.timeout, writeTimeout=0)


	def readPort(self, bits):
		while self.read:
			cmd = self.port.read(bits)
			print("Cmd: "+cmd)
			self.parent.log.addRecord(cmd)
			if cmd == "pump":
				self.parent.executePump()

########################################################################################################################

class App(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent

		self.devices = self.getSerialPumps()
		self.device_dict = dict(self.devices)

		print("Device dict: " + str(self.device_dict))

		self.menu = MainMenu(self)
		self.protocol = Protocol(self)
		self.log = Log(self)
		self.controlpanel = ControlPanel(self)		

		#print("Selected pump: " + str(self.protocol.selectedpump.get()))

		#self.pump = self.device_dict.get(self.protocol.selectedpump.get())

		#self.serial = SerialPort(self, "/dev/ttyAMA0", 9600, 1)

		#thread = threading.Thread(target=self.serial.readPort, args=(20,))		
		#thread.start()

	def setPump(self, port):
		print("Setting pump: " + str(port))
		self.pump = self.device_dict.get(port)

	def donothing(self):
		pass


	def quit(self):
		self.parent.destroy()


	def findSerialPumps(self):
		return TecanAPISerial.findSerialPumps()


	def getSerialPumps(self):
		''' Assumes that the pumps are XCaliburD pumps and returns a list of
		(<serial port>, <instantiated XCaliburD>) tuples
		'''
		pump_list = self.findSerialPumps()
		return [(ser_port, XCaliburD(com_link=TecanAPISerial(0,ser_port, 9600))) for ser_port, _, _ in pump_list]


	def executePump(self):
		#log.delete("0.0", "end")
		#log.insert("0.0", pump.getEncoderPos())
		self.setPump(self.protocol.selectedpump.get())
		print(self.pump.getPlungerPos())
		#global pump
		toport = int(self.protocol.sb_toport.get())
		fromport = int(self.protocol.sb_fromport.get())
		volume = int(self.protocol.sb_volume.get())
		speed = int(self.protocol.sb_speed.get())
	
		timesleep = 45

		timewait = int(self.protocol.sb_timemin.get())*60+int(self.protocol.sb_timesec.get())
	
		wasteornot = self.protocol.waste.get()
		print(wasteornot)

		self.pump.setSpeed(speed)
		sleep(5)
		#pump.setMicrostep(True)
		#sleep(5)
		self.pump.extract(fromport, volume, execute=True)
		sleep(timesleep)
		self.pump.dispense(toport, volume, execute=True)	

		sleep(timesleep)

		sleep(timewait)

		self.pump.extract(toport, volume, execute=True)

		sleep(timesleep)

		if wasteornot == 0:
			print("Dump to port: "+str(fromport))
			self.pump.dispense(fromport, volume, execute=True)
		elif wasteornot == 1:
			print("Dump to port: 9")
			self.pump.dispense(9, volume, execute=True)

		sleep(timesleep)
		if self.pump.getPlungerPos() != 0:
			print("Plunger didn't end up where it was supposed to be, resetting to 0")
			self.pump.movePlungerAbs(0, execute=True)

		sleep(5)	

########################################################################################################################

#--------------------------- @30 1000uL = 88sec
#--------------------------- @31 1000uL = 102sec
#--------------------------- @32 1000uL = 122sec
#--------------------------- @33 1000uL = 152sec

if __name__ == "__main__":
	#thread = threading.Thread(target=readSerial, args=())
	#thread.start()


	root = tk.Tk()
	root.wm_title("Microscope-Pump Control")

	app = App(root)
	app.pack()
	
	#print(app.pump)

	root.mainloop()
