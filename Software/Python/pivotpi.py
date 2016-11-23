import PCA9685

SERVO_1 = 0
SERVO_2 = 1
SERVO_3 = 2
SERVO_4 = 3
SERVO_5 = 4
SERVO_6 = 5
SERVO_7 = 6
SERVO_8 = 7

#map 0-180 to pulse length between 150-600
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

class servo(object):
    servo_controller=None
    addr_00=0x40
    addr_01=0x41
    addr_10=0x42
    addr_11=0x43
    
    # Configure min and max servo pulse lengths
    servo_min = 150  # Min pulse length out of 4096
    servo_max = 600  # Max pulse length out of 4096
    frequency = 60;
    def __init__(self, addr = 0x40, actual_frequency = 60):# Set the address and optionally the PWM frequency, which should be 60Hz, but can be off by at least 5%. One measures at about 59.1, one at about 60.1, and one at about 63.5Hz.
        try:
            self.servo_controller = PCA9685.PCA9685(address=addr)
            self.frequency = actual_frequency;
            
            # Set frequency to 60hz, good for servos.
            self.servo_controller.set_pwm_freq(60)
        except:
            # pass
            raise IOError("PivotPi not connected")
        return
    
    def PWM(self, channel, on, off):
        try:
            self.servo_controller.set_pwm(channel, on, off)
        except:
            raise IOError("PivotPi not connected")
    
    def Angle(self, channel, angle):
        if angle >= 0 and angle <= 180 and channel >= 0 and channel <= 7:
            pwm_to_send = 4095 - translate(angle, 0, 180, self.servo_min, self.servo_max)
            try:
                self.servo_controller.set_pwm(channel, 0, int(pwm_to_send))
                return 1
            except:
                raise IOError("PivotPi not connected")
        return -1
    
    def AngleMicroseconds(self, channel, time):
        if channel >= 0 and channel <= 7:
            try:
                if(time <= 0):
                    self.servo_controller.set_pwm(channel, 4096, 4095)
                else:
                    pwm_to_send = 4095 - ((4096.0 / (1000000.0 / self.frequency)) * time)
                    if(pwm_to_send < 0):
                        pwm_to_send = 0
                    if(pwm_to_send > 4095):
                        pwm_to_send = 4095
                    self.servo_controller.set_pwm(channel, 0, int(pwm_to_send))
                return 1
            except:
                raise IOError("PivotPi not connected")
        return -1
    
    def LED(self, channel, percent):
        if channel >= 0 and channel <= 7:
            try:
                if(percent >= 100):
                    self.servo_controller.set_pwm(channel + 8, 4096, 4095)
                else:
                    if(percent < 0):
                        percent = 0
                    pwm_to_send = percent * 40.95
                    self.servo_controller.set_pwm(channel + 8, 0, int(pwm_to_send))
                return 1
            except:
                raise IOError("PivotPi not connected")
        return -1