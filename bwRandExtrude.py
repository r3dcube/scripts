import maya.cmds as mc
import random

currentObjSel = mc.ls(sl=True, tr=True)
objFaceCnt = mc.polyEvaluate(currentObjSel, f=True)
print objFaceCnt

randnum = random.sample(xrange(0, objFaceCnt), (objFaceCnt))

for value in randnum:
	#print(value)
	
	currentFaceCnt = mc.polyEvaluate(currentObjSel, f=True) #used in the next for loop
	#print currentFaceCnt
	
	extRand = random.uniform(1,3)
	mc.select(currentObjSel[0] + '.f[' + str(value) + ']', r=True)
	mc.polyExtrudeFacet(ltz = extRand, d=2)
	
	for obj in range(1):
		
		newFaceCnt = mc.polyEvaluate(currentObjSel, f=True)
		getFace = newFaceCnt - currentFaceCnt
		print getFace