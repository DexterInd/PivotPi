/*************************************************************************
 * pca9685.c
 *
 * This software is a devLib extension to wiringPi <http://wiringpi.com/>
 * and enables it to control the Adafruit PCA9685 16-Channel 12-bit
 * PWM/Servo Driver <http://www.adafruit.com/products/815> via I2C interface.
 *
 * Copyright (c) 2014 Reinhard Sprung
 *
 * If you have questions or improvements email me at
 * reinhard.sprung[at]gmail.com
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * The given code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.
 *
 * You can view the contents of the licence at <http://www.gnu.org/licenses/>.
 **************************************************************************
 */

#include <wiringPi.h>
#include <wiringPiI2C.h>

#include "pca9685.h"

// Setup registers
#define PCA9685_MODE1 0x0
#define PCA9685_PRESCALE 0xFE

// // Define first LED and all LED. We calculate the rest
// #define LED0_ON_L 0x6
#define LEDALL_ON_L 0xFA

#define PIN_ALL 16

#define MODE1               0x00
#define MODE2               0x01
#define SUBADR1             0x02
#define SUBADR2             0x03
#define SUBADR3             0x04
#define PRESCALE            0xFE
#define LED0_ON_L           0x06
#define LED0_ON_H           0x07
#define LED0_OFF_L          0x08
#define LED0_OFF_H          0x09
#define ALL_LED_ON_L        0xFA
#define ALL_LED_ON_H        0xFB
#define ALL_LED_OFF_L       0xFC
#define ALL_LED_OFF_H       0xFD

//Bits:
#define RESTART             0x80
#define SLEEP               0x10
#define ALLCALL             0x01
#define INVRT               0x10
#define OUTDRV              0x04

// Declare
static void myPwmWrite(struct wiringPiNodeStruct *node, int pin, int value);
static void myOnOffWrite(struct wiringPiNodeStruct *node, int pin, int value);
static int myOffRead(struct wiringPiNodeStruct *node, int pin);
static int myOnRead(struct wiringPiNodeStruct *node, int pin);
int baseReg(int pin);


/**
 * Setup a PCA9685 device with wiringPi.
 *  
 * pinBase: 	Use a pinBase > 64, eg. 300
 * i2cAddress:	The default address is 0x40
 */
int pca9685Setup(const int pinBase, const int i2cAddress)
{
	// Create a node with 16 pins [0..15] + [16] for all
	struct wiringPiNodeStruct *node = wiringPiNewNode(pinBase, PIN_ALL + 1);

	// Check if pinBase is available
	if (!node)
		return -1;

	// Check i2c address
	int fd = wiringPiI2CSetup(i2cAddress);
	if (fd < 0)
		return fd;

	// Setup the chip. Enable auto-increment of registers.
	// int settings = wiringPiI2CReadReg8(fd, PCA9685_MODE1) & 0x7F;
	// int autoInc = settings | 0x20;
	set_all_pwm(fd,0, 0);
	// wiringPiI2CWriteReg8(fd, PCA9685_MODE1, autoInc);
	wiringPiI2CWriteReg8(fd, MODE2, (OUTDRV | INVRT));
	wiringPiI2CWriteReg8(fd, MODE1, ALLCALL);
	delay(5);

	node->fd			     = fd;
	node->pwmWrite		 = myPwmWrite;
	node->digitalWrite = myOnOffWrite;
	node->digitalRead	 = myOffRead;
	node->analogRead   = myOnRead;

	return fd;
}

/**
 * Sets the frequency of PWM signals.
 * Frequency will be capped to range [40..1000] Hertz. Try 50 for servos.
 */
void pca9685PWMFreq(int fd, float freq)
{
	// Cap at min and max
	freq = (freq > 1000 ? 1000 : (freq < 40 ? 40 : freq));

	// To set pwm frequency we have to set the prescale register. The formula is:
	// prescale = round(osc_clock / (4096 * frequency))) - 1 where osc_clock = 25 MHz
	// Further info here: http://www.nxp.com/documents/data_sheet/PCA9685.pdf Page 24
	int prescale = (int)(25000000.0f / (4096 * freq) - 0.5f);

	// Get settings and calc bytes for the different states.
	int settings = wiringPiI2CReadReg8(fd, PCA9685_MODE1) & 0x7F;	// Set restart bit to 0
	int sleep	= settings | 0x10;									// Set sleep bit to 1
	int wake 	= settings & 0xEF;									// Set sleep bit to 0
	int restart = wake | 0x80;										// Set restart bit to 1

	// Go to sleep, set prescale and wake up again.
	wiringPiI2CWriteReg8(fd, PCA9685_MODE1, sleep);
	wiringPiI2CWriteReg8(fd, PCA9685_PRESCALE, prescale);
	wiringPiI2CWriteReg8(fd, PCA9685_MODE1, wake);

	// Now wait a millisecond until oscillator finished stabilizing and restart PWM.
	delay(1);
	wiringPiI2CWriteReg8(fd, PCA9685_MODE1, restart);
}

/**
 * Set all leds back to default values (: fullOff = 1)
 */
void pca9685PWMReset(int fd)
{
	wiringPiI2CWriteReg16(fd, LEDALL_ON_L	 , 0x0);
	wiringPiI2CWriteReg16(fd, LEDALL_ON_L + 2, 0x1000);
}

/**
 * Write on and off ticks manually to a pin
 * (Deactivates any full-on and full-off)
 */
