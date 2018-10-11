import maya.cmds as mc
import copy
import itertools

#allSrcEdges = ['pCylinder3.e[0]', 'pCylinder3.e[3]', 'pCylinder3.e[7]', 'pCylinder3.e[11]', 'pCylinder3.e[15]', 'pCylinder3.e[19]', 'pCylinder3.e[23]', 'pCylinder3.e[27]', 'pCylinder3.e[31]', 'pCylinder3.e[35]', 'pCylinder3.e[39]', 'pCylinder3.e[43]', 'pCylinder3.e[47]', 'pCylinder3.e[51]', 'pCylinder3.e[55]', 'pCylinder3.e[56]', 'pCylinder3.e[112]', 'pCylinder3.e[168]', 'pCylinder3.e[224]', 'pCylinder3.e[280]', 'pCylinder3.e[336]', 'pCylinder3.e[392]', 'pCylinder3.e[448]', 'pCylinder3.e[504]', 'pCylinder3.e[560]', 'pCylinder3.e[6074]', 'pCylinder3.e[6135]', 'pCylinder3.e[6195]', 'pCylinder3.e[6255]', 'pCylinder3.e[6315]', 'pCylinder3.e[6375]', 'pCylinder3.e[6435]', 'pCylinder3.e[6495]', 'pCylinder3.e[6555]', 'pCylinder3.e[6615]', 'pCylinder3.e[6623]', 'pCylinder3.e[6627]', 'pCylinder3.e[6631]', 'pCylinder3.e[6635]', 'pCylinder3.e[6639]', 'pCylinder3.e[6643]', 'pCylinder3.e[6647]', 'pCylinder3.e[6651]', 'pCylinder3.e[6655]', 'pCylinder3.e[6659]', 'pCylinder3.e[6663]', 'pCylinder3.e[6667]', 'pCylinder3.e[6671]', 'pCylinder3.e[6675]', 'pCylinder3.e[6677]', 'pCylinder3.e[6743]', 'pCylinder3.e[6744]', 'pCylinder3.e[6747]', 'pCylinder3.e[6748]', 'pCylinder3.e[6751]', 'pCylinder3.e[6752]', 'pCylinder3.e[6755]', 'pCylinder3.e[6756]', 'pCylinder3.e[6759]', 'pCylinder3.e[6760]', 'pCylinder3.e[6763]', 'pCylinder3.e[6764]', 'pCylinder3.e[6767]', 'pCylinder3.e[6768]', 'pCylinder3.e[6771]', 'pCylinder3.e[6772]', 'pCylinder3.e[6775]', 'pCylinder3.e[6776]', 'pCylinder3.e[6779]', 'pCylinder3.e[6780]', 'pCylinder3.e[6783]', 'pCylinder3.e[6784]', 'pCylinder3.e[6785]', 'pCylinder3.e[6788]', 'pCylinder3.e[6820]', 'pCylinder3.e[6822]', 'pCylinder3.e[6824]', 'pCylinder3.e[6826]', 'pCylinder3.e[6828]', 'pCylinder3.e[6830]', 'pCylinder3.e[6832]', 'pCylinder3.e[6834]', 'pCylinder3.e[6836]', 'pCylinder3.e[6838]', 'pCylinder3.e[6840]', 'pCylinder3.e[6842]', 'pCylinder3.e[6843]', 'pCylinder3.e[7014]', 'pCylinder3.e[7100]']
#selSrcStartEdge = ['pCylinder3.e[6627]']


#--------------------------------------------------------------  G L O B A L S ------------------------------------------
selSrcStartEdge = []
selSrcSecondEdge = []
selSrcBorderEdge = []
selTgtStartEdge = []
selTgtSecondEdge = []
selTgtBorderEdge = []
srcTgtCrntState = []
sortedList = []
orderedVertList = []
spacerCollector = []
newEdgeCurve = ''
spacerNode = ''

def edgeCleanExe():
	global srcTgtCrntState

	#query the if the geo has transforms data
	srcTgtCrntState = 1
	orderEdges() 	 #Loop 1
	orderVerts()	 #Loop 2
	buildEdgeCurve() #Loop 3
	srcTgtCrntState = 2
	orderEdges() 	 #Loop 1
	orderVerts()	 #Loop 2
	spacerBuilder()  #Loop 4
	edgeConnect()	 #Loop 5
	srcTgtCrntState = 1

