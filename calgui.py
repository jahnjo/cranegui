'''
Cranemaster Realtime LMI GUI
Inputs:
    Incline X (roll) (units:deg) (range -20:20)
    Incline Y (pitch) (units:deg) (range -20:20)
    Outrigger Right (units:inches) (range 0:34)
    Outrigger Left (units:inches) (range 0:34)
    Boom Angle (units:deg) (range 0:75)
'''


from Tkinter import *
import math
import datetime
import u6


#DAQ = u6.U6()


WIDTH = 800
HEIGHT = 480
CANVAS_MID_X = WIDTH/2.5
CANVAS_MID_Y = HEIGHT/2
SIDE = 400



'''
Crane length is 22'7" and the width (no outrigger extension) is 12'
so the width is shorter by a factor of 1.8816. The outriggers extended
fully makes the width 17.8'. 
'''
craneLength = 200
craneWidth = craneLength / 1.8816

'''
With the outiggers extending 34" in each directions that mean that each inch 
increment will increment 1.476 pixels (if the crane length is 400, else pixels per
inch needs to be recalculated) described by the outriggerMod.
'''
outriggerExtRight = 0
outriggerExtLeft = 0
inchToPixel = 1.476

'''
Outrigger length is a constant 9'6", which is 114 inches. The outrigger length, width,
and pitch/roll will be used to calculate the depths for the gui. 
'''
outriggerLength = 114
#base width, but will change with outrigger extension
outriggerRightWidth = 72
outriggerLeftWidth = 72

roll = 0
pitch = 0
slewAngle = 0

boomAngle = 0
boomExtension = 0

backIncX = True
backIncY = True
backBoom = True
polyColor = "green"

root = Tk()
canvas = Canvas(root, bg="white", height=HEIGHT, width=WIDTH)
canvas.pack(fill=BOTH, expand=1)

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

def calibrateBoomAngle(boomAngle):
    calibratedVal = (boomAngle / 0.0667)
    if calibratedVal < 0:
        calibratedVal = 0
    elif calibratedVal > 75:
        calibratedVal = 75
    return calibratedVal

def calibrateBoomExtension(boomExtension):
    calibratedVal = (boomExtension / 0.1786) + 26
    if calibratedVal < 26:
        calibratedVal = 26
    elif calibratedVal > 54:
        calibratedVal = 54
    return calibratedVal

def adjustBoom(midx, midy, boomAngle, boomExtension):
    defaultBoomExt = 26
    radAngle = math.radians(boomAngle)
    boomMod = (math.cos(radAngle)*boomExtension)
    boomPoints = [
        [CANVAS_MID_X - 7, CANVAS_MID_Y - 175 - (boomMod*inchToPixel)],
        [CANVAS_MID_X + 7, CANVAS_MID_Y - 175 - (boomMod*inchToPixel)],
        [CANVAS_MID_X + 7, CANVAS_MID_Y - 20],
        [CANVAS_MID_X - 7, CANVAS_MID_Y - 20],
    ]
    return boomPoints

def polygonColors(inclX, inclY):
    global polyColor
    if inclX > 14 or inclX < -14 or inclY > 14 or inclY < -14:
        polyColor = "red"
    elif inclX > 7 or inclX < -7 or inclY > 7 or inclY < -7:
        polyColor = "yellow"
    elif inclX < 7 or inclX > -7 or inclY < 7 or inclY > -7:
        polyColor = "green"
    return polyColor

def colors(number):
    color = "green"
    if number > 14 or number < -14:
        color = "red"
    elif number > 7 or number < -7:
        color = "yellow"
    elif number < 7 or number > -7:
        color = "green"
    return color

#Very important, takes in sensor values and modifies the shape of the polygon
#based on outrigger pos and inclinometer x/y.
def sensorInput(craneLength, craneWidth, midx, midy, orExtR, orExtL, pitch, roll):
    vertices = [
        [CANVAS_MID_X - craneWidth/2 - (orExtL*inchToPixel) - (roll*3), CANVAS_MID_Y - craneLength/2 + (pitch*3)],
        [CANVAS_MID_X + craneWidth/2 + (orExtR*inchToPixel) + (roll*3), CANVAS_MID_Y - craneLength/2 - (pitch*3)],
        [CANVAS_MID_X + craneWidth/2 + (orExtR*inchToPixel) - (roll*3), CANVAS_MID_Y + craneLength/2 + (pitch*3)],
        [CANVAS_MID_X - craneWidth/2 - (orExtL*inchToPixel) + (roll*3), CANVAS_MID_Y + craneLength/2 - (pitch*3)],
    ]
    return vertices

