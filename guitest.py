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
With the ouriggers extending 34" in each directions that mean that each inch 
increment will increment 1.476 pixels (if the crane length is 400, else pixels per
inch needs to be recalculated) described by the outriggerMod.
'''
outriggerExtRight = 0
outriggerExtLeft = 0
outriggerMod = 1.476

leftWindow = [
    [5,5],
    [600,5],
    [600,475],
    [5,475]
]

rightWindow = [
    [605,5],
    [795,5],
    [795,475],
    [605,475]
]

inclX = 0
inclY = 0
deg = 0
boomAngle = 0

backIncX = True
backIncY = True
backBoom = True
polyColor = "green"

root = Tk()
canvas = Canvas(root, bg="white", height=HEIGHT, width=WIDTH)
canvas.pack(fill=BOTH, expand=1)



def adjustBoom(midx, midy, boomAngle):
    boomPoints = [
        [CANVAS_MID_X - 7, CANVAS_MID_Y - 175 + (boomAngle*2.5)],
        [CANVAS_MID_X + 7, CANVAS_MID_Y - 175 + (boomAngle*2.5)],
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
def sensorInput(craneLength, craneWidth, midx, midy, orExtR, orExtL, inclX, inclY):
    vertices = [
        [CANVAS_MID_X - craneWidth/2 - (orExtL*outriggerMod) - (inclY*3), CANVAS_MID_Y - craneLength/2 + (inclX*3)],
        [CANVAS_MID_X + craneWidth/2 + (orExtR*outriggerMod) + (inclY*3), CANVAS_MID_Y - craneLength/2 - (inclX*3)],
        [CANVAS_MID_X + craneWidth/2 + (orExtR*outriggerMod) - (inclY*3), CANVAS_MID_Y + craneLength/2 + (inclX*3)],
        [CANVAS_MID_X - craneWidth/2 - (orExtL*outriggerMod) + (inclY*3), CANVAS_MID_Y + craneLength/2 - (inclX*3)],
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
    global deg
    if deg > 359:
        deg = 0
    else:
        deg += 1

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
    global inclX
    global backIncX
    if backIncX:
        if inclX > 20:
            inclX = 20
            backIncX = False
        else:
            inclX += 1
    elif not backIncX:
        if inclX < -20:
            inclX = -20
            backIncX = True
        else:
            inclX -= 1

def incrementInclineY():
    global inclY
    global backIncY
    if backIncY:
        if inclY > 20:
            inclY = 20
            backIncY = False
        else:
            inclY += 1
    elif not backIncY:
        if inclY < -20:
            inclY = -20
            backIncY = True
        else:
            inclY -= 1

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

def rotateAndDraw(rotDeg, basePoints, inclX, inclY, midx, midy, boomAngle):
    
    #rewriting canvas
    canvas.delete("all")

    canvas.create_polygon(leftWindow, fill='white', outline='black')
    canvas.create_polygon(rightWindow, fill='white', outline='black')

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
    newSquare = rotate(basePoints, rotDeg, center)

    #create points for the corners to be printed on
    cornerSq = createCorners(basePoints)
    cornerPts = rotate(cornerSq, rotDeg, center)

    #draw square
    draw_square(newSquare, polyColor)

    staticBoomArm = adjustBoom(midx, midy, boomAngle)
    canvas.create_polygon(staticBoomArm, fill='white', outline='black')


    #draw degrees in center
    canvas.create_text((82,170),fill="black",font="Courier 20",text="DEG:")
    canvas.create_text((195,170),fill="black",font="Courier 20",text=rotDeg)

    #draw incline degrees
    canvas.create_text((100,50),fill="black",font="Courier 20",text="PCH: ")
    canvas.create_text((195,50),fill="black",font="Courier 20",text=inclX)
    canvas.create_text((100,80),fill="black",font="Courier 20",text="ROL: ")
    canvas.create_text((195,80),fill="black",font="Courier 20",text=inclY)

    #draw outrigger positions
    canvas.create_text((88,110),fill="black",font="Courier 20",text="ORR:")
    canvas.create_text((195,110),fill="black",font="Courier 20",text=outriggerExtRight)
    canvas.create_text((88,140),fill="black",font="Courier 20",text="ORL: ")
    canvas.create_text((195,140),fill="black",font="Courier 20",text=outriggerExtLeft)

    canvas.create_text((88,200),fill="black",font="Courier 20",text="BAN:")
    canvas.create_text((230,200),fill="black",font="Courier 20",text=str(round(boomAngle,2)))
    canvas.create_text((88,230),fill="black",font="Courier 20",text="BEX: ")
    canvas.create_text((230,230),fill="black",font="Courier 20",text=str(round(boomExtension,2)))

'''
    #draw corner numbers either , 1-4, or incline values (still under dev)
    canvas.create_text(cornerPts[0],fill=colorY,font="Courier 30",text="1")
    canvas.create_text(cornerPts[1],fill=colorX,font="Courier 30",text="2")
    canvas.create_text(cornerPts[2],fill=colorX,font="Courier 30",text="3")
    canvas.create_text(cornerPts[3],fill=colorY,font="Courier 30",text="4")
'''
    

def clock():
    #all increment functions simulate sensor input
    #incrementDeg()
    #incrementOr()
    #incrementInclineX()
    #incrementInclineY()
    #incrementBoomAngle()

    drawingPts = sensorInput(craneLength, craneWidth, CANVAS_MID_X, CANVAS_MID_Y, outriggerExtRight, outriggerExtLeft, inclX, inclY)   
    rotateAndDraw(deg, drawingPts, inclX, inclY, CANVAS_MID_X, CANVAS_MID_Y, boomAngle)

    #50, running at 20 Hz
    root.after(50, clock) # run itself again after 50 ms



clock()
root.mainloop()