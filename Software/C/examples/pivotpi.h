#define SERVO_1 0
#define SERVO_2 1
#define SERVO_3 2
#define SERVO_4 3
#define SERVO_5 4
#define SERVO_6 5
#define SERVO_7 6
#define SERVO_8 7

#define addr_00 0x40
#define addr_01 0x41
#define addr_10 0x42
#define addr_11 0x43

#define servo_min 150  // Min pulse length out of 4096
#define servo_max 600  // Max pulse length out of 4096
#define frequency 60

void sleep_ms(int val);
int translate(int value,int leftMin,int leftMax,int rightMin,int rightMax);
int pivotpi_setup(int addr,float actual_frequency);
int pwm(int channel,int on,int off);
int angle(int channel,int angle);
int angle_microseconds(int channel,int time);
int led(int channel,int percent);