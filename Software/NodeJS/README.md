# PivotPi library for Node.js
PivotPi is a Servo Controller for the Raspberry Pi!

[Learn more about the PivotPi Servo Controller for the Raspberry Pi here.](https://www.dexterindustries.com/pivotpi)

![alt text](https://raw.githubusercontent.com/DexterInd/PivotPi/master/pivotpi-header.jpg)

## Getting Ideas

Need an idea to get started? [We have a few project examples to get your creative juices flowing.](https://github.com/DexterInd/PivotPi/tree/master/Projects)

## Getting Help
Need help? We [have a forum here where you can ask questions or make suggestions](http://forum.dexterindustries.com/c/pivotpi-servo-controller-for-raspberry-pi.

See more at the [PivotPi Site](https://www.dexterindustries.com/pivotpi/)

## Install/Update Node.js
This library supports Node.js 8.x version, we provide a couple of bash scripts to install/uninstall the proper Node.js version.
To install NVM (Node Version Manager), Node.js and NPM:
1. Run the install script: `bash ./NodeJS/install.sh`
2. Follow the instructions

To uninstall NVM, Node.js and NPM:
1. Run the install script: `bash ./NodeJS/uninstall.sh`
2. Follow the instructions

# Use in your application
This library is published as a NPM package.
1. Add it to your project: `npm install node-pivotpi --save`
2. Use it in your code: `const PivotPi = require('node-pivotpi')`

For any initial hint please check the "examples" folder. Feel free to use the forum for any extra help.

# License

Please review the [LICENSE.md] file for license information.

[LICENSE.md]: ./LICENSE.md

Notes for developers
=======

# Features
* Build with [Babel](https://babeljs.io). (ES6 -> ES5)
* Test with [mocha](https://mochajs.org).
* Cover with [istanbul](https://github.com/gotwarlost/istanbul).
* Check with [eslint](eslint.org).
* Deploy with [Travis](travis-ci.org).

# Commands
- `npm run clean` - Remove `lib/` directory
- `npm test` - Run tests. Tests can be written with ES6 (WOW!)
- `npm test:watch` - You can even re-run tests on file changes!
- `npm run cover` - Yes. You can even cover ES6 code.
- `npm run lint` - We recommend using [airbnb-config](https://github.com/airbnb/javascript/tree/master/packages/eslint-config-airbnb). It's fantastic.
- `npm run test:examples` - We recommend writing examples on pure JS for better understanding module usage.
- `npm run build` - Do some magic with ES6 to create ES5 code.