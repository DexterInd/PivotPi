// https://www.dexterindustries.com/PivotPi/
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/PivotPi/blob/master/LICENSE.md

const shell = require('shelljs');

class Platform {
    static UNKNOWN = 0;
    static RASPBERRY_PI = 1;
    static BEAGLEBONE_BLACK = 2;
    static MINNOWBOARD = 3;

    platformDetect() {
        const uname = String(shell.exec('uname - a', { silent: true }).stdout).toLowerCase();
        if (uname.indexOf('bone') > -1 || uname.indexOf('beaglebone') > -1) {
            return Platform.BEAGLEBONE_BLACK;
        }

        if (uname.indexOf('minnow') > -1 || uname.indexOf('minnowboard') > -1) {
            return Platform.MINNOWBOARD;
        }

        const pi = this.piVersion();
        if (pi) {
            return Platform.RASPBERRY_PI;
        }

        return Platform.UNKNOWN;
    }

    piRevision() {
        const rev = String(shell.exec("cat /proc/cpuinfo | grep 'Revision' | awk '{print $3}'", { silent: true }).stdout).replace(/\W/, '').toLowerCase();
        if (rev === '0000' || rev === '0002' || rev === '0003') {
            return 1;
        } else if (rev.length <= 6) {
            return 2;
        }
        console.log('Unknown revision', rev);
        throw new Error('Could not determine Raspberry Pi revision.');
    }

    piVersion() {
        const ver = String(shell.exec("cat /proc/cpuinfo | grep 'Hardware' | awk '{print $3}'", { silent: true }).stdout).replace(/\W/, '');

        if (ver === 'BCM2708') {
            // Pi 1
            return 1;
        } else if (ver === 'BCM2709') {
            // Pi 2
            return 2;
        }
        // Something else, not a pi.
        return false;
    }
}

module.exports = Platform;
