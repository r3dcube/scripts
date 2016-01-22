#This script takes all the objects selected and moves them x units across and y units down but every 10 objs it starts a new row.
#Useful for sorting a lot of unordered blendshapes
import maya.cmds as mc
posX = 40
posY = 0
i = 0
getObjs = mc.ls(sl=True)
    
for i in range(0 , len(getObjs)):
    print "%d index" %(i)
    if i%10 == 0:
        print posY
        posY = posY - 15
        posX = 0
        
    mc.move(posX, posY, 0, getObjs[i])
    posX = posX + 10
    #print posX