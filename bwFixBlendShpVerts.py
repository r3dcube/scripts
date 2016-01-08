//Make verts match

import maya cmds as mc
"""
MAKE SURE THE TWO OBJECTS ARE ON TOP OF EACH OTHER AT THEIR ORGIN

SELECT THE BASE THEN THE TARGET TO FIX
"""
getObjs = mc.ls(sl=True, tr=True)
mc.setAttr(getObjs[0] + ".visibility", 0)


"""
SELECT THE VERTS ON THE BASE THAT NEED CORRECTED ON THE TARGET.
"""

getVerts = mc.ls(sl=True, fl=True )

for currentVert in getVerts:
	print currentVert
	vertNum = currentVert.split('.')
	
	getPos = mc.xform(getObjs[0] + "." + vertNum[1], ws=True, q=True, translation=True)	
	print getObjs[1] + "." + vertNum[1]
	mc.xform(getObjs[1] + "." + vertNum[1], t=(getPos[0], getPos[1], getPos[2]))