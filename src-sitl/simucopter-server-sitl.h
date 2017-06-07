#ifndef SIMUCOPTER_BRIDGE_SIMUCOPTER_SERVER_SITL_H
#define SIMUCOPTER_BRIDGE_SIMUCOPTER_SERVER_SITL_H

#include <AP_HAL/AP_HAL.h>
#include "bridge/bridge.h"

#define ADDR_SITL       "tcp://127.0.0.1:5556"

/*****************************************************************************\
 * Message IDs ***  ************************************************************
\*****************************************************************************/

#define MSG_PING                  0x0000
#define MSG_ERROR                 0xffff

// SITL-related messages start at 0x3000

#define MSG_SITL_WHATEVER         0x3000


/*****************************************************************************\
 * Class *********************************************************************
\*****************************************************************************/

class SimucopterSitlServer {
public:
    void step();
    void init();
    void stop() { /* nothing */ }

private:
    void* sock_rep;
};


/*****************************************************************************\
 * Functions *****************************************************************
\*****************************************************************************/

void simucopter_sitl_init();
void simucopter_sitl_stop();


#endif //SIMUCOPTER_BRIDGE_SIMUCOPTER_SERVER_SITL_H
