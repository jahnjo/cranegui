import u6
import os
import time

DAQ = u6.U6()

def calibrateIncline(incline):
	calibratedVal = (incline / 0.125) - 20
	if calibratedVal < -20:
		calibratedVal = -20
	elif calibratedVal > 20:
		calibratedVal = 20
	return calibratedVal

def calibrateOutrigger(outriggerPos):
	calibratedVal = (outriggerPos / 0.1471)
	if calibratedVal < 0:
		calibratedVal = 0
	elif calibratedVal > 34:
		calibratedVal = 34
	return calibratedVal

def calibrateSlewAngle(slewAngle):
	calibratedVal = (slewAngle / 0.0139)
	if calibratedVal < 0:
		calibratedVal = 0
	elif calibratedVal > 359:
		calibratedVal = 359
	return calibratedVal

while True:
	test0 = DAQ.getAIN(0)
	test1 = DAQ.getAIN(1)
	test2 = DAQ.getAIN(2)
	test3 = DAQ.getAIN(3)
	test4 = DAQ.getAIN(4)
	test5 = DAQ.getAIN(5)
	test6 = DAQ.getAIN(6)
	test7 = DAQ.getAIN(7)
	test8 = DAQ.getAIN(8)
	test9 = DAQ.getAIN(9)

	pitch = calibrateIncline(test5)
	roll = calibrateIncline(test6)
	outL = calibrateOutrigger(test3)
	outR = calibrateOutrigger(test4)
	slewAngle = calibrateSlewAngle(test0)

	print 'slew angle     ' + ' ' + str(slewAngle)
	print 'boom length    ' + ' ' + str(test1)
	print 'boom angle     ' + ' ' + str(test2)
	print 'left outrigger ' + ' ' + str(outL)
	print 'right outrigger' + ' ' + str(outR)
	print 'pitch          ' + ' ' + str(pitch)
	print 'roll           ' + ' ' + str(roll)
	print 'load y         ' + ' ' + str(test7)
	print 'load x         ' + ' ' + str(test8)
	print 'load weight    ' + ' ' + str(test9)

	time.sleep(1)
	os.system('clear')