from __future__ import print_function
from __future__ import division
from builtins import input

import time     # for reference to elapsed time, and for delays
import colorsys # for RGB to HSV conversion

import pivotpi  # import the PivotPi drivers
import brickpi3 # import the BrickPi3 drivers

pivotpi = pivotpi.PivotPi(0x40, 63.54) # Use PivotPi I2C address 0x40, and set the calibration frequency to 63.54Hz (unique to each PivotPi)

BP = brickpi3.BrickPi3()

COLOR_SENSOR_PORT = BP.PORT_1 # Color sensor on BrickPi sensor port 1
TOUCH_SENSOR_PORT = BP.PORT_2 # Touch sensor on BrickPi sensor port 1
BELT_MOTOR_PORT   = BP.PORT_A # Belt motor on BrickPi motor port A
ARM_SERVO         = 0         # Arm servo on PivotPi servo channel 1

BP.set_sensor_type(COLOR_SENSOR_PORT, BP.SENSOR_TYPE.NXT_COLOR_FULL) # Configure for an NXT color sensor on BrickPi sensor port 1.
BP.set_sensor_type(TOUCH_SENSOR_PORT, BP.SENSOR_TYPE.TOUCH)          # Configure for a touch sensor on BrickPi sensor port 2.

# Tell the arm to be extended or retracted
def Arm(Position):
    if Position:
        pivotpi.angle_microseconds(ARM_SERVO, 1250)
    else:
        pivotpi.angle_microseconds(ARM_SERVO, 1450)

# Scale a value from one range to another
def ScaleRange(OldValue, OldMin, OldMax, NewMin, NewMax):
    return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

# Clip a value to a range
def ClipRange(OldValue, Min, Max):
    if OldValue < Min:
        return Min
    if OldValue > Max:
        return Max
    return OldValue

# Scale a value to a range and clip the result
def ScaleClipRange(OldValue, OldMin, OldMax, NewMin, NewMax):
    return ClipRange(ScaleRange(OldValue, OldMin, OldMax, NewMin, NewMax), NewMin, NewMax)

# Get the color of an M&M on the belt
def GetMMColor():
    r = 0
    g = 0
    b = 0
    h = 0
    s = 0
    v = 0.01
    
    v_max = 0.00
    
    R = 0
    G = 0
    B = 0
    H = 0
    S = 0
    V = 0
    while((R == r and G == g and B == b) or v > v_max): # while RGB is the same (the sensor readings haven't been updated) or it's brighter than last reading (M&M getting closer to the sensor)
        if(v > v_max): # If it's brighter than last time, update the values
            R = r
            G = g
            B = b
            H = h
            S = s
            V = v
            v_max = v
        values, error = BP.get_sensor(COLOR_SENSOR_PORT) # read the color sensor
        if not error:
            r = ScaleClipRange(values[1], 123, 534, 0.0, 1.0) # calibrate and normalize the Red (the calibration will vary between sensors)
            g = ScaleClipRange(values[2], 116, 416, 0.0, 1.0) #              ''             Green                  ''
            b = ScaleClipRange(values[3], 107, 414, 0.0, 1.0) #              ''             Blue                   ''
            hsv = colorsys.rgb_to_hsv(r, g, b)                # Convert the RGB values to HSV values
            [h, s, v] = list(hsv)
            #print("%4.2f %4.2f %4.2f   %4.2f %4.2f %4.2f" % (r, g, b, h, s, v))
        else:
            return 0
        time.sleep(0.007) # Give the BrickPi time to update the color sensor values
    
    # red
    if(V >= 0.63 and V <= 0.81 and (H <= 0.05 or H >= 0.97)):
        return 1
    
    # orange
    if(V >= 0.89 and (H <= 0.04 or H >= 0.97)):
        return 2
    
    # yellow
    if(V >= 0.90 and H <= 0.18 and H >= 0.12):
        return 3
    
    # green
    if(V >= 0.65 and H <= 0.37 and H >= 0.29):
        return 4
    
    # blue
    if(V >= 0.8 and H <= 0.62 and H >= 0.54):
        return 5
    
    # brown
    if(R >= 0.25 and V <= 0.42 and G >= 0.12 and B >= 0.12):
        return 6
    
    return 0 # no color detected

print('Sorting M&Ms. Press Ctrl-C to stop...')

ColorList = ["None", "Red", "Orange", "Yellow", "Green", "Blue", "Brown"]

ColorMMLast = 0
ArmReturn = 0
try:
    # Start with the arm retracted
    Arm(False)
    while True:
        # Get the current time in milliseconds
        millis = int(round(time.time() * 1000))
        
        # Run the motor while the touch sensor is pressed
        if(BP.get_sensor(TOUCH_SENSOR_PORT)[0]):
            BP.set_motor_speed(BELT_MOTOR_PORT, -50)
        else:
            BP.set_motor_speed(BELT_MOTOR_PORT, 0)
        
        # Sort the M&M's based on color
        ColorMM = GetMMColor()                    # Get the M&M color
        if ColorMM != ColorMMLast:                # If new color
            ColorMMLast = ColorMM
            if ColorMM != 0:                      # M&M color detected
                print(ColorList[ColorMM])         # Print the color detected
                if(ColorMM == 1 or ColorMM == 4): # if it's red or green
                    Arm(True)                     # Make the arm grab the M&M off the belt
                    ArmReturn = millis + 400      # Keep the arm in place for 0.4 seconds
                time.sleep(0.1)                   # Slow down a bit so that a single M&M won't read as multiple colors
        
        # Check if it's time to make the arm return
        if(ArmReturn and ArmReturn <= millis):    # After the specified time
            Arm(False)                            # Return the arm
            ArmReturn = 0

except KeyboardInterrupt:                         # On keyboard interrupt
    pivotpi.angle_microseconds(ARM_SERVO, 0)      # Make the arm servo float
    BP.reset_all()                                # Reset the BrickPi motor and sensors
    print('exiting')