#------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------- E D G E  O R D E R --------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
def orderEdges():
	global srcTgtCrntState
	global selSrcStartEdge
	global selSrcSecondEdge
	global selTgtStartEdge
	global selTgtSecondEdge
	global sortedList
	global edgVrtList

	#Choose between the source and target selected edges to run
	if srcTgtCrntState == 1:
		edgeOne = selSrcStartEdge
		edgeTwo = selSrcSecondEdge #the variable names the change to need to be changed- confusing
		allTheEdges = selSrcBorderEdge
	elif srcTgtCrntState > 1:
		edgeOne = selTgtStartEdge
		edgeTwo = selTgtSecondEdge
		allTheEdges = selTgtBorderEdge
	#Ordered edge list
	#mc.select(edgeOne[0])
	#mc.polySelectConstraint( pp=4, m2a=45.0, m3a=90.0)
	#allTheEdges = mc.ls(sl=True, fl=True)
	allTheEdges.remove(edgeOne[0])
	kindaFancyDict = {}
	for edge in allTheEdges:
		kindaFancyDict[edge] = {}
		getVerts = mc.ls(mc.polyListComponentConversion(edge, fe=True, tv=True), fl=True)
		kindaFancyDict[edge]['vtx0'] = mc.xform(getVerts[0], ws=True, q=True, translation=True)
		#kindaFancyDict[edge]['vtx0N'] = getVerts[0]
		kindaFancyDict[edge]['vtx1'] = mc.xform(getVerts[1], ws=True, q=True, translation=True)
		#kindaFancyDict[edge]['vtx1N'] = getVerts[1]
	fancyDict = {}
	fancyDict = copy.deepcopy(kindaFancyDict)
	key = edgeTwo[0]
	sortedList = [edgeOne[0], edgeTwo[0]] #selSecondEdge 0 could become a variable to choose direction
	while key in fancyDict:
		edge0 = fancyDict[key]['vtx0']
		edgel = fancyDict[key]['vtx1']
		originalKey = key
		for vtx0key, vtx in fancyDict.iteritems():
			if edgel == vtx['vtx0'] or edge0 == vtx['vtx1'] or edgel == vtx['vtx1'] or edge0 == vtx['vtx0'] :
				if vtx0key != key:
					sortedList.append(vtx0key)
					key = vtx0key
					break
		#print 'The origKey = ' + originalKey, 'The key = ' + key, 'Items in sorted list ' + str(len(sortedList)), 'length of the dict ' + str(len(fancyDict))
		if originalKey == key:
			break
		del fancyDict[originalKey]
	edgVrtList = copy.copy(sortedList)
	getSrcEdgeOrder()
	print sortedList

#--------------------------------------------------------------------------------------------------------
def orderVerts():
	global edgVrtList
	global orderedVertList
	#Ordered Vert list
	orderedVertList = []
	edgeList = []
	firstEdgeVerts = mc.ls(mc.polyListComponentConversion(edgVrtList[0], fe=True, tv=True), fl=True)
	SecondEdgeVerts = mc.ls(mc.polyListComponentConversion(edgVrtList[1], fe=True, tv=True), fl=True)
	[commonVert for commonVert in firstEdgeVerts if commonVert in SecondEdgeVerts]
	firstEdgeVerts.remove(commonVert)
	orderedVertList.append(firstEdgeVerts[0])
	orderedVertList.append(commonVert)
	edgVrtList.remove(edgVrtList[0])
	edgVrtList.remove(edgVrtList[0])#The first two items need to be removed, 0 is used twice since the first item is deleted prior
	for edge in edgVrtList:
		#print edge
		edgeVerts = mc.ls(mc.polyListComponentConversion(edge, fe=True, tv=True), fl=True)
		for vertPair in edgeVerts:
			if vertPair not in orderedVertList:
				orderedVertList.append(vertPair)
	print orderedVertList
