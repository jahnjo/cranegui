import numpy as np

roll = 1
pitch = 0
yaw = 0

newList=[]

orPos = [[   -6,    6,     6,    -6], #x
         [11.25,11.25,-11.25,-11.25], #y
         [    0,    0,     0,     0]  #z
        ]

roZ = [[np.cos(np.radians(yaw)),-np.sin(np.radians(yaw)),0],
       [np.sin(np.radians(yaw)),np.cos(np.radians(yaw)),0],
       [0,0,1]
      ]

roY = [[np.cos(np.radians(-roll)),0,np.sin(np.radians(-roll))],
       [0,1,0],
       [-np.sin(np.radians(-roll)),0,np.cos(np.radians(-roll))]
      ]

roX = [[1,0,0],
       [0,np.cos(np.radians(-pitch)),-np.sin(np.radians(-pitch))],
       [0,np.sin(np.radians(-pitch)),np.cos(np.radians(-pitch))]
      ]

#[Z]*[Y]*[X]*[Outrigger Positions]
ZY = np.dot(roZ,roY)  
ZYX = np.dot(ZY,roX)
rotPos=np.dot(ZYX,orPos)

#All Z values
newList.append(round(rotPos.item(8),1))
newList.append(round(rotPos.item(9),1))
newList.append(round(rotPos.item(10),1))
newList.append(round(rotPos.item(11),1))


print np.matrix(rotPos)
print newList