#include "pivotpi.h"

int fd;

//map 0-180 to pulse length between 150-600
int translate(int value, int leftMin, int leftMax, int rightMin, int rightMax){
  int leftSpan,rightSpan;
    float valueScaled;
    
    // Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin;
    rightSpan = rightMax - rightMin;
    
    // Convert the left range into a 0-1 range (float)
    valueScaled = ((float)value - leftMin) / ((float)leftSpan);
    // Convert the 0-1 range into a value in the right range.
    return ((int) (rightMin + (valueScaled * rightSpan)));
}

int pivotpi_setup(int addr, float frequency_actual){
  Frequency_Actual = frequency_actual;
  fd = pca9685Setup(300, addr);
  if(fd >= 0){
    pca9685PWMFreq(fd, FREQUENCY_TARGET);
    return fd;
  }
  return -1;
}

int pwm(int channel, int on, int off){
  pca9685PWMWrite(fd, channel, on, off);
}

int angle(int channel, int angle){
  int pwm_to_send;
  if( angle >= 0 && angle <= 180 && channel >= 0 && channel <= 7)
  {
    pwm_to_send = 4095 - translate(angle, 0, 180, SERVO_MIN, SERVO_MAX);
    pca9685PWMWrite(fd, channel, 0, (int)pwm_to_send);
    return 1;
  }
  return -1;
}

int angle_microseconds(int channel,int time){
  int pwm_to_send;
  if(channel >= 0 && channel <= 7){
    if(time <= 0){
      pca9685PWMWrite(fd, channel, 4096, 4095);
    }else{
      pwm_to_send = 4095 - ((4096.0 / (1000000.0 / Frequency_Actual)) * time);
      if(pwm_to_send < 0)
        pwm_to_send = 0;
      if(pwm_to_send > 4095)
        pwm_to_send = 4095;
      pca9685PWMWrite(fd, channel, 0, (int)pwm_to_send);
    }
    return 1;
  }
  return -1;
}

int led(int channel, int percent){
  int pwm_to_send;
  if(channel >= 0 && channel <= 7){
    if(percent >= 100){
      pca9685PWMWrite(fd, channel + 8, 4096, 4095);
    }else{
      if(percent < 0)
        percent = 0;
      pwm_to_send = percent * 40.95;
      pca9685PWMWrite(fd, channel + 8, 0, (int)pwm_to_send);
    }
    return 1;
  }
  return -1;
}