#--------------------------------------------------------------------------------------------------------
def buildEdgeCurve():
	global sortedList
	global newEdgeCurve
	global spacerNode
	#Create a curve that fits the selected edges
	crvGarbageCollect = []
	for edgCrv in sortedList:
		curveAttach = mc.duplicateCurve(edgCrv, ch=True, rn=0, local=0, n=("edgeCurve"))
		crvGarbageCollect.append(curveAttach[0])
	newEdgeCurve = mc.attachCurve(crvGarbageCollect, ch=False, rpo=False, kmk = 1, m = 0, n= 'bigEdgeCurve', bb = 0.5, bki = 0, p=0.1)
	mc.rebuildCurve(newEdgeCurve, ch=False, rpo=True, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=400, d=1, tol=0.01)
	#Rebuild is mandatory otherwise the EP joints are too unevenly spaced, this helps to correct the problem. Uneven EP's result in poor placement of the locators for snapping.
	mc.delete(crvGarbageCollect) # A bit of tidyness
	bigCrvShp =  mc.ls(newEdgeCurve, s=True, dag=True)
	spacerNode = mc.shadingNode('pointOnCurveInfo',au=True,  n='spacerCurveInfo')
	mc.setAttr(spacerNode + '.turnOnPercentage', 1)
	mc.connectAttr(bigCrvShp[0] + '.worldSpace[0]', spacerNode + '.inputCurve')

#--------------------------------------------------------------------------------------------------------
def spacerBuilder():
	global orderedVertList
	global spacerCollector
	global spacerNode
	#create the same amount of evenly spaced locators as there are verts on the newEdgeCurve
	spacerCollector = []
	#mc.setAttr(spacerNode + '.parameter', 0.0)

	#newSpacer = mc.spaceLocator(n='spacer_0', p=(0,0,0))#Make some locators
	#getParamPos = mc.getAttr(spacerNode + '.position')#query the placement of the pointOnCurveInfo node for locator placement
	#mc.xform(newSpacer[0], t=getParamPos[0])
	#spacerCollector.append(newSpacer)
	upVal=1
	for invertSpacer in orderedVertList:
		crntParamPos = float(upVal)/float(len(orderedVertList))
		#print crntParamPos
		newSpacer = mc.spaceLocator(n='spacer_0', p=(0,0,0))#Make some locators
		getParamPos = mc.getAttr(spacerNode + '.position')#query the placement of the pointOnCurveInfo node for locator placement
		mc.xform(newSpacer[0], t=getParamPos[0])
		mc.setAttr(spacerNode + '.parameter', crntParamPos)
		spacerCollector.append(newSpacer)
		upVal += 1

		#print crntParamPos

#--------------------------------------------------------------------------------------------------------
def edgeConnect():
	global orderedVertList
	global spacerCollector
	global newEdgeCurve
	print len(orderedVertList), orderedVertList
	print len(spacerCollector), spacerCollector
	
	for inc, spacerPos in enumerate(spacerCollector):
		locWSPos = mc.xform(spacerPos[0], ws=True, q=True, translation=True)
		mc.xform(orderedVertList[inc], t=locWSPos)
	#Clean up
	for loc in spacerCollector:
		mc.delete(loc)
	mc.delete(newEdgeCurve)
	#print spacerCollector
	#print newEdgeCurve
	
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------- G U I ----------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
def evenSpacerGui():

	if (mc.window("evenSpacerWin", exists=True)):
		mc.deleteUI("evenSpacerWin", wnd=True)
		mc.windowPref("evenSpacerWin", r=True)

	# C R E A T E  U I
	mc.window("evenSpacerWin", s=True, tlb=True, rtf=True, t="Evenly Spaced Border Geo")
	mc.columnLayout(adj=True)

	# F I R S T  S O U R C E  E D G E
	mc.frameLayout(l="Source: Select Starting Edge", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 350)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=5)
	mc.textScrollList("srcStartEdgeList", h=30, ams=False)
	mc.button('allSrcBtn',l='Add Src Edge', bgc=(0.21, 0.67, 0.72), c='srcStartEdge()', h = 30, w=80)
	mc.setParent('..')
	mc.setParent('..')

	# S E C O N D   S O U R C E  E D G E
	mc.frameLayout(l="Source: Select Next Edge", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 350)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=5)
	mc.textScrollList("srcSecndEdgeList", h=30, ams=False)
	mc.button('stSrcBtn',l='Add Src Edge', bgc=(0.21, 0.67, 0.72), c='getSrcSecondEdge()', h = 30, w=80)
	mc.setParent('..')
	mc.setParent('..')

	# B O R D E R   E D G E
	mc.frameLayout(l="Select Source Border Edge", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 350)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=5)
	mc.textScrollList("srcBrdEdgList", h=30, ams=False)
	mc.button('srcBrdEdgBtn',l='Add Brdr Edge', bgc=(0.21, 0.67, 0.72), c='getSrcBorderEdge()', h = 30, w=80)
	mc.setParent('..')
	mc.setParent('..')

	# F I R S T  T A R G E T   E D G E
	mc.frameLayout(l="Target: Select Starting Edge", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 350)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=5)
	mc.textScrollList("tgtEdgeList", h=30, ams=False)
	mc.button('allTgtBtn',l='Add Tgt Edge', bgc=(0.21, 0.67, 0.72), c='getTgtAllEdges()', h = 30, w=80)
	mc.setParent('..')
	mc.setParent('..')

	# S E C O N D  T A R G E T  E D G E
	mc.frameLayout(l="Target: Select Next Edge", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 350)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=5)
	mc.textScrollList("tgtStrtEdgeList", h=30, ams=False)
	mc.button('stTgtBtn',l='Add Tgt Edge', bgc=(0.21, 0.67, 0.72), c='getTgtStartEdge()', h = 30, w=80)
	mc.setParent('..')
	mc.setParent('..')

	# T A R G E T  B O R D E R   E D G E
	mc.frameLayout(l="Select Target Border Edge", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 350)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=5)
	mc.textScrollList("tgtBrdEdgList", h=30, ams=False)
	mc.button('tgtBrdEdgBtn',l='Add Brdr Edge', bgc=(0.21, 0.67, 0.72), c='getTgtBorderEdge()', h = 30, w=80)
	mc.setParent('..')
	mc.setParent('..')

	mc.frameLayout( l="Source Edge Order", la="top", bgc=(0.1, 0.1, 0.1), cll=True, cl=True, w = 350)
	mc.textField('srcStartEdgeList', h=85)
	mc.setParent('..')
	mc.setParent('..')

	# E X E C U T E

	mc.button('exeEdgeBtn',l='E X E C U T E', bgc=(0.21, 0.67, 0.72), c='edgeCleanExe()', h = 30, w=80)

	mc.setParent('..')
	mc.setParent('..')

	# S H O W  W I N D O W
	mc.showWindow("evenSpacerWin")

