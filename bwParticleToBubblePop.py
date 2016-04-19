###########################################################################
#name:				bwParticleToBubblePop -- Oct 2015
#Created by: Bryan Woodard & Chris Jones(github.com/csjones)
#This script will build a curve and attach a locator to the
#curve using the pathAnimation command (motion path). It will then build
#a simple sphere and give it specific nCloth properties
#
#Use: make sure you have an nParticle named nParticle1 in the scene.
#
#Future updates - update so selected nParticle systems can work. Also update
#attributes for nCloth.
#
#Tested on Maya 2016 for Windows
#Use at your own risk
############################################################################

import maya.cmds as mc
import random
import maya.mel as mel

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
        mc.setAttr(bubbleNClothName + ".trappedCheck", 1)
        mc.setAttr(bubbleNClothName + ".pressure", 1)

        mc.setAttr(bubbleNClothName + ".pointMass", .2)

        #set the visibiliy of the LOCATORS on when it's moving and off when it has stopped
        setOn = mc.setKeyframe( locObj[0], attribute='visibility', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
        mc.setAttr(locObj[0] + ".visibility", 0)
        setOff = mc.setKeyframe( locObj[0], attribute='visibility', t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[-1]+1])
        
        ######################################################################
        #pop the bubble - we know there are 152 vers in the bubble. Pick a random number in that and go up and down from that number by 35 to get random selections
        getRandNum = random.randint(34,116) #this is 35 above 0 and 35 below 151 so that we don't reach higher
        randVertValHi = getRandNum + 35
        randVertValLo = getRandNum - 35
        
        mc.select(makeBubble[0] + ".vtx[" + str(randVertValLo) + ":" + str(randVertValHi) + "]")
        makeTearable = mel.eval('createNConstraint tearableSurface false;')
        
        #Increase pressure before the tear happens
        mc.setKeyframe(bubbleNClothName, attribute='pres', t=[sortedKeyFrameList[-1]-3])
        mc.setAttr(bubbleNClothName + ".pres", 10)
        mc.setKeyframe(bubbleNClothName, attribute='pres', t=[sortedKeyFrameList[-1]-2])
        
        #Tear it apart 10frames before it ends its run
        mc.setKeyframe(makeTearable, attribute='gls', t=[sortedKeyFrameList[-1]-2])
        mc.setAttr(makeTearable[0] + ".glueStrength", 0)
        mc.setKeyframe(makeTearable, attribute='gls', t=[sortedKeyFrameList[-1]-1])
		#######################################################################

        #place the newly created objects into nCloth_Objs folder
        mc.parent(locObj,curveObj,bubbleNClothName,makeTearable, emptyFolder)




mc.select("*bubble*")



