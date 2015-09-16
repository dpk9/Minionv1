try:
	import cPickle as pickle 
except:
	import pickle
import copy

init_protocol = [{'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 1000, 'toport': 8, 'cmdnumber': 0, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 1000, 'toport': 8, 'cmdnumber': 1, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 400, 'toport': 9, 'cmdnumber': 2, 'speed': 30, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Output 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 250, 'toport': 8, 'cmdnumber': 3, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 2, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'T4 ligase mix', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 4, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 5, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 6, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 7, 'speed': 16, 'cycle': 0, 'waitmins': 45, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 400, 'toport': 9, 'cmdnumber': 8, 'speed': 30, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 9, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 10, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 11, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 12, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 13, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 14, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 15, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 750, 'toport': 8, 'cmdnumber': 16, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 900, 'toport': 9, 'cmdnumber': 17, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Output 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 18, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 19, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 20, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 250, 'toport': 8, 'cmdnumber': 21, 'speed': 16, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 1, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'cleave solution 1', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 22, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 23, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 24, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 250, 'toport': 8, 'cmdnumber': 25, 'speed': 16, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 1, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'cleave solution 1', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 26, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 27, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 28, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 250, 'toport': 8, 'cmdnumber': 29, 'speed': 16, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 2, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'cleave solution 2.1', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 30, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 31, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 32, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 250, 'toport': 8, 'cmdnumber': 33, 'speed': 16, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 2, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'cleave solution 2.1', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 34, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 35, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 36, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 1000, 'toport': 8, 'cmdnumber': 37, 'speed': 16, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 1000, 'toport': 8, 'cmdnumber': 38, 'speed': 16, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 1000, 'toport': 8, 'cmdnumber': 39, 'speed': 16, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 250, 'toport': 8, 'cmdnumber': 40, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 2, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'T4 ligase mix', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 41, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 42, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 43, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 44, 'speed': 8, 'cycle': 1, 'waitmins': 45, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 400, 'toport': 9, 'cmdnumber': 45, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 46, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 47, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 48, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 49, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 50, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 51, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 52, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 750, 'toport': 8, 'cmdnumber': 53, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}]
ports = [{'reagent': 'cleave solution 1', 'pump': '/dev/ttyUSB1', 'port': 1}, {'reagent': 'cleave solution 2.1', 'pump': '/dev/ttyUSB1', 'port': 2}, {'reagent': '1x instrument - cleave', 'pump': '/dev/ttyUSB1', 'port': 3}, {'reagent': '', 'pump': '/dev/ttyUSB1', 'port': 4}, {'reagent': '', 'pump': '/dev/ttyUSB1', 'port': 5}, {'reagent': '', 'pump': '/dev/ttyUSB1', 'port': 6}, {'reagent': 'Air 1', 'pump': '/dev/ttyUSB1', 'port': 7}, {'reagent': 'Output 1', 'pump': '/dev/ttyUSB1', 'port': 8}, {'reagent': 'Waste 1', 'pump': '/dev/ttyUSB1', 'port': 9}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 1}, {'reagent': 'T4 ligase mix', 'pump': '/dev/ttyUSB0', 'port': 2}, {'reagent': '1x instrument - ligase', 'pump': '/dev/ttyUSB0', 'port': 3}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 4}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 5}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 6}, {'reagent': 'Air 2', 'pump': '/dev/ttyUSB0', 'port': 7}, {'reagent': 'Output 2', 'pump': '/dev/ttyUSB0', 'port': 8}, {'reagent': 'Waste 2', 'pump': '/dev/ttyUSB0', 'port': 9}]

first_cycle = []

for a in range(len(init_protocol)):
    if init_protocol[a].get('cycle') == 0:
            #if init_protocol[a].get('toportreagent') == 'Output 2' and init_protocol[a].get('fromportreagent') == '1x instrument - ligase' and init_protocol[a].get('waitmins') == 0 and init_protocol[a].get('type') == 1:
            #        init_protocol[a]['waitmins'] = 55
            first_cycle.append(init_protocol[a])
        
full_cycle = []

for b in range(len(init_protocol)):
    if init_protocol[b].get('cycle') == 1:
        if init_protocol[b].get('toportreagent') == 'Output 2' and init_protocol[b].get('fromportreagent') == '1x instrument - ligase' and init_protocol[b].get('waitmins') == 0 and init_protocol[b].get('type') == 1:
                init_protocol[b]['waitmins'] = 5
        full_cycle.append(init_protocol[b])

#full_cycle.extend(first_cycle)

#print full_cycle

full_protocol = []
full_protocol.extend(first_cycle)

print full_protocol

cmdnum = len(first_cycle)

for i in range (0, 6):
    corrected_full_cycle = copy.deepcopy(full_cycle)
    for j in range(len(full_cycle)):
        corrected_full_cycle[j]['cmdnumber'] = cmdnum
        cmdnum += 1
        corrected_full_cycle[j]['cycle'] = i+1
    full_protocol.extend(corrected_full_cycle)


filename = 'Aug26-v2.pkl'

file = open(filename, 'wb')
pickle.dump(ports, file)
pickle.dump(full_protocol, file)
file.close()