#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------- G U I  T E X T S C R O L L  L I S T ----------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
def srcStartEdge():
	global	selSrcStartEdge
	selSrcStartEdge = mc.ls(sl=True, fl=True)
	mc.textScrollList("srcStartEdgeList", e=True, ra=True)
	for i in selSrcStartEdge:
		mc.textScrollList("srcStartEdgeList", e=True, a=(i))
#--------------------------------------------------------------------------------------------------------

def getSrcSecondEdge():
	global selSrcSecondEdge
	selSrcSecondEdge = mc.ls(sl=True, fl=True)
	mc.textScrollList("srcSecndEdgeList", e=True, ra=True)
	for i in selSrcSecondEdge:
		mc.textScrollList("srcSecndEdgeList", e=True, a=(i))
#--------------------------------------------------------------------------------------------------------

def getSrcBorderEdge():
	global selSrcBorderEdge
	selSrcBorderEdge = mc.ls(sl=True, fl=True)
	mc.textScrollList("srcBrdEdgList", e=True, ra=True)
	for i in selSrcBorderEdge:
		mc.textScrollList("srcBrdEdgList", e=True, a=(i))
#--------------------------------------------------------------------------------------------------------

def getTgtAllEdges():
	global selTgtStartEdge
	selTgtStartEdge = mc.ls(sl=True, fl=True)
	mc.textScrollList("tgtEdgeList", e=True, ra=True)
	for i in selTgtStartEdge:
		mc.textScrollList("tgtEdgeList", e=True, a=(i))
#--------------------------------------------------------------------------------------------------------

def getTgtStartEdge():
	global selTgtSecondEdge
	selTgtSecondEdge = mc.ls(sl=True, fl=True)
	mc.textScrollList( "tgtStrtEdgeList", e=True, ra=True)
	if len(selTgtSecondEdge) > 1:
		mc.warning('There should only be the target start edge selected')
	else:
		for i in selTgtSecondEdge:
			mc.textScrollList("tgtStrtEdgeList", e=True, a=(i))
#--------------------------------------------------------------------------------------------------------

def getTgtBorderEdge():
	global selTgtBorderEdge
	selTgtBorderEdge = mc.ls(sl=True, fl=True)
	mc.textScrollList("tgtBrdEdgList", e=True, ra=True)
	for i in selTgtBorderEdge:
		mc.textScrollList("tgtBrdEdgList", e=True, a=(i))
#--------------------------------------------------------------------------------------------------------

def getSrcEdgeOrder():
	global sortedList
	mc.textField('srcStartEdgeList', e=True, tx=str(sortedList))
evenSpacerGui()
