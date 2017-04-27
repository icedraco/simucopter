#ifndef ARDUPILOT_SIMUCOPTER_H
#define ARDUPILOT_SIMUCOPTER_H


//-----------------------------------------------------------------------------
// Simulink Agent -> prepare bridge client/requester
//-----------------------------------------------------------------------------
#ifdef SIMULINK_AGENT
#include "simucopter-requester.h"

//-----------------------------------------------------------------------------
// Bridge Diagnostic Component
//-----------------------------------------------------------------------------
#elif DIAGNOSTIC
#include "simucopter-requester.h"

//-----------------------------------------------------------------------------
// ArduPilot Server
//-----------------------------------------------------------------------------
#else
#include <pthread.h>
#include "simucopter-copter.h"
#include "current-flight-mode.h"
#endif

#include "Copter.h"

#define ADDR_ARDUCOPTER "tcp://127.0.0.1:5555"
#define ADDR_SITL       "tcp://127.0.0.1:5556"


struct copter_envelope {
    Copter copter;
    copter_envelope(Copter& c) : copter(c) {}
};

extern void simucopter_init();
extern void simucopter_stop();
void simucopter_requester_init();
void simucopter_requester_stop();
void simucopter_flight_mode_init();
void simucopter_flight_mode_run();


/*****************************************************************************\
 * Simulink Message IDs ******************************************************
\*****************************************************************************/

#define MSG_PING                  0x0000
#define MSG_ERROR                 0xffff

// UAV-related messages start at 0x1000

#define MSG_GET_ACCEL_X           0x1001
#define MSG_GET_ACCEL_Y           0x1002
#define MSG_GET_ACCEL_Z           0x1003

#define MSG_GET_GYRO_X            0x1011
#define MSG_GET_GYRO_Y            0x1012
#define MSG_GET_GYRO_Z            0x1013

#define MSG_GET_STATE_YAW         0x1031
#define MSG_GET_STATE_ROLL        0x1032
#define MSG_GET_STATE_PITCH       0x1033

#define MSG_GET_DESIRED_YAW       0x1041
#define MSG_GET_DESIRED_ROLL      0x1042
#define MSG_GET_DESIRED_PITCH     0x1043
#define MSG_GET_DESIRED_THROTTLE  0x1044

#define MSG_SET_RATE_TARGET_YAW   0x1051
#define MSG_SET_RATE_TARGET_ROLL  0x1052
#define MSG_SET_RATE_TARGET_PITCH 0x1053

#define MSG_SET_MOTORS_YAW        0x1061
#define MSG_SET_MOTORS_ROLL       0x1062
#define MSG_SET_MOTORS_PITCH      0x1063
#define MSG_SET_MOTORS_THROTTLE   0x1064

// GCS communication messages start at 0x2000

#define MSG_GCS_SEND_TEXT         0x2001

// SITL-related messages start at 0x3000

#define MSG_SITL_WHATEVER         0x3000


/*****************************************************************************\
 * Flight Mode Functions *****************************************************
\*****************************************************************************/

/** IMPORTANT:
 * These functions must be implemented by all sides executing the flight mode!
 */

double copter_get_accel_x();
double copter_get_accel_y();
double copter_get_accel_z();

double copter_get_gyro_x();
double copter_get_gyro_y();
double copter_get_gyro_z();

double copter_get_state_yaw();
double copter_get_state_roll();
double copter_get_state_pitch();

double copter_get_desired_yaw();
double copter_get_desired_roll();
double copter_get_desired_pitch();
double copter_get_desired_throttle();

void copter_set_rate_target_yaw(double yaw);
void copter_set_rate_target_pitch(double pitch);
void copter_set_rate_target_roll(double roll);

// see ardupilot/libraries/AP_Motors/AP_Motors_Class.h
void copter_motors_set_roll(double roll);
void copter_motors_set_pitch(double pitch);
void copter_motors_set_yaw(double yaw);
void copter_motors_set_throttle(double throttle);

void copter_gcs_send_text(int severity, const char* str);

double sitl_whatever();

#endif //ARDUPILOT_SIMUCOPTER_H