def incrementBoomAngle():
    global boomAngle
    global backBoom
    if backBoom:
        if boomAngle > 75:
            boomAngle = 75
            backBoom = False
        else:
            boomAngle += 1
    elif not backBoom:
        if boomAngle < 0:
            boomAngle = 0
            backBoom = True
        else:
            boomAngle -= 1

def incrementDeg():
    global slewAngle
    if slewAngle > 359:
        slewAngle = 0
    else:
        slewAngle += 1

def incrementOr():
    global outriggerExtRight
    global outriggerExtLeft
    if outriggerExtRight > 34:
        outriggerExtRight = 0
    else:
        outriggerExtRight += 1
    
    if outriggerExtLeft > 34:
        outriggerExtLeft = 0
    else:
        outriggerExtLeft += 1

def incrementInclineX():
    global roll
    global backIncX
    if backIncX:
        if roll > 20:
            roll = 20
            backIncX = False
        else:
            roll += 1
    elif not backIncX:
        if roll < -20:
            roll = -20
            backIncX = True
        else:
            roll -= 1

def incrementInclineY():
    global pitch
    global backIncY
    if backIncY:
        if pitch > 20:
            pitch = 20
            backIncY = False
        else:
            pitch += 1
    elif not backIncY:
        if pitch < -20:
            pitch = -20
            backIncY = True
        else:
            pitch -= 1

def createCorners(points):
    cornerPoints = []
    n = 0
    for x in points:
        if n == 0:
            a = x[0] - 20
            b = x[1] - 20
            cornerPoints.append([a,b])
        elif n == 1:
            a = x[0] + 20
            b = x[1] - 20
            cornerPoints.append([a,b])
        elif n == 2:
            a = x[0] + 20
            b = x[1] + 20
            cornerPoints.append([a,b])
        elif n == 3:
            a = x[0] - 20
            b = x[1] + 20 
            cornerPoints.append([a,b])   
        n += 1
    return cornerPoints

def rotate(points, angle, center):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center
    new_points = []
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    return new_points

def draw_square(points, polyColor):
    canvas.create_polygon(points, fill=polyColor, outline='black')

def draw_bg():
    leftWindow = [[5,5],[600,5],[600,475],[5,475]]
    one = [[605,5],[800,5],[800,55],[605,55]]
    two = [[605,60],[800,60],[800,110],[605,110]]
    three = [[605,115],[800,115],[800,165],[605,165]]
    four = [[605,170],[800,170],[800,220],[605,220]]
    five = [[605,225],[800,225],[800,275],[605,275]]
    six = [[605,280],[800,280],[800,330],[605,330]]
    seven = [[605,335],[800,335],[800,385],[605,385]]
    eight = [[605,390],[697,390],[697,475],[605,475]]
    nine = [[702,390],[800,390],[800,475],[702,475]]


    

    canvas.create_polygon(leftWindow, fill='white', outline='black')
    canvas.create_polygon(one, fill='white', outline='black')
    canvas.create_polygon(two, fill='white', outline='black')
    canvas.create_polygon(three, fill='white', outline='black')
    canvas.create_polygon(four, fill='white', outline='black')
    canvas.create_polygon(five, fill='white', outline='black')
    canvas.create_polygon(six, fill='white', outline='black')
    canvas.create_polygon(seven, fill='white', outline='black')
    canvas.create_polygon(eight, fill='white', outline='black')
    canvas.create_polygon(nine, fill='white', outline='black')


    


