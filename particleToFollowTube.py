import maya.cmds as mc
import random
import math
#Global variables
nParticlesList = []

def selNParticles():
	global nParticlesList
	nParticlesList = mc.ls(sl=True, dag=True, lf=True)
	for item in nParticlesList:
		mc.textScrollList("getnPartiList", e=True, ra=True)
		if len(nParticlesList) > 0 and mc.nodeType(item) == 'nParticle':
			mc.textScrollList("getnPartiList", e=True, a=(item))
			pass
		else:
			mc.textScrollList("getnPartiList", e=True, ra=True)
			print 'reselct only nParticles'

def createCurves():
	inc=0
	global nParticlesList

	allParticleDictionary = {}
	minFrames = mc.playbackOptions( q=True, min=True)
	maxFrames = mc.playbackOptions( q=True, max=True)

	for shapeSel in nParticlesList:
		if "nParticle" == mc.objectType(shapeSel) and len(nParticlesList) != 0:#check and make sure that what we have selected are nParticles.

			getTrans = mc.pickWalk(shapeSel, d="up")
			theParticle = mc.ls(getTrans, type = "transform")
			everyThingFolder = mc.group(em=True, n="AllTheThingsAreHERE")

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


		
					rndDwnCurveLength = math.trunc(mc.arclen(curveObj))

					if rndDwnCurveLength <= 1: #check to see if the curve has at least 3 segments.
						print "This error has occured because the particle animation hasn't finished in the timeline" #This is why it's a good idea to animate the emitter to 0 several frames before the animation ends. Otherwise you emit a particle and there are less then 2 spans in the curve at the end.
					else:
						tubeDiv = int(mc.textField('tubeDetail', q=True, text=True)) #Query the textfield to get the user tube div value
						tubeRad = float(mc.textField('tubeRadius', q=True, text=True)) #Query the textfield to get the user radius value
						bendDet = int(mc.textField('bendDetail', q=True, text=True)) #Query the textfield to get the user radius value
						newCylinder = mc.polyCylinder(name="tubePoly_0" + str(inc), ch=True, r=tubeRad, ax=[0,0,90], sh=(rndDwnCurveLength*2 + tubeDiv), h=rndDwnCurveLength)
						newCylBlendShp_A = mc.polyCylinder(name="tubeBlendShpA_0" + str(inc), ch=True, r=tubeRad, ax=[0,0,90], sh=(rndDwnCurveLength*2 + tubeDiv), h=rndDwnCurveLength)

						getBndBoxDim = mc.xform(newCylBlendShp_A[0], q=True, ws=True, bb=True)
						mc.setAttr(newCylBlendShp_A[0] + ".visibility", 0)
						#print getBndBoxDim
						mc.xform(newCylBlendShp_A, p=True, sp=[0,0, getBndBoxDim[2]], rp=[0,0, getBndBoxDim[2]])
						newCylBlendShp_B = mc.polyCylinder(name="tubeBlendShpB_0" + str(inc), ch=True, r=tubeRad, ax=[0,0,90], sh=(rndDwnCurveLength*2 + tubeDiv), h=rndDwnCurveLength)
						mc.setAttr(newCylBlendShp_B[0] + ".visibility", 0)
						mc.xform(newCylBlendShp_B, p=True, sp=[0,0, getBndBoxDim[5]], rp=[0,0, getBndBoxDim[5]])

						mc.scale(1,1,.001, newCylBlendShp_A, r=True)
						mc.makeIdentity(newCylBlendShp_A,a=True, s=True)
						mc.scale(1,1,.001, newCylBlendShp_B, r=True)
						mc.makeIdentity(newCylBlendShp_B,a=True, s=True)

						theBlndShp = mc.blendShape(newCylBlendShp_A[0], newCylBlendShp_B[0], newCylinder[0])
						moPathVar =  mc.pathAnimation(newCylinder, fa="Z", fm=True, f=True, ua="y", wut = "vector", su=0.5, eu=0.5, stu=(mc.playbackOptions(q=True, minTime=True)), etu=(mc.playbackOptions(q=True, maxTime=True)) ,c=curveObj)
						getCon = mc.listConnections(moPathVar, c=True)

						mc.cutKey(moPathVar, at="uValue", cl=True)
						mc.setAttr(moPathVar + ".uValue", 0.5)
						if rndDwnCurveLength > 133: #the divisions in dv can't go over 400 without an erro, force it's hand if it tries to add too many divisions.

							theFlow = mc.flow(newCylinder[0], oc =False, lc=True, dv=(2,2,rndDwnCurveLength*3 + bendDet), ld=(2,2,2))
							#print("I have too many divisions to be multiplied by 3")
						else:
							theFlow = mc.flow(newCylinder[0], oc =False, lc=True, dv=(2,2,rndDwnCurveLength*3 + bendDet), ld=(2,2,2))

						mc.setAttr(theFlow[2] + ".visibility", 0)

						extruOffset = int(mc.textField('extOffSet', q=True, text=True)) #Query the textfield to get the offset value

						"""set the blendshape animation offset is set to 20 look at randomizing this so it's not so similar
						otherwise this turns into too much consistancy"""

						print theBlndShp[0] + ".w[0]"
						mc.setKeyframe(theBlndShp[0] + ".w[0]", v=1, t=[sortedKeyFrameList[0], sortedKeyFrameList[0]])
						mc.setKeyframe(theBlndShp[0] + ".w[0]", v=0, t=[sortedKeyFrameList[-1], sortedKeyFrameList[-1]])


						if mc.checkBox("extAnim", q=True, v=1) == True:
							print 'Extrusion Visible checkbox is on'
							mc.setKeyframe(theBlndShp[0] + ".w[1]", v=0, t=[(sortedKeyFrameList[0]+ extruOffset), (sortedKeyFrameList[0]+ extruOffset)])
							mc.setKeyframe(theBlndShp[0] + ".w[1]", v=1, t=[(sortedKeyFrameList[-1]+ extruOffset), (sortedKeyFrameList[-1]+ extruOffset)])
						else:
							print 'Extrusion Visible checkbox is off'

						#set the visibility

						mc.setKeyframe(newCylinder[0] + ".v", v=0, t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[0]-1])
						mc.setKeyframe(newCylinder[0] + ".v", v=1, t=[sortedKeyFrameList[0], sortedKeyFrameList[0]])


						if mc.checkBox("aniVis", q=True, v=1) == True:
							print 'Animation visibility checkbox is on'
							mc.setKeyframe(newCylinder[0] + ".v", v=1, t=[sortedKeyFrameList[-1]+ extruOffset, sortedKeyFrameList[-1]+ extruOffset])
							mc.setKeyframe(newCylinder[0] + ".v", v=0, t=[sortedKeyFrameList[-1]+ extruOffset +1, sortedKeyFrameList[-1]+ extruOffset + 1])
						else:
							print 'Animation visibility checkbox is off'


						inc += 1
						mc.parent(newCylinder[0], newCylBlendShp_A[0], newCylBlendShp_B[0], theFlow[2], theFlow[3], curveObj, grpFolder)
						mc.parent(grpFolder, everyThingFolder)


		else:
			print "Your selection may include something that's not an nParticle, please reselect only nParticles." #add condition if nothing is selected
