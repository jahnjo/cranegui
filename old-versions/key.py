from evdev import InputDevice, categorize, ecodes
import time
import threading


def getKeyboardInput():
	device = InputDevice("/dev/input/event19")
	device.grab()
	for event in device.read_loop():
	    if event.code == ecodes.KEY_1:
			print "i pressed 1 lol"

def printRegThread():
	while True:
		print "Reg Thread 1"
			time.sleep(0.5)


regThread = threading.Thread(target=printRegThread, args=())
testThread = threading.Thread(target=getKeyboardInput, args=())

regThread.start()
testThread.start()

device.ungrab()

	



