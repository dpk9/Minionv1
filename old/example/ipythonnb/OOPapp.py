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

	def __init__(self, parent, root, *args, **kwargs):
		tk.Menu.__init__(self, parent)

		self.parent = parent
		self.root = root

		self.menubar = tk.Menu(self.root)

		self.filemenu = tk.Menu(self.menubar, tearoff=0)
#		self.filemenu.add_command(label="New protocol", command=self.parent.protocol.newProtocol)
		self.filemenu.add_command(label="Open protocol...", command=self.parent.protocol.loadProtocol)
		self.filemenu.add_command(label="Save protocol...", command=self.parent.protocol.saveProtocol)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.root.destroy)

		self.menubar.add_cascade(menu=self.filemenu, label="File")

		self.root.config(menu=self.menubar)
		
########################################################################################################################

class Log(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.loglabelframe = tk.LabelFrame(self, text=" Log ")
		self.loglabelframe.grid(row=2, column=1, padx=5, pady=5, sticky="ns")

		self.renderLog()

#		self.pack()


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
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.priminglf = tk.LabelFrame(self.parent, text=" Port Priming ")
		self.priminglf.grid(row=0, column=0, padx=5, pady=5, sticky="n")

		self.caliblf = tk.LabelFrame(self.parent, text=" Out-Port Calibration ")
		self.caliblf.grid(row=1, column=0, padx=5, pady=5, sticky="n")

		self.cmdlf = tk.LabelFrame(self.parent, text=" Control Panel ")
		self.cmdlf.grid(row=0, column=2, padx=5, pady=5, sticky="n")

		self.renderCP()

#		self.pack()


	def renderCP(self):
		tk.Label(self.priminglf, text="Port").grid(row=0, column=0)
		tk.Label(self.priminglf, text="Tubing Type").grid(row=0, column=1, columnspan=2)
#		tk.Label(self.priminglf, text="Length(in)").grid(row=0, column=2)

		self.portstoprime = []
		self.tubingtypes = []
#		self.lengths = []

		for i in range(1, 10):
			port = tk.DoubleVar()
			tk.Checkbutton(self.priminglf, text=str(i), variable=port).grid(row=i, column=0)
			self.portstoprime.append(port)

			tubingtype = tk.IntVar()
			tk.Radiobutton(self.priminglf, text="PEEK", variable=tubingtype, value=1).grid(row=i, column=1)
			tk.Radiobutton(self.priminglf, text="non-PEEK", variable=tubingtype, value=2).grid(row=i, column=2)
			self.tubingtypes.append(tubingtype)

#			length = tk.DoubleVar()
#			tk.Entry(self.primingll, width=4, textvariable=length).grid(row=i, column=2)
#			self.lengths.append(length)

		pf = tk.Frame(self.priminglf)
		self.volume = tk.Spinbox(pf, from_=500, to=1000, width=4)
		self.volume.pack(side='left')
#		tk.Label(pf, text="uL").pack(side='left')
		tk.Button(pf, text="Prime Ports", command=lambda: self.parent.protocol.primePorts(self.portstoprime, self.volume, self.tubingtypes)).pack(side='left')
		pf.grid(row=len(self.portstoprime)+1, column=0, columnspan=3, padx=5, pady=5)

		ttk.Separator(self.priminglf, orient='horizontal').grid(row=len(self.portstoprime)+2, column=0, columnspan=3, sticky='ew')

		tk.Button(self.priminglf, text="Return Port Contents", command=lambda: self.parent.protocol.returnPortContents(self.portstoprime)).grid(row=len(self.portstoprime)+3, column=0, columnspan=3, padx=5, pady=5)

		########################################

		cf = tk.Frame(self.caliblf)
		self.calibvolume = tk.Spinbox(cf, from_=0, to=1000, width=4)
		self.calibvolume.pack(side='left')
		tk.Button(cf, text="Calibrate", command=lambda: self.parent.protocol.calibrateOutput(self.calibvolume)).pack(side='left')		
		cf.pack(padx=5, pady=5)

		########################################

		tk.Button(self.cmdlf, text="Execute Cycle", command=self.parent.protocol.executeCycle, width=12).grid(row=0, column=0, padx=5, pady=5)
		tk.Button(self.cmdlf, text="Update Protocol", command=self.parent.protocol.updateProtocol, width=12).grid(row=1, column=0, padx=5, pady=5)
		tk.Button(self.cmdlf, text="Add Command", command=self.parent.protocol.addCommand, width=12).grid(row=2, column=0, padx=5, pady=5)

		ttk.Separator(self.cmdlf, orient='horizontal').grid(row=3, column=0, sticky='ew')

		pumps = [x[0] for x in self.parent.protocol.devices]
		self.selectedpump = tk.StringVar()
		self.selectedpump.set(pumps[0])
		option = tk.OptionMenu(self.cmdlf, self.selectedpump, *pumps)
		option.grid(row=4, column=0, padx=5, pady=5)
		
		tk.Button(self.cmdlf, text="Reset Pump", command=self.parent.protocol.resetPump, width=12).grid(row=5, column=0, padx=5, pady=5)

#		ttk.Separator(self.cmdll, orient='horizontal').grid(row=6, column=0, sticky='ew')		

#		tk.Button(self.cmdlf, text="Load Protocol", command=self.parent.protocol.loadProtocol, width=12).grid(row=7, column=0, padx=5, pady=5)
#		tk.Button(self.cmdlf, text="Save Protocol", command=self.parent.protocol.saveProtocol, width=12).grid(row=8, column=0, padx=5, pady=5)

########################################################################################################################

class Protocol(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.devices = self.getSerialPumps()
		self.device_dict = dict(self.devices)

		if not self.device_dict:
			print("There is no pump connected. Please connect one and try again.")
			sys.exit()
		else:
			print("Device dict: " + str(self.device_dict))

		self.protocol = []

		self.protocol.append({})

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

		self.calibrationvolume = 0

		self.labelframe = tk.LabelFrame(self, text=" Protocol ", width=1000, height=600)
		self.labelframe.pack(padx=5, pady=5)

		self.frame = VerticalScrolledFrame(self.labelframe)
		self.frame.pack()

		self.renderProtocol()


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


	def resetProtocol(self):
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

#		self.renderProtocol()


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
#		self.protocol = self.cmdnumbers = self.cycles = self.names = self.pumpports = self.fromports = self.toports = self.volumes = self.speeds = self.waitmins = self.waitsecs = self.wasteornots = self.statuses = []
		self.resetProtocol()
		self.protocol = protocol
		print("Native protocol: " + str(self.protocol))
		self.renderProtocol()
		#self.insertFieldValues()


	def addCommand(self):
		print("Previous command list: "+str(self.protocol))
		self.protocol.append({})
		print("Appended command list: "+str(self.protocol))

		self.renderCommand(len(self.protocol)-1)

#		self.update_idletasks()


	def insertFieldValues(self):
		for i in range(len(self.protocol)):
			if self.protocol[i].get('cycle') is not None:	
				self.cycles[i]['value'] = self.protocol[i].get('cycle')
				#self.sb_cycle['value'] = self.protocol[i].get('cycle')
			

	def renderCommand(self, i):
		tk.Label(self.frame.interior, text=str(i+1)+") ").grid(row=i, column=0)

		self.cmdnumbers.append(i)

		tk.Label(self.frame.interior, text="Cycle: ").grid(row=i, column=1)
		sb_cycle = tk.Spinbox(self.frame.interior, from_=0, to=99, width=2)
		sb_cycle.grid(row=i, column=2)

		self.cycles.append(sb_cycle)

		if self.protocol[i].get('cycle') is not None:
			sb_cycle['value'] = self.protocol[i].get('cycle') 

		tk.Label(self.frame.interior, text="Name: ").grid(row=i, column=3)
		commandname = tk.StringVar()
		en_name = tk.Entry(self.frame.interior, textvariable=commandname)
		en_name.grid(row=i, column=4)

		self.names.append(commandname)

		if self.protocol[i].get('name') is not None:
			self.names[i].set(self.protocol[i].get('name'))

		tk.Label(self.frame.interior, text="Pump: ").grid(row=i, column=5)
		pumps = [x[0] for x in self.devices]
		#print("List of pumps: " + str(pumps))
		selectedpump = tk.StringVar()
		selectedpump.set(pumps[0])
		#self.parent.setPump(self.selectedpump.get())
		#print("Selected pump: " + str(self.selectedpump.get()))
		option = tk.OptionMenu(self.frame.interior, selectedpump, *pumps)
		option.grid(row=i, column=6)

		self.pumpports.append(selectedpump)

		if self.protocol[i].get('pump') is not None:
			self.pumpports[i].set(self.protocol[i].get('pump'))

		tk.Label(self.frame.interior, text="From Port: ").grid(row=i, column=7)
		sb_fromport = tk.Spinbox(self.frame.interior, from_=1, to=9, width=1)
		sb_fromport.grid(row=i, column=8)

		self.fromports.append(sb_fromport)

		if self.protocol[i].get('fromport') is not None:
			self.fromports[i]['value'] = self.protocol[i].get('fromport')

		tk.Label(self.frame.interior, text="To Port: ").grid(row=i, column=9)
		sb_toport = tk.Spinbox(self.frame.interior, from_=1, to=9, width=1)
		sb_toport.grid(row=i, column=10)

		self.toports.append(sb_toport)

		if self.protocol[i].get('toport') is not None:
			self.toports[i]['value'] = self.protocol[i].get('toport')

		tk.Label(self.frame.interior, text="Volume(uL): ").grid(row=i, column=11)
		sb_volume = tk.Spinbox(self.frame.interior, from_=1, to=1000, width=4)
		sb_volume.grid(row=i, column=12)

		self.volumes.append(sb_volume)

		if self.protocol[i].get('volume') is not None:
			self.volumes[i]['value'] = self.protocol[i].get('volume')

		tk.Label(self.frame.interior, text="Speed(0-40): ").grid(row=i, column=13)
		sb_speed = tk.Spinbox(self.frame.interior, from_=0, to=40, width=2)
		sb_speed.grid(row=i, column=14)

		self.speeds.append(sb_speed)

		if self.protocol[i].get('speed') is not None:
			self.speeds[i]['value'] = self.protocol[i].get('speed')

		tk.Label(self.frame.interior, text="Leave for: ").grid(row=i, column=15)
		sb_timemin = tk.Spinbox(self.frame.interior, from_=0, to=600, width=3)
		sb_timemin.grid(row=i, column=16)
		tk.Label(self.frame.interior, text="min").grid(row=i, column=17)
		sb_timesec = tk.Spinbox(self.frame.interior, from_=5, to=59, width=2)
		sb_timesec.grid(row=i, column=18) 
		tk.Label(self.frame.interior, text="sec").grid(row=i, column=19)

		self.waitmins.append(sb_timemin)
		self.waitsecs.append(sb_timesec)

		if self.protocol[i].get('waitmins') is not None:
			self.waitmins[i]['value'] = self.protocol[i].get('waitmins')
		if self.protocol[i].get('waitsecs') is not None:
			self.waitsecs[i]['value'] = self.protocol[i].get('waitsecs')

		waste = tk.IntVar()
		tk.Radiobutton(self.frame.interior, text="Return", variable=waste, value=0).grid(row=i, column=20)
		tk.Radiobutton(self.frame.interior, text="Waste", variable=waste, value=1).grid(row=i, column=21)

		self.wasteornots.append(waste)

		if self.protocol[i].get('waste') is not None:
			self.wasteornots[i].set(self.protocol[i].get('waste'))

		tk.Label(self.frame.interior, text="  -  ").grid(row=i, column=22)
		status = tk.Label(self.frame.interior, text="Not complete")
		status.grid(row=i, column=23)

		self.statuses.append(status)

#		self.parent.update_idletasks()


	def renderProtocol(self):
		for i in range(len(self.protocol)):
			self.renderCommand(i)


	def primePorts(self, portstoprime, volume, tubingtypes):
		pump = self.device_dict.get('/dev/ttyUSB0')

		buffertime = 2
		speed = 0

		for i in range(len(portstoprime)):
			if portstoprime[i].get() == 1:
				if tubingtypes[i].get() == 1:
					speed = 28
				elif tubingtypes[i].get() == 2:
					speed = 14
				v = int(volume.get())	 
				port = i+1

				print("Priming port "+str(port)+" with "+str(v)+"uL at speed: "+str(speed))
				self.parent.log.addRecord("Priming port "+str(port)+" with "+str(v)+"uL at speed: "+str(speed))

				pump.primePort(port, v, speed, port)

				sleep(buffertime)


	def returnPortContents(self, portstoprime):
		pump = self.device_dict.get('/dev/ttyUSB0')

		volume = 500
		speed = 14
		buffertime = 2

		pump.setSpeed(speed)
		sleep(1)

		for i in range(len(portstoprime)):
			if portstoprime[i].get() == 1:
				port = i+1
				
				print("Returning contents of port " +str(port))
				self.parent.log.addRecord("Returning contents of port " +str(port))
				esttime = pump.extract(7, volume, execute=True)
				sleep(esttime+buffertime)
				esttime = pump.dispense(port, volume, execute=True)
				sleep(esttime+buffertime)


	def calibrateOutput(self, volume):
		self.calibrationvolume = int(volume.get())
		self.parent.log.addRecord("Output port has been calibrated for additional " + str(self.calibrationvolume) + "uL \n")


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

		pump = self.device_dict.get(self.protocol[i].get('pump'))

		name = str(self.protocol[i].get('name'))
		toport = int(self.protocol[i].get('toport'))
		fromport = int(self.protocol[i].get('fromport'))
		volume = int(self.protocol[i].get('volume')) + self.calibrationvolume
		speed = int(self.protocol[i].get('speed'))
		waitmins = int(self.protocol[i].get('waitmins'))
		waitsecs = int(self.protocol[i].get('waitsecs'))

		timebuffer = 6

		timewait = waitmins*60 + waitsecs

		waste = int(self.protocol[i].get('waste'))

		self.parent.log.addRecord("Starting command '" + name+ "'")
		self.parent.log.addRecord("Selected pump for this command is: " + str(pump))		
		self.parent.log.addRecord("Setting pump speed to " + str(speed))
		pump.setSpeed(speed)
		sleep(2)
		
		self.parent.log.addRecord("Extracting " + str(volume) + "uL from port " + str(fromport))
		esttime = pump.extract(fromport, volume, execute=True)
		self.parent.log.addRecord("Estimated time: " + str(esttime) + "sec")
		sleep(esttime+timebuffer)

		self.parent.log.addRecord("Dispensing " + str(volume) + "uL to port " + str(toport))
		esttime = pump.dispense(toport, volume, execute=True)
		sleep(esttime+timebuffer)

		self.parent.log.addRecord("Waiting for " + str(waitmins) + "min " + str(waitsecs) + "sec before extraction")
		sleep(timewait)

		self.parent.log.addRecord("Setting pump speed to 30 for extraction")
		pump.setSpeed(30)
		sleep(2)
		self.parent.log.addRecord("Extracting " + str(volume) + "uL from port " + str(toport))
		esttime = pump.extract(toport, volume, execute=True)
		sleep(esttime+timebuffer)
		self.parent.log.addRecord("Setting pump speed back to  " + str(speed))
		pump.setSpeed(speed)
		sleep(2)
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
		port = self.parent.cp.selectedpump.get()
		pump = self.device_dict.get(port)
		self.parent.log.addRecord("Resetting pump " + str(pump) + "\n")
		pump.init()


	def findSerialPumps(self):
		return TecanAPISerial.findSerialPumps()


	def getSerialPumps(self):
		pump_list = self.findSerialPumps()
		return [(ser_port, XCaliburD(com_link=TecanAPISerial(0,ser_port, 9600))) for ser_port, _, _ in pump_list]

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

class SerialThread(threading.Thread):
	def __init__(self, parent, port, baud, timeout):
		threading.Thread.__init__(self)
	
#		self.queue = queue
		self.parent = parent
		self.port = port
		self.baud = baud
		self.timeout = timeout


	def run(self):
		s = Serial(self.port, self.baud, timeout=self.timeout)
		while True:
#			if s.inWaiting():
			cmd = s.read(5)
			print('Cmd: '+str(cmd))
			if len(cmd) > 0:
				self.parent.log.addRecord("Received serial command '" + str(cmd) + "'")
			if cmd == 'pump':
				self.parent.protocol.executeCycle()	

########################################################################################################################

class VerticalScrolledFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)

		vscrollbar = tk.Scrollbar(self, orient='vertical')
		vscrollbar.pack(fill='y', side='right', expand=False)

		canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
		canvas.pack(side='left', fill='both', expand=True)

		vscrollbar.config(command=canvas.yview)

		canvas.xview_moveto(0)
		canvas.yview_moveto(0)

		self.interior = interior = tk.Frame(canvas)
		interior_id = canvas.create_window(0, 0, window=interior, anchor='nw')

		def _configure_interior(event):
			size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
			canvas.config(scrollregion="0 0 %s %s" % size)
			if interior.winfo_reqwidth() != canvas.winfo_width():
				canvas.config(width=interior.winfo_reqwidth())
		interior.bind('<Configure>', _configure_interior)

		def _configure_canvas(event):
			if interior.winfo_reqwidth() != canvas.winfo_width():
				canvas.itemconfigure(interior_id, width=canvas.winfo_width())
		canvas.bind('<Configure>', _configure_canvas)

########################################################################################################################

#--------------------------- @30 1000uL = 88sec
#--------------------------- @31 1000uL = 102sec
#--------------------------- @32 1000uL = 122sec
#--------------------------- @33 1000uL = 152sec

if __name__ == "__main__":

	class App(tk.Frame):
		def __init__(self, parent, *args, **kwargs):
			tk.Frame.__init__(self, parent, *args, **kwargs)

			self.parent = parent

#			root = tk.Tk.__init__(self, *args, **kwargs)
#			root.title("Computer-Cued Pump Automation")

			self.protocol = Protocol(self)
			self.protocol.grid(row=0, column=1, sticky='n')

			self.menu = MainMenu(self, self.parent)

			self.cp = ControlPanel(self)
			self.cp.grid(row=0, column=0)

			self.log = Log(self)
			self.log.grid(row=1, column=1)

#			self.queue = Queue.Queue()
			thread = SerialThread(self, '/dev/ttyAMA0', 9600, 1)
			thread.start()
#			self.processSerial()

#			self.serial = SerialPort(self, "/dev/ttyAMA0", 9600, 1)

#			thread = threading.Thread(target=self.serial.readPort, args=(20,))		
#			thread.start()


		def processSerial(self):
			while self.queue.qsize():
				try:
					cmd = self.queue.get()
					print("Cmd: " + str(cmd))
					if cmd == 'pump':
						self.protocol.executeCycle()
				except Queue.Empty:
					pass
			self.after(100, self.processSerial)


	root = tk.Tk()
	root.wm_title("Computer-Aided Pump Automation")

	app = App(root)
	app.pack()

	root.mainloop()
