import maya.cmds as mc
#----------------------------------------------------------------------------------------------------------
#------------------------------                Tool for Toggling           --------------------------------
#----------------------------------------------------------------------------------------------------------

'''
                USE THIS TOOL FOR SIMPLE TOGGLING OF OBJECT PARAMATERS WHILE MODELING. THE TOOL IS AIMED
                AT BRINGING COMMON EVERYDAY TOOLS TO THE FOREGROUND AND OUTSIDE OF THE NUMEROUS MENUS THEY LIVE
                BEHIND. ALLOWS YOU TO TOGGLE BORDER EDGES, BACKFACE CULLING, NORMALS, WIREFRAME/SHADED, BOUNDING BOX,
                VERTICES,XRAY ON SELECTION AND EVEN MOVE PIVOT TO THE BASE OF AN OBJECT.
                TO USE - Source the script then run bwToggle from the command line : bwToggle
                

'''

#----------------------------------------------------------------------------------------------------------
def togNormals():
	global nrmBtn
	labelNrmOn = 'Toggle Normals ON'
	labelNrmOff = 'Toggle Normals OFF'
	tgNrmls = mc.ls(sl=True, dag=True, lf=True)
	crntState = mc.button('btn1', q=True, l=True)	
	
	if crntState != labelNrmOn:
		mc.button('btn1', e=True, l=labelNrmOn)
		for normals in tgNrmls:
			mc.setAttr(normals + '.displayNormal', 1)
	else:
		mc.button('btn1', e=True, l=labelNrmOff)
		for normals in tgNrmls:
			mc.setAttr(normals + '.displayNormal', 0)
#----------------------------------------------------------------------------------------------------------
def revNormals():	
	labelRevOn = 'Toggle Reverse Front'
	labelRevOff = 'Toggle Reverse Back'
	revNrmls = mc.ls(sl=True, dag=True, lf=True)
	revState = mc.button('btn2', q=True, l=True)
		
	if revState != labelRevOn:
		mc.button('btn2', e=True, l=labelRevOn)
		for revNrm in revNrmls:
			mc.polyNormal(revNrm, nm=0,unm=0, ch=True)
	else:
		mc.button('btn2', e=True, l=labelRevOff)
		for revNrm in revNrmls:
			mc.polyNormal(revNrm, nm=0,unm=0, ch=True)	

#----------------------------------------------------------------------------------------------------------
def wireOrShade():
	labelWireOn = 'Wireframe ON'
	labelWireOff = 'Shading ON'
	getWireShade = mc.ls(sl=True, dag=True, lf=True)
	wireState = mc.button('btn3', q=True, l=True)

	if wireState != labelWireOn:
		mc.button('btn3', e=True, l=labelWireOn)
		for wireItem in getWireShade:
			mc.setAttr(wireItem + '.overrideEnabled', 1)
			mc.setAttr(wireItem + '.overrideShading', 0)
	else:
		mc.button('btn3', e=True, l=labelWireOff)
		for wireItem in getWireShade:
			mc.setAttr(wireItem + '.overrideShading', 1)
			mc.setAttr(wireItem + '.overrideEnabled', 0)

#----------------------------------------------------------------------------------------------------------		
def toggleBorderEdge():
	labelBorderOn = 'Border ON'
	labelBorderOff = 'Border OFF'
	getBorderState = mc.ls(sl=True, dag=True, lf=True)
	borderState = mc.button('btn4', q=True, l=True)

	if borderState != labelBorderOn:
		mc.button('btn4', e=True, l=labelBorderOn)
		for border in getBorderState:
			mc.setAttr(border + '.displayBorders', 1)
			mc.setAttr(border + '.borderWidth', 5)
	else:
		mc.button('btn4', e=True, l=labelBorderOff)
		for border in getBorderState:
			mc.setAttr(border + '.borderWidth', 2)
			mc.setAttr(border + '.displayBorders', 0)
