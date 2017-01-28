import bridge
from time import sleep

client = bridge.BridgeClient()
client.connect('127.0.0.1', '5555')

while True:
	x = client.request(bridge.MSG_GET_STATE_YAW)
	print "YAW = {}".format(x)

	client.request(bridge.MSG_SET_MOTORS_THROTTLE, 1.0)
	sleep(0.5)

