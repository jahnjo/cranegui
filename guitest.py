from Tkinter import *
import math
import datetime

WIDTH = 1200
HEIGHT = 800
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = 400
outriggerExtRight = 0
outriggerExtLeft = 0
inclX = -20
inclY = -20
deg = 0
backIncX = True
backIncY = True

root = Tk()
canvas = Canvas(root, bg="white", height=HEIGHT, width=WIDTH)
canvas.pack(fill=BOTH, expand=1)

staticBoomArm = [
    [CANVAS_MID_X - 7, CANVAS_MID_Y - 350],
    [CANVAS_MID_X + 7, CANVAS_MID_Y - 350],
    [CANVAS_MID_X + 7, CANVAS_MID_Y - 20],
    [CANVAS_MID_X - 7, CANVAS_MID_Y - 20],
]



vertice = [
    [CANVAS_MID_X - SIDE/5, CANVAS_MID_Y - SIDE/6],
    [CANVAS_MID_X + SIDE/6, CANVAS_MID_Y - SIDE/3],
    [CANVAS_MID_X + SIDE/5, CANVAS_MID_Y + SIDE/2],
    [CANVAS_MID_X - SIDE/3, CANVAS_MID_Y + SIDE/6],
]

def sensorInput(SIDE, midx, midy, orExtR, orExtL, inclX, inclY):
    vertices = [
        [CANVAS_MID_X - SIDE/2 - (orExtL*3) - (inclY*3), CANVAS_MID_Y - SIDE/2 + (inclX*3)],
        [CANVAS_MID_X + SIDE/2 + (orExtR*3) + (inclY*3), CANVAS_MID_Y - SIDE/2 - (inclX*3)],
        [CANVAS_MID_X + SIDE/2 - (orExtR*3) - (inclY*3), CANVAS_MID_Y + SIDE/2 + (inclX*3)],
        [CANVAS_MID_X - SIDE/2 + (orExtL*3) + (inclY*3), CANVAS_MID_Y + SIDE/2 - (inclX*3)],
    ]
    return vertices
    
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

def draw_square(points, color="white"):
    canvas.create_polygon(points, fill=color, outline='black')

def rotateAndDraw(rotDeg, basePoints, inclX, inclY):
    #rewriting canvas
    canvas.delete("all")

    #establishing center
    center = (CANVAS_MID_X, CANVAS_MID_Y)

    #generate corners for polygon and corner points for numbers
    newSquare = rotate(basePoints, rotDeg, center)

    #create points for the corners to be printed on
    cornerSq = createCorners(basePoints)
    cornerPts = rotate(cornerSq, rotDeg, center)

    #draw square
    draw_square(newSquare)

    #draw degrees in center
    canvas.create_text((77,170),fill="black",font="Courier 20",text="Degrees:")
    canvas.create_text((195,170),fill="black",font="Courier 20",text=rotDeg)

    #draw incline degrees
    canvas.create_text((100,50),fill="black",font="Courier 20",text="Incline X: ")
    canvas.create_text((195,50),fill="black",font="Courier 20",text=inclX)
    canvas.create_text((100,80),fill="black",font="Courier 20",text="Incline Y: ")
    canvas.create_text((195,80),fill="black",font="Courier 20",text=inclY)

    #draw outrigger positions
    canvas.create_text((85,110),fill="black",font="Courier 20",text="OR Right:")
    canvas.create_text((195,110),fill="black",font="Courier 20",text=outriggerExtRight)
    canvas.create_text((85,140),fill="black",font="Courier 20",text="OR Left: ")
    canvas.create_text((195,140),fill="black",font="Courier 20",text=outriggerExtLeft)


    #draw corner numbers
    canvas.create_text(cornerPts[0],fill="red",font="Courier 30",text='1')
    canvas.create_text(cornerPts[1],fill="red",font="Courier 30",text='2')
    canvas.create_text(cornerPts[2],fill="blue",font="Courier 30",text='3')
    canvas.create_text(cornerPts[3],fill="blue",font="Courier 30",text='4')

    #draw boom arm
    canvas.create_polygon(staticBoomArm, fill='white', outline='black')

def clock():
    incrementDeg()
    #incrementOr()
    incrementInclineX()
    incrementInclineY()
    drawingPts = sensorInput(SIDE, CANVAS_MID_X, CANVAS_MID_Y, outriggerExtRight, outriggerExtLeft, inclX, inclY)   
    rotateAndDraw(deg, drawingPts, inclX, inclY)

    root.after(50, clock) # run itself again after 1000 ms



clock()
root.mainloop()