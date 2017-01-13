#! /bin/bash
curl --silent https://raw.githubusercontent.com/DexterInd/script_tools/master/install_script_tools.sh | bash

# needs to be sourced from here when we call this as a standalone
source /home/pi/Dexter/lib/Dexter/script_tools/functions_library.sh

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root" 
	exit 1
fi

SCRIPTDIR="$(readlink -f $(dirname $0))"
pushd $SCRIPTDIR > /dev/null

if  ! quiet_mode
then
	echo "  _____            _                                ";
	echo " |  __ \          | |                               ";
	echo " | |  | | _____  _| |_ ___ _ __                     ";
	echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
	echo " | |__| |  __/>  <| ||  __/ |                       ";
	echo " |_____/ \___/_/\_\\__\___|_| _        _            ";
	echo " |_   _|         | |         | |      (_)           ";
	echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
	echo "   | | | '_ \ / _\ | | | / __| __| '__| |/ _ \/ __|";
	echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
	echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
	echo "                                                    ";
	echo "                                                    ";
	echo " "
fi



echo "  ____  _            _   ____  _ "
echo " |  _ \(_)_   _____ | |_|  _ \(_)"
echo " | |_) | \ \ / / _ \| __| |_) | |"
echo " |  __/| |\ V / (_) | |_|  __/| |"
echo " |_|   |_| \_/ \___/ \__|_|   |_|"
echo ""

echo "Welcome to PivotPi Installer."

if ! quiet_mode
	then
	sudo apt-get update
fi
sudo apt-get install python-pip git libi2c-dev i2c-tools python-smbus python3-smbus python-dev -y

echo " "
RASPI_BL="/etc/modprobe.d/raspi-blacklist.conf"
MODS="i2c spi"
if [ -f ${RASPI_BL} ]; then
    echo "Removing blacklist from ${RASPI_BL} . . ."
    echo "=================================================================="
    echo " "
    for i in ${MODS}
    do
        MOD_NAME=$(echo $i | tr [a-z] [A-Z])
        sudo sed -i -e "s/blacklist ${i}-bcm2708/#blacklist ${i}-bcm2708/g" ${RASPI_BL}
        echo "${MOD_NAME} not present or removed from blacklist"
    done
fi

#Adding in /etc/modules
echo " "
echo "Adding I2C-dev and i2c-bcm2708 in /etc/modules . . ."
echo "================================================"
if grep -q "i2c-dev" /etc/modules; then
	echo "I2C-dev already present"
else
	echo i2c-dev >> /etc/modules
	echo "I2C-dev added"
fi
if grep -q "i2c-bcm2708" /etc/modules; then
	echo "i2c-bcm2708 already present"
else
	echo i2c-bcm2708 >> /etc/modules
	echo "i2c-bcm2708 added"
fi

echo " "
echo "Making I2C changes in /boot/config.txt . . ."
echo "================================================"

BOOT_CONFIG="/boot/config.txt"
DTPARAMS="i2c1 i2c_arm"
for i in ${DTPARAMS}
do
    if grep -q "^dtparam=${i}=on$" ${BOOT_CONFIG}; then
        echo "${i} already present"
    else
        echo "dtparam=${i}=on" >> /boot/config.txt
    fi
done

			
cd ../Software/Python
sudo python setup.py install
sudo python3 setup.py install

# install desktop control panel
if [ ! -f /home/pi/Desktop/pivotpi_control_panel.desktop ]
then
	echo "Putting PivotPi Controller on the desktop"
	sudo cp $SCRIPTDIR/../Software/Python/Control_Panel/pivotpi_control_panel.desktop /home/pi/Desktop/.
fi

if [ ! -d /home/pi/Desktop/PivotPi ] 
then
	echo "Putting PivotPi folder on the desktop"
	sudo ln -s  /home/pi/Dexter/PivotPi /home/pi/Desktop/PivotPi
fi

popd					 

if quiet_mode
then
    echo " "
    echo "Installation all done"
    echo "Enjoy your PivotPi!"
else
	echo " "
	echo "Please restart to implement changes!"
	echo "  _____  ______  _____ _______       _____ _______ "
	echo " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|"
	echo " | |__) | |__  | (___    | |  /  \  | |__) | | |   "
	echo " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   "
	echo " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   "
	echo " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   "
	echo " "
	echo "Please restart to implement changes!"
	echo "To Restart type sudo reboot"

	echo "To finish changes, we will reboot the Pi."
	echo "Pi must reboot for changes and updates to take effect."
	echo "If you need to abort the reboot, press Ctrl+C.  Otherwise, reboot!"
	echo "Rebooting in 5 seconds!"
	sleep 1
	echo "Rebooting in 4 seconds!"
	sleep 1
	echo "Rebooting in 3 seconds!"
	sleep 1
	echo "Rebooting in 2 seconds!"
	sleep 1
	echo "Rebooting in 1 seconds!"
	sleep 1
	echo "Rebooting now!  Your Pi wake up with a freshly updated Raspberry Pi!"
	sleep 1
	sudo reboot
fi

