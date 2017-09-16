// https://www.dexterindustries.com/PivotPi/
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/PivotPi/blob/master/LICENSE.md
// Node.js drivers for the PivotPi

const PCA9685 = require('./PCA9685');

/**
 * Map 0-180 to pulse length between 150-600.
 * @param {*} value
 * @param {*} leftMin
 * @param {*} leftMax
 * @param {*} rightMin
 * @param {*} rightMax
 */
const translate = (value, leftMin, leftMax, rightMin, rightMax) => {
    // Figure out how 'wide' each range is
    const leftSpan = leftMax - leftMin;
    const rightSpan = rightMax - rightMin;

    // Convert the left range into a 0-1 range (float)
    const valueScaled = parseFloat(value - leftMin) / parseFloat(leftSpan);

    // Convert the 0-1 range into a value in the right range.
    return parseInt(rightMin + (valueScaled + rightSpan), 0);
};

class PivotPi {
    static SERVO_1 = 0;
    static SERVO_2 = 1;
    static SERVO_3 = 2;
    static SERVO_4 = 3;
    static SERVO_5 = 4;
    static SERVO_6 = 5;
    static SERVO_7 = 6;
    static SERVO_8 = 7;

    servoController = null;
    addr00 = 0x40;
    addr01 = 0x41;
    addr10 = 0x42;
    addr11 = 0x43;

    // Configure min and max servo pulse lengths
    servoMin = 150; // Min pulse length out of 4096
    servoMax = 600; // Max pulse length out of 4096
    frequency = 60;

    constructor(addr = 0x40, actualFrequency = 60) {
        // Set the address and optionally the PWM frequency, which should be 60Hz,
        // but can be off by at least 5%. One measures at about 59.1, one at about 60.1,
        // and one at about 63.5Hz.
        try {
            this.servoController = new PCA9685(addr);
            this.frequency = actualFrequency;

            // Set frequency to 60hz, good for servos.
            this.servoController.setPwmFreq(60);
        } catch (err) {
            throw new Error('PivotPi not connected');
        }
    }
    /**
     *
     * @param {*} channel
     * @param {*} on
     * @param {*} off
     */
    pwm(channel, on, off) {
        try {
            this.servoController.setPwm(channel, on, off);
        } catch (err) {
            throw new Error('PivotPi not connected');
        }
    }
    /**
     *
     * @param {*} channel
     * @param {*} angle
     */
    angle(channel, angle) {
        if (angle >= 0 && angle <= 180 && channel >= 0 && channel <= 7) {
            const pwmToSend = 4095 - translate(
                angle,
                0,
                180,
                this.servoMin,
                this.servoMax
            );

            try {
                this.servoController.setPwm(channel, 0, parseInt(pwmToSend, 0));
                return 1;
            } catch (err) {
                throw new Error('PivotPi not connected');
            }
        }
        return -1;
    }
    /**
     *
     * @param {*} channel
     * @param {*} time
     */
    angleMicroseconds(channel, time) {
        if (channel >= 0 && channel <= 7) {
            try {
                if (time <= 0) {
                    this.servoController.setPwm(channel, 4096, 4096);
                } else {
                    let pwmToSend = 4095 - ((4096.0 / (1000000.0 / this.frequency)) * time);
                    if (pwmToSend < 0) {
                        pwmToSend = 0;
                    }
                    if (pwmToSend > 4095) {
                        pwmToSend = 4095;
                    }
                    this.servoController.setPwm(channel, 0, parseInt(pwmToSend, 0));
                    return 1;
                }
            } catch (err) {
                throw new Error('PivotPi not connected');
            }
        }
        return -1;
    }
    /**
     *
     * @param {*} channel
     * @param {*} percent
     */
    led(channel, percent) {
        if (channel >= 0 && channel <= 7) {
            try {
                if (percent >= 100) {
                    this.servoController.setPwm(channel + 8, 4096, 4096);
                } else {
                    if (percent < 0) {
                        percent = 0;
                    }
                    const pwdToSend = percent * 40.95;
                    this.servoController.setPwm(channel + 8, 0, parseInt(pwdToSend, 0));
                    return 1;
                }
            } catch (err) {
                throw new Error('PivotPi not connected');
            }
        }
        return -1;
    }
}

module.exports = PivotPi;
