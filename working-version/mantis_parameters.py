import numpy as np

#class mantis_parameters (object):

def right_outrigger ():
    r_outrigger = 42.0
    return r_outrigger

def left_outrigger():
    l_outrigger = 42.0
    return l_outrigger

def left_sideframeCG ():
    l_sideframeCG = np.array([0.0, 120.0, 0.0])
    return l_sideframeCG

def right_sideframeCG ():
    r_sideframeCG = np.array([0.0, -120.0, 0.0])
    return r_sideframeCG

def head_pin ():
    headpin_position = np.array([0.0, 506.5, -47.0])
    return headpin_position

def headpin_weight ():
    head_pin_weight = np.array([1.0, 1.0, 1.0])
    return head_pin_weight

def hing_pin ():
     hingepin_position = np.array([0.0, -83.75, 130.1])
     return hingepin_position

def carbody_weight ():
     cb_weight = 40666.0
     return cb_weight

def carbodyCG ():
    carbody_CG = np.array([0.0, 0.0, 0.0])
    return carbody_CG

def sideframe_weight ():
    sf_weight = 30300.0
    return sf_weight

def boom_weight ():
    boomWeight = 41334.0
    return boomWeight

def boom_extension ():
    boomExtension = 338.4
    return boomExtension

def boom_CG ():
    boomCG = np.array([379.62, 0.0, 0.0])
    return boomCG

def upper_CG ():
    upperCG = np.array([-40.0, 0.0, 80.0])
    return upperCG

def upper_weight ():
    upperWeight = 50000.0
    return upperWeight

def slew_bearing ():
    slewBearing = np.array([0.0, 0.0, 60.0])
    return slewBearing

def counterweight_extension ():
    counterweightE = 0
    return counterweightE

def counterweight_weight ():
    counterW = 100000
    return counterW

def counterweight_CG ():
    counterweightCG = np.array([-164.0, 0.0, 91.0])
    return counterweightCG

def theta ():
    thetaAngle = 0
    return thetaAngle

def beta ():
    betaAngle = 0
    return betaAngle

def error ():
    error1 = 0.0001
    return error1