#include "pca9685.h"

#define SERVO_1 0
#define SERVO_2 1
#define SERVO_3 2
#define SERVO_4 3
#define SERVO_5 4
#define SERVO_6 5
#define SERVO_7 6
#define SERVO_8 7

#define ADDR_00 0x40
#define ADDR_01 0x41
#define ADDR_10 0x42
#define ADDR_11 0x43

#define SERVO_MIN 150  // Min pulse length out of 4096
#define SERVO_MAX 600  // Max pulse length out of 4096
#define FREQUENCY_TARGET 60

float Frequency_Actual = FREQUENCY_TARGET; // Default to FREQUENCY_TARGET

int translate(int value, int leftMin, int leftMax, int rightMin, int rightMax);
int pivotpi_setup(int addr, float frequency_actual);
int pwm(int channel, int on, int off);
int angle(int channel, int angle);
int angle_microseconds(int channel, int time);
int led(int channel, int percent);
