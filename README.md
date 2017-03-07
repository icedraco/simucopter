# Installing ArduPilot and SimuCopter
Follow the steps below to install ArduPilot and SimuCopter on the UAV / Raspberry Pi.


## Install Prerequisites
    sudo apt-get install python-matplotlib python-serial python-wxgtk2.8 python-wxtools python-lxml python-scipy python-opencv ccache gawk git python-pip python-pexpect libzmq3-dev
    
    sudo pip install future pymavlink MAVProxy


## Install ArduPilot
    cd ~
    git clone https://github.com/ArduPilot/ardupilot
    cd ardupilot
    git submodule update --init --recursive

Reference URL: http://ardupilot.org/dev/docs/setting-up-sitl-on-linux.html


## Install SimuCopter
    cd ~
    git clone https://github.com/icedraco/simucopter.git simucopter
    cd simucopter
    git submodule update --init --recursive


## Patch ArduCopter code
    cp ~/simucopter/patch/control_simulink.cpp ~/ardupilot/ArduCopter/
    cd ~/ardupilot
    patch -p5 < ~/simucopter/patch/simucopter-20170306.patch


## Test Deploy Script

You may now use simutool to deploy (i.e., compile and run) the arducopter executable and make sure that everything compiles as it should:


    python ~/simucopter/simutool/simutool.py deploy TestFlightMode

**NOTE**


Make sure your Simulink build path is set to **/home/pi/simucopter** and that there is a compiled version of **TestFlightMode.elf** exists in the build path. You may need to run TestFlightMode from Simulink first to deploy that executable.


## Debugging

You may watch the compilation/execution process in the log file:

    tail -f ~/simucopter/runtime.log

It will be created as soon as the deploy script is executed by the Simulink agent. If **runtime.log** is not in ~/simucopter (it should be), try looking in ~ instead.


#### MAVProxy Configuration

Start MAVProxy like so in order to connect to the running ArduCopter:

    "C:\Program Files (x86)\MAVProxy\mavproxy.exe" --master=tcp:10.66.66.254:5760 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --console --map
- Replace 10.66.66.254 with the IP address of the Raspberry PI


## Killing Processes

Currently, there is no way to gracefully shut down the system in mid-operation. As such, you may need to kill executables before re-running the deployment process from Simulink:


    sudo killall -9 TestFlightMode.elf arducopter


## Updating ArduPilot

When updating ArduPilot to the latest version from its Git repository, it is necessary to stash the modifications we made to the source code, update the source from origin, then restore the SimuCopter changes onto the newly updated source code:


    cd ~/ardupilot
    git stash
    git pull
    git stash pop
