const I2C = require('./I2C');
const sleep = require('sleep');

class PCA9685 {
    static PCA9685_ADDRESS    = 0x40;
    static MODE1              = 0x00;
    static MODE2              = 0x01;
    static SUBADR1            = 0x02;
    static SUBADR2            = 0x03;
    static SUBADR3            = 0x04;
    static PRESCALE           = 0xFE;
    static LED0_ON_L          = 0x06;
    static LED0_ON_H          = 0x07;
    static LED0_OFF_L         = 0x08;
    static LED0_OFF_H         = 0x09;
    static ALL_LED_ON_L       = 0xFA;
    static ALL_LED_ON_H       = 0xFB;
    static ALL_LED_OFF_L      = 0xFC;
    static ALL_LED_OFF_H      = 0xFD;

    // Bits:
    static RESTART            = 0x80;
    static SLEEP              = 0x10;
    static ALLCALL            = 0x01;
    static INVRT              = 0x10;
    static OUTDRV             = 0x04;

    /**
     * Initialize the PCA9685.
     * @param {*} address
     * @param {*} i2c
     */
    constructor(address = PCA9685.PCA9685_ADDRESS) {
        // Setup I2C interface for the device.
        this.device = I2C.device(address);
        this.setAllPwm(0, 0);
        this.device.write8(PCA9685.MODE2, (PCA9685.OUTDRV | PCA9685.INVRT));
        // Totem pole drive, and inverted signal.
        this.device.write8(PCA9685.MODE1, PCA9685.ALLCALL);
        sleep.usleep(5);
        // wait for oscillator
        let mode1 = this.device.readU8(PCA9685.MODE1);
        mode1 &= ~PCA9685.SLEEP;
        // wake up (reset sleep)
        this.device.write8(PCA9685.MODE1, mode1);
        sleep.usleep(5);
        // wait for oscillator
    }
    /**
     * Set the PWM frequency to the provided value in hertz.
     * @param {*} freqHz
     */
    setPwmFreq(freqHz) {
        let prescaleval = 25000000.0;
        // 25MHz
        prescaleval /= 4096.0;
        // 12-bit
        prescaleval /= parseFloat(String(freqHz));
        prescaleval -= 1.0;

        console.log('Setting PWM frequency to %d Hz', freqHz);
        console.log('Estimated pre-scale: %d', prescaleval);

        const prescale = parseInt(Math.floor(prescaleval + 0.5), 0);
        console.log('Final pre-scale: %d', prescale);

        const oldMode = this.device.readU8(PCA9685.MODE1);
        const newMode = (oldMode & 0x7F) | 0x10;
        // Sleep
        this.device.write8(PCA9685.MODE1, newMode);
        // Go to sleep
        this.device.write8(PCA9685.PRESCALE, prescale);
        this.device.write8(PCA9685.MODE1, oldMode);
        sleep.usleep(5);
        this.device.write8(PCA9685.MODE1, oldMode | 0x80);
    }
    /**
     * Sets a single PWM channel.
     * @param {*} channel
     * @param {*} on
     * @param {*} off
     */
    setPwm(channel, on, off) {
        this.device.write8(PCA9685.LED0_ON_L + 4 * channel, on & 0xFF);
        this.device.write8(PCA9685.LED0_ON_H + 4 * channel, on >> 8);
        this.device.write8(PCA9685.LED0_OFF_L + 4 * channel, off & 0xFF);
        this.device.write8(PCA9685.LED0_OFF_H + 4 * channel, off >> 8);
    }
    /**
     * Sets all PWM channels.
     * @param {*} on
     * @param {*} off
     */
    setAllPwm(on, off) {
        this.device.write8(PCA9685.ALL_LED_ON_L, on & 0xFF);
        this.device.write8(PCA9685.ALL_LED_ON_H, on >> 8);
        this.device.write8(PCA9685.ALL_LED_OFF_L, off & 0xFF);
        this.device.write8(PCA9685.ALL_LED_OFF_H, off >> 8);
    }
}

module.exports = PCA9685;
