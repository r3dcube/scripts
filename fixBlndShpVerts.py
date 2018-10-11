import maya.cmds as mc

			##################################################################################
			#																		 		 #
			#  TO RUN THIS SCRIPT JUST SELECT ALL AND EXECUTE OR PLACE THE MAKEGUI() AT THE  # 
			#  BOTTOM INTO A SHELF BUTTON	 												 #
			#																		 		 #
			##################################################################################

# G L O B A L S
getSrcObjs = []
getTrgtObjs = []
getVerts = []

#--------------------------------------------------------------------------------------------------------

def getSourceObj():	
	global getSrcObjs
	getSrcObjs = mc.ls(sl=True, tr=True)
	getSrcShp = mc.listRelatives(s=True)
	mc.textScrollList("getSrcObjList", e=True, ra=True)	
	for i in getSrcObjs:
		mc.textScrollList("getSrcObjList", e=True, a=(i))
	if len(getSrcObjs) == 1 and mc.nodeType(getSrcShp) == 'mesh' :
		print 'you have one object'
		pass		
	else:
		print('selection requires 1 poly object, you have %i %s' % (len(getSrcObjs), getSrcShp))
		mc.textScrollList("getSrcObjList", e=True, ra=True)
		getSrcObjs = []
		
#--------------------------------------------------------------------------------------------------------			

def getTargetObj():
	global getTrgtObjs
	getTrgtObjs = mc.ls(sl=True, tr=True)
	for trgt in getTrgtObjs:
		getTrgtShp = mc.listRelatives(trgt, s=True)	
		mc.textScrollList("getTargetObjList", e=True, ra=True)
		if mc.nodeType(getTrgtShp)	== 'mesh':
			for i in getTrgtObjs:
				mc.textScrollList("getTargetObjList", e=True, a=(i))
		else:
			print 'you need to have a poly object selected'

#--------------------------------------------------------------------------------------------------------	

def getVerticies():
	global getVerts
	getVerts = mc.ls(sl=True, fl=True)
	isVert = mc.polyEvaluate(getVerts, vc=True)
	mc.textScrollList("getSelVertList", e=True, ra=True)
	if isVert != 0:
		mc.textScrollList("getSelVertList", e=True, a=(str(len(getVerts))) + ' verts selected')
		print('you have selected %s verts' % (str(len(getVerts))))
	else:
		mc.textScrollList("getSelVertList", e=True, ra=True)
		print 'There are no vertices selected'	
	
#--------------------------------------------------------------------------------------------------------

def sortObjs():
	global getVerts
	global getTrgtObjs
	global getSrcObjs	
	if getSrcObjs == [] or getTrgtObjs == [] or getVerts == []:
		if getSrcObjs == []:			
			print'You have no source object selected'
		if getTrgtObjs == []:			
			print'You have no target object selected'
		if getVerts == []:			
			print'You have no target vertices selected'
		
	else:
		for objs in getTrgtObjs:
			print('working on ' + objs)
			i=0
			for currentVert in getVerts:
				totalVerts = len(getVerts)
				vertNum = currentVert.split('.')					
				getPos = mc.xform(getSrcObjs[0] + "." + vertNum[1], ws=True, q=True, translation=True)				
				mc.xform(objs + "." + vertNum[1], t=(getPos[0], getPos[1], getPos[2]))
				if i % 1000 == 0:
					print 'Working on vert %i of %i' % (i, totalVerts) 				
				i+=1
		print ('process completed, all ' + str(len(getVerts)) + ' have been transfered')
		
#--------------------------------------------------------------------------------------------------------
def createVertSet():	
	global getTrgtObjs
	global getVerts
	mc.textScrollList("vertSetList", e=True, ra=True)
	polyVerts = mc.polyListComponentConversion(getTrgtObjs, tv=True)
	mc.select(polyVerts)
	convVerts = mc.ls(sl=True, fl=True)
	setVerts = set(convVerts) - set(getVerts)
	mc.select(list(setVerts))
	setName = mc.sets(name= str(getTrgtObjs[0]) +'_SET')
	mc.select(cl=True)
	mc.textScrollList("vertSetList", e=True, a=(setName + ' set created'))

#-------------------------------------------------------------------------------------------------------- 
def setOutlineColor():
	getRedVal = mc.floatField("intRedValField", q=True, v=True)
	getGreenVal = mc.floatField("intGreenValField", q=True, v=True)
	getBlueVal = mc.floatField("intBlueValField", q=True, v=True)
	print getRedVal,getGreenVal,getBlueVal  
	
	getOutlinerItems = mc.ls(sl=True, tr=True)
	for item in getOutlinerItems:
		mc.setAttr(item + ".useOutlinerColor", 1)
		mc.setAttr(item + ".outlinerColor", getRedVal,getGreenVal,getBlueVal)
		
#-------------------------------------------------------------------------------------------------------- 
	
def makeGui():
	
	if (mc.window("fixVertWin", exists=True)):
		mc.deleteUI("fixVertWin", wnd=True)
		mc.windowPref("fixVertWin", r=True)
	
	# C R E A T E  U I
	mc.window("fixVertWin", s=False, tlb=True, rtf=True, t="Translate Vertex")
	mc.columnLayout(adj=True)

	# S O U R C E  O B J E C T S
	mc.frameLayout(l="Source", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.button(label="Set Source Object",bgc=(0.27, 0.68, 0.66), c =lambda *x:getSourceObj() , h = 30 )	
	mc.textScrollList("getSrcObjList", h=30, ams=False)
	mc.setParent('..')
	mc.setParent('..')

	# T A R G E T  O B J E C T S
	mc.frameLayout(l="Target", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.button(label="Set Target Object(s)", bgc=(0.21, 0.67, 0.72), c =lambda *x:getTargetObj(), h = 30 )
	mc.textScrollList("getTargetObjList", h=100, ams=False)

	# T A R G E T  V E R T I C E S
	mc.frameLayout(l="Vertex Selection", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.button(label="Get Selected Verts", bgc=(0.21, 0.67, 0.72), c =lambda *x:getVerticies() , h = 30 )
	mc.textScrollList("getSelVertList", h=30, ams=False)
	
	# I N V E R S E  S E T  S E L E C T I O N
	mc.frameLayout(l="Outliner Set Selection", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.button(label="Create Inverse Vert Set", bgc=(0.21, 0.67, 0.72), c =lambda *x:createVertSet() , h = 30 )
	mc.textScrollList("vertSetList", h=30, ams=False)
	
	# O U T L I N E R  C O L O R
	mc.frameLayout(l="Outliner Color", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=5)
	mc.floatField('intRedValField', min=0.0, max=1.0,w=40)
	mc.floatField('intGreenValField', min=0.0, max=1.0,w=40)
	mc.floatField('intBlueValField', min=0.0, max=1.0,w=40)
	mc.button( label="Set Color", bgc=(0.21, 0.67, 0.72), c =lambda *x:setOutlineColor() , h = 30, w=80)
	mc.setParent('..')
	mc.setParent('..')
	# U P D A T E  V E R T I C E S
	
	mc.button(label="Update Verts", bgc=(0.24, 0.72, 0.46), c =lambda *x:sortObjs() , h = 40 )	
		
	mc.setParent('..')
	mc.setParent('..')

	# S H O W  W I N D O W
	mc.showWindow("fixVertWin")
	

makeGui()