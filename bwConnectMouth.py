#the list below are for the inner mouth to connect with the outside head
import maya.cmds as mc
getObj = mc.ls( sl=True, tr=True)
#lips
listA = [1700,158, 159, 578, 623, 836,838,2070,2071,1445,1388,948,951,2142,2143,1947,1946,1446,154,153,157,156,155,1493,1495,1212,1210,1209,399,398,1980,1979,1864,1863,1701]
#mouth
listB = [3331,3318, 3316, 3317, 3321, 3322,3338,3339,3335,3328,3319,3320,3343,3344,3342,3336,3337,3315,3310,3311,3314,3312,3313,3329,3330,3325,3323,3324,3326,3327,3334,3341,3340,3333,3332]


#top to bottom	
for i in range(0, len(listA)):
	
	print listA[i]
	getPos = mc.xform(getObj[0] + ".vtx[" + str(listB[i]) + "]" , os=True, q=True, translation=True)	
	mc.xform(getObj[0] + ".vtx[" + str(listA[i]) + "]", t=(getPos[0], getPos[1], getPos[2]))
#bottom to top	
for i in range(0, len(listA)):
	
	print listA[i]
	getPos = mc.xform(getObj[0] + ".vtx[" + str(listA[i]) + "]" , os=True, q=True, translation=True)	
	mc.xform(getObj[0] + ".vtx[" + str(listB[i]) + "]", t=(getPos[0], getPos[1], getPos[2]))