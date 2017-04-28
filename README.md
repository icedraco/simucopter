  **NOTE**: The MATLAB/Simulink side of this project is located here: https://github.com/icedraco/simucopter-matlab
  

# Installing ArduPilot and SimuCopter
Follow the steps below to install ArduPilot and SimuCopter on the UAV / Raspberry Pi.

```
cd ~
git clone https://github.com/icedraco/simucopter.git simucopter
cd simucopter
bash ./install.sh
```

The install script will attempt to build everything, and if necessary,
also download and install ArduPilot for you in the home directory.


## Testing Deploy Script

You may use simutool directly to deploy (i.e., compile and run) the arducopter executable
and make sure that everything compiles as it should:

    python ~/simucopter/simutool/simutool.py deploy TestFlightMode

**NOTE**


Make sure your Simulink build path is set to **/home/pi/simucopter** and that there is a compiled version of **TestFlightMode.elf** exists in the build path. You may need to run TestFlightMode from Simulink first to deploy that executable.


## Debugging

You may watch the compilation/execution process in the log file:

    tail -f ~/TestFlightMode.log

It will be created as soon as the deploy script is executed by the Simulink
agent.


#### MAVProxy Configuration

Start MAVProxy like so in order to connect to the running ArduCopter:

    "C:\Program Files (x86)\MAVProxy\mavproxy.exe" --master=tcp:10.66.66.254:5760 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --console --map
- Replace 10.66.66.254 with the IP address of the Raspberry PI


## Killing Processes

Currently, there is no way to gracefully shut down the system in mid-operation. As such, you may need to kill executables before re-running the deployment process from Simulink:


    sudo killall -9 TestFlightMode.elf arducopter


## Updating ArduPilot

The most fool-proof way to go about doing that is to remove the existing `~/ardupilot`
directory and re-run `install.sh` from `simucopter`. This will download a new current
copy to the RaspberryPi and re-install the SimuCopter code. Downloading ArduPilot,
however may take a while.

You may also try to `git stash` the changes made to `ardupilot`, `git pull` to update
ArduPilot, then `git stash pop` to restore those changes:

    cd ~/ardupilot
    git stash
    git pull
    git stash pop

This operation, however, may be less trivial.
