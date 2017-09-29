package org.dexind.pivotpi;

import com.pi4j.io.i2c.I2CFactory;
import com.pi4j.io.i2c.I2CFactory.UnsupportedBusNumberException;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.pi4j.io.i2c.I2CBus;

/**
 * PivotPi implements three additional methods, which aren't in the base class.
 * The logger uses default java logging.
 * 
 * @author peter lin
 *
 */
public class PivotPi extends BasePCA9685 implements ServoController {

	public final int addr_00 = 0x40;
	public final int addr_01 = 0x41;
	public final int addr_10 = 0x42;
	public final int addr_11 = 0x43;
	
    // Configure min and max servo pulse lengths
	public final int servo_min = 150;  // Min pulse length out of 4096
	public final int servo_max = 600;  // Max pulse length out of 4096
    private float frequency = 60f;
    
    private I2CBus bus = null;
		
	public PivotPi() {
		super();
		try {
			this.bus = I2CFactory.getInstance(1);
			this.i2cDevice = this.bus.getDevice(PCA9685.PCA9685_ADDRESS);
			this.setPwmFrequency(frequency);
			this.log = Logger.getLogger(PivotPi.class.getName());
		} catch (UnsupportedBusNumberException e) {
			e.printStackTrace();
			log.log(Level.SEVERE, "Error instantiating PivotPi", e);
		} catch (IOException e) {
			e.printStackTrace();
			log.log(Level.SEVERE, "Error instantiating PivotPi", e);
		}
	}
	
	/**
	 * Set the PWM frequency to the provided value in Hertz. The method
	 * is similar to the python driver function.
	 */
	public void setPwmFrequency(float hertz) throws IOException {
		float prescaleVal = 25000000.0f; // 25Mhz
		prescaleVal = prescaleVal / 4096.0f; // 12bit
		prescaleVal = prescaleVal / hertz;
		prescaleVal = prescaleVal - 1.0f;
		
		System.out.println("Seting PWM Freq to " + hertz + "Hz");
		int freqVal = (int)Math.floor(prescaleVal + 0.5f);
		int oldMode = this.i2cDevice.read(MODE1);
		int newMode = (oldMode & 0x7F) | 0x10;
		this.write8(MODE1, newMode);
		this.write8(PRESCALE, freqVal);
		this.write8(MODE1, oldMode);
		try {
			Thread.sleep(1);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		this.write8(MODE1, oldMode | 0x80);
	}
	
	@Override
	public void angle(int channel, int angle) {
		if (angle >= 0 && angle <= 180 && channel >= 0 && channel <= 7) {
			int pwmToSend = 4095 - this.translate(angle, 0, 180, servo_min, servo_max);
			try {
				this.setPWM(channel, 0, pwmToSend);
			} catch (IOException e) {
				System.err.println(e.getMessage());
				e.printStackTrace();
			}
		}
	}

	@Override
	public void angleMicroseconds(int channel, int time) {
		if (channel >= 0 && channel <= 7) {
			try {
				if (time <= 0) {
					this.setPWM(channel, 4096, 4095);
				} else {
					float f = (4096.0f / (1000000.0f / frequency)) * time;
					int pwmToSend = 4095 - (int)f;
					if (pwmToSend < 0) {
						pwmToSend = 0;
					}
					if (pwmToSend > 4096) {
						pwmToSend = 4095;
					}
					this.setPWM(channel, 0, pwmToSend);
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	/**
	 * Set the LED on the PivotPi. There are 8 LED starting with
	 * index 0 to 7.
	 */
	@Override
	public void led(int channel, float percent) {
		if (channel >= 0 && channel <= 7) {
			try {
				if (percent >= 100) {
					this.setPWM(channel + 8, 4096, 4095);
				} else {
					if (percent < 0) {
						percent = 0;
					}
					float pwmToSend = percent * 40.95f;
					this.setPWM(channel + 8, 0, (int)pwmToSend);
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	@Override
	public int translate(int val, int leftMin, int leftMax, int rightMin, int rightMax) {
		// Figure out how 'wide' each range is
	    int leftSpan = leftMax - leftMin;
	    int rightSpan = rightMax - rightMin;

	    // Convert the left range into a 0-1 range (float)
	    float valueScaled = (float)(val - leftMin) / (float)(leftSpan);

	    // Convert the 0-1 range into a value in the right range.
	    return (int)(rightMin + (valueScaled * rightSpan));
	}
	
	/**
	 * setPWM is the main method for issuing commands to the PCA 9685. The
	 * implementation is similar to the Python driver. The main difference
	 * is we use Integer class and call byteValue().
	 * 
	 * @param channel
	 * @param on
	 * @param off
	 * @throws IOException
	 */
	public void setPWM(int channel, int on, int off) throws IOException {

		Integer onl = new Integer(on & 0xFF);
		Integer onh = new Integer(on >> 8);
		Integer offl = new Integer(off & 0xFF);
		Integer offh = new Integer(off >> 8);
		
		this.write8(LED0_ON_L + 4 * channel, onl.byteValue());
		this.write8(LED0_ON_H + 4 * channel, onh.byteValue());
		this.write8(LED0_OFF_L + 4 * channel, offl.byteValue());
		this.write8(LED0_OFF_H + 4 * channel, offh.byteValue());
	}

	public void write8(int register, int value) throws IOException {
		Integer intvalue = new Integer(value & 0xFF);
		this.writeRegister(register, intvalue.byteValue());
	}
	
	public void write16(int register, int value) throws IOException {
		Integer intvalue = new Integer(value & 0xFFFF);
		this.writeRegister(register, intvalue.byteValue());
	}
}
