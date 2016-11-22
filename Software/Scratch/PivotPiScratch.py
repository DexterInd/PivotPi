#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from builtins import input

import scratch,sys,threading,math
import time
import re
import string


import sys
pivotpilib = "/home/pi/Dexter/PivotPi/Software/Python"
try:
	sys.path.insert(0, pivotpilib)
	import PivotPi
except:
	print("Cannot find PivotPi library in %" % pivotpilib)

en_debug = 1
en_pivotpi = 1
pivot = "Pivot"  # used for dictionary key in the return value


# Regex: PivotPi followed by one of Angle,Ms,PWM or LED
# followed by one digit from 0 to 7
# followed by at least one digit
# a potential % sign (0 or 1 time)

# with PWM in, in case we eventually choose to support it in Scratch
# regexpivotpi="^PivotPi(Angle|ms|PWM|LED)([1-8])([0-9]+)([%]?)"
regexpivotpi="^(Pivot|Pivot\s*LED)\s*([1-8])\s*([0-9]+|ON|OFF)\s*(%?)$"
compiled_pivotPi = re.compile(regexpivotpi, re.IGNORECASE)

# print("Lets get the party started")
servo=None

try:
	servo = PivotPi.servo(0x40, 60)
except IOError:
	print("no PivotPi Found: {}".format(servo))

def isPivotPiMsg(msg):
	'''
	Is the msg supposed to be handled by PivotPi?
	Return: Boolean 
		True if valid for PivotPi
		False otherwise
	'''
	retval = compiled_pivotPi.match(msg)

	if retval == None:
		return False
	else:
		return True

def handlePivotPi(msg):
	'''
	Scratch is sending a msg to PivotPi. 
	Use regex to validate it and take it apart
	'''

	if en_debug:
		print ("handlePivotPi Rx: {}".format(msg))

	# strip all punctuation except the % sign
	# this is overkill, taking it out
	# msg = msg.strip(string.punctuation.replace("%",""))

	retval="0"
	retdict={}

	regObj = compiled_pivotPi.match(msg)
	if regObj == None:
		print ("PivotPi command is not recognized")
		return ({pivot: "Command not recognized"})
	# else:
	# 	print ("matching done")


	if regObj:

		# print (regObj.groups())

		# remove potential spaces from within the cmd 
		cmd = regObj.group(1).lower().replace(" ","")

		port = int(regObj.group(2))-1  # port goes from 0 to 7 from now on

		# handle value. Possible incoming values are integers, "on", and "off"
		value = regObj.group(3).lower()

		try:
			# print (regObj.group(4).lower())
			modifier = regObj.group(4).lower()
		except:
			modifier=None

		if value == "On".lower():
			# if user set it to "On", then go full value
			value = 100
			modifier = "%"
		elif value == "Off".lower():
			# if set to off, then turn off
			value = 0
		else:
			value = int(value)

		# prepare returning dictionary values
		retdict["pivotcmd"]=cmd
		retdict["pivotport"]=port
		retdict["pivotvalue"]=value

	else:
		return({pivot:"unknown regex error"})


	if cmd == "Pivot".lower():
		try:
			# print ("Modifier is {}".format(modifier))
			if modifier == "%":
				value = value * 180 // 100
			if en_debug:
				print ("setting Pivot {} to angle {}".format(port+1,value))
			if en_pivotpi:
				retval = servo.Angle(port, value)
			else:
				retval = "No PivotPi"
		except :
			retdict[pivot]="Not responding"
			print("PivotPi not responding")
			return retdict

	elif cmd == "PivotLED".lower():
		if en_debug:
			print("setting LED {} to {}".format(port+1,value))
		if en_pivotpi:
			retval=servo.LED(port,value)
		else:
			retval="No PivotPi"

	# this else should never be reached
	else: 
		if en_debug:
			print("PivotPi Ignoring Command: {}".format(msg))
		retval="Unknown"

	retdict[pivot]=retval
	# if en_debug:
	# 	print(retdict)
	return (retdict)




class myThread (threading.Thread):     
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while running:
            time.sleep(.2)              # sleep for 200 ms

thread1 = myThread(1, "Thread-Pivot", 1)        #Setup and start the thread
thread1.setDaemon(True)



if __name__ == '__main__':

	connected = 0	# This variable tells us if we're successfully connected.

	while(connected == 0):
		startTime = time.time()
		try:
			s = scratch.Scratch()
			if s.connected:
				print ("PivotPi Scratch: Connected to Scratch successfully")
			connected = 1	# We are succesfully connected!  Exit Away!
			# time.sleep(1)

		except scratch.ScratchError:
			arbitrary_delay = 10 # no need to issue error statement if at least 10 seconds haven't gone by.
			if (time.time() - startTime > arbitrary_delay):  
				print ("PivotPi Scratch: Scratch is either not opened or remote sensor connections aren't enabled")
			



	try:
		s.broadcast('READY')
	except NameError:
		print ("PivotPi Scratch: Unable to Broadcast")


	while True:
		try:
			m = s.receive()
			
			while m==None or m[0] == 'sensor-update' :
				m = s.receive()
		
			msg = m[1]
			print("Rx:{}".format(msg))

			if msg == 'SETUP' :
				print ("Setting up sensors done")

			elif msg == 'START' :
				running = True
				if thread1.is_alive() == False:
					thread1.start()
				print ("Service Started")

			else:
				sensors = handlePivotPi(msg)
				s.sensorupdate(sensors)
				
		except KeyboardInterrupt:
			running= False
			print ("PivotPi Scratch: Disconnected from Scratch")
			break
		except (scratch.scratch.ScratchConnectionError,NameError) as e:
			while True:
				#thread1.join(0)
				print ("PivotPi Scratch: Scratch connection error, Retrying")
				time.sleep(5)
				try:
					s = scratch.Scratch()
					s.broadcast('READY')
					print ("PivotPi Scratch: Connected to Scratch successfully")
					break;
				except scratch.ScratchError:
					print ("PivotPi Scratch: Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n")
		except:
			e = sys.exc_info()[0]
			print ("PivotPi Scratch: Error %s" % e	)