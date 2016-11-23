import pivotpi
import time

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
servo = PivotPi.servo(0x40, 63.54)
#servo2 = PivotPi.servo(0x41, 60.11)
#servo3 = PivotPi.servo(0x42, 59.04)

print('Moving servo on channel 0-7, press Ctrl-C to quit...')
while True:
    # Move servo on channel 0-7.
    
    for i in range (8):
        #servo.Angle(i, 0)
        servo.LED(i, 0)
        servo.AngleMicroseconds(i, 1500)
        time.sleep(0.05)
#    for i in range (8):
#        #servo.Angle(i, 0)
#        servo2.LED(i, 0)
#        servo2.AngleMicroseconds(i, 1500)
#        time.sleep(0.05)
#    for i in range (8):
#        #servo.Angle(i, 0)
#        servo3.LED(i, 0)
#        servo3.AngleMicroseconds(i, 1500)
#        time.sleep(0.05)
    for i in range (8):
        #servo.Angle(i, 180)
        servo.LED(i, (i + 1) * 4)
        servo.AngleMicroseconds(i, 550 + (i * 272))
        time.sleep(0.05)
#    for i in range (8):
#        #servo.Angle(i, 180)
#        servo2.LED(i, (i + 9) * 4)
#        servo2.AngleMicroseconds(i, 550 + (i * 272))
#        time.sleep(0.05)
#    for i in range (8):
#        #servo.Angle(i, 180)
#        servo3.LED(i, (i + 17) * 4)
#        servo3.AngleMicroseconds(i, 550 + (i * 272))
#        time.sleep(0.05)