def rotateAndDraw(slewAngle, basePoints, inclX, inclY, midx, midy, boomAngle, boomExtension):
    #rewriting canvas
    canvas.delete("all")

    draw_bg()

    #coloring the polygon based on the incline
    #polyColor = polygonColors(inclX, inclY)

    #coloring the corner incline values based on its value
    #colorX = colors(inclX)
    #colorY = colors(inclY)

    #default color
    polyColor = "white"
    colorX = "black"
    colorY = "black"
    

    #establishing center
    center = (CANVAS_MID_X, CANVAS_MID_Y)

    #generate corners for polygon and corner points for numbers
    newSquare = rotate(basePoints, slewAngle, center)

    #create points for the corners to be printed on
    cornerSq = createCorners(basePoints)
    cornerPts = rotate(cornerSq, slewAngle, center)

    #draw square
    draw_square(newSquare, polyColor)

    #draw degrees in center
    canvas.create_text((43,170),fill="black",font="Courier 20",text="DEG:")
    canvas.create_text((120,170),fill="black",font="Courier 20",text=str(round(slewAngle,2)))

    #draw incline degrees
    canvas.create_text((50,50),fill="black",font="Courier 20",text="ROL: ")
    canvas.create_text((120,50),fill="black",font="Courier 20",text=str(round(inclX,2)))
    canvas.create_text((50,80),fill="black",font="Courier 20",text="PIT: ")
    canvas.create_text((120,80),fill="black",font="Courier 20",text=str(round(inclY,2)))

    #draw outrigger positions
    canvas.create_text((50,110),fill="black",font="Courier 20",text="ORR: ")
    canvas.create_text((120,110),fill="black",font="Courier 20",text=str(round(outriggerExtRight,2)))
    canvas.create_text((50,140),fill="black",font="Courier 20",text="ORL: ")
    canvas.create_text((120,140),fill="black",font="Courier 20",text=str(round(outriggerExtLeft,2)))

    #draw boom angle and extension
    canvas.create_text((43,200),fill="black",font="Courier 20",text="BAN:")
    canvas.create_text((120,200),fill="black",font="Courier 20",text=str(round(boomAngle,2)))
    canvas.create_text((50,230),fill="black",font="Courier 20",text="BEX: ")
    canvas.create_text((120,230),fill="black",font="Courier 20",text=str(round(boomExtension,2)))


    #draw corner numbers either , 1-4, or incline values (still under dev)
    #canvas.create_text(cornerPts[0],fill=colorY,font="Courier 30",text=str(round(inclY,2)))
    #canvas.create_text(cornerPts[1],fill=colorX,font="Courier 30",text=str(round(inclX,2)))
    #canvas.create_text(cornerPts[2],fill=colorX,font="Courier 30",text=str(round(inclX,2)))
    #canvas.create_text(cornerPts[3],fill=colorY,font="Courier 30",text=str(round(inclY,2)))

    #draw boom arm
    staticBoomArm = adjustBoom(midx, midy, boomAngle,boomExtension)
    canvas.create_polygon(staticBoomArm, fill='white', outline='black')

def clock():
    global pitch
    global roll
    global outriggerExtLeft
    global outriggerExtRight
    global slewAngle
    global boomExtension
    global boomAngle
    #all increment functions simulate sensor input
    #incrementDeg()
    #incrementOr()
    #incrementInclineX()
    #incrementInclineY()
    #incrementBoomAngle()

    '''
    test0 = DAQ.getAIN(0)
    test1 = DAQ.getAIN(1)
    test2 = DAQ.getAIN(2)
    test3 = DAQ.getAIN(3)
    test4 = DAQ.getAIN(4)
    test5 = DAQ.getAIN(5)
    test6 = DAQ.getAIN(6)

    pitch = calibrateIncline(test5)
    roll = calibrateIncline(test6)
    outriggerExtLeft = calibrateOutrigger(test3)
    outriggerExtRight = calibrateOutrigger(test4)
    slewAngle = calibrateSlewAngle(test0)
    boomExtension = calibrateBoomExtension(test1)
    boomAngle = calibrateBoomAngle(test2)
    '''
    drawingPts = sensorInput(craneLength, craneWidth, CANVAS_MID_X, CANVAS_MID_Y, outriggerExtRight, outriggerExtLeft, pitch, roll)   
    rotateAndDraw(slewAngle, drawingPts, pitch, roll, CANVAS_MID_X, CANVAS_MID_Y, boomAngle, boomExtension)
    

    #50, running at 20 Hz
    root.after(50, clock) # run itself again after 50 ms



clock()
root.mainloop()