''' 
In this project we show you how to Animate an Elf on a Shelf with the PivotPi, a Raspberry Pi Servo Controller, making it a smart Elf.  We'll attach a small servo to the Elf's arm to make it wave, we'll use a distance sensor to see if anyone is close to the Elf on a Shelf, and we will tie it all together with the Raspberry Pi and GrovPi Zero.

See more about the PivotPi: https://www.dexterindustries.com/pivotpi

See the written project here:   https://www.dexterindustries.com/projects/animate-elf-shelf-raspberry-pi-servo-controller

'''

When someone approaches, the Elf will begin enthusiastically waving!  This project will demonstrate how to easily add motion to an otherwise lifeless Elf and other toys.

from __future__ import print_function
from __future__ import division
from builtins import input

import time

import pivotpi
import grovepi

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 3

# angle(channel, degrees) will set a servo position to roughly the degrees you specify. However
# each servo is different, so if it's calibrated for one servo, it won't be the same for others.
#
# led(channel, percent) will set the LED brightness in percent (0-100). Using a floating point
# percent value will increase the precision if necessary (e.g. 21.2 or 0.075). The PWM scale is 12-bit + 1
# so the 0-100 percent range is divided into 4096 values (about 0.025% per value).

# Initialise the PivotPi servo controller with the right address (0x40 if both switches are low), and the frequency
# that it's actually running at. You can use 60 (target frequency).

try:
    pivotpi = pivotpi.PivotPi(0x40, 60)
except:
    print("PivotPi not found - quitting")
    exit(-1)

print('The Elf is Live! Press Ctrl-C to quit...')

while True:
    try:
        # Read distance value from Ultrasonic
		distance = grovepi.ultrasonicRead(ultrasonic_ranger)
		
		if distance < 50:
				print("Distance: " + str(distance))
				pivotpi.angle(0, 160)		# Set the angle to 160.
				pivotpi.led(0, 0)		# Set the LED power to 0%.
				time.sleep(0.5)

				pivotpi.angle(0, 0)		# Set the angle to 0.
				pivotpi.led(0, 100)		# Set the LED power to 100%.
				time.sleep(0.5)
		else:
			print("Distance: " + str(distance))
    except TypeError:
        print ("Error")
    except IOError:
        print ("Error")
