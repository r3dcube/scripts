import maya.cmds as mc

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
		makeBubble = mc.polyCube(name="bubble",w=.1,h=.1, d=.1, sx=5, sy=5, sz=5)
		
		#print pointList

makeBubble = mc.polyCube(name="bubble",w=.1,h=.1, d=.1, sx=5, sy=5, sz=5)
mc.sculpt(makeBubble, maxDisplacement=.1)
mc.delete(makeBubble, ch=True)
mc.nClothCreate()
