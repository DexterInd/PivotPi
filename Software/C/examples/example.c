#include "pivotpi.c"

#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>

// gcc example.c -lwiringPi -lwiringPiDev -lpthread -lm -lwiringPiPca9685

int main(void)
{
  int i;
  printf("PivotPi Servo and LED example\n");

  if(pivotpi_setup(ADDR_00, FREQUENCY_TARGET) < 0){ // Set up a PivotPi with address 00, and set the calibration to the default frequency.
    printf("Error in setup\n");
    return -1;
  }
  
  while(1){
    for (i = 0; i < 8; i++){
      //angle(i, 0)
      led(i, 0);                              // Set the LED to 0 Power
      angle_microseconds(i, 1500);            // Set the Servo to 1500 angle
      delay(50);                              // Slow down so you can see the changes
    }
    for (i = 0; i < 8; i++){
      //angle(i, 180)
      led(i, (i + 1) * 12);                    // Increase the LED Power
      angle_microseconds(i, 550 + (i * 272)); // Change the pivotpi Angle
      delay(50);                              // Slow down so you can see the changes
    }
  }
}
