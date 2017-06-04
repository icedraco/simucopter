/***
 * This module is responsible for handling messages on behalf of SITL
 * executable and knows how to handle SITL-specific messages
 */

#include <assert.h>

#include "simucopter-server-sitl.h"

extern const AP_HAL::HAL& hal;

static void* sock_rep;

void simucopter_sitl_step()
{
    int rc;
    struct s_req_msg msg;

    rc = bridge_recv(sock_rep, &msg);
    assert(rc >= 0);
    if (rc > 0) {
        assert(msg.flag_ok);
        switch (msg.msg_id) {
            case MSG_PING:
                bridge_rep_confirm(msg.socket, msg.msg_id);
                break;

            case MSG_SITL_WHATEVER:
                bridge_rep_double(msg.socket, msg.msg_id, 13.37);
                break;

            default:
                bridge_rep_confirm(msg.socket, msg.msg_id);
                break;
        }
    }


// TODO: Implement setters as necessary using the example below
//        if (msg.data_sz > 0) {
//            // received a bridge_req_set_double()
//            memcpy(&current_value, msg.data, msg.data_sz);
//            bridge_rep_confirm(sock_rep, msg.msg_id);
//        } else {
//            // received a bridge_req_double()
//            current_value = G_TEST_VALUES[i++];
//            bridge_rep_double(sock_rep, msg.msg_id, current_value);
//            if (current_value == 0) i = 0; // reached end of list
//        }
}

void simucopter_sitl_init()
{
    // this function is activated from ArduPilot/SITL module

    // server-side initialization
    bridge_init();
    sock_rep = bridge_rep_socket(ADDR_SITL);
    if (sock_rep == NULL) {
        perror("bridge_rep_socket");
        assert(false); // bridge_rep_socket() returned NULL
    }

    hal.scheduler->register_timer_process(FUNCTOR_BIND_MEMBER(simucopter_sitl_step, void));
}

void simucopter_sitl_stop()
{
    // no way to stop yet
}
