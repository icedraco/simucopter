#!/usr/bin/python2.7

import zmq
import struct

DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 5555

ZMQ_CONTEXT = zmq.Context()


class BridgeCommand(object):
    @staticmethod
    def by_msg_id(msg_id):
        """
        :param int msg_id: message ID
        :return: message object for the given ID, or None if unknown message ID
        :rtype: BridgeCommand|None
        """
        result = [cmd for cmd in ALL_COMMANDS if cmd.msg_id == msg_id]  # TODO: optimize if really necessary
        return result[0] if result else None

    def __init__(self, msg_id, arg_types=None, ret_type=None):
        """
        :param int msg_id:
        :param str arg_types:
        :param str ret_type:
        """
        self.msg_id = msg_id
        self.arg_types = arg_types
        self.ret_type = ret_type

    def ret(self, data):
        """
        :param str data:
        :return:
        :rtype: str|None
        """
        return struct.unpack(self.ret_type, data)[0] if self.ret_type else None

    def args(self, *args):
        """
        :param tuple args:
        :return:
        :rtype: str|None
        """
        return struct.pack(self.arg_types, *args) if self.arg_types else None


class BridgeClient(object):
    DEFAULT_BLOCKING_TIMEOUT = 1000  # msec

    def __init__(self):
        self.socket = None

    @property
    def is_connected(self):
        return self.socket is not None

    def connect(self, addr=None, port=None):
        if self.is_connected:
            raise AssertionError('already connected')

        self.socket = ZMQ_CONTEXT.socket(zmq.REQ)
        self.socket.connect('tcp://{}:{}'.format(addr or DEFAULT_ADDR, port or DEFAULT_PORT))
        self.socket.RCVTIMEO = self.DEFAULT_BLOCKING_TIMEOUT

    def disconnect(self):
        if self.is_connected:
            self.socket.close()
            self.socket = None

    def request(self, cmd, *args):
        """
        :param BridgeCommand cmd: bridge command
        :param tuple args: arguments to the command itself in its appropriate type
        :return: result from the command in its appropriate type
        """
        assert self.is_connected

        raw_data = cmd.args(*args)
        raw_meta_msg = pack_meta(cmd.msg_id, len(raw_data) if raw_data is not None else 0)
        if raw_data is None:
            self.socket.send(raw_meta_msg)
        else:
            self.socket.send(raw_meta_msg, flags=zmq.SNDMORE)
            self.socket.send(raw_data)

        # get response
        raw_meta_msg = self.socket.recv()
        rep_msg_id, raw_data = unpack_meta(raw_meta_msg)
        assert cmd.msg_id == rep_msg_id

        return cmd.ret(self.socket.recv()) if self.socket.RCVMORE else None


class BridgeResponder(object):
    def __init__(self):
        self.handle_funcs = {}
        self.socket = None

    @property
    def is_listening(self):
        return self.socket is not None

    def listen(self, addr=None, port=None):
        if self.is_listening:
            raise AssertionError("Already listening")

        self.socket = ZMQ_CONTEXT.socket(zmq.REP)
        self.socket.bind('tcp://{}:{}'.format(addr or DEFAULT_ADDR, port or DEFAULT_PORT))

    def handle(self, cmd, handle_func):
        """
        :param BridgeCommand cmd:
        :param callable handle_func: handler function that receives arguments for the command and returns the response
        :return: self
        """
        self.handle_funcs[cmd.msg_id] = handle_func
        return self

    def loop(self):
        assert self.is_listening
        # TODO: try to handle the next message for X msecs; return if handled or expired

        pass


def pack_meta(msg_id, data_size=0):
    return struct.pack('II', msg_id, data_size)


def unpack_meta(data):
    msg_id, data_size = struct.unpack('II', data)
    return msg_id, data_size


###############################################################################
# BRIDGE COMMANDS #############################################################
###############################################################################

# return types
RET_DOUBLE = 'd'
RET_UINT = 'I'
RET_INT = 'i'

# argument types
ARG_DOUBLE = 'd'
ARG_UINT = 'I'
ARG_INT = 'i'

# commands themselves
MSG_PING = BridgeCommand(0x0000)

MSG_GET_ACCEL_X = BridgeCommand(0x1001, ret_type=RET_DOUBLE)
MSG_GET_ACCEL_Y = BridgeCommand(0x1002, ret_type=RET_DOUBLE)
MSG_GET_ACCEL_Z = BridgeCommand(0x1003, ret_type=RET_DOUBLE)

MSG_GET_GYRO_X = BridgeCommand(0x1011, ret_type=RET_DOUBLE)
MSG_GET_GYRO_Y = BridgeCommand(0x1012, ret_type=RET_DOUBLE)
MSG_GET_GYRO_Z = BridgeCommand(0x1013, ret_type=RET_DOUBLE)

MSG_GET_STATE_YAW = BridgeCommand(0x1031, ret_type=RET_DOUBLE)
MSG_GET_STATE_ROLL = BridgeCommand(0x1032, ret_type=RET_DOUBLE)
MSG_GET_STATE_PITCH = BridgeCommand(0x1033, ret_type=RET_DOUBLE)

MSG_GET_DESIRED_YAW = BridgeCommand(0x1041, ret_type=RET_DOUBLE)
MSG_GET_DESIRED_ROLL = BridgeCommand(0x1042, ret_type=RET_DOUBLE)
MSG_GET_DESIRED_PITCH = BridgeCommand(0x1043, ret_type=RET_DOUBLE)
MSG_GET_DESIRED_THROTTLE = BridgeCommand(0x1044, ret_type=RET_DOUBLE)

MSG_SET_RATE_TARGET_YAW = BridgeCommand(0x1051, arg_types=ARG_DOUBLE)
MSG_SET_RATE_TARGET_ROLL = BridgeCommand(0x1052, arg_types=ARG_DOUBLE)
MSG_SET_RATE_TARGET_PITCH = BridgeCommand(0x1053, arg_types=ARG_DOUBLE)

MSG_SET_MOTORS_YAW = BridgeCommand(0x1061, arg_types=ARG_DOUBLE)
MSG_SET_MOTORS_ROLL = BridgeCommand(0x1062, arg_types=ARG_DOUBLE)
MSG_SET_MOTORS_PITCH = BridgeCommand(0x1063, arg_types=ARG_DOUBLE)
MSG_SET_MOTORS_THROTTLE = BridgeCommand(0x1064, arg_types=ARG_DOUBLE)

MSG_GCS_SEND_TEXT = BridgeCommand(0x2001)  # TODO

ALL_COMMANDS = [
    MSG_GET_ACCEL_X, MSG_GET_ACCEL_Y, MSG_GET_ACCEL_Z,
    MSG_GET_GYRO_X, MSG_GET_GYRO_Y, MSG_GET_GYRO_Z,
    MSG_GET_STATE_YAW, MSG_GET_STATE_ROLL, MSG_GET_STATE_PITCH,
    MSG_GET_DESIRED_YAW, MSG_GET_DESIRED_ROLL, MSG_GET_DESIRED_PITCH, MSG_GET_DESIRED_THROTTLE,
    MSG_SET_RATE_TARGET_YAW, MSG_SET_RATE_TARGET_ROLL, MSG_SET_RATE_TARGET_PITCH,
    MSG_SET_MOTORS_YAW, MSG_SET_MOTORS_ROLL, MSG_SET_MOTORS_PITCH, MSG_SET_MOTORS_THROTTLE,
    MSG_GCS_SEND_TEXT,
]
