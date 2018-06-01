#! /bin/bash
# This script updates the the code repos on Raspbian for Robots.

# definitions needed for standalone call
PIHOME=/home/pi
DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER
RASPBIAN=$PIHOME/di_update/Raspbian_For_Robots
PIVOTPI_DIR=$DEXTER_PATH/PivotPi
DEXTERSCRIPT=$DEXTER_PATH/lib/Dexter/script_tools

################################################
######## Parsing Command Line Arguments ########
################################################

# the top-level module name of each package
# used for identifying present packages
REPO_PACKAGE=pivotpi

# called way down bellow
check_if_run_with_pi() {
  ## if not running with the pi user then exit
  if [ $(id -ur) -ne $(id -ur pi) ]; then
    echo "PivotPi installer script must be run with \"pi\" user. Exiting."
    exit 7
  fi
}

# called way down below
parse_cmdline_arguments() {

  # whether to install the dependencies or not (avrdude, apt-get, wiringpi, and so on)
  installdependencies=true
  updaterepo=true
  install_rfrtools=true
  install_pkg_rfrtools=true

  # the following 3 options are mutually exclusive
  systemwide=true
  userlocal=false
  envlocal=false
  usepython3exec=true

  # the following option tells which branch has to be used
  selectedbranch="master"

  declare -ga rfrtools_options=("--system-wide")
  # iterate through bash arguments
  for i; do
    case "$i" in
      --no-dependencies)
        installdependencies=false
        ;;
      --no-update-aptget)
        updaterepo=false
        ;;
      --bypass-rfrtools)
        install_rfrtools=false
        ;;
      --bypass-python-rfrtools)
        install_pkg_rfrtools=false
        ;;
      --user-local)
        userlocal=true
        systemwide=false
        declare -ga rfrtools_options=("--user-local")
        ;;
      --env-local)
        envlocal=true
        systemwide=false
        declare -ga rfrtools_options=("--env-local")
        ;;
      --system-wide)
        ;;
      develop|feature/*|hotfix/*|fix/*|DexterOS*|v*)
        selectedbranch="$i"
        ;;
    esac
  done

  # show some feedback on the console
  if [ -f $DEXTERSCRIPT/functions_library.sh ]; then
    source $DEXTERSCRIPT/functions_library.sh
    # show some feedback for the PivotPi
    if [[ quiet_mode -eq 0 ]]; then
      echo "  _____            _                                ";
      echo " |  __ \          | |                               ";
      echo " | |  | | _____  _| |_ ___ _ __                     ";
      echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
      echo " | |__| |  __/>  <| ||  __/ |                       ";
      echo " |_____/ \___/_/\_\\\__\___|_|          _            ";
      echo " |_   _|         | |         | |      (_)           ";
      echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
      echo "   | | | '_ \ / _\ | | | / __| __| '__| |/ _ \/ __| ";
      echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
      echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
      echo "                                                    ";
      echo "                                                    ";
      echo "  ____  _            _   ____  _ "
      echo " |  _ \(_)_   _____ | |_|  _ \(_)"
      echo " | |_) | \ \ / / _ \| __| |_) | |"
      echo " |  __/| |\ V / (_) | |_|  __/| |"
      echo " |_|   |_| \_/ \___/ \__|_|   |_|"
      echo ""
    fi

    feedback "Welcome to PivotPi Installer."
  else
    echo "Welcome to PivotPi Installer."
  fi

  echo "Updating PivotPi for $selectedbranch branch with the following options:"
  ([[ $installdependencies = "true" ]] && echo "  --no-dependencies=false") || echo "  --no-dependencies=true"
  ([[ $updaterepo = "true" ]] && echo "  --no-update-aptget=false") || echo "  --no-update-aptget=true"
  ([[ $install_rfrtools = "true" ]] && echo "  --bypass-rfrtools=false") || echo "  --bypass-rfrtools=true"
  ([[ $install_pkg_rfrtools = "true" ]] && echo "  --bypass-python-rfrtools=false") || echo "  --bypass-python-rfrtools=true"
  echo "  --user-local=$userlocal"
  echo "  --env-local=$envlocal"
  echo "  --system-wide=$systemwide"

  # in case the following packages are not installed and `--no-dependencies` option has been used
  if [[ $installdependencies = "false" || $install_rfrtools = "false" ]]; then
    command -v git >/dev/null 2>&1 || { echo "This script requires \"git\" but it's not installed. Don't use --no-dependencies option. Exiting." >&2; exit 1; }
    command -v python >/dev/null 2>&1 || { echo "Executable \"python\" couldn't be found. Don't use --no-dependencies option. Exiting." >&2; exit 2; }
    command -v python3 >/dev/null 2>&1 || { echo "Executable \"python3\" couldn't be found. Don't use --no-dependencies option. Exiting." >&2; exit 3; }
    command -v pip >/dev/null 2>&1 || { echo "Executable \"pip\" couldn't be found. Don't use --no-dependencies option. Exiting." >&2; exit 4; }
    command -v pip3 >/dev/null 2>&1 || { echo "Executable \"pip3\" couldn't be found. Don't use --no-dependencies option. Exiting." >&2; exit 5; }
  fi

  # create rest of list of arguments for rfrtools call
  rfrtools_options+=("$selectedbranch")
  [[ $usepython3exec = "true" ]] && rfrtools_options+=("--use-python3-exe-too")
  [[ $updaterepo = "true" ]] && rfrtools_options+=("--update-aptget")
  [[ $installdependencies = "true" ]] && rfrtools_options+=("--install-deb-deps")
  [[ $install_pkg_rfrtools = "true" ]] && rfrtools_options+=("--install-python-package")

  # create list of arguments for script_tools call
  declare -ga scriptools_options=("$selectedbranch")

  echo "Using \"$selectedbranch\" branch"
  echo "Options used for RFR_Tools script: \"${rfrtools_options[@]}\""
  echo "Options used for script_tools script: \"${scriptools_options[@]}\""
}

#################################################
## Cloning PivotPi, Script_Tools & RFR_Tools ####
#################################################

# called way down below
install_scriptools_and_rfrtools() {

  # if rfrtools is not bypassed then install it
  if [[ $install_rfrtools = "true" ]]; then
    curl --silent -kL https://raw.githubusercontent.com/DexterInd/RFR_Tools/$selectedbranch/scripts/install_tools.sh > $PIHOME/.tmp_rfrtools.sh
    echo "Installing RFR_Tools. This might take a while.."
    bash $PIHOME/.tmp_rfrtools.sh ${rfrtools_options[@]} # > /dev/null
    ret_val=$?
    rm $PIHOME/.tmp_rfrtools.sh
    if [[ $ret_val -ne 0 ]]; then
      echo "RFR_Tools failed installing with exit code $ret_val. Exiting."
      exit 7
    fi
    echo "Done installing RFR_Tools"
  fi

  # update script_tools first
  curl --silent -kL https://raw.githubusercontent.com/DexterInd/script_tools/$selectedbranch/install_script_tools.sh > $PIHOME/.tmp_script_tools.sh

  echo "Installing script_tools. This might take a while.."
  bash $PIHOME/.tmp_script_tools.sh $selectedbranch > /dev/null
  ret_val=$?
  rm $PIHOME/.tmp_script_tools.sh
  if [[ $ret_val -ne 0 ]]; then
    echo "script_tools failed installing with exit code $ret_val. Exiting."
    exit 6
  fi
  # needs to be sourced from here when we call this as a standalone
  source $DEXTERSCRIPT/functions_library.sh
  feedback "Done installing script_tools"
}

# called way down bellow
clone_pivotpi() {
  # $DEXTER_PATH is still only available for the pi user
  # shortly after this, we'll make it work for any user
  sudo mkdir -p $DEXTER_PATH
  sudo chown pi:pi -R $DEXTER_PATH
  cd $DEXTER_PATH
  # it's simpler and more reliable (for now) to just delete the repo and clone a new one
  # otherwise, we'd have to deal with all the intricacies of git
  sudo rm -rf $PIVOTPI_DIR
  git clone --quiet --depth=1 -b $selectedbranch https://github.com/DexterInd/PivotPi.git
  cd $PIVOTPI_DIR
}

################################################
######## Install Python Packages & Deps ########
################################################

# called by <<install_python_pkgs_and_dependencies>>
install_python_packages() {
  [[ $systemwide = "true" ]] && sudo python setup.py install \
              && [[ $usepython3exec = "true" ]] && sudo python3 setup.py install
  [[ $userlocal = "true" ]] && python setup.py install --user \
              && [[ $usepython3exec = "true" ]] && python3 setup.py install --user
  [[ $envlocal = "true" ]] && python setup.py install \
              && [[ $usepython3exec = "true" ]] && python3 setup.py install
}

# called by <<install_python_pkgs_and_dependencies>>
remove_python_packages() {
  # the 1st and only argument
  # takes the name of the package that needs to removed
  rm -f $PIHOME/.pypaths

  # get absolute path to python package
  # saves output to file because we want to have the syntax highlight working
  # does this for both root and the current user because packages can be either system-wide or local
  # later on the strings used with the python command can be put in just one string that gets used repeatedly
  python -c "import pkgutil; import os; \
              eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
              output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
  sudo python -c "import pkgutil; import os; \
              eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
              output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
  if [[ $usepython3exec = "true" ]]; then
    python3 -c "import pkgutil; import os; \
                eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
                output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
    sudo python3 -c "import pkgutil; import os; \
                eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
                output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
  fi

  # removing eggs for $1 python package
  # ideally, easy-install.pth needs to be adjusted too
  # but pip seems to know how to handle missing packages, which is okay
  while read path;
  do
    if [ ! -z "${path}" -a "${path}" != " " ]; then
      echo "Removing ${path} egg"
      sudo rm -f "${path}"
    fi
  done < $PIHOME/.pypaths
}

# called by <<install_python_pkgs_and_dependencies>>
configure_interfaces() {
  RASPI_BL="/etc/modprobe.d/raspi-blacklist.conf"
  MODS="i2c spi"
  if [ -f ${RASPI_BL} ]; then
      echo "Removing blacklist from ${RASPI_BL} . . ."
      for i in ${MODS}
      do
          MOD_NAME=$(echo $i | tr [a-z] [A-Z])
          sudo sed -i -e "s/blacklist ${i}-bcm2708/#blacklist ${i}-bcm2708/g" ${RASPI_BL}
          echo "${MOD_NAME} not present or removed from blacklist"
      done
  fi

  #Adding in /etc/modules
  echo "Adding I2C-dev and i2c-bcm2708 in /etc/modules . . ."
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

  echo "Making I2C changes in /boot/config.txt . . ."

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
}

# called way down bellow
install_python_pkgs_and_dependencies() {
  feedback "Configuring interface for PivotPi and installing python package. This might take a while.."
  configure_interfaces

  # install control panel on desktop
  if [[ -d $PIHOME/Desktop ]]; then
    cp $PIVOTPI_DIR/Software/Python/Control_Panel/pivotpi_control_panel.desktop $PIHOME/Desktop
  fi

  feedback "Removing \"$REPO_PACKAGE\" to make space for the new one"
  remove_python_packages "$REPO_PACKAGE"

  # installing the package itself
  pushd $PIVOTPI_DIR/Software/Python > /dev/null
  install_python_packages
  popd > /dev/null
}

################################################
######## Aggregating all function calls ########
################################################

check_if_run_with_pi
parse_cmdline_arguments "$@"
install_scriptools_and_rfrtools
clone_pivotpi
configure_interfaces
install_python_pkgs_and_dependencies
exit 0
