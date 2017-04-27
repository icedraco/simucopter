#!/usr/bin/env bash

SIMUCOPTER_ROOT=`pwd`
ARDUPILOT_ROOT="${HOME}/ardupilot"

APT_PACKAGES="
    python-matplotlib python-serial python-wxgtk2.8 python-wxtools python-lxml
    python-scipy python-opencv ccache gawk git python-pip python-pexpect
    libzmq3-dev"

PIP_PACKAGES="future pymavlink MAVProxy"

DIAG_SOURCES="
    simucopter.h
    src-agent/Copter.h
    src-agent/simucopter-agent.cpp
    src-agent/simucopter-requester.cpp
    src-agent/simucopter-requester.h
    src-agent/simucopter-requester.h"

###############################################################################

do_install_ardupilot () {
    set -e  # abort on non-zero return code (important!)
    pushd ${HOME}

    git clone https://github.com/ArduPilot/ardupilot
    cd ardupilot
    git submodule update --init --recursive

    popd
    set +e  # DISABLE abort on non-zero return code (important!)
}

echo "--- SimuCopter System Installer Script 1.0 -----------------------------"

###############################################################################

echo
echo ">>> Locating ArduPilot..."
if [ ! -d "${ARDUPILOT_ROOT}" ]; then
    echo "  > ArduPilot directory not found at ${ARDUPILOT_ROOT}!"
    echo "  > Attempt to install it from GitHub?"
    select ans in "Install from GitHub" "Quit"; do
        case ${ans} in
            "Install from GitHub" ) do_install_ardupilot; break;;
            "Quit" ) exit;;
        esac
    done

    # verify
    if [ ! -d "${ARDUPILOT_ROOT}" ]; then
        "FATAL: ArduPilot root still not found! Please resolve this before continuing..."
        exit 1
    fi
fi

###############################################################################

echo
echo ">>> Installing prerequisites..."
echo
sudo apt -y install ${APT_PACKAGES}
sudo pip install ${PIP_PACKAGES}

###############################################################################

echo
echo ">>> Loading submodules (if necessary)..."
echo
if [ ! -f "bridge/bridge.cpp" ] || [ ! -f "simutool/simutool.py" ]; then
    echo "      -> MISSING!"
    git submodule update --init --recursive
fi

###############################################################################

echo
echo ">>> Cleaning all links..."
echo
find -type l -print -delete

###############################################################################

echo
echo ">>> Linking simucopter.h across components..."
echo
for d in "src-agent src-ardupilot"; do
    ln -v simucopter.h ${d}/

    # verify
    if [ ! -f "${d}/simucopter.h" ]; then
        echo "FATAL: simucopter.h NOT FOUND AT DESTINATION: ${d}"
        exit 1
    fi
done

###############################################################################

echo
echo ">>> Preparing bridge diagnostic component..."
echo
for f in ${DIAG_SOURCES}; do
    ln -sv ${f} src-diagnostic/

    # verify
    if [ ! -f "src-diagnostic/${f}" ]; then
        echo "WARNING/DIAGNOSTIC COMPONENT: LINK FAILED FOR ${f}"
    fi
done

###############################################################################

echo
echo ">>> Installing SimuCopter system..."
echo

if [ ! -d "patch" ]; then
    echo "FATAL: Cannot locate the 'patch' subfolder!"
    exit 1
fi

# fetch absolute path for the patch folder for later
pushd patch
PATCH_ROOT=`pwd`
popd

echo "  > ARDUPILOT_ROOT:  ${ARDUPILOT_ROOT}"
echo "  > SIMUCOPTER_ROOT: ${SIMUCOPTER_ROOT}"
echo "  > PATCH_ROOT:      ${PATCH_ROOT}"
echo

# begin install

#------------------------------------------------------------------------------
# NOTE: DO NOT SYMLINK FILES INTO ArduCopter DIRECTORY!
#       SYMLINKS ARE DYNAMICALLY CREATED AND DESTROYED, AND THIS LINK WILL TOO!
#------------------------------------------------------------------------------

echo "  * Copying/linking SimuCopter files into ArduPilot..."
echo "      > ArduCopter files..."
cp -v "${PATCH_ROOT}/control_simulink.cpp" "${ARDUPILOT_ROOT}/ArduCopter/"
echo

echo "      > general bridge library"
pushd "${ARDUPILOT_ROOT}/libraries"
#---
mkdir -p bridge
pushd bridge
ln -vs "${SIMUCOPTER_ROOT}/bridge/bridge*" ./
echo
popd  # bridge
#---

pushd AP_HAL_SITL
echo "      > SITL bridge server"
ln -vs "${SIMUCOPTER_ROOT}/src-sitl/*" ./
echo
popd  # AP_HAL_SITL
popd  # ardupilot/libraries

echo "  * Applying SimuCopter patch..."
pushd ${ARDUPILOT_ROOT}
patch -p1 < "${PATCH_ROOT}/simucopter.patch"
popd

###############################################################################

echo
echo "### DEPLOYMENT COMPLETE"
echo
exit 0
