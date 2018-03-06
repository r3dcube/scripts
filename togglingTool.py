#----------------------------------------------------------------------------------------------------------
#------------------------------         T O O L  F O R  T O G G L I N G    --------------------------------
#----------------------------------------------------------------------------------------------------------
'''
             USE THIS TOOL FOR SIMPLE TOGGLING OF OBJECT PARAMATERS WHILE MODELING. THE TOOL IS AIMED
             AT BRINGING COMMON EVERYDAY TOOLS TO THE FOREGROUND AND OUTSIDE OF THE NUMEROUS MENUS THEY LIVE
             BEHIND. ALLOWS YOU TO TOGGLE BORDER EDGES, BACKFACE CULLING, NORMALS, WIREFRAME/SHADED, BOUNDING BOX,
             VERTICES,XRAY ON SELECTION AND EVEN MOVE PIVOT TO THE BASE OF AN OBJECT.
             TO USE - Source the script then run toggleStuff() from the command line : toggleStuff()           
'''
import maya.cmds as mc
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - T O G G L E  N O R M A L S -  - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def togNormals():
	global nrmBtn
	labelNrmOn = 'Toggle Normals ON'
	labelNrmOff = 'Toggle Normals OFF'
	tgNrmls = mc.ls(sl=True, dag=True, lf=True)
	crntState = mc.button('btn1', q=True, l=True)	
	if crntState != labelNrmOn:
		mc.button('btn1', e=True, l=labelNrmOn, bgc=(0.2, 0.5, 1.0))
		for normals in tgNrmls:
			mc.setAttr(normals + '.displayNormal', 1)
	else:
		mc.button('btn1', e=True, l=labelNrmOff, bgc=(0.24, 0.72, 0.46))
		for normals in tgNrmls:
			mc.setAttr(normals + '.displayNormal', 0)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - R E V E R S E  N O R M A L S -  - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def revNormals():	
	labelRevOn = 'Toggle Reverse Front'
	labelRevOff = 'Toggle Reverse Back'
	revNrmls = mc.ls(sl=True, dag=True, lf=True)
	revState = mc.button('btn2', q=True, l=True)		
	if revState != labelRevOn:
		mc.button('btn2', e=True, l=labelRevOn, bgc=(0.2, 0.5, 1.0))
		for revNrm in revNrmls:
			mc.polyNormal(revNrm, nm=0,unm=0, ch=True)
	else:
		mc.button('btn2', e=True, l=labelRevOff, bgc=(0.24, 0.72, 0.46))
		for revNrm in revNrmls:
			mc.polyNormal(revNrm, nm=0,unm=0, ch=True)	
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - T O G G L E  W I R E / S H A D E D -  - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def wireOrShade():
	labelWireOn = 'Wireframe ON'
	labelWireOff = 'Shading ON'
	getWireShade = mc.ls(sl=True, dag=True, lf=True)
	wireState = mc.button('btn3', q=True, l=True)
	if wireState != labelWireOn:
		mc.button('btn3', e=True, l=labelWireOn, bgc=(0.2, 0.5, 1.0))
		for wireItem in getWireShade:
			mc.setAttr(wireItem + '.overrideEnabled', 1)
			mc.setAttr(wireItem + '.overrideShading', 0)
	else:
		mc.button('btn3', e=True, l=labelWireOff, bgc=(0.24, 0.72, 0.46))
		for wireItem in getWireShade:
			mc.setAttr(wireItem + '.overrideShading', 1)
			mc.setAttr(wireItem + '.overrideEnabled', 0)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - T O G G L E  B O R D E R  E D G E-  - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -	
def toggleBorderEdge():
	labelBorderOn = 'Border ON'
	labelBorderOff = 'Border OFF'
	getBorderState = mc.ls(sl=True, dag=True, lf=True)
	borderState = mc.button('btn4', q=True, l=True)
	if borderState != labelBorderOn:
		mc.button('btn4', e=True, l=labelBorderOn, bgc=(0.2, 0.5, 1.0))
		for border in getBorderState:
			mc.setAttr(border + '.displayBorders', 1)
			mc.setAttr(border + '.borderWidth', 5)
	else:
		mc.button('btn4', e=True, l=labelBorderOff, bgc=(0.24, 0.72, 0.46))
		for border in getBorderState:
			mc.setAttr(border + '.borderWidth', 2)
			mc.setAttr(border + '.displayBorders', 0)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - T O G G L E  T E M P L A T E -  - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -		
