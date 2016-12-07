from __future__ import print_function
from __future__ import division
from builtins import input


# In this example we turn three servos on the PivotPi by 90 Degrees, back and forth.  

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

from time import sleep
from pivotpi import *

try:
    pivotpi = PivotPi(0x40, 60)
except:
    print ("PivotPi not found - quitting ")
    exit(-1)


print('Moving servos on channels 1-3, press Ctrl-C to quit...')
while True:
    pivotpi.angle(SERVO_1, 0)
    pivotpi.angle(SERVO_2, 0)
    pivotpi.angle(SERVO_3, 0)
    
    pivotpi.led(SERVO_1, 0)
    pivotpi.led(SERVO_2, 0)
    pivotpi.led(SERVO_3, 0)
    
    sleep(0.5)
    
    pivotpi.angle(SERVO_1, 90)
    pivotpi.angle(SERVO_2, 90)
    pivotpi.angle(SERVO_3, 90)
    
    pivotpi.led(SERVO_1, 75)
    pivotpi.led(SERVO_2, 75)
    pivotpi.led(SERVO_3, 75)
    
    sleep(0.5)
