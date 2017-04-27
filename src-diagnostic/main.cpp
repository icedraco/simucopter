#include <stdio.h>

#include "simucopter-requester.h"



int main(int argc, char **argv) {
    printf("=== Simulink-ArduPilot Bridge Diagnostic Tool 1.0 =================\n\n");

    printf(" * requester_init()... ");
    requester_init();
    printf("OK\n");

    printf(" * Requesting getter commands (ArduPilot component)...\n");
    printf("     > copter_get_accel_x() -> %.4f\n", copter_get_accel_x());
    printf("     > copter_get_accel_y() -> %.4f\n", copter_get_accel_y());
    printf("     > copter_get_accel_z() -> %.4f\n", copter_get_accel_z());
    printf("     > copter_get_gyro_x() -> %.4f\n", copter_get_gyro_x());
    printf("     > copter_get_gyro_y() -> %.4f\n", copter_get_gyro_y());
    printf("     > copter_get_gyro_z() -> %.4f\n", copter_get_gyro_z());
    printf("     > copter_get_state_yaw() -> %.4f\n", copter_get_state_yaw());
    printf("     > copter_get_state_roll() -> %.4f\n", copter_get_state_roll());
    printf("     > copter_get_state_pitch() -> %.4f\n", copter_get_state_pitch());
    printf("     > copter_get_desired_yaw() -> %.4f\n", copter_get_desired_yaw());
    printf("     > copter_get_desired_roll() -> %.4f\n", copter_get_desired_roll());
    printf("     > copter_get_desired_pitch() -> %.4f\n", copter_get_desired_pitch());
    printf("     > copter_get_desired_throttle() -> %.4f\n", copter_get_desired_throttle());
    printf("\n");

    printf(" * Requesting getter commands (SITL component)...\n");
    printf("     > sitl_whatever() -> %.4f\n", sitl_whatever());
    printf("\n");

    printf(" * requester_stop()...\n");
    requester_stop();
    printf("DONE\n");
    return 0;
}