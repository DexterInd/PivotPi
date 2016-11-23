import pivotpi
import time

# In this example we turn three servos on the PivotPi by 90 Degrees, back and forth.  

# servo.Angle(channel, degrees) will set a servo position to roughly the degrees you specify. However
# each servo is different, so if it's calibrated for one servo, it won't be the same for others.
#
# servo.AngleMicroseconds(channel, us) will set servo's pulse width in microseconds. Setting this to 0
# will disable the servo (let it float). 1500 is about center, and the range will depend on the servo.
# Typically about 750 to 2250 is safe. If you set it to a number outside of the servo range, the servo
# will try to fight it's mechanical stops, leaing to hot or burned out servos and increased battery load.
# If this is acting differently between different PivotPi boards, try adjusting the calibation frequency
# when you initialize the controller (i.e. when you call "servo = PivotPi.servo(0x40, 63.54)").
#
# servo.LED(channel, percent) will set the LED brightness in percent (0-100). Using a floating point
# percent value will increase the precision if necessary (e.g. 21.2 or 0.075). The PWM scale is 12-bit + 1
# so the 0-100 percent range is divided into 4097 values (about 0.025% per value).

# Initialise the servo controller with the right address (0x40 if both switches are low), and the frequency
# that it's actually running at. You can use 60 (target frequency), but in reality it can be off by more than 5%.
# You can leave these two parameters empty to default to address 0x40 and the target frequency of 60Hz.
servo = PivotPi.servo(0x40, 60)


print('Moving servo on channel 0-7, press Ctrl-C to quit...')
while True:
	# Move servo on channel 0-2.
	
	servo.Angle(0, 0)
	servo.Angle(1, 0)
	servo.Angle(2, 0)
	
	servo.LED(0, 0)
	servo.LED(1, 0)
	servo.LED(2, 0)
	
	time.sleep(0.5)
	
	servo.Angle(0, 90)
	servo.Angle(1, 90)
	servo.Angle(2, 90)
	
	servo.LED(0, 75)
	servo.LED(1, 75)
	servo.LED(2, 75)
	
	time.sleep(0.5)
