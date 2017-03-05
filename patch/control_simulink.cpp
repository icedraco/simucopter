#include "simucopter.h"
#include "Copter.h"

/*
 * Init and run calls for simulink flight mode
 */

// simulink_init - initialise simulink controller
bool Copter::simulink_init(bool ignore_checks)
{
    simucopter_flight_mode_init();
    return true;
}

// simulink_run - runs the simulink controller
// should be called at 100hz or more
void Copter::simulink_run()
{
    simucopter_flight_mode_run();
}

