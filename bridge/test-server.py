#!/usr/bin/python2.7

# This script simulates a SimuCopter Client instance and communicates with the
# server via the ZMQ-based protocol.

import zmq
import struct
import logging as log

from time import time


MSG_PING                  = 0x0000

MSG_GET_ACCEL_X           = 0x1001
MSG_GET_ACCEL_Y           = 0x1002
MSG_GET_ACCEL_Z           = 0x1003

MSG_GET_GYRO_X            = 0x1011
MSG_GET_GYRO_Y            = 0x1012
MSG_GET_GYRO_Z            = 0x1013

MSG_GET_STATE_YAW         = 0x1031
MSG_GET_STATE_ROLL        = 0x1032
MSG_GET_STATE_PITCH       = 0x1033

MSG_GET_DESIRED_YAW       = 0x1041
MSG_GET_DESIRED_ROLL      = 0x1042
MSG_GET_DESIRED_PITCH     = 0x1043
MSG_GET_DESIRED_THROTTLE  = 0x1044

MSG_SET_RATE_TARGET_YAW   = 0x1051
MSG_SET_RATE_TARGET_ROLL  = 0x1052
MSG_SET_RATE_TARGET_PITCH = 0x1053

MSG_SET_MOTORS_YAW        = 0x1061
MSG_SET_MOTORS_ROLL       = 0x1062
MSG_SET_MOTORS_PITCH      = 0x1063
MSG_SET_MOTORS_THROTTLE   = 0x1064

MSG_GCS_SEND_TEXT         = 0x2001


SERVER_ADDR = '127.0.0.1'
SERVER_PORT = 5555
ZMQ_ADDR = 'tcp://{}:{}'.format(SERVER_ADDR, SERVER_PORT)


def pack_meta(msg_id, data_size=0):
	return struct.pack('II', msg_id, data_size);

def unpack_meta(data):
	msg_id, data_size = struct.unpack('II', data)
	return msg_id, data_size

def send_msg(sock, msg_id, data):
	pkt_meta = pack_meta(msg_id, len(data))
	sock.send(pkt_meta, flags=zmq.SNDMORE)
	sock.send(data)

def recv_msg(sock):
	meta = sock.recv()
	msg_id, data_size = unpack_meta(meta)
	data = ""
	if sock.getsockopt(zmq.RCVMORE):
		data = sock.recv()

	return msg_id, data


def get_accel(sock):
	def get_part(msg):
		send_msg(sock, msg, "")
		msg_id, data = recv_msg(sock)
		assert msg_id == msg
		return struct.unpack('d', data)[0]
	
	return get_part(MSG_GET_ACCEL_X), get_part(MSG_GET_ACCEL_Y), get_part(MSG_GET_ACCEL_Z)


# INIT

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(ZMQ_ADDR)

from time import sleep
while True:
	x, y, z = get_accel(socket)
	print "Accel: ({:.2f}, {:.2f}, {:.2f})".format(x, y, z)
	sleep(1)
