from evdev import InputDevice, categorize, ecodes


device = InputDevice("/dev/input/event19")
device.grab()

for event in device.read_loop():
	if event.code == ecodes.KEY_1:
		print "i pressed 1 lol"

device.ungrab()





	



