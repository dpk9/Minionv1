from __future__ import print_function
from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

try:
	import cPickle as pickle 
except:
	import pickle

import Tkinter as tk
import ttk
import Queue
import threading, tkFileDialog
import smbus
import time
import datetime
from subprocess import call
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
		self.sepframe = tk.Frame(self.wrapperframe, bg=self.parent.parent.darkentrycolor, height=2)
		self.sepframe.grid(row=1, column=0, sticky='we')

		self.bodyframe = tk.Frame(self.wrapperframe, bg=self.parent.parent.framecolor)
		self.bodyframe.grid(row=2, column=0, sticky='we')
		
		self.wrapperframe.pack(padx=10, pady=10)
		
########################################################################################################################

class MainMenu(tk.Menu):

	def __init__(self, parent, root, *args, **kwargs):
		tk.Menu.__init__(self, parent)

		self.parent = parent
		self.root = root

		self.menubar = tk.Menu(self.root, bg=self.parent.framecolor, fg=self.parent.bodyfc, relief='flat', activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc)

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
		
		self.filemenu.config(bg=self.parent.framecolor, fg=self.parent.headfc, relief='flat', bd=1, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc)
		self.helpmenu.config(bg=self.parent.framecolor, fg=self.parent.headfc, relief='flat', bd=1, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc)

		self.root.config(menu=self.menubar)
		
########################################################################################################################

