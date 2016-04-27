'''
###########################################################################
name:				bwParticleToBubblePop -- Oct 2015
Created by: Bryan Woodard & Chris Jones(github.com/csjones
This script will build a curve and attach a locator to the
curve using the pathAnimation command (motion path). It will then build
a simple sphere and give it specific nCloth properties

Use: make sure you have an nParticle named nParticle1 in the scene.

Future updates - update so selected nParticle systems can work. Also update
attributes for nCloth.
version history
v0.1 - scipt has the ability to make bubbles
v0.2 - User must select any nParticle
	 - Some added error handling
	 - Can now pop bubbles

Tested on Maya 2016 for Windows
Use at your own risk
############################################################################
'''
import maya.cmds as mc
import random
import maya.mel as mel
inc=0


getSelPartiShape = mc.ls(sl=True, dag=True, lf=True)


minFrames = mc.playbackOptions( q=True, min=True)
maxFrames = mc.playbackOptions( q=True, max=True)


for shapeSel in getSelPartiShape:
	if "nParticle" == mc.objectType(shapeSel):#check and make sure that what we have selected are nParticles. 
		allParticleDictionary = {}
		getTrans = mc.pickWalk(shapeSel, d="up")
		theParticle = mc.ls(getTrans, type = "transform")
		everyThingFolder = mc.group(em=True, n=(theParticle[0] + "_GRP"))
		print theParticle #since there is no progress bar this let's the user know which particle is being processed.
		
		
		
		for currentFrame in range(0, int(maxFrames)):
			#print('Frame=' + str(currentFrame))
			mc.currentTime(currentFrame, update=True, edit=True)
		
		
			for part in theParticle:
				for particleCount in range(0,mc.particle(part, q=True,ct=True)):
		
					particleName = mc.particle(part, q=True, order=particleCount, at='id')
					particlesPosition = mc.particle(part, q=True, order=particleCount, at='position')
		
					particleDictionary = {}
					if str(particleName[0]) in allParticleDictionary.keys():
						particleDictionary = allParticleDictionary[str(particleName[0])]
		
					particleDictionary[currentFrame] = particlesPosition
					allParticleDictionary[str(particleName[0])] = particleDictionary
		
				
		for curveParticleId in allParticleDictionary.keys():
			pointList = []
		
			sortedKeyFrameList = sorted(allParticleDictionary[curveParticleId].keys())
			if len(sortedKeyFrameList) > 1:
		
				for keyFrame in sortedKeyFrameList:
					pointList.append(allParticleDictionary[curveParticleId][keyFrame])
				
				grpFolder = mc.group(em=True, n="groupOfThingsFolder" + str(inc))		
				
				curveName = "partiCurve" + str(curveParticleId)
				curveObj = mc.curve(name = curveName, p = pointList)
				locName = "locatorName" + str(curveParticleId)
				locObj = mc.spaceLocator(name = (locName+theParticle[0]))
				mc.pathAnimation(locObj, stu=sortedKeyFrameList[0], etu=sortedKeyFrameList[-1] ,c=curveObj,n=("moPath_" + theParticle[0]))
				
				#For every locator we create, make a bubble and attach that to the locator in worldspace and parent in underneath
		
				makeBubble = mc.polyCube(name=("bubble" + str(inc)), w=.1, h=.1, d=.1, sx=5, sy=5, sz=5)
		        mc.sculpt(makeBubble, maxDisplacement=.1)
		        mc.delete(makeBubble, ch=True)
		        getPos = mc.xform(locObj, ws=True, q=True, translation=True)
		        mc.xform(makeBubble[0], t=(getPos[0], getPos[1], getPos[2]))
		        mc.parent(makeBubble[0], locObj)
		        randBubbleSize = random.uniform(.2, .8)#This is what will give our bubbles the random size
		        mc.scale(randBubbleSize, randBubbleSize, randBubbleSize, makeBubble[0])
		
		        #Create nCloth for each bubble and set the collide strength to turn on when the bubble moves, never before.
		        mc.select(makeBubble[0])
		        mc.nClothCreate()
		        bubbleNClothName = mc.rename("nCloth1", ("nClothBub" + str(inc)))
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
		        mc.setAttr(bubbleNClothName + ".isDynamic", 0)
		
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
		        
		        inc += 1
		        mc.parent(locObj,curveObj,bubbleNClothName,makeTearable, grpFolder)
		        mc.parent(grpFolder, everyThingFolder)
		        

	else:
		print("The item selected doesn't appear to be an nCloth object --> " + shapeSel + " <--")


#check to see if the nCloth is enabled and if so turn it off so the next round of bubbles isn't slow
getnClothEnabledItmes = mc.ls(type='nCloth')#this is a dumb way to grab things
if len(getnClothEnabledItmes) > 0:
	for item in getnClothEnabledItmes:
		print item
		mc.setAttr(item + ".isDynamic", 1)
		
		
		
		


'''

After you cache the bubbles this part will select the
bubbles and move the cache to the input mesh and 
then display the input mesh, now ready to be exported.

NOTE -- the key to this working is that the input mesh
has all the cuts in the edges allowing for a static value
in the vert count, otherwise this wouldn't work.

'''	
import maya.mel as mel	
	
mc.select('bubble*')
bubbleToExportSet = mc.sets(n="bubblesToExport")
getTheBubble = mc.ls(sl=True, tr=True)
for bubble in getTheBubble:		
	
	mc.select(bubble)	
	mel.eval('moveCacheToInput 0;')
	mel.eval('displayNClothMesh "input";')
	print bubble
	
	
	
		

	
	
	
	
	
	
	
	
	
	
	
	