#----------------------------------------------------------------------------------------------------------			
def toggleCulling():
	labelCullOn = 'Backface Culling ON'
	labelCullOff = 'Backface Culling OFF'
	getCullState = mc.ls(sl=True, dag=True, lf=True)
	cullState = mc.button('btn5', q=True, l=True)
	
	if cullState != labelCullOn:
		mc.button('btn5', e=True, l=labelCullOn)
		for cullItm in getCullState:
			mc.setAttr(cullItm + '.backfaceCulling', 3)
			
	else:
		mc.button('btn5', e=True, l=labelCullOff)
		for cullItm in getCullState:
			mc.setAttr(cullItm + '.backfaceCulling', 0)			
	
#----------------------------------------------------------------------------------------------------------
def toggleTemplate():
	labelTempOn = 'Template ON'
	labelTempOff = 'Template OFF'
	getTempState = mc.ls(sl=True, dag=True, lf=True)
	tempState = mc.button('btn6', q=True, l=True)
	
	if tempState != labelTempOn:
		mc.button('btn6', e=True, l=labelTempOn)
		for tmplte in getTempState:
			mc.setAttr(tmplte + '.template', 1)
			
	else:
		mc.button('btn6', e=True, l=labelTempOff)
		for tmplte in getTempState:
			mc.setAttr(tmplte + '.template', 0)

#----------------------------------------------------------------------------------------------------------
def toggleBB():
	labelBBOn = 'Bounding Box ON'
	labelBBOff = 'Bounding Box OFF'
	getBBState = mc.ls(sl=True, dag=True, lf=True)
	BBState = mc.button('btn7', q=True, l=True)
	
	if BBState != labelBBOn:
		mc.button('btn7', e=True, l=labelBBOn)
		for bb in getBBState:
			mc.setAttr(bb + '.overrideEnabled', 1)
			mc.setAttr(bb + '.overrideLevelOfDetail', 1)			
	else:
		mc.button('btn7', e=True, l=labelBBOff)
		for bb in getBBState:
			mc.setAttr(bb + '.overrideLevelOfDetail', 0)
			mc.setAttr(bb + '.overrideEnabled', 0)

#----------------------------------------------------------------------------------------------------------
def toggleVert():
	labelVertOn = 'Vertices ON'
	labelVertOff = 'Vertices OFF'
	getVertState = mc.ls(sl=True, dag=True, lf=True)
	vertState = mc.button('btn8', q=True, l=True)	
	if vertState != labelVertOn:
		mc.button('btn8', e=True, l=labelVertOn)
		for vert in getVertState:
			mc.setAttr(vert + '.displayVertices', 1)
						
	else:
		mc.button('btn8', e=True, l=labelVertOff)
		for vert in getVertState:
			mc.setAttr(vert + '.displayVertices', 0)
#----------------------------------------------------------------------------------------------------------
def movePivot():
	labelPivotOn = 'Pivot Moved to Base'
	labelPivotOff = 'Pivot Centered'
	moveItemsPiv = mc.ls(sl=True, tr=True)
	pivotState = mc.button('btn9', q=True, l=True)
	
	for pivItems in moveItemsPiv:
		BBBox = mc.xform(pivItems, ws=True, q=True, bb=True)
		print BBBox			
		xAxis = ((BBBox[0] + BBBox[3])/2)
		zAxis = ((BBBox[2] + BBBox[5])/2)
		cPivot = mc.xform(cp=True)
		getPivInfo = mc.xform(q=True, piv=True)
		mc.xform(pivItems, piv=[xAxis,BBBox[1],zAxis], ws=True)	

