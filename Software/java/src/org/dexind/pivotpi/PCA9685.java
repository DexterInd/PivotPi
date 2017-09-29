package org.dexind.pivotpi;

/**
 * The interface defines the static constants needed for PCA9685. The constants
 * are the same as the Python drivers.
 * 
 * @author peter lin
 *
 */
public interface PCA9685 {

	/**********************/
	/***    Registers   ***/
	/**********************/
	public static int PCA9685_ADDRESS = 0x40;
	public static int MODE1 = 0x00;
	public static int MODE2 = 0x01;
	public static int SUBADR1 = 0x02;
	public static int SUBADR2 = 0x03;
	public static int SUBADR3 = 0x04;
	public static int PRESCALE = 0xFE;
	public static int LED0_ON_L = 0x06;
	public static int LED0_ON_H = 0x07;
	public static int LED0_OFF_L = 0x08;
	public static int LED0_OFF_H = 0x09;
	public static int ALL_LED_ON_L = 0xFA;
	public static int ALL_LED_ON_H = 0xFB;
	public static int ALL_LED_OFF_L = 0xFC;
	public static int ALL_LED_OFF_H = 0xFD;
	
	/**********************/
	/***      bits      ***/
	/**********************/
	public static int RESTART = 0x80;
	public static int SLEEP = 0x10;
	public static int ALLCALL = 0x01;
	public static int INVRT = 0x10;
	public static int OUTDRV = 0x04;

}
