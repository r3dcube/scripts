import maya.cmds as mc
import random

allParticleDictionary = {}
minFrames = mc.playbackOptions( q=True, min=True)
maxFrames = mc.playbackOptions( q=True, max=True)

for currentFrame in range(0, int(maxFrames)):
	#print('Frame=' + str(currentFrame))
	mc.currentTime(currentFrame, update=True, edit=True)
	mc.select('nParticle1')

	theParticle = mc.ls(sl=True, type='transform')

	for part in theParticle:
		for particleCount in range(0,mc.particle(part, q=True,ct=True)):

			particleName = mc.particle(part, q=True, order=particleCount, at='id')
			particlesPosition = mc.particle(part, q=True, order=particleCount, at='position')

			#print (particleName, particlesPosition, particleCount)

			particleDictionary = {}
			if str(particleName[0]) in allParticleDictionary.keys():
				particleDictionary = allParticleDictionary[str(particleName[0])]

			particleDictionary[currentFrame] = particlesPosition
			allParticleDictionary[str(particleName[0])] = particleDictionary

#House cleaning
emptyFolder = mc.group(em=True, n="nCloth_Objs")	
		
for curveParticleId in allParticleDictionary.keys():
	#print sorted(allParticleDictionary[curveParticleId].keys())
	#print curveParticleId
	pointList = []

	sortedKeyFrameList = sorted(allParticleDictionary[curveParticleId].keys())
	if len(sortedKeyFrameList) > 1:

		for keyFrame in sortedKeyFrameList:
			pointList.append(allParticleDictionary[curveParticleId][keyFrame])
					
		curveName = "partiCurve" + str(curveParticleId)
		curveObj = mc.curve(name = curveName, p = pointList)
		locName = "locatorName" + str(curveParticleId)
		locObj = mc.spaceLocator(name = locName)
		mc.pathAnimation(locObj, stu=sortedKeyFrameList[0], etu=sortedKeyFrameList[-1] ,c=curveObj)		
		
		#For every locator we create, make a bubble and attach that to the locator in worldspace and parent in underneath
	    
		makeBubble = mc.polyCube(name="bubble" + str(curveParticleId), w=.1, h=.1, d=.1, sx=5, sy=5, sz=5)		
        mc.sculpt(makeBubble, maxDisplacement=.1)
        mc.delete(makeBubble, ch=True)		
        getPos = mc.xform(locObj, ws=True, q=True, translation=True)        
        mc.xform(makeBubble[0], t=(getPos[0], getPos[1], getPos[2]))
        mc.parent(makeBubble[0], locObj)
        randBubbleSize = random.uniform(.4,.6)#This is what will give our bubbles the random size
        mc.scale(randBubbleSize, randBubbleSize, randBubbleSize, makeBubble[0])        
        
        #Create nCloth for each bubble and set the collide strength to turn on when the bubble moves, never before.
        mc.select(makeBubble[0])
        mc.nClothCreate()
        bubbleNClothName = mc.rename("nCloth1", "bubbleCloth")
        #mc.setAttr(locObj + ".collideStrength", 0)
        mc.setKeyframe(bubbleNClothName, attribute='collideStrength', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
        mc.setAttr(bubbleNClothName + ".collideStrength", 0)
        mc.setKeyframe(bubbleNClothName, attribute='collideStrength', t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[-1]+1])
        
        mc.setKeyframe(bubbleNClothName, attribute='rigidity', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]+10])
        mc.setAttr(bubbleNClothName + ".rigidity", .1)
        mc.setKeyframe(bubbleNClothName, attribute='rigidity', t=[sortedKeyFrameList[0]+10, sortedKeyFrameList[-1]])
        
        mc.setAttr(bubbleNClothName + ".inputMeshAttract", .7)
        mc.setKeyframe(bubbleNClothName, attribute='inputMeshAttract', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]+10])
        mc.setAttr(bubbleNClothName + ".inputMeshAttract", .4)
        mc.setKeyframe(bubbleNClothName, attribute='inputMeshAttract', t=[sortedKeyFrameList[0]+10, sortedKeyFrameList[-1]])
        
        mc.setAttr(bubbleNClothName + ".stretchResistance", 20)
        mc.setAttr(bubbleNClothName + ".compressionResistance", 80)
        mc.setAttr(bubbleNClothName + ".selfCollisionFlag", 4)
        
        mc.setAttr(bubbleNClothName + ".pointMass", .2)
          
        #set the visibiliy of the LOCATORS on when it's moving and off when it has stopped        
        setOn = mc.setKeyframe( locObj[0], attribute='visibility', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
        mc.setAttr(locObj[0] + ".visibility", 0)
        setOff = mc.setKeyframe( locObj[0], attribute='visibility', t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[-1]+1])
        
        #place the newly created objects into our nCloth_Objs folder   
        mc.parent(locObj,curveObj, emptyFolder)




mc.select("*bubble*")
































getBubbles = mc.ls(sl=True)
mc.nClothCreate()
mc.select("*nCloth*")
getnCloth = mc.ls(sl=True, tr=True)
for locObj in getnCloth:
    print locObj
    #mc.setAttr(locObj + ".collideStrength", 0)
    mc.setKeyframe( locObj, attribute='collideStrength', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
    mc.setAttr(locObj + ".collideStrength", 0)
    setOff = mc.setKeyframe( locObj, attribute='visibility', t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[-1]+1])


#THis doesn't work because ncloth dosen't respect scale

        #because of self pentration this is added at the beginning to scale up the bubble. This could be converted
        #in the future to a run time command that handles a setAttr at the specific keyframe the animation starts on the 
        #loctor to enable nCloth
        mc.setAttr(locObj[0] + ".scaleX", .01)
        mc.setAttr(locObj[0] + ".scaleY", .01)
        mc.setAttr(locObj[0] + ".scaleZ", .01)
        mc.setKeyframe( locObj[0], attribute='scaleX', t=[sortedKeyFrameList[0]])
        mc.setKeyframe( locObj[0], attribute='scaleY', t=[sortedKeyFrameList[0]])
        mc.setKeyframe( locObj[0], attribute='scaleZ', t=[sortedKeyFrameList[0]])
        mc.setAttr(locObj[0] + ".scaleX", 1)
        mc.setAttr(locObj[0] + ".scaleY", 1)
        mc.setAttr(locObj[0] + ".scaleZ", 1)
        mc.setKeyframe( locObj[0], attribute='scaleX', t=[sortedKeyFrameList[0]+10])
        mc.setKeyframe( locObj[0], attribute='scaleY', t=[sortedKeyFrameList[0]+10])
        mc.setKeyframe( locObj[0], attribute='scaleZ', t=[sortedKeyFrameList[0]+10])



makeBubble = mc.polyCube(name="bubble" + str(curveParticleId), w=.1, h=.1, d=.1, sx=5, sy=5, sz=5)
		
mc.sculpt(makeBubble, maxDisplacement=.1)
mc.delete(makeBubble, ch=True)		






mc.nClothCreate()