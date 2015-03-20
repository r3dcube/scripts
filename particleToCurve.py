import maya.cmds as mc


directoryPath = "C:\\Users\Bryan\\Dropbox (Dig-It Games)\\Dig-It\\Temp Files\\2015_02_beaker\\3d\\maya\\particleMess"
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
		mc.curve(p = pointList)
		#print pointList


#cmds.curve( p=[(0, 0, 0), (3, 5, 6), (5, 6, 7), (9, 9, 9), (12, 10, 2)], k=[0,0,0,1,2,2,2] )


#print allParticleDictionary
