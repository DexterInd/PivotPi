package org.dexind.pivotpi;

public interface ServoController {
	public static final int SERVO_1 = 0;
	public static final int SERVO_2 = 1;
	public static final int SERVO_3 = 2;
	public static final int SERVO_4 = 3;
	public static final int SERVO_5 = 4;
	public static final int SERVO_6 = 5;
	public static final int SERVO_7 = 6;
	public static final int SERVO_8 = 7;
	
	/**
	 * 0-180 to pulse length between 150-600
	 * @param val
	 * @param leftMin
	 * @param leftMax
	 * @param rightMin
	 * @param rightMax
	 * @return
	 */
	int translate(int val, int leftMin, int leftMax, int rightMin, int rightMax);
	void angle(int channel, int angle);
	void angleMicroseconds(int channel, int time);
	void led(int channel, float percent);
}
