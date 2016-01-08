import wrap

# 1. Loading Basemesh
print "Loading basemesh..."
basemeshFileName = wrap.openFileDialog("Select Basemesh",filter = "OBJ-file (*.obj)",dir = wrap.demoModelsPath)
basemesh = wrap.Geom(basemeshFileName)
print "OK"

# 2. Loading Scan
print "Loading scan..."
scanFileName = wrap.openFileDialog("Select Scan",filter = "OBJ-file (*.obj)",dir = wrap.demoModelsPath)
scaleFactor = 1000
scan = wrap.Geom(scanFileName,scaleFactor = scaleFactor)
scan.wireframe = False
print "OK"

print "Loading texture..."
textureFileName = wrap.openFileDialog("Select Scan\'s Texture",filter = "Image (*.jpg *.png *.bmp *.tga)",dir = wrap.demoModelsPath)
if textureFileName is not None:
    scan.texture = wrap.Image(textureFileName)
    scan.texture.show()
    print "OK"
else:
    print "No texture set"



# 3. Rigid Alignment
print "Rigid alignment..."
(pointsScan, pointsBasemesh) = wrap.selectPoints(scan,basemesh)
rigidTransformation = wrap.rigidAlignment(basemesh,pointsBasemesh,scan,pointsScan,matchScale = True)
basemesh.transform(rigidTransformation)
basemesh.fitToView()
print "OK"

# 4. Non-rigid Registration
print "Non-rigid Registration..."
(controlPointsScan,controlPointsBasemesh) = wrap.selectPoints(scan,basemesh)
freePolygonsBasemesh = wrap.selectPolygons(basemesh)
basemesh = wrap.nonRigidRegistration(basemesh,scan,controlPointsBasemesh,controlPointsScan,freePolygonsBasemesh,minNodes = 15,initialRadiusMultiplier = 1.0,smoothnessFinal = 0.1,maxIterations = 20)
print "OK"


# 8. Saving Result
print "Saving result..."
fileName = wrap.saveFileDialog("Save resulting model",filter = "OBJ-file (*.obj)")
basemesh.save(fileName,scaleFactor = 1.0 / scaleFactor)
if scan.texture is not None:
    textureFileName = wrap.saveFileDialog("Save resulting texture",filter = "Image (*.jpg *.png *.bmp *.tga)")
    basemesh.texture.save(textureFileName)
print "OK"
