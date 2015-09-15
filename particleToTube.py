import maya.cmds as mc
import random
import math
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
emptyFolder = mc.group(em=True, n="extruPath")
emptyCirFolder = mc.group(em=True, n="circleCreation")	
empty_ACirFolder = mc.group(em=True, n="circleGeo")
empty_curveFolder = mc.group(em=True, n="curveExtrusions")
		
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
			
		
		#For every locator we create, make a bubble and attach that to the locator in worldspace and parent in underneath
        getCurvLen = mc.arclen(curveObj)
        makeCvrLenInt = math.ceil(getCurvLen*.25) 
        
        
        makeCircle = mc.circle(n="newCircle",d=1, s=12)
        aCircle = mc.planarSrf(makeCircle[0], n="extruTube", d=3, po=1)

        
        getCurveCVPos = mc.xform(curveObj + ".cv[0]", ws=True, q=True, translation=True)
        mc.xform(makeCircle[0], ws=True, t=(getCurveCVPos[0], getCurveCVPos[1], getCurveCVPos[2]),ro=(90, 0, 0))
        
        tubes = mc.polyExtrudeFacet(aCircle[0] + ".f[0]", inc=curveObj, d=makeCvrLenInt)
        subCurveCreate = mc.createNode("subCurve", n="subCurve_" + curveObj)
        curveShape = mc.listRelatives(curveObj, s=True)
        
        mc.setAttr(subCurveCreate + ".relative", 1)
        mc.connectAttr(curveShape[0] + ".worldSpace", subCurveCreate + ".inputCurve", f=True)
        mc.connectAttr(subCurveCreate + ".outputCurve", tubes[0] + ".inputProfile", f=True)     
        
        
        mc.setAttr(subCurveCreate + ".maxValue", 0)
        mc.setKeyframe(subCurveCreate, attribute='maxValue', t=[sortedKeyFrameList[0]])
        mc.setAttr(subCurveCreate + ".maxValue", 1)
        mc.setKeyframe(subCurveCreate, attribute='maxValue', t=[sortedKeyFrameList[-1]])
        
        #set the visibility
        mc.setAttr(aCircle[0] + ".visibility", 1)
        mc.setKeyframe(aCircle[0], attribute='visibility', t=[sortedKeyFrameList[0]])
        #mc.currentTime((sortedKeyFrameList[0]-1), update=True, edit=True)
        mc.setAttr(aCircle[0] + ".visibility", 0)
        mc.setKeyframe(aCircle[0], attribute='visibility', t=[sortedKeyFrameList[0]-1])
        
        mc.parent(makeCircle, emptyCirFolder)
        mc.parent(aCircle, empty_ACirFolder)
        mc.parent(curveObj, empty_curveFolder)
        
mc.parent(empty_curveFolder,emptyCirFolder,empty_ACirFolder, emptyFolder)
        
        
        
