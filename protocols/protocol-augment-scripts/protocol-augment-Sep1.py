try:
	import cPickle as pickle 
except:
	import pickle
import copy

init_protocol = [{'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 0, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 1, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 2', 'heatwhen': 0, 'volume': 250, 'fromport': 2, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 8, 'cmdnumber': 2, 'waste': 0, 'speed': 16, 'fromportreagent': 'T4 ligase mix', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 2', 'heatwhen': 0, 'volume': 35, 'fromport': 7, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 8, 'cmdnumber': 3, 'waste': 0, 'speed': 25, 'fromportreagent': 'Air 2', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 4, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 5, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 6, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 7, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 45, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 8, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 350, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 9, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 10, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 11, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 12, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 13, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 2', 'heatwhen': 0, 'volume': 250, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 1, 'toport': 8, 'cmdnumber': 14, 'waste': 1, 'speed': 16, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 1, 'toport': 9, 'cmdnumber': 15, 'waste': 1, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 2', 'heatwhen': 0, 'volume': 250, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 1, 'toport': 8, 'cmdnumber': 16, 'waste': 1, 'speed': 16, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 1, 'toport': 9, 'cmdnumber': 17, 'waste': 1, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 2', 'heatwhen': 0, 'volume': 250, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 1, 'toport': 8, 'cmdnumber': 18, 'waste': 1, 'speed': 16, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 1, 'toport': 9, 'cmdnumber': 19, 'waste': 1, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 500, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 20, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 2', 'heatwhen': 0, 'volume': 250, 'fromport': 5, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 8, 'cmdnumber': 21, 'waste': 0, 'speed': 16, 'fromportreagent': 'Imaging buffer', 'cycle': 0}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 500, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 22, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 1', 'heatwhen': 0, 'volume': 700, 'fromport': 1, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 1, 'cmdnumber': 23, 'waste': 0, 'speed': 21, 'fromportreagent': 'Cleave solution 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 1, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 24, 'waste': 0, 'speed': 20, 'fromportreagent': 'Cleave solution 1', 'cycle': 1}, {'waitmins': 5, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 35, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 25, 'waste': 0, 'speed': 25, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 400, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 26, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 1, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 27, 'waste': 0, 'speed': 20, 'fromportreagent': 'Cleave solution 1', 'cycle': 1}, {'waitmins': 5, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 35, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 28, 'waste': 0, 'speed': 25, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 400, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 29, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 6, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 30, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 6, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 31, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 32, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 33, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 34, 'waste': 0, 'speed': 20, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 1', 'heatwhen': 0, 'volume': 700, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 1, 'cmdnumber': 35, 'waste': 0, 'speed': 21, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave 2 part 1', 'heatwhen': 0, 'volume': 700, 'fromport': 2, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 2, 'cmdnumber': 36, 'waste': 0, 'speed': 21, 'fromportreagent': 'Cleave 2 part 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 270, 'fromport': 2, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 37, 'waste': 0, 'speed': 20, 'fromportreagent': 'Cleave 2 part 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 700, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 38, 'waste': 0, 'speed': 21, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave 2 part 1', 'heatwhen': 0, 'volume': 700, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 2, 'cmdnumber': 39, 'waste': 0, 'speed': 21, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 6, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 40, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 6, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 41, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 42, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 43, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave 2 part 2', 'heatwhen': 0, 'volume': 700, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 3, 'cmdnumber': 44, 'waste': 0, 'speed': 21, 'fromportreagent': 'Cleave 2 part 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 750, 'fromport': 3, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 45, 'waste': 0, 'speed': 20, 'fromportreagent': 'Cleave 2 part 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 700, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 46, 'waste': 0, 'speed': 21, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave 2 part 2', 'heatwhen': 0, 'volume': 700, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 3, 'cmdnumber': 47, 'waste': 0, 'speed': 21, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 4500, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 48, 'waste': 0, 'speed': 8, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 500, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 49, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 700, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 50, 'waste': 0, 'speed': 21, 'fromportreagent': 'Cleave solution 2.1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 51, 'waste': 0, 'speed': 20, 'fromportreagent': 'Cleave solution 2.1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 35, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 52, 'waste': 0, 'speed': 25, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 5, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 700, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 53, 'waste': 0, 'speed': 21, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 400, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 54, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 700, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 55, 'waste': 0, 'speed': 21, 'fromportreagent': 'Cleave solution 2.1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 56, 'waste': 0, 'speed': 20, 'fromportreagent': 'Cleave solution 2.1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 35, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 57, 'waste': 0, 'speed': 25, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 5, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Cleave solution 2.1', 'heatwhen': 0, 'volume': 700, 'fromport': 7, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 4, 'cmdnumber': 58, 'waste': 0, 'speed': 21, 'fromportreagent': 'Air 1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 400, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 59, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 2000, 'fromport': 4, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 60, 'waste': 0, 'speed': 16, 'fromportreagent': 'Cleave solution 2.1', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 6, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 61, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 6, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 62, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 63, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 1', 'heatwhen': 0, 'volume': 4000, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 9, 'cmdnumber': 64, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 5, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 65, 'waste': 0, 'speed': 20, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 500, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 66, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 5, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 67, 'waste': 0, 'speed': 20, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 500, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 68, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 5, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 69, 'waste': 0, 'speed': 20, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 500, 'fromport': 8, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 70, 'waste': 0, 'speed': 30, 'fromportreagent': 'Output 2', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 4, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 71, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 4, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 72, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 4, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 73, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 4, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 74, 'waste': 0, 'speed': 8, 'fromportreagent': 'dH2O - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 75, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 76, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 77, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 78, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Waste 2', 'heatwhen': 0, 'volume': 1000, 'fromport': 3, 'pump': '/dev/ttyUSB0', 'type': 0, 'toport': 9, 'cmdnumber': 79, 'waste': 0, 'speed': 8, 'fromportreagent': '1x instrument - ligase', 'cycle': 1}, {'waitmins': 0, 'waitsecs': 5, 'temp': 25, 'toportreagent': 'Output 1', 'heatwhen': 0, 'volume': 300, 'fromport': 5, 'pump': '/dev/ttyUSB1', 'type': 0, 'toport': 8, 'cmdnumber': 80, 'waste': 0, 'speed': 20, 'fromportreagent': '1x instrument - cleave', 'cycle': 1}]

for cmd in init_protocol:
        if cmd['cycle'] == 0:
                print '#', cmd['cmdnumber'], ' ', cmd['fromportreagent'], ' to ', cmd['toportreagent'], ' - ', cmd['volume'], 'uL'

wash1 = copy.copy(init_protocol[14])
wash2 = copy.copy(init_protocol[15])
wash2['volume'] = 750
wash2['type'] = 0
wash = []
wash.append(wash1)
wash.append(wash2)
print wash

first_half = init_protocol[:20]
second_half = init_protocol[20:]


full_protocol = []
full_protocol.extend(first_half)

for i in range(20):
        full_protocol.extend(copy.deepcopy(wash))
        
full_protocol.extend(second_half)

for i in range(len(full_protocol)):
        full_protocol[i]['cmdnumber'] = i

print '___________________________________________'

#print full_protocol


for cmd in full_protocol:
        if cmd['cycle'] == 0 or cmd['cycle'] == 1:
                print '#', cmd['cmdnumber'], ' ', cmd['fromportreagent'], ' to ', cmd['toportreagent'], ' - ', cmd['volume'], 'uL for ', cmd['waitmins']


print '--------------------------------------------------'

wash1 = copy.copy(full_protocol[105])
wash1['waitmins'] = 0
wash2 = copy.copy(full_protocol[106])

wash = []
wash.append(wash1)
wash.append(wash2)

print wash

first_half = full_protocol[:105]
second_half = full_protocol[111:]


full_protocol = []
full_protocol.extend(first_half)

for i in range(10):
        full_protocol.extend(copy.deepcopy(wash))
full_protocol.extend(second_half)

print '___________________________________________'

for cmd in full_protocol:
        if cmd['cycle'] == 1:
                print '#', cmd['cmdnumber'], ' ', cmd['fromportreagent'], ' to ', cmd['toportreagent'], ' - ', cmd['volume'], 'uL for ', cmd['waitmins']


ports = [{'reagent': 'Cleave solution 1', 'pump': '/dev/ttyUSB1', 'port': 1}, {'reagent': 'Cleave 2 part 1', 'pump': '/dev/ttyUSB1', 'port': 2}, {'reagent': 'Cleave 2 part 2', 'pump': '/dev/ttyUSB1', 'port': 3}, {'reagent': 'Cleave solution 2.1', 'pump': '/dev/ttyUSB1', 'port': 4}, {'reagent': '1x instrument - cleave', 'pump': '/dev/ttyUSB1', 'port': 5}, {'reagent': 'dH2O - cleave', 'pump': '/dev/ttyUSB1', 'port': 6}, {'reagent': 'Air 1', 'pump': '/dev/ttyUSB1', 'port': 7}, {'reagent': 'Output 1', 'pump': '/dev/ttyUSB1', 'port': 8}, {'reagent': 'Waste 1', 'pump': '/dev/ttyUSB1', 'port': 9}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 1}, {'reagent': 'T4 ligase mix', 'pump': '/dev/ttyUSB0', 'port': 2}, {'reagent': '1x instrument - ligase', 'pump': '/dev/ttyUSB0', 'port': 3}, {'reagent': 'dH2O - ligase', 'pump': '/dev/ttyUSB0', 'port': 4}, {'reagent': 'Imaging buffer', 'pump': '/dev/ttyUSB0', 'port': 5}, {'reagent': '', 'pump': '/dev/ttyUSB0', 'port': 6}, {'reagent': 'Air 2', 'pump': '/dev/ttyUSB0', 'port': 7}, {'reagent': 'Output 2', 'pump': '/dev/ttyUSB0', 'port': 8}, {'reagent': 'Waste 2', 'pump': '/dev/ttyUSB0', 'port': 9}]


init_protocol = copy.deepcopy(full_protocol)


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

for i in range (0, 10, 2):
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
        corrected_ligate_cycle[l]['cycle'] = i+2
        
    full_protocol.extend(corrected_ligate_cycle)

print('\n\n\n')
print 'full 0'
print full_protocol[0]
print len(full_protocol)

#print cleave_cycle

for cmd in range(len(full_protocol)):
        print cmd


filename = 'FISSEQ-Sep1-smallWashes-mixCleave.pkl'

file = open(filename, 'wb')
pickle.dump(ports, file)
pickle.dump(full_protocol, file)
file.close()


