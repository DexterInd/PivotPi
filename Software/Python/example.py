#!/usr/bin/env python
#
# This is an example for controlling servo's and onboard LED's with the PivotPi (https://www.dexterindustries.com/Pivotpi/)
'''
## License
The code here is Licensed under  The MIT License (MIT) . Please review the  LICENSE.md file or (here)[https://github.com/DexterInd/Raspbian_For_Robots/blob/master/LICENSE.md] for more information
Copyright (C) 2016 Dexter Industries
'''

from __future__ import print_function
from __future__ import division
from builtins import input



# angle(channel, degrees) will set a servo position to roughly the degrees you specify. However
# each servo is different, so if it's calibrated for one servo, it won't be the same for others.
#
# angle_microseconds(channel, us) will set servo's pulse width in microseconds. Setting this to 0
# will disable the servo (let it float). 1500 is about center, and the range will depend on the servo.
# Typically about 750 to 2250 is safe. If you set it to a number outside of the servo range, the servo
# will try to fight it's mechanical stops, leaing to hot or burned out servos and increased battery load.
# If this is acting differently between different PivotPi boards, try adjusting the calibation frequency
# when you initialize the controller (i.e. when you call "pivotpi = PivotPi.servo(0x40, 60)").
#
# led(channel, percent) will set the LED brightness in percent (0-100). Using a floating point
# percent value will increase the precision if necessary (e.g. 21.2 or 0.075). The PWM scale is 12-bit + 1
# so the 0-100 percent range is divided into 4096 values (about 0.025% per value).

# Initialise the PivotPi servo controller with the right address (0x40 if both switches are low), and the frequency
# that it's actually running at. You can use 60 (target frequency), but in reality it can be off by more than 5%.
# You can leave these two parameters empty to default to address 0x40 and the target frequency of 60Hz.

import time
import pivotpi

# Setup the PivotPi
try:
    pivotpi = pivotpi.PivotPi(0x40, 60)
except IOError:
    print("PivotPi not found - quitting")
    exit(-1)
except: 
    print("Unknown error with PivotPi. Is there a problem with the library?")
    exit(-1)

print('Moving servos on channel 1-8, press Ctrl-C to quit...')
try:
    while True:
        for i in range (8):
            #pivotpi.angle(i, 0)
            pivotpi.led(i, 0)                       # Set the LED to 0 Power
            pivotpi.angle_microseconds(i, 1500)     # Set the Servo to 1500 angle
            time.sleep(0.05)        
        for i in range (8):
            #pivotpi.angle(i, 180)
            pivotpi.led(i, (i + 1) * 4)             # Increase the LED Power
            pivotpi.angle_microseconds(i, 550 + (i * 272))  # Change the pivotpi Angle
            time.sleep(0.05)                        # Give the system a rest.
except KeyboardInterrupt:
    print("\nGoodbye")
except:
    print("Unknown error")
