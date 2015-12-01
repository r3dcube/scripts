import maya.cmds as mc
import math

rndDwnCurveLength = math.trunc(mc.arclen("curve1"))
getSpans = mc.getAttr("curve1" + ".spans")
getDegree = mc.getAttr("curve1" + ".degree")
CVTotalOnCurve = getSpans + getDegree
rndDwnIncrement = int(rndDwnCurveLength / CVTotalOnCurve)

def create_array(CVTotalOnCurve):
    return [[0,0,x] for x in range(0, CVTotalOnCurve * rndDwnIncrement, rndDwnIncrement)]

curvePoints = create_array(CVTotalOnCurve)
curveName = "partiCurve" + str("0_1")
curveObj = mc.curve(name = curveName, ws=True, p =curvePoints)

'''
You will need to look at the math of the curve as it needs to increment by the float so it's not an int
'''

newCylinder = mc.polyCylinder(name="tubePoly_0", ch=True, r=.25, ax=[0,0,90], sh=rndDwnCurveLength, h=rndDwnCurveLength/2)
latDeformer = mc.lattice(newCylinder[0], n=('lattice'+ newCylinder[0]), dv=[2,2,2], oc=True, ldv=[2,2,2])
mc.select(latDeformer[1] + ".pt" + "[0:1][0:1][1]")
tempClusterA = mc.cluster( n="tempClusterA")
mc.select(latDeformer[1] + ".pt" + "[0:1][0:1][0]")
tempClusterB = mc.cluster(n="tempClusterB")


getClusterWS = mc.xform(tempClusterA[1], ws=True, q=True, translation=True)
getCurveLastCV = mc.xform(curveObj + ".cv[" + str(CVTotalOnCurve-1) + "]", ws=True, q=True, translation=True)
mc.xform(tempClusterA, t=(getCurveLastCV[0], getCurveLastCV[1], getCurveLastCV[2]))
#mc.move(0,0,(CVTotalOnCurve * rndDwnIncrement/2) ,newCylinder, r=True)

latDeformer = mc.lattice(newCylinder[0], n=('lattice'+ newCylinder[0]), dv=[2,2,2], oc=True, ldv=[2,2,2])
mc.select(latDeformer[1] + ".pt" + "[0:1][0:1][0]")
mc.cluster()
mc.select(latDeformer[1] + ".pt" + "[0:1][0:1][1]")
mc.cluster()

mc.wire( curveObj, newCylinder[0], gw=False, ce=0, en=1, li=0)
mc.wire(curveObj, e=True, w=curveObj)

for indCV in range(0,CVTotalOnCurve):    
    
    getCurveCVPos = mc.xform("curve1" + ".cv[" + str(indCV) + "]", ws=True, q=True, translation=True)
    mc.xform(curveObj + ".cv[" + str(indCV) + "]", t=(getCurveCVPos[0], getCurveCVPos[1], getCurveCVPos[2]))
   