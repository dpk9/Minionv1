from __future__ import print_function
from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

import Tkinter as tk
import ttk

try:
	import cPickle as pickle 
except:
	import pickle

import threading, tkFileDialog
from serial import Serial
from time import sleep, time, strftime
from math import pi

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
#		self.filemenu.add_command(label="New protocol", command=self.parent.protocol.newProtocol)
		self.filemenu.add_command(label="Open protocol...", command=self.parent.protocol.loadProtocol)
		self.filemenu.add_command(label="Save protocol...", command=self.parent.protocol.saveProtocol)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.parent.quit)

		self.menubar.add_cascade(menu=self.filemenu, label="File")

		self.parent.parent.config(menu=self.menubar)
		
########################################################################################################################

class Log(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent

		self.loglabelframe = tk.LabelFrame(self.parent, text="Log")
		self.loglabelframe.grid(row=2, column=1, padx=5, pady=5, sticky="ns")

		self.renderLog()

		self.pack()


	def addRecord(self, text):
		self.log.configure(state="normal")
		formattedtext = self.format(text)+"\n"
		self.log.insert("end", formattedtext)
		self.log.configure(state="disabled")
		self.log.see("end")


	def format(self, text):
		formattedtime = strftime('%d %b %H:%M:%S')
		formattedtext = str(formattedtime)+" - "+text
		
		return formattedtext


	def renderLog(self):
		self.log = tk.Text(self.loglabelframe, height="20", width="150")
		self.log.pack(padx=5, pady=5, fill="both", expand=1)
		self.log.configure(state="disabled")

########################################################################################################################

class ControlPanel(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent

		self.primingll = tk.LabelFrame(self.parent, text=" Port Priming ")
		self.primingll.grid(row=0, column=0, padx=5, pady=5, sticky="n")

		self.cmdll = tk.LabelFrame(self.parent, text=" Control Panel ")
		self.cmdll.grid(row=0, column=2, padx=5, pady=5, sticky="n")

		self.renderCP()

		self.pack()


	def renderCP(self):
#		tk.Label(self.primingll, text="Ports").grid(row=0, column=0)
#		tk.Label(self.primingll, text="I.D.(in)").grid(row=0, column=1)
#		tk.Label(self.primingll, text="Length(in)").grid(row=0, column=2)

		self.portstoprime = []
		self.tubingtypes = []
#		self.lengths = []

		for i in range(1, 10):
			port = tk.DoubleVar()
			tk.Checkbutton(self.primingll, text="Port "+str(i), variable=port).grid(row=i, column=0)
			self.portstoprime.append(port)

			tubingtype = tk.IntVar()
			tk.Radiobutton(self.primingll, text="PEEK", variable=tubingtype, value=1).grid(row=i, column=1)
			tk.Radiobutton(self.primingll, text="non-PEEK", variable=tubingtype, value=2).grid(row=i, column=2)
			self.tubingtypes.append(tubingtype)

#			length = tk.DoubleVar()
#			tk.Entry(self.primingll, width=4, textvariable=length).grid(row=i, column=2)
#			self.lengths.append(length)

		tk.Button(self.primingll, text="Prime Ports", command=lambda: self.parent.protocol.primePorts(self.portstoprime, self.tubingtypes)).grid(row=len(self.portstoprime)+1, column=0, columnspan=3, padx=5, pady=5)


		tk.Button(self.cmdll, text="Execute Cycle", command=self.parent.protocol.executeCycle, width=12).grid(row=0, column=0, padx=5, pady=5)

#		ttk.Separator(self.cmdll, orient='vertical').pack()

		pumps = [x[0] for x in self.parent.devices]
		self.selectedpump = tk.StringVar()
		self.selectedpump.set(pumps[0])
		option = tk.OptionMenu(self.cmdll, self.selectedpump, *pumps)
		option.grid(row=3, column=0, padx=5, pady=5)
		
		tk.Button(self.cmdll, text="Reset Pump", command=self.parent.protocol.resetPump, width=12).grid(row=4, column=0, padx=5, pady=5)
		tk.Button(self.cmdll, text="Add Command", command=self.parent.protocol.addCommand, width=12).grid(row=2, column=0, padx=5, pady=5)
		tk.Button(self.cmdll, text="Update Protocol", command=self.parent.protocol.updateProtocol, width=12).grid(row=1, column=0, padx=5, pady=5)

########################################################################################################################

class Protocol(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent
#		self.command = {}
		self.protocol = []
#		self.protocol.append({})

		self.cmdnumbers = []
		self.cycles = []
		self.names = []
		self.pumpports = []
		self.fromports = []
		self.toports = []
		self.volumes = []
		self.speeds = []
		self.waitmins = []
		self.waitsecs = []
		self.wasteornots = []
		self.statuses = []

		self.cyclecounter = 0
		self.cmdcounter = 0

		self.labelframe = tk.LabelFrame(self.parent, text=" Protocol ", width=1000, height=20)
		self.labelframe.grid(row=0, column=1, padx=5, pady=5, sticky="n")

		self.renderProtocol()
		
		self.pack()


	def updateProtocol(self):
		for i in range(len(self.protocol)):
			self.protocol[i] = {
						'cmdnumber': int(self.cmdnumbers[i]),
						'cycle': int(self.cycles[i].get()),
						'name': self.names[i].get(),
						'pump': self.pumpports[i].get(),
						'fromport': int(self.fromports[i].get()),
						'toport': int(self.toports[i].get()),
						'volume': int(self.volumes[i].get()),
						'speed': int(self.speeds[i].get()),
						'waitmins': int(self.waitmins[i].get()),
						'waitsecs': int(self.waitsecs[i].get()),
						'waste': int(self.wasteornots[i].get()),
						
						}
		print("Updated command list: " + str(self.protocol))


	def newProtocol(self):
		self.protocol = []
		self.cmdcounter = 0
		self.cyclecounter = 0

		self.cmdnumbers = []
		self.cycles = []
		self.names = []
		self.pumpports = []
		self.fromports = []
		self.toports = []
		self.volumes = []
		self.speeds = []
		self.waitmins = []
		self.waitsecs = []
		self.wasteornots = []
		self.statuses = []

		self.renderProtocol()

	def saveProtocol(self):
		self.updateProtocol()
		filename = tkFileDialog.asksaveasfilename(defaultextension='.pkl')
		if filename is None:
			return
		file = open(filename, 'wb')
		pickle.dump(self.protocol, file)
		file.close()


	def loadProtocol(self):
		filename = tkFileDialog.askopenfilename(filetypes=[('Pickled protocols', '*.pkl')])
		if filename is None:
			return
		file = open(filename, 'rb')
		protocol = pickle.load(file)
		file.close()
		print("Loaded protocol: " + str(protocol))
		self.protocol = protocol
		print("Native protocol: " + str(self.protocol))
		self.renderProtocol()
		#self.insertFieldValues()

	def addCommand(self):
		print("Previous command list: "+str(self.protocol))
		self.protocol.append({})
		print("Appended command list: "+str(self.protocol))

		self.renderCommand(len(self.protocol)-1)


	def insertFieldValues(self):
		for i in range(len(self.protocol)):
			if self.protocol[i].get('cycle') is not None:	
				self.cycles[i]['value'] = self.protocol[i].get('cycle')
				#self.sb_cycle['value'] = self.protocol[i].get('cycle')
			

	def renderCommand(self, i):
		tk.Label(self.labelframe, text=str(i+1)+") ").grid(row=i, column=0)

		self.cmdnumbers.append(i)

		tk.Label(self.labelframe, text="Cycle: ").grid(row=i, column=1)
		sb_cycle = tk.Spinbox(self.labelframe, from_=0, to=99, width=2)
		sb_cycle.grid(row=i, column=2)

		self.cycles.append(sb_cycle)

		if self.protocol[i].get('cycle') is not None:
			sb_cycle['value'] = self.protocol[i].get('cycle') 

		tk.Label(self.labelframe, text="Name: ").grid(row=i, column=3)
		commandname = tk.StringVar()
		en_name = tk.Entry(self.labelframe, textvariable=commandname)
		en_name.grid(row=i, column=4)

		self.names.append(commandname)

		if self.protocol[i].get('name') is not None:
			self.names[i].set(self.protocol[i].get('name'))

		tk.Label(self.labelframe, text="Pump: ").grid(row=i, column=5)
		pumps = [x[0] for x in self.parent.devices]
		#print("List of pumps: " + str(pumps))
		selectedpump = tk.StringVar()
		selectedpump.set(pumps[0])
		#self.parent.setPump(self.selectedpump.get())
		#print("Selected pump: " + str(self.selectedpump.get()))
		option = tk.OptionMenu(self.labelframe, selectedpump, *pumps)
		option.grid(row=i, column=6)

		self.pumpports.append(selectedpump)

		if self.protocol[i].get('pump') is not None:
			self.pumpports[i].set(self.protocol[i].get('pump'))

		tk.Label(self.labelframe, text="From Port: ").grid(row=i, column=7)
		sb_fromport = tk.Spinbox(self.labelframe, from_=1, to=9, width=1)
		sb_fromport.grid(row=i, column=8)

		self.fromports.append(sb_fromport)

		if self.protocol[i].get('fromport') is not None:
			self.fromports[i]['value'] = self.protocol[i].get('fromport')

		tk.Label(self.labelframe, text="To Port: ").grid(row=i, column=9)
		sb_toport = tk.Spinbox(self.labelframe, from_=1, to=9, width=1)
		sb_toport.grid(row=i, column=10)

		self.toports.append(sb_toport)

		if self.protocol[i].get('toport') is not None:
			self.toports[i]['value'] = self.protocol[i].get('toport')

		tk.Label(self.labelframe, text="Volume(uL): ").grid(row=i, column=11)
		sb_volume = tk.Spinbox(self.labelframe, from_=1, to=1000, width=4)
		sb_volume.grid(row=i, column=12)

		self.volumes.append(sb_volume)

		if self.protocol[i].get('volume') is not None:
			self.volumes[i]['value'] = self.protocol[i].get('volume')

		tk.Label(self.labelframe, text="Speed(0-40): ").grid(row=i, column=13)
		sb_speed = tk.Spinbox(self.labelframe, from_=0, to=40, width=2)
		sb_speed.grid(row=i, column=14)

		self.speeds.append(sb_speed)

		if self.protocol[i].get('speed') is not None:
			self.speeds[i]['value'] = self.protocol[i].get('speed')

		tk.Label(self.labelframe, text="Leave for: ").grid(row=i, column=15)
		sb_timemin = tk.Spinbox(self.labelframe, from_=0, to=600, width=3)
		sb_timemin.grid(row=i, column=16)
		tk.Label(self.labelframe, text="min").grid(row=i, column=17)
		sb_timesec = tk.Spinbox(self.labelframe, from_=5, to=59, width=2)
		sb_timesec.grid(row=i, column=18) 
		tk.Label(self.labelframe, text="sec").grid(row=i, column=19)

		self.waitmins.append(sb_timemin)
		self.waitsecs.append(sb_timesec)

		if self.protocol[i].get('waitmins') is not None:
			self.waitmins[i]['value'] = self.protocol[i].get('waitmins')
		if self.protocol[i].get('waitsecs') is not None:
			self.waitsecs[i]['value'] = self.protocol[i].get('waitsecs')

		waste = tk.IntVar()
		tk.Radiobutton(self.labelframe, text="Return", variable=waste, value=0).grid(row=i, column=20)
		tk.Radiobutton(self.labelframe, text="Waste", variable=waste, value=1).grid(row=i, column=21)

		self.wasteornots.append(waste)

		if self.protocol[i].get('waste') is not None:
			self.wasteornots[i].set(self.protocol[i].get('waste'))

		tk.Label(self.labelframe, text="  -  ").grid(row=i, column=22)
		status = tk.Label(self.labelframe, text="Not complete")
		status.grid(row=i, column=23)

		self.statuses.append(status)


	def renderProtocol(self):
		for i in range(len(self.protocol)):
			self.renderCommand(i)


	def primePorts(self, portstoprime, tubingtypes):
#		self.updateProtocol()

		pump = self.parent.device_dict.get('/dev/ttyUSB0')

		for i in range(len(portstoprime)):
			speed = 0
			if portstoprime[i].get() == 1:
				if tubingtypes[i].get() == 1:
					speed = 28
				elif tubingtypes[i].get() == 2:
					speed = 14
				volume = 500
				port = i+1

				print("Port "+str(port)+": "+str(volume)+"uL at speed: "+str(speed))

				pump.primePort(port, volume, speed, port)

				waittime = 1
				sleep(waittime)


	def executeCycle(self):
		self.updateProtocol()

		for cmd in self.protocol:
			
			if cmd['cycle'] == self.cyclecounter:
				self.parent.log.addRecord("Beginning cycle: " + str(self.cyclecounter))
				print("Found cmd with appropriate cycle")
				self.executeCommand(self.cmdcounter)
				self.cmdcounter += 1
		
		self.cyclecounter += 1


	def executeCommand(self, index):
		self.updateProtocol()
		
		i = index

		status = self.statuses[i]
		status.config(bg="yellow")
		status['text'] = 'Processing'

		pump = self.parent.device_dict.get(self.protocol[i].get('pump'))

		name = str(self.protocol[i].get('name'))
		toport = int(self.protocol[i].get('toport'))
		fromport = int(self.protocol[i].get('fromport'))
		volume = int(self.protocol[i].get('volume'))
		speed = int(self.protocol[i].get('speed'))
		waitmins = int(self.protocol[i].get('waitmins'))
		waitsecs = int(self.protocol[i].get('waitsecs'))

		timebuffer = 6

		timewait = waitmins*60 + waitsecs

		waste = int(self.protocol[i].get('waste'))

		self.parent.log.addRecord("Starting command: " + name)
		self.parent.log.addRecord("Selected pump for this command is: " + str(pump))		
		self.parent.log.addRecord("Setting pump speed code: " + str(speed))
		pump.setSpeed(speed)
		sleep(timebuffer)
		
		self.parent.log.addRecord("Extracting " + str(volume) + "uL from port " + str(fromport))
		esttime = pump.extract(fromport, volume, execute=True)
		self.parent.log.addRecord("Estimated time: " + str(esttime) + "sec")
		sleep(esttime+timebuffer)

		self.parent.log.addRecord("Dispensing " + str(volume) + "uL to port " + str(toport))
		esttime = pump.dispense(toport, volume, execute=True)
		sleep(esttime+timebuffer)

		self.parent.log.addRecord("Waiting for " + str(waitmins) + "min " + str(waitsecs) + "sec before extraction")
		sleep(timewait)

		self.parent.log.addRecord("Extracting " + str(volume) + "uL from port " + str(toport))
		esttime = pump.extract(toport, volume, execute=True)
		sleep(esttime+timebuffer)
		if waste == 0:
			self.parent.log.addRecord("Dispensing " + str(volume) + "uL back to port " + str(fromport))
			settime = pump.dispense(fromport, volume, execute=True)
			sleep(esttime+timebuffer)
		elif waste == 1:
			self.parent.log.addRecord("Dispensing " + str(volume) + "uL to waste port 9")
			esttime = pump.dispense(9, volume, execute=True)
			sleep(esttime+timebuffer)

		self.parent.log.addRecord("Command '" + name + "' is finished \n")

		status['text'] = 'Complete'
		status.config(bg='green')


		#if (self.cmdcounter+1) == len(self.protocol):
		#	print("Resetting cmdcounter to 0")
		#	self.cmdcounter = 0
		#	self.resetStatuses()
		#else:
		#	print("Incrementing cmdcounter")
		#	self.cmdcounter += 1


	def resetStatuses(self):
		for i in range(len(self.protocol)):
			status = self.statuses[i]
			status['text'] = 'Not complete'
			status.config(fg='black')


	def resetPump(self):
		port = self.parent.controlpanel.selectedpump.get()
		pump = self.parent.device_dict.get(port)
		self.parent.log.addRecord("Resetting pump " + str(pump) + "\n")
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
			if len(cmd) > 0:
				self.parent.log.addRecord("Received serial command: " + str(cmd))
			if cmd == "pump":
				self.parent.protocol.executeCycle()

########################################################################################################################

class App(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self)

		self.parent = parent

		self.devices = self.getSerialPumps()
		self.device_dict = dict(self.devices)

		if not self.device_dict:
			print("There is no pump connected. Please connect one and try again.")
			sys.exit()

		print("Device dict: " + str(self.device_dict))

		self.note = ttk.Notebook(self)

		self.protocoltab = tk.Frame(self.note)
		self.logtab = tk.Frame(self.note)

		self.protocol = Protocol(self)
		self.log = Log(self)
		self.controlpanel = ControlPanel(self)		
		self.menu = MainMenu(self)

		self.note.add(self.protocoltab, text="Protocol")
		self.note.add(self.logtab, text="Log")

		#self.note.pack()

		self.serial = SerialPort(self, "/dev/ttyAMA0", 9600, 1)

		thread = threading.Thread(target=self.serial.readPort, args=(20,))		
		thread.start()


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

########################################################################################################################

#--------------------------- @30 1000uL = 88sec
#--------------------------- @31 1000uL = 102sec
#--------------------------- @32 1000uL = 122sec
#--------------------------- @33 1000uL = 152sec

if __name__ == "__main__":


	root = tk.Tk()
	root.wm_title("Microscope-Pump Control")

	app = App(root)
	app.pack()
	
	#thread = threading.Thread(target=app.serial.readPort, args=(20,))
	#thread.start()

	#print(app.pump)

	root.mainloop()
