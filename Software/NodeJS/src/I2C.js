// https://www.dexterindustries.com/PivotPi/
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/PivotPi/blob/master/LICENSE.md

const Platform = require('./platform');
const i2c = require('i2c-bus');

/**
 * Class for communicating with an I2C device using the smbus library.
    Allows reading and writing 8-bit, 16-bit, and byte array values to registers
    on the device.
 */
class Device {
    /**
     * Create an instance of the I2C device at the specified address on the
        specified I2C bus number.
     * @param {*} address
     * @param {*} busnum
     * @param {*} opts
     */
    constructor(address, busnum) {
        this.address = address;
        this.bus = i2c.openSync(busnum);
        console.log(`Adafruit_I2C.Device.Bus.${busnum}.Address.${address}`);
    }

    /**
     * Write an 8-bit value on the bus (without register).
     * @param {*} value
     */
    writeRaw8(value) {
        value &= 0xFF;
        this.bus.sendByteSync(this.address, value);
        console.log('Wrote', value);
    }
    /**
     * Write an 8-bit value to the specified register.
     * @param {*} register
     * @param {*} value
     */
    write8(register, value) {
        value &= 0xFF;
        this.bus.writeByteSync(this.address, register, value);
        console.log('Wrote', value, 'to register', register);
    }
    /**
     * Write a 16-bit value to the specified register.
     * @param {*} register
     * @param {*} value
     */
    write16(register, value) {
        value &= 0xFFFF;
        this.bus.writeWordSync(this.address, register, value);
        console.log('Wrote', value, 'to register pair', register, register + 1);
    }
    /**
     * Write bytes to the specified register.
     * @param {*} register
     * @param {*} data
     */
    writeList(register, data) {
        const buffer = new Buffer(data);
        this.bus.writeI2cBlockSync(this.address, register, buffer.length, buffer);
        console.log('Wrote', data, 'to register', register);
    }
    /**
     * "Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray.
     * @param {*} register
     * @param {*} length
     */
    readList(register, length) {
        const buffer = new Buffer(length);
        this.bus.readI2cBlockSync(this.address, register, length, buffer);
        console.log('Read from register', register, buffer);
        return buffer;
    }
    /**
     * Read an 8-bit value on the bus (without register).
     */
    readRaw8() {
        const byte = this.bus.receiveByteSync(this.address) & 0xFF;
        console.log('Read', byte);
        return byte;
    }
    /**
     * Read an unsigned byte from the specified register.
     * @param {*} register
     */
    readU8(register) {
        const byte = this.bus.readByteSync(this.address, register) & 0xFF;
        console.log('Read', byte, 'from register', register);
        return byte;
    }
    /**
     * Read a signed byte from the specified register.
     * @param {*} register
     */
    readS8(register) {
        let byte = this.readU8(register);
        if (byte > 127) {
            byte -= 256;
        }
        return byte;
    }
    /**
     * Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
     * @param {*} register
     * @param {*} littleEndian
     */
    readU16(register, littleEndian = true) {
        let bytes = this.bus.readWordSync(this.address, register) & 0xFFFF;
        console.log('Read', bytes, 'from register pair', register, register + 1);
        if (!littleEndian) {
            bytes = ((bytes << 8) & 0xFF00) + (bytes >> 8);
        }
        return bytes;
    }
    /**
     * Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
     * @param {*} register
     * @param {*} littleEndian
     */
    readS16(register, littleEndian = true) {
        let bytes = this.readU16(register, littleEndian);
        if (bytes > 32767) {
            bytes -= 65536;
        }
        return bytes;
    }
    /**
     * Read an unsigned 16-bit value from the specified register, in little
        endian byte order.
     * @param {*} register
     */
    readU16LE(register) {
        return this.readU16(register, true);
    }
    /**
     * Read an unsigned 16-bit value from the specified register, in big
        endian byte order.
     * @param {*} register
     */
    readU16BE(register) {
        return this.readU16(register, false);
    }
    /**
     * Read a signed 16-bit value from the specified register, in little
        endian byte order.
     * @param {*} register
     */
    readS16LE(register) {
        return this.readS16(register, true);
    }
    /**
     * Read a signed 16-bit value from the specified register, in big
        endian byte order.
     * @param {*} register
     */
    readS16BE(register) {
        return this.readS16(register, false);
    }
}

/**
 * Return the default bus number based on the device platform.  For a
    Raspberry Pi either bus 0 or 1 (based on the Pi revision) will be returned.
    For a Beaglebone Black the first user accessible bus, 1, will be returned.
 */
const getDefaultBus = () => {
    let output = 0;
    const platformDetector = new Platform();
    const platform = platformDetector.platformDetect();

    if (platform === Platform.RASPBERRY_PI) {
        if (platformDetector.piRevision() === 1) {
            // Revision 1 Pi uses I2C bus 0.
            output = 0;
        } else {
            // Revision 2 Pi uses I2C bus 1.
            output = 1;
        }
    } else if (platform === Platform.BEAGLEBONE_BLACK) {
        // Beaglebone Black has multiple I2C buses, default to 1 (P9_19 and P9_20).
        output = 1;
    } else {
        throw new Error('Could not determine default I2C bus for platform.');
    }
    return output;
};
/**
 * Return an I2C device for the specified address and on the specified bus.
    If busnum isn't specified, the default I2C bus for the platform will attempt
    to be detected.
 * @param {*} address
 * @param {*} busnum
 * @param {*} opts
 */
const getI2cDevice = (address, busnum = false, opts) => {
    if (!busnum) {
        busnum = getDefaultBus();
    }
    return new Device(address, busnum, opts);
};

module.exports = {
    'device': getI2cDevice
};
