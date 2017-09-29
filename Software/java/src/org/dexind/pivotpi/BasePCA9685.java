package org.dexind.pivotpi;

import java.io.IOException;
import java.util.logging.Logger;

import com.pi4j.io.i2c.I2CDevice;

/**
 * Subclasses need to use pi4j i2c factory class to get the I2CBus. Once you have
 * the bus, you can get the device by the address. The address used by the python
 * driver is 0x40.<p/>
 * 
 * BasePCA9685 implements the write and read methods. Subclasses need to call
 * the write/read methods. You can use the I2CDevice directly, but it's better
 * to use the base methods.
 * 
 * @author peter lin
 *
 */
public abstract class BasePCA9685 implements PCA9685 {

	/**
	 * pi4j I2C device
	 */
	protected I2CDevice i2cDevice;
	protected Logger log = null;
	
	public BasePCA9685() {
		super();
	}
	
	public void writeRegister(int address, byte value) throws IOException {
        i2cDevice.write(address, value);
    }

    public void writeRegisters(int address, byte[] values) throws IOException {
        i2cDevice.write(address, values, 0, values.length);
    }

    public int readRegister(int address) throws IOException {
        int value = i2cDevice.read(address);
        return value;
    }

    public int readRegisters(int address, byte[] buffer, int offset, int size) throws IOException {
        return i2cDevice.read(address, buffer, 0, buffer.length);
    }
}