#----------------------------------------------------------------------------------------------------------			
def objXray():
	getObjShp = mc.ls(sl=True, dag=True, ap=True, s=True)
	labelXrayOn = 'Xray On'
	labelXrayOff = 'Xray Off'
	
	for xrayObj in getObjShp:
		xrayState = mc.displaySurface(xrayObj, q=True, x=True)
		if xrayState[0] == True:
			mc.displaySurface(xrayObj, x=0)
			mc.button('btn10', e=True, l=labelXrayOff)
		else:
			mc.displaySurface(xrayObj, x=1)
			mc.button('btn10', e=True, l=labelXrayOn)			
			
#----------------------------------------------------------------------------------------------------------			
def triFaces():	
	selTriObj = mc.ls(sl=True)
	if len(selTriObj):
		mc.selectMode(co=True)
		mc.selectType(smp=False, sme=True, smf=False, smu=False, pv=False, pe=True, pf=False, puv=False)
		mc.polySelectConstraint( m=3, type=0x0008, size=1)
		mc.polySelectConstraint(disable=True)
		getTriFaces = mc.polyEvaluate(fc=True)
		print('You have %i triangle(s) in your mesh' % (getTriFaces))
	else:
		print('Please select a polygonal object')
#----------------------------------------------------------------------------------------------------------		
def ngonFaces():
	selNGonObj = mc.ls(sl=True)
	if len(selNGonObj):
		mc.selectMode(co=True)
		mc.selectType(smp=False, sme=True, smf=False, smu=False, pv=False, pe=True, pf=False, puv=False)
		mc.polySelectConstraint(m=3, type=0x0008, size=3)
		mc.polySelectConstraint(disable=True)
		getTriFaces = mc.polyEvaluate(fc=True)
		print('You have %i ngon(s) in your mesh' % (getTriFaces))
	else:
		print('Please select a polygonal object')	
#----------------------------------------------------------------------------------------------------------	
def toggleStuff():

	if (mc.window("toggle_Win", exists=True)):
		mc.deleteUI("toggle_Win", wnd=True)
		mc.windowPref("toggle_Win", r=True)

	# C R E A T E  U I
	mc.window("toggle_Win", s=False, tlb=True, rtf=True, t="Toggling Tools")
	mc.columnLayout(adj=True)

	# L I S T  S E L E C T E D  C U R V E S
	mc.frameLayout(l="UV name derived from object name", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True, rs=5)
	mc.button('btn1',l='Toggle Normals ON/OFF',bgc=(0.24, 0.72, 0.46), c='togNormals()')
	mc.button('btn2',l='Reverse Normals Direction',bgc=(0.24, 0.72, 0.46), c='revNormals()')
	mc.button('btn3',l='Toggle Wireframe/Shaded',bgc=(0.24, 0.72, 0.46), c='wireOrShade()')
	mc.button('btn4',l='Toggle Border Edge',bgc=(0.24, 0.72, 0.46), c='toggleBorderEdge()')
	mc.button('btn5',l='Toggle Backface Culling',bgc=(0.24, 0.72, 0.46), c='toggleCulling()')
	mc.button('btn6',l='Toggle Template',bgc=(0.24, 0.72, 0.46), c='toggleTemplate()')
	mc.button('btn7',l='Toggle Bounding Box',bgc=(0.24, 0.72, 0.46), c='toggleBB()')
	mc.button('btn8',l='Toggle Vertices',bgc=(0.24, 0.72, 0.46), c='toggleVert()')
	mc.button('btn9',l='Move Pivot to Object Base',bgc=(0.24, 0.72, 0.46), c='movePivot()')
	mc.button('btn10',l='Toggle X-Ray',bgc=(0.24, 0.72, 0.46), c='objXray()')
	mc.button('btn11',l='Toggle Tris',bgc=(0.24, 0.72, 0.46), c='triFaces()')
	mc.button('btn12',l='Toggle N-Gons',bgc=(0.24, 0.72, 0.46), c='ngonFaces()')
	
	mc.setParent('..')
	mc.setParent('..')
	


	# S H O W  W I N D O W
	mc.showWindow("toggle_Win")



toggleStuff()
