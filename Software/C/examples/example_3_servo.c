#include "pivotpi.c"

#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>

// gcc example_3_servo.c -lwiringPi -lwiringPiDev -lpthread -lm -lwiringPiPca9685

int main(void)
{
  printf("PivotPi 3 servo example\n");

  if(pivotpi_setup(ADDR_00, FREQUENCY_TARGET) < 0){
    printf("Error in setup\n");
    return -1;
  }
  
  while(1){
    angle(SERVO_1, 0);   // Set Servo 1 to 0 Degrees
    angle(SERVO_2, 0);   // Set Servo 2 to 0 Degrees
    angle(SERVO_3, 0);   // Set Servo 3 to 0 Degrees
    
    led(SERVO_1, 0);     // Set LED 1 to 0 Power
    led(SERVO_2, 0);     // Set LED 2 to 0 Power
    led(SERVO_3, 0);     // Set LED 3 to 0 Power
    delay(500);
    
    angle(SERVO_1, 90);  // Set Servo 1 to a 90 Degree Angle
    angle(SERVO_2, 90);
    angle(SERVO_3, 90);
    
    led(SERVO_1, 75);    // Set LED 1 to 75 Power
    led(SERVO_2, 75);
    led(SERVO_3, 75);
    delay(500);
  }
}
