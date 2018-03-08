import maya.cmds as mc
from functools import partial
import math

uMax = 1
vMax = 1
outputDir = ''
imageFormat = ''
amount = 0.0
maxUval = 0
maxVval = 0

def exportUDIM():
	
	global uMax	
	global vMax
	global amount
	global outputDir
	global maxUval
	global maxVval
	cntu = 1	
	
	getObjUVsName = mc.textScrollList('getUDIMObj', q=True, ai=True)	
	for polySel in getObjUVsName:
		amount=0.0
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		UDIM = 1
		polyShp = mc.listRelatives(polySel, ni=True, s=True)
		if mc.nodeType(polyShp) == 'mesh':
			getUVTiles()
			uMax = maxUval		
			vMax = maxVval			
			imageFormat = mc.optionMenu( 'imgFormat', q=True, value=True)
			onek = mc.checkBox( 'uvRes1', q=True, v=True)
			twok = mc.checkBox( 'uvRes2', q=True,v=True)
			fourk = mc.checkBox( 'uvRes3', q=True, v=True)
			eightk = mc.checkBox( 'uvRes4', q=True, v=True)
			
			if onek == True:
				uvRes = 1024
			elif twok == True:
				uvRes = 2048
			elif fourk == True:
				uvRes = 4096
			elif eightk == True:
				uvRes = 8192
			else:
				mc.error( 'Select a UV resolution')	
			
			totalUDIM = float(uMax * vMax)
		
			for incv in range(vMax): #Check the U & V
				UDIM = UDIM + 1000
				r=0
				for incu in range(uMax):
					print incu, incv
					dirUVOutput = (outputDir + polySel + '_UV.' + str(UDIM+r) + '.' + imageFormat)
					mc.uvSnapshot(polySel, aa=True, umn=incu, umx=incu, vmn=incv, vmx=incv, n=(dirUVOutput), xr=uvRes, yr=uvRes, r=0, g=0, b=0, o=True, ff=imageFormat)			
					mc.progressBar('progBar', e=True, pr=amount, st='working')			
					amount=((cntu/totalUDIM)*100)
					r+=1
					cntu+=1
								
			amount=100
			mc.progressBar('progBar', e=True, pr=amount, st='working')
		else:
			mc.error( 'Current selection is not a polygonal mesh')
		amount=0
		mc.progressBar('progBar', e=True, pr=amount, st='working')	
	
def setOutputDir():

	global outputDir    
    	#User sets the source directory
	getOutDir = mc.fileDialog2(cap = 'Set The Output Directory', ds = 2, fm = 3, okc = "Set Directory")
	outputDir = getOutDir[0] + '/'    
	mc.textScrollList("setDirOutput", e=True, ra=True)	
	mc.textScrollList("setDirOutput", e=True, a=(outputDir))

def chckBxs(button,*args):

	mc.checkBox('uvRes1', e=True, v=False)
	mc.checkBox('uvRes2', e=True, v=False)
	mc.checkBox('uvRes3', e=True, v=False)
	mc.checkBox('uvRes4', e=True, v=False)
	mc.checkBox(button, e=True, v=True)

def getUDIMObjs():	
	
	getSrcObjs = mc.ls(sl=True, tr=True)
	getSrcShp = mc.listRelatives(s=True)
	mc.textScrollList('getUDIMObj', e=True, ra=True)	
	for i in getSrcObjs:
		mc.textScrollList('getUDIMObj', e=True, a=(i))
	

def getUVTiles():
	global maxUval
	global maxVval
	uTest = 0
	vTest = 0
	maxUval = 0
	maxVval = 0
	mel.eval('ConvertSelectionToUVs;')
	getauv = mc.ls(sl=True, fl=True)
	for uv in getauv:	
		uvPos = cmds.polyEditUV(uv, q=1)	
		uTest = int(math.ceil(uvPos[0]))
		vTest = int(math.ceil(uvPos[1]))
		if uTest > maxUval:
			maxUval=uTest
		if vTest > maxVval:
			maxVval=vTest
	mc.select(cl=True)	
	print('There are %i U tiles and %i V tiles in this mesh' % (maxUval, maxVval))

#--------------------------------------------------------------------------------------------------------

def multiUDIMGui():
	
	if (mc.window("UDIM_Win", exists=True)):
		mc.deleteUI("UDIM_Win", wnd=True)
		mc.windowPref("UDIM_Win", r=True)

	# C R E A T E  U I
	mc.window("UDIM_Win", s=False, tlb=True, rtf=True, t="UDIM Snapshot")
	mc.columnLayout(adj=True)

	# L I S T  S E L E C T E D  C U R V E S
	mc.frameLayout(l="UV name derived from object name", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.button(l='Set Output Directory',bgc=(0.24, 0.72, 0.46), c='setOutputDir()')
	mc.textScrollList('setDirOutput', h=30, ams=False)
	
	mc.setParent('..')
	mc.setParent('..')
	

	# U D I M  M I N & M A X
	
	mc.frameLayout(l="UDIM Obj Export Selection", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.button(label="Select UV Export",bgc=(0.24, 0.72, 0.46), c =lambda *x:getUDIMObjs() , h = 30 )	
	mc.textScrollList('getUDIMObj', h=60, ams=False)
	mc.setParent('..')
	mc.setParent('..')

	# U V  R E S O L U T I O N
	mc.frameLayout(l="UV Resolution", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 10)
	mc.columnLayout(adj=True)
	mc.rowLayout(nc=4, cw4=(50,50,50,50))
	mc.checkBox('uvRes1', label='1k', onc=partial(chckBxs,'uvRes1'))
	mc.checkBox('uvRes2', label='2k', v=True, onc=partial(chckBxs,'uvRes2'))
	mc.checkBox('uvRes3', label='4k', onc=partial(chckBxs,'uvRes3'))
	mc.checkBox('uvRes4', label='8k', onc=partial(chckBxs,'uvRes4'))

	mc.setParent('..')
	mc.setParent('..')	
	
	# I M A G E  O U T P U T 
	mc.frameLayout( l="Image Format", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.optionMenu('imgFormat', label='Image Format' )
	mc.menuItem(label = 'png')
	mc.menuItem(label = 'iff')
	mc.menuItem(label = 'sgi') 
	mc.menuItem(label = 'tif') 
	mc.menuItem(label = 'als') 
	mc.menuItem(label = 'gif') 
	mc.menuItem(label = 'rla')
	mc.menuItem(label = 'jpg')	
	
	mc.setParent('..')
	mc.setParent('..')
	
	# E X P O R T  U D I M/s
	mc.button(label="Export UDIM/s", bgc=(0.24, 0.72, 0.46), c=lambda *x:exportUDIM(), h = 40 )
	progressControl = mc.progressBar( 'progBar', pr=amount, width=195, st='working')
	
	mc.setParent('..')
	mc.setParent('..')

	# S H O W  W I N D O W
	mc.showWindow("UDIM_Win")



multiUDIMGui()
