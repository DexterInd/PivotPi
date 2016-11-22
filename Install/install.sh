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



echo "  ____  _            _   ____  _ "
echo " |  _ \(_)_   _____ | |_|  _ \(_)"
echo " | |_) | \ \ / / _ \| __| |_) | |"
echo " |  __/| |\ V / (_) | |_|  __/| |"
echo " |_|   |_| \_/ \___/ \__|_|   |_|"
echo ""

echo "Welcome to PivotPi Installer."
			
pushd /home/pi/Dexter/PivotPi/Software/Python
sudo python setup.py install
sudo python3 setup.py install
popd					 

if [[ "$quiet_mode" -eq 0 ]]
then
    echo " "
    echo "Installation all done"
    echo "Enjoy your PivotPi!"
fi