void pca9685PWMWrite(int fd, int channel, int on, int off)
{
	// int reg = baseReg(pin);

	// Write to on and off registers and mask the 12 lowest bits of data to overwrite full-on and off
	// wiringPiI2CWriteReg16(fd, reg	 , on  & 0x0FFF);
	// wiringPiI2CWriteReg16(fd, reg + 2, off & 0x0FFF);
	wiringPiI2CWriteReg8(fd, LED0_ON_L+4*channel, on & 0xFF);
    wiringPiI2CWriteReg8(fd, LED0_ON_H+4*channel, on >> 8);
    wiringPiI2CWriteReg8(fd, LED0_OFF_L+4*channel, off & 0xFF);
    wiringPiI2CWriteReg8(fd, LED0_OFF_H+4*channel, off >> 8);
}

void set_all_pwm(int fd, int on, int off)
{
	// int reg = baseReg(pin);

	// Write to on and off registers and mask the 12 lowest bits of data to overwrite full-on and off
	// wiringPiI2CWriteReg16(fd, reg	 , on  & 0x0FFF);
	// wiringPiI2CWriteReg16(fd, reg + 2, off & 0x0FFF);
	wiringPiI2CWriteReg8(fd, ALL_LED_ON_L, on & 0xFF);
	wiringPiI2CWriteReg8(fd, ALL_LED_ON_H, on >> 8);
	wiringPiI2CWriteReg8(fd, ALL_LED_OFF_L, off & 0xFF);
	wiringPiI2CWriteReg8(fd, ALL_LED_OFF_H, off >> 8);
}

/**
 * Reads both on and off registers as 16 bit of data
 * To get PWM: mask each value with 0xFFF
 * To get full-on or off bit: mask with 0x1000
 * Note: ALL_LED pin will always return 0
 */
void pca9685PWMRead(int fd, int pin, int *on, int *off)
{
	int reg = baseReg(pin);

	if (on)
		*on  = wiringPiI2CReadReg16(fd, reg);
	if (off)
		*off = wiringPiI2CReadReg16(fd, reg + 2);
}

/**
 * Enables or deactivates full-on
 * tf = true: full-on
 * tf = false: according to PWM
 */
void pca9685FullOn(int fd, int pin, int tf)
{
	int reg = baseReg(pin) + 1;		// LEDX_ON_H
	int state = wiringPiI2CReadReg8(fd, reg);

	// Set bit 4 to 1 or 0 accordingly
	state = tf ? (state | 0x10) : (state & 0xEF);

	wiringPiI2CWriteReg8(fd, reg, state);

	// For simplicity, we set full-off to 0 because it has priority over full-on
	if (tf)
		pca9685FullOff(fd, pin, 0);
}

/**
 * Enables or deactivates full-off
 * tf = true: full-off
 * tf = false: according to PWM or full-on
 */
void pca9685FullOff(int fd, int pin, int tf)
{
	int reg = baseReg(pin) + 3;		// LEDX_OFF_H
	int state = wiringPiI2CReadReg8(fd, reg);

	// Set bit 4 to 1 or 0 accordingly
	state = tf ? (state | 0x10) : (state & 0xEF);

	wiringPiI2CWriteReg8(fd, reg, state);
}

/**
 * Helper function to get to register
 */
int baseReg(int pin)
{
	return (pin >= PIN_ALL ? LEDALL_ON_L : LED0_ON_L + 4 * pin);
}




//------------------------------------------------------------------------------------------------------------------
//
//	WiringPi functions
//
//------------------------------------------------------------------------------------------------------------------




/**
 * Simple PWM control which sets on-tick to 0 and off-tick to value.
 * If value is <= 0, full-off will be enabled
 * If value is >= 4096, full-on will be enabled
 * Every value in between enables PWM output
 */
static void myPwmWrite(struct wiringPiNodeStruct *node, int pin, int value)
{
	int fd   = node->fd;
	int ipin = pin - node->pinBase;

	if (value >= 4096)
		pca9685FullOn(fd, ipin, 1);
	else if (value > 0)
		pca9685PWMWrite(fd, ipin, 0, value);	// (Deactivates full-on and off by itself)
	else
		pca9685FullOff(fd, ipin, 1);
}

/**
 * Simple full-on and full-off control
 * If value is 0, full-off will be enabled
 * If value is not 0, full-on will be enabled
 */
static void myOnOffWrite(struct wiringPiNodeStruct *node, int pin, int value)
{
	int fd   = node->fd;
	int ipin = pin - node->pinBase;

	if (value)
		pca9685FullOn(fd, ipin, 1);
	else
		pca9685FullOff(fd, ipin, 1);
}

/**
 * Reads off registers as 16 bit of data
 * To get PWM: mask with 0xFFF
 * To get full-off bit: mask with 0x1000
 * Note: ALL_LED pin will always return 0
 */
static int myOffRead(struct wiringPiNodeStruct *node, int pin)
{
	int fd   = node->fd;
	int ipin = pin - node->pinBase;

	int off;
	pca9685PWMRead(fd, ipin, 0, &off);

	return off;
}

/**
 * Reads on registers as 16 bit of data
 * To get PWM: mask with 0xFFF
 * To get full-on bit: mask with 0x1000
 * Note: ALL_LED pin will always return 0
 */
static int myOnRead(struct wiringPiNodeStruct *node, int pin)
{
	int fd   = node->fd;
	int ipin = pin - node->pinBase;

	int on;
	pca9685PWMRead(fd, ipin, &on, 0);

	return on;
}






