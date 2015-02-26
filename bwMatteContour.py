import maya.cmds as mc
import random

	
if mc.window("makeMatteWindowUI", exists=True):
		mc.deleteUI("makeMatteWindowUI")	
		
window = mc.window("makeMatteWindowUI",  mxb=False, s=0, title="Mattes & Countours 0.1")


mc.rowColumnLayout(nc=1, cw=[1,275], cal=[1,'left'])
mc.rowColumnLayout(nr=3, rh=[(1, 50), (2, 30), (3, 20)]
createMatteBtn = mc.button(label="Create Mattes", c="makeMattes()")
lineThickBtn = mc.button(label="Enable Contour/Change Line Thickness", c="lineThickness()", w=30)
queryLineValue = mc.floatSliderGrp(field=True, cat=(1,'left',1), min=0.0, max=5.0, value=1)	
	
mc.showWindow("makeMatteWindowUI")	

def makeMattes():
	allObjects = mc.ls( sl=True, o=True, dag=True, s=True)	
	lineThickness = mc.floatSliderGrp(queryLineValue, q=True, value=True)
	
	howManyObjs = len(allObjects)
	
	for obj in allObjects:
		#Get the current shader and engine so we can delete later	
		shadingGrps = mc.listConnections(obj,type='shadingEngine')
		currentShader = mc.ls(mc.listConnections(shadingGrps),materials=1)
		getLetters = (str(currentShader)[:9])
		#checking to see if there are any previously created SS on the objs.
		if (getLetters == "[u'SS_TTT"):
			print 'There is a surfaceshader connected'
			#assign lambert1 so the obj isnt void of a texture
			mc.select(obj)
			mc.hyperShade(assign='lambert1')
			lambertShader = mc.ls('*lambert1*')
			#after the assignment let's delete our old shaders and engines to keep our scene clean
			mc.delete(shadingGrps)
			mc.delete(currentShader)
			#everything is cleaned lets now add new surface shaders
			surfaceShade = mc.shadingNode('surfaceShader', asShader=True, name="SS_TTTexture")		
			red = random.random()
			green = random.random()
			blue = random.random()		
			mc.setAttr(surfaceShade + '.outColor', red, green, blue, type='double3')
			mc.select (obj)
			mc.hyperShade(assign= surfaceShade)
			
		else:
			#something other then our surface shaders are assigned, lets add 
			#lambert1 and then create new surface shaders
			print 'lets add new shaders'
			
			mc.select(obj)
			mc.hyperShade(assign='lambert1')
			#mc.hyperShade(obj, assign='lambert1')
				
			surfaceShade = mc.shadingNode('surfaceShader', asShader=True, name="SS_TTTexture")		
			red = random.random()
			green = random.random()
			blue = random.random()		
			mc.setAttr(surfaceShade + '.outColor', red, green, blue, type='double3')
			mc.select (obj)
			mc.hyperShade(assign= surfaceShade)
			
	mc.warning( 'Matte Creator has created %i new surface shaders' % howManyObjs)
			
		
def lineThickness():
	#print("you've done it")	
	lineThickness = mc.floatSliderGrp(queryLineValue, q=True, value=True)
	mc.select("SS_TTT*")
	getShdr = mc.ls(sl=True)
	#print(getShdr)
	for shdr in getShdr:
	
		shadingEng = mc.listConnections(shdr, type='shadingEngine')
		#print(shadingEng[0])
		mc.setAttr(shadingEng[0] + '.miContourEnable', 1)
		mc.setAttr(shadingEng[0] + '.miContourWidth', lineThickness)
	
	
	
	