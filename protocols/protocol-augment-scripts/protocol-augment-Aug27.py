try:
	import cPickle as pickle 
except:
	import pickle
import copy

init_protocol = [{'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 800, 'toport': 9, 'cmdnumber': 0, 'speed': 30, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 250, 'toport': 8, 'cmdnumber': 1, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 350, 'toport': 9, 'cmdnumber': 2, 'speed': 30, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 250, 'toport': 8, 'cmdnumber': 3, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 2, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'T4 ligase mix', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 4, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 5, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 6, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 100, 'toport': 9, 'cmdnumber': 7, 'speed': 8, 'cycle': 0, 'waitmins': 45, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 350, 'toport': 9, 'cmdnumber': 8, 'speed': 30, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 9, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 10, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 11, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 12, 'speed': 8, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 250, 'toport': 8, 'cmdnumber': 13, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 250, 'toport': 8, 'cmdnumber': 14, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 15, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 16, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 17, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 1000, 'toport': 8, 'cmdnumber': 18, 'speed': 16, 'cycle': 0, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 1, 'type': 1}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 800, 'toport': 9, 'cmdnumber': 19, 'speed': 30, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 2', 'volume': 750, 'toport': 8, 'cmdnumber': 20, 'speed': 16, 'cycle': 0, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Imaging buffer', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 800, 'toport': 9, 'cmdnumber': 21, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 800, 'toport': 8, 'cmdnumber': 22, 'speed': 20, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 850, 'toport': 9, 'cmdnumber': 23, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 300, 'toport': 8, 'cmdnumber': 24, 'speed': 20, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 1, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 350, 'toport': 9, 'cmdnumber': 25, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 300, 'toport': 8, 'cmdnumber': 26, 'speed': 20, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 1, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 350, 'toport': 9, 'cmdnumber': 27, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 800, 'toport': 8, 'cmdnumber': 28, 'speed': 20, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2 - part 1', 'volume': 800, 'toport': 2, 'cmdnumber': 29, 'speed': 21, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 2, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2 - part 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2.1', 'volume': 280, 'toport': 4, 'cmdnumber': 30, 'speed': 20, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 2, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2 - part 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2.1', 'volume': 500, 'toport': 4, 'cmdnumber': 31, 'speed': 20, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Air 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 4000, 'toport': 9, 'cmdnumber': 32, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2 - part 2', 'volume': 800, 'toport': 3, 'cmdnumber': 33, 'speed': 21, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2 - part 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2.1', 'volume': 750, 'toport': 4, 'cmdnumber': 34, 'speed': 20, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2 - part 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2.1', 'volume': 500, 'toport': 4, 'cmdnumber': 35, 'speed': 20, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Air 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2.1', 'volume': 4000, 'toport': 4, 'cmdnumber': 36, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Air 1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 900, 'toport': 9, 'cmdnumber': 37, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Cleave solution 2.1', 'volume': 800, 'toport': 4, 'cmdnumber': 38, 'speed': 21, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2.1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 300, 'toport': 8, 'cmdnumber': 39, 'speed': 20, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2.1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 350, 'toport': 9, 'cmdnumber': 40, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 300, 'toport': 8, 'cmdnumber': 41, 'speed': 20, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2.1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 350, 'toport': 9, 'cmdnumber': 42, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 1000, 'toport': 9, 'cmdnumber': 43, 'speed': 16, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'Cleave solution 2.1', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 4000, 'toport': 9, 'cmdnumber': 44, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 6, 'pump': '/dev/ttyUSB1', 'fromportreagent': 'dH2O - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 1', 'volume': 4000, 'toport': 9, 'cmdnumber': 45, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 800, 'toport': 8, 'cmdnumber': 46, 'speed': 20, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 900, 'toport': 9, 'cmdnumber': 47, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 800, 'toport': 8, 'cmdnumber': 48, 'speed': 20, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 900, 'toport': 9, 'cmdnumber': 49, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Output 1', 'volume': 800, 'toport': 8, 'cmdnumber': 50, 'speed': 20, 'cycle': 1, 'waitmins': 5, 'temp': 25, 'heatwhen': 0, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'fromportreagent': '1x instrument - cleave', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 900, 'toport': 9, 'cmdnumber': 51, 'speed': 30, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'Output 2', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 52, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 4, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'dH2O - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 53, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 4, 'pump': '/dev/ttyUSB0', 'fromportreagent': 'dH2O - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 54, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 55, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}, {'waitsecs': 5, 'toportreagent': 'Waste 2', 'volume': 1000, 'toport': 9, 'cmdnumber': 56, 'speed': 8, 'cycle': 1, 'waitmins': 0, 'temp': 25, 'heatwhen': 0, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'fromportreagent': '1x instrument - ligase', 'waste': 0, 'type': 0}]


