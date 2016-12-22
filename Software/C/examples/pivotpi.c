#include "pivotpi.h"
#include "pca9685.h"

#include <wiringPi.h>
#include <wiringPiI2C.h>

#include <stdio.h>
#include <stdlib.h>

#define PIN_BASE 300
#define MAX_PWM 4096
#define HERTZ 50

int fd;

void sleep_ms(int val)
{
	delay(val);
}

//map 0-180 to pulse length between 150-600
int translate(int value,int leftMin,int leftMax,int rightMin,int rightMax)
{
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

int pivotpi_setup(int addr ,float actual_frequency)
// int pivotpi_setup(int addr ,float actual_frequency)
{
	fd = pca9685Setup(PIN_BASE, addr, actual_frequency);
	if (fd < 0)
	{
		printf("Error in setup\n");
		return fd;
	}

	// pca9685PWMReset(fd);
	return 1;
}

int pwm(int channel,int on,int off)
{
	pca9685PWMWrite(fd,channel,on,off);
}
    
int angle(int channel,int angle)
{
	int pwm_to_send;
	if( angle >= 0 && angle <= 180 && channel >= 0 && channel <= 7)
	{
		pwm_to_send = 4095 - translate(angle, 0, 180, servo_min, servo_max);
		
        pca9685PWMWrite(fd,channel, 0, (int)pwm_to_send);
		return 1;
	}
	return -1;
}
int angle_microseconds(int channel,int time)
{
	int pwm_to_send;
	if(channel >= 0 && channel <= 7)
	{
		if(time <= 0)
			pca9685PWMWrite(fd,channel, 4096, 4095);
		else
		{
			pwm_to_send = 4095 - ((4096.0 / (1000000.0 / frequency)) * time);
			if(pwm_to_send < 0)
				pwm_to_send = 0;
			if(pwm_to_send > 4095)
				pwm_to_send = 4095;
			pca9685PWMWrite(fd,channel, 0, (int)pwm_to_send);
		}
		return 1;
	}
	return -1;
}
    
int led(int channel,int percent)
{
	int pwm_to_send;
	if (channel >= 0 && channel <= 7)
	{
		if(percent >= 100)
			pca9685PWMWrite(fd,channel + 8, 4096, 4095);
		else
		{
			if(percent < 0)
				percent = 0;
			pwm_to_send = percent * 40.95;
			pca9685PWMWrite(fd,channel + 8, 0, (int)pwm_to_send);
		}
		return 1;
	}
	return -1;
}
