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

class AppWidget(tk.Frame):
	def __init__(self, parent, title="App Widget", scrolled=False):
		tk.Frame.__init__(self, parent)
		
		self.parent = parent
		self.title = title
		self.scrolled = scrolled
		
		self.wrapperframe = tk.Frame(self.parent, bg=self.parent.parent.framecolor)
		
		self.titleframe = tk.Frame(self.wrapperframe, bg=self.parent.parent.headcolor)
		self.title = tk.Label(self.titleframe, text=self.title, bg=self.parent.parent.headcolor)
		self.title.config(font=self.parent.parent.headfont, fg=self.parent.parent.headfc)
		self.title.pack()
		self.titleframe.grid(row=0, column=0, ipadx=5, sticky='we')

		self.bodyframe = tk.Frame(self.wrapperframe, bg=self.parent.parent.framecolor)
		self.bodyframe.grid(row=1, column=0, sticky='we')
		
		self.wrapperframe.pack(padx=10, pady=10)
		
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

		self.helpmenu = tk.Menu(self.menubar, tearoff=0)
		self.helpmenu.add_command(label="About...")
		self.helpmenu.add_command(label="Manual...")

		self.menubar.add_cascade(menu=self.filemenu, label="File")
		self.menubar.add_cascade(menu=self.helpmenu, label="Help")
		
		self.filemenu.config(bg=self.parent.headcolor, fg=self.parent.headfc, bd=1, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc)
		self.helpmenu.config(bg=self.parent.headcolor, fg=self.parent.headfc, bd=1, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc)

		self.root.config(menu=self.menubar)
		
########################################################################################################################

