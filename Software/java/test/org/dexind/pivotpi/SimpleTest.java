package org.dexind.pivotpi;

public class SimpleTest {

	public static void main(String[] args) {
		PivotPi pvpi = new PivotPi();
		System.out.print("Instantiated PivotPi: Start test");
		while (true) {
			for (int i=0; i < 8; i++) {
				pvpi.led(i, 0); // Set the LED to 0 Power
				pvpi.angleMicroseconds(i, 1500); // Set the Servo to 1500 angle
			}
			try {
				Thread.sleep(50);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			for (int j=0; j < 8; j++) {
				pvpi.led(j, (j + 1) * 4); // Increase the LED Power
				pvpi.angleMicroseconds(j, 550 + (j * 270)); // Change the pivotpi Angle
			}
			try {
				Thread.sleep(50);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

}
