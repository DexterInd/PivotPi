#!/usr/bin/env python
#
'''
## License
The code here is Licensed under  The MIT License (MIT) . Please review the  LICENSE.md file or (here)[https://github.com/DexterInd/Raspbian_For_Robots/blob/master/LICENSE.md] for more information
Copyright (C) 2016 Dexter Industries

'''

import setuptools
setuptools.setup(
    name="pivotpi",
    description="Drivers and examples for using the PivotPi in Python",
    author="Dexter Industries",
    url="http://www.dexterindustries.com/PivotPi/",
    py_modules=['pivotpi','PCA9685', 'I2C', 'Platform'],
    #install_requires=open('requirements.txt').readlines(),
)