def toggleCulling():
	labelCullOn = 'Backface Culling ON'
	labelCullOff = 'Backface Culling OFF'
	getCullState = mc.ls(sl=True, dag=True, lf=True)
	cullState = mc.button('btn5', q=True, l=True)	
	if cullState != labelCullOn:
		mc.button('btn5', e=True, l=labelCullOn, bgc=(0.2, 0.5, 1.0))
		for cullItm in getCullState:
			mc.setAttr(cullItm + '.backfaceCulling', 3)			
	else:
		mc.button('btn5', e=True, l=labelCullOff, bgc=(0.24, 0.72, 0.46))
		for cullItm in getCullState:
			mc.setAttr(cullItm + '.backfaceCulling', 0)	
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - T O G G L E  T E M P L A T E -  - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def toggleTemplate():
	labelTempOn = 'Template ON'
	labelTempOff = 'Template OFF'
	getTempState = mc.ls(sl=True, dag=True, lf=True)
	tempState = mc.button('btn6', q=True, l=True)	
	if tempState != labelTempOn:
		mc.button('btn6', e=True, l=labelTempOn, bgc=(0.2, 0.5, 1.0))
		for tmplte in getTempState:
			mc.setAttr(tmplte + '.template', 1)			
	else:
		mc.button('btn6', e=True, l=labelTempOff, bgc=(0.24, 0.72, 0.46))
		for tmplte in getTempState:
			mc.setAttr(tmplte + '.template', 0)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - T O G G L E  B O U N D I N G  B O X -  - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def toggleBB():
	labelBBOn = 'Bounding Box ON'
	labelBBOff = 'Bounding Box OFF'
	getBBState = mc.ls(sl=True, dag=True, lf=True)
	BBState = mc.button('btn7', q=True, l=True)	
	if BBState != labelBBOn:
		mc.button('btn7', e=True, l=labelBBOn, bgc=(0.2, 0.5, 1.0))
		for bb in getBBState:
			mc.setAttr(bb + '.overrideEnabled', 1)
			mc.setAttr(bb + '.overrideLevelOfDetail', 1)			
	else:
		mc.button('btn7', e=True, l=labelBBOff, bgc=(0.24, 0.72, 0.46))
		for bb in getBBState:
			mc.setAttr(bb + '.overrideLevelOfDetail', 0)
			mc.setAttr(bb + '.overrideEnabled', 0)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - T O G G L E  V E R T I C E S -  - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def toggleVert():
	labelVertOn = 'Vertices ON'
	labelVertOff = 'Vertices OFF'
	getVertState = mc.ls(sl=True, dag=True, lf=True)
	vertState = mc.button('btn8', q=True, l=True)	
	if vertState != labelVertOn:
		mc.button('btn8', e=True, l=labelVertOn, bgc=(0.2, 0.5, 1.0))
		for vert in getVertState:
			mc.setAttr(vert + '.displayVertices', 1)			
	else:
		mc.button('btn8', e=True, l=labelVertOff, bgc=(0.24, 0.72, 0.46))
		for vert in getVertState:
			mc.setAttr(vert + '.displayVertices', 0)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - M O V E  P I V O T -  - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def movePivot():
	labelPivotOn = 'Pivot Moved to Base'
	labelPivotOff = 'Pivot Centered'
	getPivState = mc.ls(sl=True, tr=True)
	pivotState = mc.button('btn9', q=True, l=True)	
	if pivotState != labelPivotOn:
		mc.button('btn9', e=True, l=labelPivotOn, bgc=(0.2, 0.5, 1.0))
		for piv in getPivState:
			BBBox = mc.xform(piv, ws=True, q=True, bb=True)		
			xAxis = ((BBBox[0] + BBBox[3])/2)	
			zAxis = ((BBBox[2] + BBBox[5])/2)	
			mc.xform( piv, ws=True, piv=(xAxis,BBBox[1],zAxis))				
	else:
		mc.button('btn9', e=True, l=labelPivotOff, bgc=(0.24, 0.72, 0.46))
		for piv in getPivState:
			mc.xform(piv, cp=True)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - T O G G L E  X - R A Y (s) -  - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def xRayActiveObj():
	labelXRayOn = 'Active Obj(s) XRay ON'
	labelXRayOff = 'Active Obj(s) XRay OFF'
	getXrayState = mc.ls(sl=True, tr=True)
	xRayState = mc.button('btn10', q=True, l=True)
	if xRayState != labelXRayOn:
		mc.button('btn10', e=True, l=labelXRayOn, bgc=(0.2, 0.5, 1.0))
		for xRay in getXrayState:
			mc.displaySurface(x=True)
	else:
		mc.button('btn10', e=True, l=labelXRayOff, bgc=(0.24, 0.72, 0.46))
		for xRay in getXrayState:
			mc.displaySurface(x=False)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - T O G G L E  T R I S -  - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def toggleTris():
	mc.selectMode(o=True)
	labelTrisOn = 'Tri(s) Are Selected'
	labelTrisOff = 'Tri(s) Are Unselected'
	labelTrisDef = 'Toggle Tri(s)'
	getTrisState = mc.ls(sl=True, tr=True)
	trisState = mc.button('btn11', q=True, l=True)	
	if trisState != labelTrisOn:
		mc.button( 'btn11', e=True, l=labelTrisOn, bgc=(0.2, 0.5, 1.0))
		for tris in getTrisState:
			if len(tris):
				mc.selectMode(co=True)
				mc.selectType(smp=False, sme=True, smf=False, smu=False, pv=False, pe=True, pf=False, puv=False)
				mc.polySelectConstraint( m=3, type=0x0008, size=1)
				mc.polySelectConstraint(disable=True)
				getTriFaces = mc.polyEvaluate(fc=True)
				print('You have %i triangle(s) in your mesh' % (getTriFaces))
			else:
				print('Please select a polygonal object')
	else:
		mc.button('btn11', e=True, l=labelTrisOff, bgc=(0.24, 0.72, 0.46))		
		for tris in getTrisState:
			mc.select(tris, r=True)			
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - T O G G L E  N - G O N (s) - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def toggleNGons():
	mc.selectMode(o=True)
	labelNGonOn = 'NGon(s) Are Selected'
	labelNGonOff = 'NGon(s) Are Unselected'	
	getNgonsState = mc.ls(sl=True, tr=True)
	nGonState = mc.button('btn12', q=True, l=True)
	if nGonState != labelNGonOn:
		mc.button('btn12', e=True, l=labelNGonOn, bgc=(0.2, 0.5, 1.0))
		for ngon in getNgonsState:
			if len(ngon):				
				mc.selectMode(co=True)
				mc.selectType(smp=False, sme=True, smf=False, smu=False, pv=False, pe=True, pf=False, puv=False)
				mc.polySelectConstraint( m=3, type=0x0008, size=3)
				mc.polySelectConstraint(disable=True)
				getNgonFaces = mc.polyEvaluate(fc=True)
				print('You have %i NGons(s) in your mesh' % (getNgonFaces))
			else:
				print('Please select a polygonal object')

	else:
		mc.button('btn12', e=True, l=labelNGonOff, bgc=(0.24, 0.72, 0.46))		
		for ngon in getNgonsState:
			mc.select(ngon, r=True)
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - - - - T O G G L E  U I - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def toggleStuff():

	if (mc.window("toggle_Win", exists=True)):
		mc.deleteUI("toggle_Win", wnd=True)
		mc.windowPref("toggle_Win", r=True)

	# C R E A T E  U I
	mc.window("toggle_Win", s=False, tlb=True, rtf=True, t="Toggling Tools")
	mc.columnLayout(adj=True)

	# L I S T  S E L E C T E D  C U R V E S
	mc.frameLayout(l="To Use Select Poly Obj in Obj Mode", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
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
	mc.button('btn10',l='Toggle X-Ray',bgc=(0.24, 0.72, 0.46), c='xRayActiveObj()')
	mc.button('btn11',l='Toggle Tri(s)',bgc=(0.24, 0.72, 0.46), c='toggleTris()')
	mc.button('btn12',l='Toggle N-Gons',bgc=(0.24, 0.72, 0.46), c='toggleNGons()')	
	mc.setParent('..')
	mc.setParent('..')

	# S H O W  W I N D O W
	mc.showWindow("toggle_Win")

toggleStuff()