#--------------------------------------------------------------------------------------------------------

def makeTubeExtGui():

	if (mc.window("partiCurveExtrusion", exists=True)):
		mc.deleteUI("partiCurveExtrusion", wnd=True)
		mc.windowPref("partiCurveExtrusion", r=True)

	# C R E A T E  U I
	mc.window("partiCurveExtrusion", s=False, tlb=True, rtf=True, t="Tube Exxxxtrusion")
	mc.columnLayout(adj=True)

	# L I S T  n P A R T I C L E S
	mc.frameLayout(l="Add selected nParticles to list", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.button(label="Add selected nParticles",bgc=(0.24, 0.72, 0.46), c =lambda *x:selNParticles() , h = 30 )
	mc.textScrollList("getnPartiList", h=100, ams=False)
	mc.setParent('..')
	mc.setParent('..')

	# A N I M A T I O N  V I S I B I L I T Y
	mc.frameLayout(l="End of tube animation on/off", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.checkBox('extAnim',label="Animatie Extrusion", bgc=(0.21, 0.67, 0.72), v=True )

	# E X T R U S I O N   A N I M A T I O N
	mc.frameLayout(l="Tube visibility on/off", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.checkBox('aniVis', label="Animate Visibility", bgc=(0.21, 0.67, 0.72), v=True )

	# E X T R U S I O N  O F F S E T - animates the tail of the tube based off keyframes default is a hold for 20 keyframes
	mc.frameLayout(l="Animate Extrusion Tail Offset", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('extOffSet', bgc=(0.21, 0.67, 0.72), text='20')


	# T U B E  D E T A I L
	mc.frameLayout(l="Tube Divisions +", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('tubeDetail', bgc=(0.21, 0.67, 0.72), text='0')

	# T U B E  R A D I U S
	mc.frameLayout(l="Tube Radius", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('tubeRadius', bgc=(0.21, 0.67, 0.72), text='.25')

	# B E N D  D E T A I L
	mc.frameLayout(l="Bend Detail +", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('bendDetail', bgc=(0.21, 0.67, 0.72), text='0')


	# C R E A T E  C U R V E S
	mc.button(label="Create Curves", bgc=(0.24, 0.72, 0.46), c =lambda *x:createCurves() , h = 40 )

	mc.setParent('..')
	mc.setParent('..')

	# S H O W  W I N D O W
	mc.showWindow("partiCurveExtrusion")


makeTubeExtGui()
