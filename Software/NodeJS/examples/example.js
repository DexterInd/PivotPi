const sleep = require('sleep');
const PivotPi = require('../lib/pivotpi');

let pivotpi;

try {
    pivotpi = new PivotPi(0x40, 60);
} catch (err) {
    throw new Error('PivotPi not found');
}

process.stdin.setRawMode(true);
process.stdin.resume();
process.stdin.on('data', () => {
    for (let i = 0, len = 8; i < len; i++) {
        pivotpi.led(i, 0);
        // Set the LED to 0 Power
        pivotpi.angleMicroseconds(i, 1500);
        // Set the Servo to 1500 angle
        sleep.msleep(50);
    }
    process.exit(0);
});

console.log('');
console.log('Moving servos on channel 1-8, press any key to quit...');
console.log('');

setInterval(
    () => {
        for (let i = 0, len = 8; i < len; i++) {
            pivotpi.led(i, 0);
            // Set the LED to 0 Power
            pivotpi.angleMicroseconds(i, 1500);
            // Set the Servo to 1500 angle
            sleep.msleep(50);
        }
        for (let i = 0, len = 8; i < len; i++) {
            pivotpi.led(i, (i + 1) * 4);
            // Increase the LED Power
            pivotpi.angleMicroseconds(i, 550 + (i * 272));
            // Change the pivotpi Angle
            sleep.msleep(50);
            // Give the system a rest.
        }
    }
, 100);