class Log(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.config(bg=self.parent.wrapcolor)

		self.logframe = AppWidget(self, "Log", False)

		self.renderLog()


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
		self.log = tk.Text(self.logframe.bodyframe, height="15", width="120", bg=self.parent.lightercolor, bd=0, fg=self.parent.bodyfc, highlightthickness=0)
		self.log.pack(padx=10, pady=10, fill="both", expand=1)
		self.log.configure(state="disabled")

########################################################################################################################

class ControlPanel(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent
		
		self.config(bg=self.parent.wrapcolor)

		self.primingframe = AppWidget(self, "Port Priming", False)

		self.calibframe = AppWidget(self, "Output Calibration", False)

		self.cmdframe = AppWidget(self, "Control Panel", False)
		
		self.cycletimeframe = AppWidget(self, "Cycle Duration", False)

		self.renderCP()


	def renderCP(self):
		pframe = tk.Frame(self.primingframe.bodyframe, bg=self.parent.framecolor)
		pframe.pack()

		lframe = tk.Frame(pframe, bg=self.parent.darkercolor)
		lframe.grid(row=0, column=0)

		rframe = tk.Frame(pframe, bg=self.parent.lightercolor)
		rframe.grid(row=0, column=1)

		tk.Label(lframe, text="Port", bg=self.parent.darkercolor, fg=self.parent.bodyfc).grid(row=0, column=0, columnspan=2)
		tk.Label(rframe, text="Tubing Type", bg=self.parent.lightercolor, fg=self.parent.bodyfc).grid(row=0, column=0, columnspan=2)
#		tk.Label(self.priminglf, text="Length(in)").grid(row=0, column=2)

		self.portstoprime = []
		self.tubingtypes = []
#		self.lengths = []

		for i in range(1, 10):
			port = tk.DoubleVar()
			tk.Checkbutton(lframe, variable=port, bg=self.parent.darkercolor, highlightthickness=0).grid(row=i, column=0)
			tk.Label(lframe, text=str(i), bg=self.parent.darkercolor, fg=self.parent.bodyfc).grid(row=i, column=1)
			self.portstoprime.append(port)

			tubingtype = tk.IntVar()
			tk.Radiobutton(rframe, text="PEEK", variable=tubingtype, value=1, indicator=0, offrelief='flat', bg=self.parent.lightercolor, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=i, column=0)
			#tk.Label(rframe, text="PEEK", bg=self.parent.lightercolor, fg=self.parent.bodyfc).grid(row=i, column=1)
			tk.Radiobutton(rframe, text="non-PEEK", variable=tubingtype, value=2, indicator=0, offrelief='flat', bg=self.parent.lightercolor, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=i, column=1)
			#tk.Label(rframe, text="non-PEEK", bg=self.parent.lightercolor, fg=self.parent.bodyfc).grid(row=i, column=3)
			
			self.tubingtypes.append(tubingtype)

#			length = tk.DoubleVar()
#			tk.Entry(self.primingll, width=4, textvariable=length).grid(row=i, column=2)
#			self.lengths.append(length)

		pf = tk.Frame(pframe, bg=self.parent.framecolor)
		pf.grid(row=len(self.portstoprime)+2, column=0, columnspan=3, padx=5, pady=5)

		self.volume = tk.Spinbox(pf, from_=500, to=1000, width=4, bg=self.parent.entrycolor, bd=0)
		self.volume.pack(side='left', padx=5)

		#ttk.Separator(pframe, orient='horizontal').grid(row=len(self.portstoprime)+1, column=0, columnspan=3, sticky='ew')

		tk.Button(pf, text="Prime Ports", command=lambda: self.parent.protocol.primePorts(self.portstoprime, self.volume, self.tubingtypes), relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(padx=5, side='left')

		#ttk.Separator(pframe, orient='horizontal').grid(row=len(self.portstoprime)+3, column=0, columnspan=3, sticky='ew')

		tk.Button(pframe, text="Return Port Contents", command=lambda: self.parent.protocol.returnPortContents(self.portstoprime), relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=len(self.portstoprime)+3, column=0, columnspan=2, padx=5, pady=5)

		########################################
		cf = tk.Frame(self.calibframe.bodyframe, bg=self.parent.framecolor)
		cf.pack(padx=5, pady=5)

		self.calibvolume = tk.Spinbox(cf, from_=0, to=1000, width=4, bg=self.parent.entrycolor, bd=0)
		self.calibvolume.pack(padx=5, side='left')
		tk.Button(cf, text="Calibrate", command=lambda: self.parent.protocol.calibrateOutput(self.calibvolume), relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(padx=5, side='left')		

		########################################
		cpframe = tk.Frame(self.cmdframe.bodyframe, bg=self.parent.framecolor)
		cpframe.pack()

		tk.Button(cpframe, text="Execute Cycle", command=self.parent.protocol.executeCycle, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=0, column=0, padx=5, pady=5)
		tk.Button(cpframe, text="Update Protocol", command=self.parent.protocol.updateProtocol, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=1, column=0, padx=5, pady=5)
		tk.Button(cpframe, text="Add Command", command=self.parent.protocol.addCommand, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=2, column=0, padx=5, pady=5)
		tk.Button(cpframe, text="Calculate Cycle Times", command=self.parent.protocol.renderCycleTimes, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=6, column=0, padx=5, pady=5)

		#ttk.Separator(cpframe, orient='horizontal').grid(row=3, column=0, sticky='ew')
#		pumps = ['/dev/ttyUSb0']
		pumps = [x[0] for x in self.parent.protocol.devices]
		self.selectedpump = tk.StringVar()
		self.selectedpump.set(pumps[0])
		option = ttk.Combobox(cpframe, textvariable=self.selectedpump, state='readonly')
		option['values'] = pumps
		option.grid(row=4, column=0, padx=5, pady=5)
		
		tk.Button(cpframe, text="Reset Pump", command=self.parent.protocol.resetPump, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=5, column=0, padx=5, pady=5)

		########################################
		self.ctframe = tk.Frame(self.cycletimeframe.bodyframe, bg=self.parent.framecolor)
		self.ctframe.pack()
		
		tk.Label(self.ctframe, text="Cycle", bg=self.parent.darkercolor, fg=self.parent.bodyfc).grid(row=0, column=0, sticky='we')
		tk.Label(self.ctframe, text="Duration", bg=self.parent.lightercolor, fg=self.parent.bodyfc).grid(row=0, column=1, sticky='we')

########################################################################################################################

class Protocol(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.config(bg=self.parent.wrapcolor)

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

		self.protocolframe = AppWidget(self, 'Protocol', False)
		
		self.frame = VerticalScrolledFrame(self.protocolframe.bodyframe, bg=self.parent.framecolor)
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


	def renderCommand(self, i):
		if i%2 == 0:
			color = self.parent.lightercolor
		else:
			color = self.parent.darkercolor

		cframe = tk.Frame(self.frame.interior, bg=color)
		frame = tk.Frame(cframe, bg=color)

		tk.Label(frame, text=str(i+1)+") ", bg=color, width=3, fg=self.parent.bodyfc).grid(row=0, column=0)

		self.cmdnumbers.append(i)

		tk.Label(frame, text="Cycle: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=1)
		sb_cycle = tk.Spinbox(frame, from_=0, to=99, width=2, bg=self.parent.entrycolor, bd=0, fg=self.parent.entryfc)
		sb_cycle.grid(row=0, column=2)

		self.cycles.append(sb_cycle)

		if self.protocol[i].get('cycle') is not None:
			sb_cycle['value'] = self.protocol[i].get('cycle') 

		tk.Label(frame, text="Name: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=3)
		commandname = tk.StringVar()
		en_name = tk.Entry(frame, textvariable=commandname, bg=self.parent.entrycolor, width=20, bd=0)
		en_name.grid(row=0, column=4)

		self.names.append(commandname)

		if self.protocol[i].get('name') is not None:
			self.names[i].set(self.protocol[i].get('name'))

		tk.Label(frame, text="Pump: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=5)
#		pumps = ['/dev/ttyUSB0', '/dev/ttyUSB1']
		pumps = [x[0] for x in self.devices]
		#print("List of pumps: " + str(pumps))
		selectedpump = tk.StringVar()
		selectedpump.set(pumps[0])
		#self.parent.setPump(self.selectedpump.get())
		#print("Selected pump: " + str(self.selectedpump.get()))
		#option = tk.OptionMenu(frame, selectedpump, *pumps)
		option = ttk.Combobox(frame, textvariable=selectedpump, state='readonly', width=15)
		option['values'] = pumps
		option.grid(row=0, column=6)

		self.pumpports.append(selectedpump)

		if self.protocol[i].get('pump') is not None:
			self.pumpports[i].set(self.protocol[i].get('pump'))

		tk.Label(frame, text="From Port: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=7)
		sb_fromport = tk.Spinbox(frame, from_=1, to=9, width=2, bg=self.parent.entrycolor, bd=0, fg=self.parent.entryfc)
		sb_fromport.grid(row=0, column=8)

		self.fromports.append(sb_fromport)

		if self.protocol[i].get('fromport') is not None:
			self.fromports[i]['value'] = self.protocol[i].get('fromport')

		tk.Label(frame, text="To Port: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=9)
		sb_toport = tk.Spinbox(frame, from_=1, to=9, width=2, bg=self.parent.entrycolor, bd=0, fg=self.parent.entryfc)
		sb_toport.grid(row=0, column=10)

		self.toports.append(sb_toport)

		if self.protocol[i].get('toport') is not None:
			self.toports[i]['value'] = self.protocol[i].get('toport')

		tk.Label(frame, text="Volume(uL): ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=11)
		sb_volume = tk.Spinbox(frame, from_=1, to=1000, width=4, bg=self.parent.entrycolor, bd=0, fg=self.parent.entryfc)
		sb_volume.grid(row=0, column=12)

		self.volumes.append(sb_volume)

		if self.protocol[i].get('volume') is not None:
			self.volumes[i]['value'] = self.protocol[i].get('volume')

		tk.Label(frame, text="Speed(0-40): ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=13)
		sb_speed = tk.Spinbox(frame, from_=0, to=40, width=2, bg=self.parent.entrycolor, bd=0, fg=self.parent.entryfc)
		sb_speed.grid(row=0, column=14)

		self.speeds.append(sb_speed)

		if self.protocol[i].get('speed') is not None:
			self.speeds[i]['value'] = self.protocol[i].get('speed')

		tk.Label(frame, text="Leave for: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=15)
		sb_timemin = tk.Spinbox(frame, from_=0, to=600, width=3, bg=self.parent.entrycolor, bd=0, fg=self.parent.entryfc)
		sb_timemin.grid(row=0, column=16)
		tk.Label(frame, text="min", bg=color, fg=self.parent.bodyfc).grid(row=0, column=17)
		sb_timesec = tk.Spinbox(frame, from_=5, to=59, width=2, bg=self.parent.entrycolor, bd=0, fg=self.parent.entryfc)
		sb_timesec.grid(row=0, column=18) 
		tk.Label(frame, text="sec", bg=color, fg=self.parent.bodyfc).grid(row=0, column=19)

		self.waitmins.append(sb_timemin)
		self.waitsecs.append(sb_timesec)

		if self.protocol[i].get('waitmins') is not None:
			self.waitmins[i]['value'] = self.protocol[i].get('waitmins')
		if self.protocol[i].get('waitsecs') is not None:
			self.waitsecs[i]['value'] = self.protocol[i].get('waitsecs')

		waste = tk.IntVar()
		tk.Radiobutton(frame, text="Return", variable=waste, value=0, bg=color, highlightthickness=0, fg=self.parent.logofc).grid(row=0, column=20)
		tk.Radiobutton(frame, text="Waste", variable=waste, value=1, bg=color, highlightthickness=0, fg=self.parent.logofc).grid(row=0, column=21)

		self.wasteornots.append(waste)

		if self.protocol[i].get('waste') is not None:
			self.wasteornots[i].set(self.protocol[i].get('waste'))

		tk.Label(frame, text="  -  ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=22)
		status = tk.Label(frame, text="Not complete", bg=color, fg=self.parent.bodyfc)
		status.grid(row=0, column=23)

		self.statuses.append(status)

		frame.pack(pady=5, fill='x')
		cframe.grid(row=i, column=0, sticky='we')
		
#		self.parent.update_idletasks()


	def renderProtocol(self):
		for i in range(len(self.protocol)):
			self.renderCommand(i)


	def renderCycleTimes(self):
		#for i in len(set(self.protocol.get('cycle'))):
		times = {16: 18, 30: 88}
		
		numcycles = len({v['cycle']:v for v in self.protocol}.values())
		print("# cycles: "+str(numcycles))
		
		for i in range(numcycles):
			print("cycle: "+str(i))
			time = 0
			for cmd in self.protocol:
				if cmd.get('cycle') == i:
					speed = cmd.get('speed')
					#print("speed: "+str(speed))
					volume = int(cmd.get('volume'))
					#print("volume: "+str(volume))
					vratio = volume/1000.0
					#print("vratio: "+str(vratio))
					
					t1 = times.get(speed)*vratio
					#print(str(t1))
					t2 = times.get(30)*vratio
					execdelay = 8*4
					wait = int(cmd.get('waitmins'))*60+int(cmd.get('waitsecs'))
					#print(str(t2))
					delay = execdelay+wait
					tt = 3*t1+t2+delay
					#print(str(tt))
					time += tt
			tk.Label(self.parent.cp.ctframe, text=i, bg=self.parent.darkercolor, fg=self.parent.bodyfc).grid(row=i+1, column=0, sticky='we')
			tk.Label(self.parent.cp.ctframe, text=str(time)+"sec", bg=self.parent.lightercolor, fg=self.parent.bodyfc).grid(row=i+1, column=1, sticky='we')
		
	def primePorts(self, portstoprime, volume, tubingtypes):
		pump = self.device_dict.get('/dev/ttyUSB0')

		buffertime = 2
		speed = 14

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

				print("Washing valve")
				self.parent.log.addRecord("Washing valve")
				pump.primePort(5, 750, speed, 9)

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
				self.parent.log.addRecord("Carrying out cycle: " + str(self.cyclecounter))
				print("Found cmd with appropriate cycle")
				self.executeCommand(self.cmdcounter)
				self.cmdcounter += 1
		
		self.cyclecounter += 1


	def executeCommand(self, index):
		self.updateProtocol()
		
		i = index

		status = self.statuses[i]
		status.config(bg="yellow", fg="black")
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
			esttime = pump.dispense(fromport, volume, execute=True)
			sleep(esttime+timebuffer)
		elif waste == 1:
			self.parent.log.addRecord("Dispensing " + str(volume) + "uL to waste port 9")
			esttime = pump.dispense(9, volume, execute=True)
			sleep(esttime+timebuffer)

		self.parent.log.addRecord("Command '" + name + "' is finished \n")

		status['text'] = 'Complete'
		status.config(bg='green', fg="black")


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

########################################################################################################################

class SerialThread(threading.Thread):
	def __init__(self, parent, port, baud, timeout):
		threading.Thread.__init__(self)

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

		self.parent = parent

		vscrollbar = tk.Scrollbar(self, orient='vertical', relief='flat')
		vscrollbar.pack(fill='y', side='right', expand=False)

		canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
		canvas.pack(side='left', fill='both', expand=True)
		canvas.config(height=300)
		
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

			self.headfont = ('arial', 16, 'normal')

			self.logofc = "#468ef2"
			self.headcolor = "#707070"
			self.headfc = "#e5e5e5"
			self.wrapcolor = "#212121"
			self.framecolor = "#4f4f4f"
			self.buttoncolor = "#468ef2"
			self.buttonfc = "#e5e5e5"
			self.entrycolor = "#e5e5e5"
			self.entryfc = "#1c1c1c"
			self.bodyfc = "#e5e5e5"
			self.lightercolor = "#595959"
			self.darkercolor = "#4a4a4a"

			self.config(bg=self.wrapcolor)

			self.parent = parent

			self.c1 = tk.Frame(self, bg=self.wrapcolor).grid(row=0, column=0)
			self.c2 = tk.Frame(self, bg=self.wrapcolor).grid(row=0, column=1)
			self.c3 = tk.Frame(self, bg=self.wrapcolor).grid(row=0, column=2)

			tk.Label(self, text="CASPA", bg=self.wrapcolor, fg=self.logofc, font=('arial', 24, 'normal')).grid(row=0, column=1)

			self.protocol = Protocol(self)
			self.protocol.grid(row=1, column=1, sticky='n')

			self.menu = MainMenu(self, self.parent)

			self.cp = ControlPanel(self)
			self.cp.grid(row=1, column=0, rowspan=2)

			self.log = Log(self)
			self.log.grid(row=2, column=1, sticky='n')

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
	root.wm_title("Computer-Aided Syringe Pump Automation")

	app = App(root)
	app.pack(padx=5, pady=5)

	root.config(bg=app.wrapcolor)

	root.mainloop()
