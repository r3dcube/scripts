import maya.cmds as mc
import random
import math
#House cleaning
inc=0

getSelPartiShape = mc.ls(sl=True, dag=True, lf=True)

allParticleDictionary = {}
minFrames = mc.playbackOptions( q=True, min=True)
maxFrames = mc.playbackOptions( q=True, max=True)


for shapeSel in getSelPartiShape:
	if "nParticle" == mc.objectType(shapeSel):#check and make sure that what we have selected are nParticles. 
		
		getTrans = mc.pickWalk(shapeSel, d="up")
		theParticle = mc.ls(getTrans, type = "transform")
		everyThingFolder = mc.group(em=True, n="AllTheThingsAreHERE")
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
				
		
		#########################################################################################################################################################
		#ERROR CHECKING......				
		
				"""
				rndDwnCurveLength = math.trunc(mc.arclen(curveObj))
				getSpans = mc.getAttr(curveObj + ".spans")
				getDegree = mc.getAttr(curveObj + ".degree")
				CVTotalOnCurve = getSpans + getDegree
					#print everything
				print("curve" + str(curveObj), "the length = " + str(rndDwnCurveLength), "total CV's =" + str(CVTotalOnCurve) )
				if rndDwnCurveLength < 10:
						
					print("curve =" + str(curveObj), "the length = " + str(rndDwnCurveLength), "total CV's =" + str(CVTotalOnCurve) )"""
		###########################################################################################################################################################
		
		
		
				rndDwnCurveLength = math.trunc(mc.arclen(curveObj))
				if rndDwnCurveLength <= 1: #check to see if the curve has at least 3 segments.
					print "OHHHHH SHITE" #This is why it's a good idea to animate the emitter to 0 several frames before the animation ends. Otherwise you emit a particle and there are less then 2 spans in the curve at the end.
				else:
					newCylinder = mc.polyCylinder(name="tubePoly_0" + str(inc), ch=True, r=.25, ax=[0,0,90], sh=(rndDwnCurveLength*2), h=rndDwnCurveLength)
					newCylBlendShp_A = mc.polyCylinder(name="tubeBlendShpA_0" + str(inc), ch=True, r=.25, ax=[0,0,90], sh=(rndDwnCurveLength*2), h=rndDwnCurveLength)
					
					getBndBoxDim = mc.xform(newCylBlendShp_A[0], q=True, ws=True, bb=True)
					mc.setAttr(newCylBlendShp_A[0] + ".visibility", 0)
					#print getBndBoxDim																				
					mc.xform(newCylBlendShp_A, p=True, sp=[0,0, getBndBoxDim[2]], rp=[0,0, getBndBoxDim[2]])
					newCylBlendShp_B = mc.polyCylinder(name="tubeBlendShpB_0" + str(inc), ch=True, r=.25, ax=[0,0,90], sh=(rndDwnCurveLength*2), h=rndDwnCurveLength)
					mc.setAttr(newCylBlendShp_B[0] + ".visibility", 0)
					mc.xform(newCylBlendShp_B, p=True, sp=[0,0, getBndBoxDim[5]], rp=[0,0, getBndBoxDim[5]])
					
					mc.scale(1,1,.001, newCylBlendShp_A, r=True)
					mc.makeIdentity(newCylBlendShp_A,a=True, s=True)
					mc.scale(1,1,.001, newCylBlendShp_B, r=True)
					mc.makeIdentity(newCylBlendShp_B,a=True, s=True)
					
					theBlndShp = mc.blendShape(newCylBlendShp_A[0], newCylBlendShp_B[0], newCylinder[0])
					moPathVar =  mc.pathAnimation(newCylinder, fa="Z", fm=True, f=True, ua="y", wut = "vector", su=0.5, eu=0.5, stu=(mc.playbackOptions(q=True, minTime=True)), etu=(mc.playbackOptions(q=True, maxTime=True)) ,c=curveObj)
					mc.cutKey(moPathVar, at="uValue", cl=True)
					mc.setAttr(moPathVar + ".uValue", 0.5)
					if rndDwnCurveLength > 133: #the divisions in dv can't go over 400 without an erro, force it's hand if it tries to add too many divisions.
						
						theFlow = mc.flow(newCylinder[0], oc =False, lc=True, dv=(2,2,400), ld=(2,2,2))
						#print("I have too many divisions to be multiplied by 3")
					else:	
						theFlow = mc.flow(newCylinder[0], oc =False, lc=True, dv=(2,2,rndDwnCurveLength*3), ld=(2,2,2))
					
					mc.setAttr(theFlow[2] + ".visibility", 0)						
			
					"""set the blendshape animation offset is set to 20 look at randomizing this so it's not so similar
					otherwise this turns into too much consistancy"""
					mc.setKeyframe(theBlndShp[0] + ".w[0]", v=1, t=[sortedKeyFrameList[0], sortedKeyFrameList[0]])
			        mc.setKeyframe(theBlndShp[0] + ".w[0]", v=0, t=[sortedKeyFrameList[-1], sortedKeyFrameList[-1]])        
			        mc.setKeyframe(theBlndShp[0] + ".w[1]", v=0, t=[(sortedKeyFrameList[0]+20), (sortedKeyFrameList[0]+20)])
			        mc.setKeyframe(theBlndShp[0] + ".w[1]", v=1, t=[(sortedKeyFrameList[-1]+20), (sortedKeyFrameList[-1]+20)])
			        
			        #set the visibility
			        mc.setKeyframe(newCylinder[0] + ".v", v=0, t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[0]-1])
			        mc.setKeyframe(newCylinder[0] + ".v", v=1, t=[sortedKeyFrameList[0], sortedKeyFrameList[0]])
			        mc.setKeyframe(newCylinder[0] + ".v", v=1, t=[sortedKeyFrameList[-1]+20, sortedKeyFrameList[-1]+20])
			        mc.setKeyframe(newCylinder[0] + ".v", v=0, t=[sortedKeyFrameList[-1]+21, sortedKeyFrameList[-1]+21])
			        
			        inc += 1		  
			        mc.parent(newCylinder[0], newCylBlendShp_A[0], newCylBlendShp_B[0], theFlow[2], theFlow[3], curveObj, grpFolder)
			        mc.parent(grpFolder, everyThingFolder)
	        
	        
	else:
		print "Your selection may include something that's not an nParticle, please reselect only nParticles." #add condition if nothing is selected