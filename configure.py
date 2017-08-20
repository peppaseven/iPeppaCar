import json
import os.path

data={}

data["CTRIG"] = 4 # default pin for center sonar trigger
data["CECHO"] = 17 # default pin for center sonar echo
if os.path.isfile('robot.conf'):
	with open('robot.conf') as data_file:
		data = json.load(data_file)
else:
	print("Couldn't find robot.conf file, using default configuration")
