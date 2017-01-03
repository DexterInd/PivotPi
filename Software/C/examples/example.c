#include "pivotpi.c"
// gcc example.c -lwiringPi -lwiringPiDev -lpthread -lm -lwiringPiPca9685
int main(void)
{
	int i;
	printf("PCA9685 LED example\n");

	if (pivotpi_setup(addr_00,60.0) < 0)
	{
		printf("Error in setup\n");
		return -1;
	}
	
	while (1)
	{
		for (i = 0; i < 8; i++)
		{
			// //angle(i, 0)
			led(i, 0);                       // Set the LED to 0 Power
			angle_microseconds(i, 1500);     // Set the Servo to 1500 angle
			sleep_ms(50);    
		}		
		for (i = 0; i < 8; i++)
		{
			// //angle(i, 180)
			led(i, (i + 1) * 4);             // Increase the LED Power
			angle_microseconds(i, 550 + (i * 272));  // Change the pivotpi Angle
			sleep_ms(50);                        // Give the system a rest.
		}
	}
}