class Log(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.config(bg=self.parent.wrapcolor)

		self.logframe = AppWidget(self, "Log")

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
		self.log = tk.Text(self.logframe.bodyframe, height="17", width="76", bg=self.parent.darkentrycolor, bd=1, fg=self.parent.bodyfc, highlightthickness=0)
		self.log.pack(padx=10, pady=10, fill="both", expand=1)
		self.log.configure(state="disabled")

########################################################################################################################

class ControlPanel(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent
		
		self.config(bg=self.parent.wrapcolor)

		self.cmdframe = AppWidget(self, "Control Panel")

		self.renderCP()


	def renderCP(self):
		cpframe = tk.Frame(self.cmdframe.bodyframe, bg=self.parent.framecolor)
		cpframe.pack()

		tk.Button(cpframe, text="Execute Cycle", command=self.parent.passQueueCmd, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=0, column=0, padx=5, pady=5)
		tk.Button(cpframe, text="Update Protocol", command=self.parent.protocol.updateProtocol, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=0, column=1, padx=5, pady=5)
		tk.Button(cpframe, text="Calculate Cycle Times", command=self.parent.protocol.renderCycleTimes, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=0, column=2, padx=5, pady=5)

		#ttk.Separator(cpframe, orient='horizontal').grid(row=3, column=0, sticky='ew')
#		pumps = ['/dev/ttyUSb0']
		pumps = [x[0] for x in self.parent.protocol.devices]
		self.selectedpump = tk.StringVar()
		self.selectedpump.set(pumps[0])
		option = ttk.Combobox(cpframe, textvariable=self.selectedpump, state='readonly')
		option['values'] = pumps
		option.grid(row=0, column=3, padx=5, pady=5)
		
		tk.Button(cpframe, text="Reset Pump", command=self.parent.protocol.resetPump, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=0, column=4, padx=5, pady=5)

########################################################################################################################

class TempControl(tk.Frame):
        def __init__(self, parent, *args, **kwargs):
                tk.Frame.__init__(self, parent)
                
                self.parent = parent

                self.config(bg=self.parent.wrapcolor)

                self.active = False
                self.isHeating = True

                self._job = None

                self.bus = smbus.SMBus(1)
                self.address = 0x4d
                self.temperature_hysteresis = .75

                self.temperature = 0
                self.avetemperature = 0
                self.templist = [self.temperature]

                self.tempgoal = 25

                self.tempcontrolframe = AppWidget(self, "Temp Control")

                self.init()

                #self.doTempControl()

                self.renderTempControl()
                

        def renderTempControl(self):
                #self.temp = tk.Label(self.tempcontrolframe.bodyframe, text="N/A", font=('Arial', 14, 'normal'), bg=self.parent.framecolor, fg=self.parent.bodyfc)
                #self.temp.pack()

                self.avetemp = tk.Label(self.tempcontrolframe.bodyframe, text="N/A", font=('Arial', 14, 'normal'), bg=self.parent.framecolor, fg=self.parent.bodyfc)
                self.avetemp.pack()
                
                tk.Button(self.tempcontrolframe.bodyframe, text="Start", command=self.startTempControl, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(padx=5, pady=5)
                tk.Button(self.tempcontrolframe.bodyframe, text="Stop", command=self.stopTempControl, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(padx=5, pady=5)


        def init(self):
                print("initializing")
                call(["temperature_controller_init"])

                
        def get_fahrenheit_val(self): 
                data = self.bus.read_i2c_block_data(self.address, 1,2)
                val = (data[0] << 8) + data[1]
                return val/5.00*9.00/5.00+32.00

        
        def get_celsius_val(self): 
                data = self.bus.read_i2c_block_data(self.address, 1,2)
                val = (data[0] << 8) + data[1]
                return val/5.00
           
           
        def set_cold(self):
                print("cooling")
                self.avetemp.config(fg=self.parent.buttoncolor)
                call(["temp_relay_on", "cold"])
                call(["temp_relay_off", "hot"])

                
        def set_hot(self):
                print("heating")
                self.avetemp.config(fg='orange')
                call(["temp_relay_on", "hot"])
                call(["temp_relay_off", "cold"])	

                
        def set_close(self):
                print("hold")
                self.avetemp.config(fg=self.parent.bodyfc)
                call(["temp_relay_off", "cold"])
                call(["temp_relay_off", "hot"])


        def updateTemp(self):
                self.temperature = self.get_celsius_val()
                #self.temp['text'] = str(self.temperature) + u'\N{DEGREE SIGN}' + 'C'


        def getTemp(self):
                self.updateTemp()
                return self.temperature


        def getAverageTemp(self):
                self.updateTemp()
                
                samples = 10
                
                if len(self.templist) >= samples:
                        self.templist = self.templist[1:]
                        self.templist.append(self.temperature)
                else:
                        self.templist.append(self.temperature)

                print('length of temps: ' + str(len(self.templist)))

                tempSum = 0

                print(str(self.templist))

                for i in range(len(self.templist)):
                        tempSum += self.templist[i]

                averageTemp = tempSum/samples

                if len(self.templist) == samples:
                        self.avetemperature = round(averageTemp,1)
                        return round(averageTemp,1)
                else:
                        self.avetemperature = self.temperature
                        return self.temperature

                
        def doTempControl(self):

                #self.tempReached(temp)
                
                set_point = self.tempgoal
                
                try:
                        set_point=float(set_point)
                except ValueError:
                        print("the argument is not a number")

                print("set point =" + str(set_point))
                print("temperature hysteresis =" + str(self.temperature_hysteresis))
                

                if self.active is True:
                        
                        avetemp = self.getAverageTemp()

                        self.avetemp['text'] = str(avetemp) + u'\N{DEGREE SIGN}' + 'C'

                        print(self.temperature)
                        
                        if avetemp > set_point :
                                print('1')
                                self.set_cold()
                                self.isHeating = False
                        elif avetemp  <= (set_point- self.temperature_hysteresis):
                                print('2')
                                self.set_hot()
                                self.isHeating = True
                        elif self.isHeating == True and avetemp < set_point:
                                print('3')
                                self.set_hot()
                        else:
                                self.set_close()
                                
                        self._job = self.after(1000, self.doTempControl)


        def startTempControl(self, temp=25):
                #temp = t
                print("Setting active to True")
                self.parent.log.addRecord("Starting temperature control")
                self.tempgoal = temp
                self.active = True
                self.doTempControl()

                        
        def stopTempControl(self):
                print("Setting active to False")
                self.parent.log.addRecord("Stopping temperature control")
                
                self.active = False
                
                if self._job is not None:
                        self.after_cancel(self._job)
                        self._job = None

                self.set_close()
                self.templist = []


        def tempReached(self, goaltemp):
                avetemp = self.avetemperature

                if self.isHeating is True and avetemp >= (goaltemp-2):
                        return True
                elif self.isHeating is False and avetemp <= (goaltemp+2):
                        return True
                else:
                        return False

########################################################################################################################

class PumpSetup(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.config(bg=self.parent.wrapcolor)

		self.setupframe = AppWidget(self, 'Pump Setup')

		self.renderPumpSetup()


	def renderPumpSetup(self):
                sframe = tk.Frame(self.setupframe.bodyframe, bg=self.parent.framecolor)
		sframe.pack(padx=5, pady=5)
		
		self.pumps = []
		self.ports = []
		#self.portstoprime = []
		self.reagents = []
		self.reagentvolumes = []
		
		for pump in range(len(self.parent.protocol.devices)):
                        pumpport = self.parent.protocol.devices[pump][0]
                        pumpnumports = self.parent.protocol.device_dict.get(pumpport).num_ports

                        portstoprime = []
                        
			pumplf = tk.LabelFrame(sframe, text=str(pumpport), bg=self.parent.framecolor, fg=self.parent.bodyfc)
			pumplf.grid(row=0, column=pump, padx=5, pady=5)
			
			#tk.Label(pumplf, text='Pump at port: '+str(pumpport), bg=self.parent.subheadcolor, fg=self.parent.bodyfc).grid(row=0, column=0, columnspan=6, padx=5, sticky='we')
			
			tk.Label(pumplf, text='Port', bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=1, column=0, padx=5)
			tk.Label(pumplf, text='Reagent', bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=1, column=1, padx=5)
			tk.Label(pumplf, text='uL', bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=1, column=2, padx=5)
			tk.Label(pumplf, text='Need', bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=1, column=3, padx=5)
			tk.Label(pumplf, text='Prime', bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=1, column=4, padx=5)
			
			for port in range(1, pumpnumports+1):
                                self.pumps.append(pumpport)
				self.ports.append(port)
				
				tk.Label(pumplf, text=port, bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=port+1, column=0, padx=5)
				
				reagent = tk.StringVar()
				en_reagent = tk.Entry(pumplf, textvariable=reagent, bg=self.parent.darkentrycolor, fg=self.parent.bodyfc, justify='center', width=20, bd=1, highlightthickness=0)
				en_reagent.grid(row=port+1, column=1)
				
				self.reagents.append(reagent)

                                self.parent.protocol.ports.append({})
				
				if self.parent.protocol.ports[port-1].get('reagent') is not None:
                                        self.reagents[port-1].set(self.parent.protocol.ports[port-1].get('reagent'))
				
				if port == 9:
					reagent.set('Waste '+str(pump+1))
				elif port == 8:
					reagent.set('Output '+str(pump+1))
				elif port == 7:
					reagent.set('Air '+str(pump+1))
				
				volume = tk.IntVar()
				en_volume = tk.Entry(pumplf, textvariable=volume, bg=self.parent.darkentrycolor, fg=self.parent.bodyfc, justify='center', width=5, bd=1, highlightthickness=0)
				en_volume.grid(row=port+1, column=2, padx=6, pady=3)

                                self.reagentvolumes.append(volume)

                                tk.Label(pumplf, text='N/A', bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=port+1, column=3)

                                porttoprime = tk.IntVar()
                                tk.Checkbutton(pumplf, variable=porttoprime, bg=self.parent.framecolor, highlightthickness=0).grid(row=port+1, column=4)

                                portstoprime.append(porttoprime)				
				
				#self.names.append(commandname)
		
			tk.Button(pumplf, text="Set Ports", width=15, command=lambda: self.parent.protocol.updatePorts(self.pumps, self.ports, self.reagents, self.reagentvolumes), relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).grid(row=11, column=1, padx=5, pady=5)

                        pf = tk.Frame(pumplf, bg=self.parent.framecolor)
                        pf.grid(row=11, column=2, columnspan=3, padx=5, pady=5)

                        pf2 = tk.Frame(pf, bg=self.parent.framecolor)
                        pf2.pack(side='top')
                        
                        volume = tk.Spinbox(pf2, from_=500, to=1000, width=4, bg=self.parent.entrycolor, bd=0)
                        volume.pack(side='left', padx=5)

                        #ttk.Separator(pframe, orient='horizontal').grid(row=len(self.portstoprime)+1, column=0, columnspan=3, sticky='ew')
                        tk.Button(pf2, text="Prime Ports", command=lambda pumpport=pumpport, portstoprime=portstoprime, volume=volume: self.parent.protocol.primePorts(pumpport, portstoprime, volume), relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(padx=5, side='left')

                        #ttk.Separator(pframe, orient='horizontal').grid(row=len(self.portstoprime)+3, column=0, columnspan=3, sticky='ew')

                        tk.Button(pf, text="Return Port Contents", command=lambda pumpport=pumpport, portstoprime=portstoprime: self.parent.protocol.returnPortContents(pumpport, portstoprime), relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(side='bottom', padx=5, pady=5)
                        
                        '''
                        self.calibvolume = tk.Spinbox(cf, from_=0, to=1000, width=4, bg=self.parent.entrycolor, bd=0)
                        self.calibvolume.pack(padx=5, side='left')
                        tk.Button(cf, text="Calibrate", command=lambda: self.parent.protocol.calibrateOutput(self.calibvolume), relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(padx=5, side='left')		
                        '''

########################################################################################################################

class CycleDuration(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		self.parent = parent

		self.config(bg=self.parent.wrapcolor)

		self.durationframe = AppWidget(self, 'Cycle Duration')

		self.renderCycleDuration()


	def renderCycleDuration(self):
                self.cdframe = tk.Frame(self.durationframe.bodyframe, bg=self.parent.framecolor)
		self.cdframe.pack()
		
		tk.Label(self.cdframe, text="Cycle", bg=self.parent.darkercolor, fg=self.parent.bodyfc).grid(row=0, column=0, sticky='we')
		tk.Label(self.cdframe, text="Duration", bg=self.parent.lightercolor, fg=self.parent.bodyfc).grid(row=0, column=1, sticky='we')

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
		
		self.ports = []
		self.protocol = []

		#self.ports.append({})
		self.protocol.append({})

		self.cmdframes = []

		self.cmdnumbers = []
		self.cmdpumps = []
		self.cmdtypes = []
		self.cycles = []
		self.names = []
		self.fromportreagents = []
		self.cb_fromportreagents = []
		self.toportreagents = []
		self.cb_toportreagents = []
		self.volumes = []
		self.speeds = []
		self.waitmins = []
		self.waitsecs = []
		self.wasteornots = []
		self.heatwhens = []
		self.temps = []
		self.statuses = []

		self.cyclecounter = 0
		self.cmdcounter = 0

		self.calibrationvolume = 0

		self.protocolframe = AppWidget(self, 'Protocol')
		
		self.frame = VerticalScrolledFrame(self.protocolframe.bodyframe, bg=self.parent.framecolor)
		self.frame.pack()

		self.sepframe = tk.Frame(self.protocolframe.bodyframe, bg=self.parent.darkentrycolor, height=2)
		self.sepframe.pack(fill='x')

		self.controlframe = tk.Frame(self.protocolframe.bodyframe, bg=self.parent.framecolor)
		self.controlframe.pack(fill='x')

		self.renderProtocol()
                self.renderProtocolControls()
                

	def updatePorts(self, pumps, ports, reagents, volumes):
		self.ports = []
		
		for i in range(len(ports)):
			self.ports.append({})
			
			self.ports[i] = {
                                        'pump': str(pumps[i]),
					'port': int(ports[i]),
					'reagent': str(reagents[i].get()),
					'volume': int(volumes[i].get())
					}
		
		self.updateCmdComboBoxes()
		
		print("Updated port list: " + str(self.ports))


	def updateCmdComboBoxes(self):
		ports = [x.get('reagent') for x in self.ports]
		for i in range(len(self.protocol)):
			self.cb_fromportreagents[i]['values'] = self.cb_toportreagents[i]['values'] = ports
		
		
	def updateProtocol(self):
		for i in range(len(self.protocol)):
                        pump = self.getPumpByReagent(self.cb_fromportreagents[i].get())
			fromport = self.getReagentPort(self.cb_fromportreagents[i].get())
			toport = self.getReagentPort(self.cb_toportreagents[i].get())
			self.protocol[i] = {
                                                'cmdnumber': int(self.cmdnumbers[i]),
						'cycle': int(self.cycles[i].get()),
                                                'type': int(self.cmdtypes[i].get()),
                                                'pump': str(pump),
						'fromport': int(fromport),
						'fromportreagent': str(self.cb_fromportreagents[i].get()),
						'toport': int(toport),
						'toportreagent': str(self.cb_toportreagents[i].get()),
						'volume': int(self.volumes[i].get()),
						'speed': int(self.speeds[i].get()),
						'waitmins': int(self.waitmins[i].get()),
						'waitsecs': int(self.waitsecs[i].get()),
                                                'heatwhen': int(self.heatwhens[i].get()),
                                                'temp': int(self.temps[i].get()),
						'waste': int(self.wasteornots[i].get()),					
						}
		#self.renderReagentVolume()
		print("Updated command list: " + str(self.protocol))


	def getReagentPort(self, reagent):
		for i in range(len(self.ports)):
			if self.ports[i].get('reagent') == reagent:
				return self.ports[i].get('port')


	def getPumpByReagent(self, reagent):
                for i in range(len(self.ports)):
			if self.ports[i].get('reagent') == reagent:
				return self.ports[i].get('pump')
		
		
	def resetProtocol(self):
		self.ports = []
		self.protocol = []
		
		self.cmdcounter = 0
		self.cyclecounter = 0

		self.cmdframes = []

		self.cmdnumbers = []
		self.cmdpumps = []
                self.cmdtypes = []
		self.cycles = []
		self.names = []
		self.fromportreagents = []
		self.cb_fromportreagents = []
		self.toportreagents = []
		self.cb_toportreagents = []
		self.volumes = []
		self.speeds = []
		self.waitmins = []
		self.waitsecs = []
		self.wasteornots = []
		self.heatwhens = []
		self.temps = []
		self.statuses = []


	def saveProtocol(self):
		self.updateProtocol()
		filename = tkFileDialog.asksaveasfilename(defaultextension='.pkl')
		if filename is None:
			return
		file = open(filename, 'wb')
		pickle.dump(self.ports, file)
		pickle.dump(self.protocol, file)
		file.close()


	def loadProtocol(self):
		filename = tkFileDialog.askopenfilename(filetypes=[('Pickled protocols', '*.pkl')])
		if filename is None:
			return
		file = open(filename, 'rb')
		ports = pickle.load(file)
		protocol = pickle.load(file)
		file.close()
		print("Loaded ports: " + str(ports))
		print("Loaded protocol: " + str(protocol))
		self.resetProtocol()
		self.ports = ports
		self.protocol = protocol
		print("Native ports: " + str(self.ports))
		print("Native protocol: " + str(self.protocol))
		self.renderProtocol()
		self.updateRenderPorts()
		#self.renderReagenVolume()


	def addCommand(self):
		print("Previous command list: "+str(self.protocol))
		self.protocol.append({})
		print("Appended command list: "+str(self.protocol))

		self.renderCommand(len(self.protocol)-1)


	def renderPort(self, i):
		self.ports.append(port)
		
		tk.Label(pumplf, text=port, bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=port+1, column=0, padx=5)
		
		reagent = tk.StringVar()
		en_reagent = tk.Entry(pumplf, textvariable=reagent, bg=self.parent.darkentrycolor, fg=self.parent.bodyfc, justify='center', width=20, bd=0)
		en_reagent.grid(row=port+1, column=1)
		
		self.reagents.append(reagent)
		
		#if self.parent.protocol.ports[port-1].get('reagent') is not None:
		#self.reagents[port-1].set(self.parent.protocol.ports[port-1].get('reagent'))
		
		if port == 9:
			self.reagents[port-1].set('Waste')
		elif port == 8:
			self.reagents[port-1].set('Output')
		elif port == 7:
			self.reagents[port-1].set('Air')
		
		volume = tk.IntVar()
		en_volume = tk.Entry(pumplf, textvariable=volume, bg=self.parent.darkentrycolor, fg=self.parent.bodyfc, justify='center', width=5, bd=0)
		en_volume.grid(row=port+1, column=2, padx=5)
		
		self.reagentvolumes.append(volume)
		
		#self.names.append(commandname)
        '''
        def renderReagentVolume(self):
               for i in range(len(self.protocol)):
                        reagents = []
                        if protocol[i].get('fromport') is not in reagents:
                                print('adding port '+str(protocol[i].get('fromport'))
                                reagents.append(protocol[i].get('fromport'))

        '''
        def updateRenderPorts(self):
                for i in range(len(self.ports)):
                        self.parent.pumpsetup.reagents[i].set(self.ports[i].get('reagent'))
                        self.parent.pumpsetup.reagentvolumes[i].set(self.ports[i].get('volume'))

	def renderPumpPorts(self, pump):
		for i in len(range(0, 9)):
			self.renderPort(i)


	def renderPumpSetup(self):
                pass
		
		
	def renderCommand(self, i):
		if i%2 == 0:
			color = self.parent.lightercolor
		else:
			color = self.parent.darkercolor

		cmdframe = tk.Frame(self.frame.interior, bg=color)
		frame = tk.Frame(cmdframe, bg=color)

		self.cmdframes.append(cmdframe)

		tk.Label(frame, text=str(i+1)+") ", bg=color, width=3, fg=self.parent.bodyfc).grid(row=0, column=0)

		self.cmdnumbers.append(i)

		tk.Label(frame, text="Cycle: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=1)
		cycle = tk.IntVar()
		sb_cycle = tk.Spinbox(frame, textvariable=cycle, from_=0, to=99, width=2, command=self.renderCycleTimes, justify='center', buttonbackground=self.parent.headcolor, bg=self.parent.darkentrycolor, bd=1, highlightthickness=0, fg=self.parent.bodyfc)
		sb_cycle.grid(row=0, column=2)

		self.cycles.append(cycle)

		if self.protocol[i].get('cycle') is not None:
			self.cycles[i].set(self.protocol[i].get('cycle')) 

		tk.Label(frame, text=" ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=3)

		ports = [x.get('reagent') for x in self.ports]
		
		fromportreagent = tk.StringVar()
		cb_fromportreagent = ttk.Combobox(frame, textvariable=fromportreagent, state='readonly', width=15)
		cb_fromportreagent['values'] = ports
		cb_fromportreagent.grid(row=0, column=4)

		self.fromportreagents.append(fromportreagent)
		self.cb_fromportreagents.append(cb_fromportreagent)
		
		if self.protocol[i].get('fromportreagent') is not None:
			self.fromportreagents[i].set(self.protocol[i].get('fromportreagent'))
		
		tk.Label(frame, text=" to ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=5)
		
		toportreagent = tk.StringVar()
		cb_toportreagent = ttk.Combobox(frame, textvariable=toportreagent, state='readonly', width=15)
		cb_toportreagent['values'] = ports
		cb_toportreagent.grid(row=0, column=6)
		
		self.toportreagents.append(toportreagent)
		self.cb_toportreagents.append(cb_toportreagent)
		
		if self.protocol[i].get('toportreagent') is not None:
			self.toportreagents[i].set(self.protocol[i].get('toportreagent'))

                tk.Label(frame, text="  ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=7)

		cmdtype = tk.IntVar()
		tk.Radiobutton(frame, text="One-way", variable=cmdtype, value=0, indicator=0, command=self.renderCycleTimes, offrelief='flat', bg=color, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=0, column=8)
		tk.Radiobutton(frame, text="Cyclic", variable=cmdtype, value=1, indicator=0, command=self.renderCycleTimes, offrelief='flat', bg=color, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=0, column=9)

		self.cmdtypes.append(cmdtype)

		if self.protocol[i].get('type') is not None:
			self.cmdtypes[i].set(self.protocol[i].get('type'))

		tk.Label(frame, text="  Volume(uL): ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=10)
		volume = tk.IntVar()
		sb_volume = tk.Spinbox(frame, textvariable=volume, from_=1, to=1000, command=self.renderCycleTimes, width=4, justify='center', buttonbackground=self.parent.headcolor, bg=self.parent.darkentrycolor, bd=1, highlightthickness=0, fg=self.parent.bodyfc)
		sb_volume.grid(row=0, column=11)

		self.volumes.append(volume)

		if self.protocol[i].get('volume') is not None:
			self.volumes[i].set(self.protocol[i].get('volume'))

                speed = tk.IntVar()
                speed.set(16)
		tk.Label(frame, text="  Speed(0-40): ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=12)
		sb_speed = tk.Spinbox(frame, textvariable=speed, from_=0, to=40, command=self.renderCycleTimes, width=3, justify='center', buttonbackground=self.parent.headcolor, bg=self.parent.darkentrycolor, bd=1, highlightthickness=0, fg=self.parent.bodyfc)
		sb_speed.grid(row=0, column=13)

		self.speeds.append(speed)

		if self.protocol[i].get('speed') is not None:
			self.speeds[i].set(self.protocol[i].get('speed'))

		tk.Label(frame, text="  Leave for: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=14)
		minutes = tk.IntVar()
		sb_timemin = tk.Spinbox(frame, textvariable=minutes, from_=0, to=600, command=self.renderCycleTimes, width=3, justify='center', buttonbackground=self.parent.headcolor, bg=self.parent.darkentrycolor, bd=1, highlightthickness=0, fg=self.parent.bodyfc)
		sb_timemin.grid(row=0, column=15)
		tk.Label(frame, text="min", bg=color, fg=self.parent.bodyfc).grid(row=0, column=16)
		seconds = tk.IntVar()
		sb_timesec = tk.Spinbox(frame, textvariable=seconds, from_=5, to=59, command=self.renderCycleTimes, width=2, justify='center', buttonbackground=self.parent.headcolor, bg=self.parent.darkentrycolor, bd=1, highlightthickness=0, fg=self.parent.bodyfc)
		sb_timesec.grid(row=0, column=17) 
		tk.Label(frame, text="sec ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=18)

		self.waitmins.append(minutes)
		self.waitsecs.append(seconds)

		if self.protocol[i].get('waitmins') is not None:
			self.waitmins[i].set(self.protocol[i].get('waitmins'))
		if self.protocol[i].get('waitsecs') is not None:
			self.waitsecs[i].set(self.protocol[i].get('waitsecs'))

		waste = tk.IntVar()
		tk.Radiobutton(frame, text="Return", variable=waste, value=0, indicator=0, offrelief='flat', bg=color, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=0, column=20)
		tk.Radiobutton(frame, text="Waste", variable=waste, value=1, indicator=0, offrelief='flat', bg=color, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=0, column=21)

		self.wasteornots.append(waste)

		if self.protocol[i].get('waste') is not None:
			self.wasteornots[i].set(self.protocol[i].get('waste'))

		tk.Label(frame, text="  T: ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=24)
		temp = tk.IntVar()
		temp.set(25)
		sb_temp = tk.Spinbox(frame, textvariable=temp, from_=0, to=40, width=3, justify='center', buttonbackground=self.parent.headcolor, bg=self.parent.darkentrycolor, bd=1, highlightthickness=0, fg=self.parent.bodyfc)
		sb_temp.grid(row=0, column=25)
                tk.Label(frame, text=u'\N{DEGREE SIGN}' + 'C ', bg=color, fg=self.parent.bodyfc).grid(row=0, column=26)
                
		self.temps.append(temp)

		heatwhen = tk.IntVar()
		tk.Radiobutton(frame, text="Heat Off", variable=heatwhen, value=0, indicator=0, offrelief='flat', bg=color, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=0, column=27)
		tk.Radiobutton(frame, text="Heat Before", variable=heatwhen, value=1, indicator=0, offrelief='flat', bg=color, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=0, column=28)
		tk.Radiobutton(frame, text="Heat After", variable=heatwhen, value=2, indicator=0, offrelief='flat', bg=color, fg=self.parent.bodyfc, selectcolor=self.parent.buttoncolor, highlightthickness=0).grid(row=0, column=29)

		self.heatwhens.append(heatwhen)

		if self.protocol[i].get('heatwhen') is not None:
			self.heatwhens[i].set(self.protocol[i].get('heatwhen'))

		tk.Label(frame, text="  -  ", bg=color, fg=self.parent.bodyfc).grid(row=0, column=30)

		status = tk.Label(frame, text="Not started", bg='white', fg='black')
		status.grid(row=0, column=31)

		self.statuses.append(status)

		frame.pack(pady=5, fill='x')
		cmdframe.grid(row=i, column=0, sticky='we')


	def renderProtocol(self):
		for i in range(len(self.protocol)):
			self.renderCommand(i)


        def renderProtocolControls(self):
                controlframeinner = tk.Frame(self.controlframe, bg=self.parent.framecolor)
                
                tk.Button(controlframeinner, text="Add Command", command=self.addCommand, width=15, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(side='left', padx=5, pady=5)
		
                tk.Label(controlframeinner, text='Delete cmd #', bg=self.parent.framecolor, fg=self.parent.bodyfc).pack(side='left')
                sb_cmd = tk.Spinbox(controlframeinner, from_=1, to=1000, width=3, justify='center', buttonbackground=self.parent.headcolor, bg=self.parent.darkentrycolor, bd=1, highlightthickness=0, fg=self.parent.bodyfc)
		sb_cmd.pack(side='left')
		tk.Button(controlframeinner, text="Delete", command=lambda: self.deleteCommand(sb_cmd.get()), width=8, relief='flat', bg=self.parent.buttoncolor, activebackground=self.parent.buttoncolor, activeforeground=self.parent.bodyfc, fg=self.parent.buttonfc, highlightthickness=0).pack(side='left', padx=5, pady=5)
		
                #tk.Label(self.controlframe, text=self.device_dict.get('/dev/ttyUSB0').syringe_ul).pack()
                #self.device_dict.get('/dev/ttyUSB0').syringe_ul = 550
                #tk.Label(self.controlframe, text=self.device_dict.get('/dev/ttyUSB0').syringe_ul).pack()

                controlframeinner.pack()
                

        def deleteCommand(self, index):
                i = int(index)-1
                
                self.cmdframes[i].destroy()
                '''
		self.cmdnumbers.pop(i)
                self.cmdtypes.pop(i)
		self.cycles.pop(i)
		self.names.pop(i)
		self.fromportreagents.pop(i)
		self.cb_fromportreagents.pop(i)
		self.toportreagents.pop(i)
		self.cb_toportreagents.pop(i)
		self.volumes.pop(i)
		self.speeds.pop(i)
		self.waitmins.pop(i)
		self.waitsecs.pop(i)
		self.wasteornots.pop(i)
		self.heatwhens.pop(i)
		self.temps.pop(i)
		self.statuses.pop(i)
                '''
                print(self.names)
                self.protocol.pop(i)
                print(self.protocol)

                
	def renderCycleTimes(self):
		#for i in len(set(self.protocol.get('cycle'))):
                self.updateProtocol()

                cdrows = self.parent.cycleduration.cdframe.winfo_children()
                for row in cdrows:
                        row.destroy()
                
		stroketimes = {0: 1.45, 1: 1.5, 2: 1.6, 3: 1.75, 4: 1.9, 5: 2.1, 6: 2.6, 7: 3,
                                 8: 3.4, 9: 3.8, 10: 4, 11: 4.6, 12: 5, 13: 6, 14: 7.6, 15: 10.5,
                                 16: 16, 17: 34, 18: 36, 19: 38, 20: 39, 21: 40, 22: 43, 23: 46,
                                 24: 49, 25: 53, 26: 57, 27: 63, 28: 69, 29: 79, 30: 88, 31: 104,
                                 32: 124, 33: 154, 34: 208, 35: 308, 36: 340, 37: 382, 39: 515, 40: 620}
		
		numcycles = len({v['cycle']:v for v in self.protocol}.values())
		print("# cycles: "+str(numcycles))
		
		for i in range(numcycles):
			time = 0
			for cmd in self.protocol:
				if cmd.get('cycle') == i:
					speed = cmd.get('speed')
					#print("speed: "+str(speed))
					volume = int(cmd.get('volume'))
					#print("volume: "+str(volume))
					vratio = volume/1000.0
					#print("vratio: "+str(vratio))

					if cmd.get('type') == 0:
                                                t1 = stroketimes.get(speed)*vratio
                                                execdelay = 8*2
                                                wait = int(cmd.get('waitmins'))*60+int(cmd.get('waitsecs'))
                                                delay = execdelay+wait
                                                tt = 2*t1+delay
                                        elif cmd.get('type') == 1:
                                                t1 = stroketimes.get(speed)*vratio
                                                t2 = stroketimes.get(30)*vratio
                                                execdelay = 8*4
                                                wait = int(cmd.get('waitmins'))*60+int(cmd.get('waitsecs'))
                                                delay = execdelay+wait
                                                tt = 3*t1+t2+delay
                                                
					#print(str(tt))
					time += tt
			print("cycle: "+str(i)+" = "+str(time)+"sec")
			tk.Label(self.parent.cycleduration.cdframe, text=str(i)+": ", bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=i+1, column=0, sticky='we')
			tk.Label(self.parent.cycleduration.cdframe, text=str(int(time))+" sec", bg=self.parent.framecolor, fg=self.parent.bodyfc).grid(row=i+1, column=1, sticky='we')
		
	def primePorts(self, pumpport, portstoprime, volume):
#               print(pumpport)
		pump = self.device_dict.get(pumpport)

		buffertime = 2
		speed = 14

		for i in range(len(portstoprime)):
			if portstoprime[i].get() == 1:
#				if tubingtypes[i].get() == 1:
#					speed = 28
#				elif tubingtypes[i].get() == 2:
#					speed = 14
				v = int(volume.get())	 
				port = i+1

				print("Priming port "+str(port)+" with "+str(v)+"uL at speed: "+str(speed))
				self.parent.log.addRecord("Priming port "+str(port)+" with "+str(v)+"uL at speed: "+str(speed))

				pump.primePort(port, v, speed, port)

				sleep(buffertime)

				print("Washing valve")
				self.parent.log.addRecord("Washing valve")
				pump.primePort(5, 400, speed, 9)

				sleep(buffertime)


	def returnPortContents(self, pumpport, portstoprime):
		pump = self.device_dict.get(pumpport)

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
				self.executeCommand(cmd['cmdnumber'])
				#self.cmdcounter += 1

		self.soundAlarm('cycle')
		self.cyclecounter += 1


	def executeCommand(self, index):
		self.updateProtocol()
		
		i = index
		tempReady = False

		status = self.statuses[i]
		status.config(bg="yellow", fg="black")
		status['text'] = 'Processing'

		pump = self.device_dict.get(self.protocol[i].get('pump'))

		name = str(self.protocol[i].get('name'))
		cmdnumber = int(self.protocol[i].get('cmdnumber'))
		cmdtype = int(self.protocol[i].get('type'))
		toport = int(self.protocol[i].get('toport'))
		toportreagent = str(self.protocol[i].get('toportreagent'))
		fromport = int(self.protocol[i].get('fromport'))
		fromportreagent = str(self.protocol[i].get('fromportreagent'))
		volume = int(self.protocol[i].get('volume')) + self.calibrationvolume
		speed = int(self.protocol[i].get('speed'))
		heatwhen = int(self.protocol[i].get('heatwhen'))
		temp = int(self.protocol[i].get('temp'))
		waitmins = int(self.protocol[i].get('waitmins'))
		waitsecs = int(self.protocol[i].get('waitsecs'))

		timebuffer = 4

		timewait = waitmins*60 + waitsecs

		waste = int(self.protocol[i].get('waste'))

		self.parent.log.addRecord("Starting command #" + str(cmdnumber+1))
		
		self.parent.log.addRecord("Desired temperature is " + str(temp) + u'\N{DEGREE SIGN}' + 'C')

                if heatwhen != 0:
                        currenttemp = self.parent.tempcontrol.getTemp()
                        self.parent.log.addRecord("Current temperature is " + str(currenttemp) + u'\N{DEGREE SIGN}' + 'C')
                        when = 'before' if heatwhen == 0 else 'after'
                        self.parent.log.addRecord("Temperature needs to be adjusted " + when + " reagent addition")

                if heatwhen == 1:
                        self.parent.log.addRecord("Adjusting temperature...")
                        self.parent.tempcontrol.startTempControl(temp)
                        while tempReady is False:
                                tempReady = self.parent.tempcontrol.tempReached(temp)
                                print("")
                                print(tempReady)
                                print("")
                                sleep(1)

                self.parent.log.addRecord("Selected pump for this command is: " + str(pump))	
                self.parent.log.addRecord("Setting pump speed to " + str(speed))
                pump.setSpeed(speed)
                sleep(2)
                
                self.parent.log.addRecord("Extracting " + str(volume) + "uL from port " + str(fromport) + " ("+fromportreagent+")")
                esttime = pump.extract(fromport, volume, execute=True)
                self.parent.log.addRecord("Estimated time: " + str(esttime) + "sec")
                sleep(esttime+timebuffer)

                self.parent.log.addRecord("Dispensing " + str(volume) + "uL to port " + str(toport) + " ("+toportreagent+")")
                esttime = pump.dispense(toport, volume, execute=True)
                sleep(esttime+timebuffer)

                #esttime = pump.executeChain()
                #print('executeChain = '+str(esttime))
                #sleep(esttime+timebuffer)

                if heatwhen == 2:
                        self.parent.log.addRecord("Adjusting temperature...")
                        self.parent.tempcontrol.startTempControl(temp)
                        while tempReady is False:
                                tempReady = self.parent.tempcontrol.tempReached(temp)
                                print("")
                                print(tempReady)
                                print("")
                                sleep(1)

                self.parent.log.addRecord("Waiting for " + str(waitmins) + "min " + str(waitsecs) + "sec")
                sleep(timewait)

                #if cyclic, reuptake to waste or back to reservoir
                if cmdtype == 1:
                        self.parent.log.addRecord("Setting pump speed to 30 for extraction")
                        pump.setSpeed(30)
                        sleep(1)
                        self.parent.log.addRecord("Extracting " + str(volume) + "uL from port " + str(toport) + " ("+toportreagent+")")
                        esttime = pump.extract(toport, volume, execute=True)
                        sleep(esttime+timebuffer)
                        self.parent.log.addRecord("Setting pump speed back to  " + str(speed))
                        pump.setSpeed(speed)
                        sleep(1)
                        if waste == 0:
                                self.parent.log.addRecord("Dispensing " + str(volume) + "uL back to port " + str(fromport) + " ("+fromportreagent+")")
                                esttime = pump.dispense(fromport, volume, execute=True)
                                sleep(esttime+timebuffer)
                        elif waste == 1:
                                self.parent.log.addRecord("Dispensing " + str(volume) + "uL to waste port 9")
                                esttime = pump.dispense(9, volume, execute=True)
                                sleep(esttime+timebuffer)

                        #esttime = pump.executeChain()
                        #sleep(esttime+timebuffer)

                if heatwhen != 0:
                        self.parent.tempcontrol.stopTempControl()

                self.parent.log.addRecord("Command #" + str(cmdnumber+1) + " is finished \n")

                status['text'] = 'Complete'
                status.config(bg='green', fg="black")

                self.soundAlarm('cmd')

                sleep(1)

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


	def soundAlarm(self, type='cmd'):
                if type == 'cmd':
                        print('cmd beep')
                elif type == 'cycle':
                        print('cycle boop')


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
	def __init__(self, parent, queue, port, baud, timeout):
		threading.Thread.__init__(self)

		self.parent = parent
		self.queue = queue
		self.port = port
		self.baud = baud
		self.timeout = timeout


	def run(self):
		s = Serial(self.port, self.baud, timeout=1)
		while True:
#			if s.inWaiting():
			cmd = s.read(5)
			print('Cmd: '+str(cmd))
			if len(cmd) > 0:
				self.parent.log.addRecord("Received serial command '" + str(cmd) + "'")
			if cmd == 'pump' or self.queue.get() == 'qpump':
				self.parent.protocol.executeCycle()

########################################################################################################################

class VerticalScrolledFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)

		self.parent = parent

		vscrollbar = tk.Scrollbar(self, orient='vertical', relief='flat', bg='#468ef2', bd=0, activerelief='flat', activebackground='#468ef2', troughcolor='#4a4a4a')
		vscrollbar.pack(fill='y', side='right', expand=False)

		canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
		canvas.pack(side='left', fill='both', expand=True)
		canvas.config(height=300, bg='#595959')
		
		
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

		def _on_mousewheel_down(event):
                        canvas.yview_scroll(1, 'units')
                def _on_mousewheel_up(event):
                        canvas.yview_scroll(-1, 'units')
                interior.bind_all('<Button-4>', _on_mousewheel_up)
                interior.bind_all('<Button-5>', _on_mousewheel_down)

########################################################################################################################

if __name__ == "__main__":

	class App(tk.Frame):
		def __init__(self, parent, *args, **kwargs):
			tk.Frame.__init__(self, parent, *args, **kwargs)

			self.headfont = ('arial', 16, 'normal')

			self.logofc = "#468ef2"
			self.headcolor = "#707070"
			self.subheadcolor = "#5e5e5e"
			self.headfc = "#e5e5e5"
			self.wrapcolor = "#212121"
			self.framecolor = "#4f4f4f"
			self.buttoncolor = "#468ef2"
			self.buttonfc = "#e5e5e5"
			self.entrycolor = "#e5e5e5"
			self.darkentrycolor = "#404040"
			#404040
			self.entryfc = "#1c1c1c"
			self.bodyfc = "#e5e5e5"
			self.lightercolor = "#595959"
			self.darkercolor = "#4a4a4a"

			self.config(bg=self.wrapcolor)

			combostyle = ttk.Style()

			combostyle.theme_create('combostyle', parent='alt',
			                         settings = {'TCombobox':
			                                     {'configure':
			                                      {
                                                               'selectbackground': self.darkentrycolor,
							       'foreground': self.bodyfc,
			                                       'fieldbackground': self.darkentrycolor,
			                                       'background': 'grey',
			                                       }}}
			                         )
			# ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
			#combostyle.theme_use('combostyle') 
			
			# show the current styles
			# print(combostyle.theme_names())

			self.parent = parent
			self.queue = Queue.Queue()

			self.c1 = tk.Frame(self, bg=self.wrapcolor).grid(row=0, column=0)
			self.c2 = tk.Frame(self, bg=self.wrapcolor).grid(row=0, column=1)
			self.c3 = tk.Frame(self, bg=self.wrapcolor).grid(row=0, column=2)

#			tk.Label(self, text="CASPA", bg=self.wrapcolor, fg=self.logofc, font=('arial', 24, 'normal')).grid(row=0, column=0, columnspan=6)

			self.protocol = Protocol(self)
			self.protocol.grid(row=1, column=0, columnspan=6, sticky='n')

			self.menu = MainMenu(self, self.parent)

			self.log = Log(self)
			self.log.grid(row=2, column=1, sticky='n')

			#self.tempcontrol = TempControl(self)
			#self.tempcontrol.grid(row=2, column=2, sticky='n')

			self.cp = ControlPanel(self)
			self.cp.grid(row=0, column=0, columnspan=6, sticky='n')

			self.pumpsetup = PumpSetup(self)
			self.pumpsetup.grid(row=2, column=0, sticky='n')

			self.cycleduration = CycleDuration(self)
			self.cycleduration.grid(row=2, column=2, sticky='n')

                        self.serialthread = SerialThread(self, self.queue, '/dev/ttyAMA0', 9600, 1)
			self.serialthread.start()


		def passQueueCmd(self):
			self.queue.put("qpump")


	root = tk.Tk()
	root.wm_title("Computer-Aided Syringe Pump Automation")

	app = App(root)
	app.pack(padx=5, pady=5)

	root.config(bg=app.wrapcolor)

	root.mainloop()
