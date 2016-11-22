#! /bin/bash

#check if there's an argument on the command line
if [[ -f /home/pi/quiet_mode ]]
then
	quiet_mode=1
else
	quiet_mode=0
fi

if [[ "$quiet_mode" -eq "0" ]]
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


echo "Welcome to PivotPi Installer."
echo "  ____  _            _   ____  _ "
echo " |  _ \(_)_   _____ | |_|  _ \(_)"
echo " | |_) | \ \ / / _ \| __| |_) | |"
echo " |  __/| |\ V / (_) | |_|  __/| |"
echo " |_|   |_| \_/ \___/ \__|_|   |_|"
echo ""
			
pushd /home/pi/Dexter/PivotPi/Software/Python
sudo python setup.py
sudo python3 setup.py
popd					 

if [[ "$quiet_mode" -eq 0 ]]
then
	echo " "
	echo "Please restart the Raspberry Pi for the changes to take effect"
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
fi