ports = [{'reagent': 'Cleave solution 1', 'pump': '/dev/ttyUSB1', 'port': 1}, {'reagent': 'Cleave solution 2 - part 1', 'pump': '/dev/ttyUSB1', 'port': 2}, {'reagent': 'Cleave solution 2 - part 2', 'pump': '/dev/ttyUSB1', 'port': 3}, {'reagent': 'Cleave solution 2.1', 'pump': '/dev/ttyUSB1', 'port': 4}, {'reagent': '1x instrument - cleave', 'pump': '/dev/ttyUSB1', 'port': 5}, {'reagent': 'dH2O - cleave', 'pump': '/dev/ttyUSB1', 'port': 6}, {'reagent': 'Air 1', 'pump': '/dev/ttyUSB1', 'port': 7}, {'reagent': 'Output 1', 'pump': '/dev/ttyUSB1', 'port': 8}, {'reagent': 'Waste 1', 'pump': '/dev/ttyUSB1', 'port': 9}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 1}, {'reagent': 'T4 ligase mix', 'pump': '/dev/ttyUSB0', 'port': 2}, {'reagent': '1x instrument - ligase', 'pump': '/dev/ttyUSB0', 'port': 3}, {'reagent': 'dH2O - ligase', 'pump': '/dev/ttyUSB0', 'port': 4}, {'reagent': 'Imaging buffer', 'pump': '/dev/ttyUSB0', 'port': 5}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 6}, {'reagent': 'Air 2', 'pump': '/dev/ttyUSB0', 'port': 7}, {'reagent': 'Output 2', 'pump': '/dev/ttyUSB0', 'port': 8}, {'reagent': 'Waste 2', 'pump': '/dev/ttyUSB0', 'port': 9}]




cleave_cycle = []

for b in range(len(init_protocol)):
    if init_protocol[b].get('cycle') == 1:
        cleave_cycle.append(copy.deepcopy(init_protocol[b]))


ligate_cycle = []

for a in range(len(init_protocol)):
    if init_protocol[a].get('cycle') == 0:
            ligate_cycle.append(copy.deepcopy(init_protocol[a]))


full_protocol = []
full_protocol.extend(ligate_cycle)


cmdnum = len(ligate_cycle)

for i in range (0, 5):
    #print i

    corrected_ligate_cycle = copy.deepcopy(ligate_cycle)
    corrected_cleave_cycle1 = copy.deepcopy(cleave_cycle)

    for j in range(len(cleave_cycle)):
        corrected_cleave_cycle1[j]['cmdnumber'] = cmdnum
        cmdnum += 1
        corrected_cleave_cycle1[j]['cycle'] = i+1

    full_protocol.extend(corrected_cleave_cycle1)
    
    for l in range(len(ligate_cycle)):
        corrected_ligate_cycle[l]['cmdnumber'] = cmdnum
        cmdnum += 1
        corrected_ligate_cycle[l]['cycle'] = i+1
        
    full_protocol.extend(corrected_ligate_cycle)

print('\n\n\n')
print 'full 0'
print full_protocol[0]
print len(full_protocol)

#print cleave_cycle

for cmd in range(len(full_protocol)):
        print cmd


filename = 'FISSEQ-Aug29-mixCleave.pkl'

file = open(filename, 'wb')
pickle.dump(ports, file)
pickle.dump(full_protocol, file)
file.close()


