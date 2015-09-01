import maya.cmds as mc 
import os, os.path 
import fnmatch 
import shutil
	
'''	
------------------------------------------ HOW THE SCRIPT WORKS --------------------------------------------------------
THERE ARE TWO DIFFERENT FUNCTIONS OF THIS SCRIPT. THE FIRST IS TO COPY ALL FILES FROM ONE FOLDER TO ANOTHER, THE SECOND
IS TO RE-LINK THE COPIED IMAGES TO THE	TEXTURES THAT RESIDE IN	OUR	HYPERSHADE.	IN ORDER TO COPY YOU NEED A SOURCE AND
DESTINATION DIRECTORY THE HIT RUN. A PROGRESS BAR WILL APPEAR AND YOU'LL BEGIN TO SEE FILES COPIED TO YOUR DESTINATION
DIRECTORY. IF YOUR IMAGES ARE ALREADY IN THE CORRECT FOLDER BUT JUST NEED TO BE UPDATED TO THE PROJECTS RELATIVE
PATH WITHIN SOURCEIMAGES THEN USE THE DESTINATION DIRECTORY TO SET THE PATH FOR THE CONVERSION. ONCE SET JUST HIT THE
CONVERSION BUTTON AND THE IMAGES NAME WILL BE RETAINED BUT WITH THE PATH TO THE FOLDER YOU SELECTED.

To Run copy and run in python command line: transferFiles()
'''

getSrcDir = ""
getDesDir = ""

def transferFiles():
    
    # build Ul
    windowName = 'DirectoryFix' 
    windowTitle = 'Directory Fixer v_0.1'
    
    if mc.window(windowName, exists=True):
        mc.deleteUI(windowName, window=True)
        
    mc.window(windowName, title=windowTitle, rtf=True, s=False, w=450, h=215)
    
    form = mc.formLayout(numberOfDivisions=100)    
    #The text	 Left side of column 	
    selSource = mc.text(l='Select source Directory')
    sourceDir = mc.text(l='Source Directory') 
    selDestination = mc.text(l='Select Destination Directory')
    desDir = mc.text(l='Destination Directory')
    copyToFrom = mc.text(align="left",l='Copy files from source to \ndestination directory')
    convert2Rel = mc.text(l='Convert file path to relative')
    #The functional!ity	 Right side of column 	
    broSourceDir = mc.button(w=150,l='Browse Source Directory', c='getSrcDirectory()')
    dirText = mc.textFieldGrp('obj1', l="", text = '', editable = False)
    broDesDir = mc.button(w=150, l='Browse Destination Directory', c='getDesDirectory()')
    sourceText = mc.textFieldGrp('obj2',	l="",	text = "", editable = False)
    copyNowBTN = mc.button(w=150,l='copy Files over!', c='copyFileNewDir()')
    convertNowBTN = mc.button(w=150,l='Run Conversion Now!', c='changeFileDir()')
    
    aFormLayout = mc.formLayout(form, edit=True,
    
    attachForm=[(selSource, 'top', 5),(selSource, 'left', 5),(sourceDir, 'left', 5),(broSourceDir, 'left', 50), (broSourceDir, 'top', 5), (selDestination, 'left',
    5),(desDir, 'left', 5),(copyToFrom, 'left', 5),(convert2Rel, 'left', 5), (broSourceDir, 'left', 158),(dirText, 'left', 15),(sourceText, 'left',
    15),(broDesDir, 'left', 158),(copyNowBTN, 'left', 158),(convertNowBTN, 'left',158)],    
    
    attachControl=[(sourceDir, 'top', 18, selSource),(dirText, 'top', 5, broSourceDir),(selDestination, 'top', 15, sourceDir), (broDesDir, 'top', 5, dirText), (sourceText, 'top', 5, broDesDir), (dirText, 'top', 5, broSourceDir),(desDir, 'top', 18, selDestination),
    (copyToFrom, 'top', 25, desDir), (convert2Rel, 'top', 15, copyToFrom), (copyNowBTN, 'top', 25, sourceText), (convertNowBTN, 'top', 10, copyNowBTN)])
    
    mc.showWindow(windowName)
#_______________________________________GET SOURCE DIRECTORY_____________________________________________________

def getSrcDirectory():
    global getSrcDir
    #User sets the source directory
    getSrcDir = mc.fileDialog2(cap = 'Set The Source Directory', ds = 2, fm = 3, okc = "Set Directory")
    txtSrcDir = getSrcDir[0]
    mc.textFieldGrp('obj1', l='', e=True, text=txtSrcDir)
    #print getSrcDir
    
#_______________________________________GET DESTINATION DIRECTORY_________________________________________________
def getDesDirectory():
    global getDesDir
    #user sets the destination directory
    getDesDir = mc.fileDialog2(cap = 'Set The Destination Directory', ds = 2, fm = 3, okc = "Set Directory")
    txtDesDir = getDesDir[0]
    mc.textFieldGrp('obj2', l='', e=True, text = txtDesDir) 
    #print getDesDir


#___________________________________SORT THE FILES RELATIVE PATH IN MAYA_______________________________
def changeFileDir():
    if getDesDir == '':
        mc.warning("You need to set the destination directory in order to fix the absolute path.")
    else:
        print getDesDir 
        relativePath = ""
        getImageFileName = mc.ls(type = 'file')
        #getDesDir = mc.fileDialog2(cap = 'Set The image Path Directory', ds =2, fm = 3, okc = "Set Directory") 
        blah = getDesDir[0]
        split_pn = getDesDir[0].split("/")
        index = split_pn.index("sourceimages")
        relativePath = os.sep.join(split_pn[index:])
        howmany = len(fnmatch.filter(os.listdir(blah), '*png'))
        line = "\\"
        output = relativePath + line
        #we need the user to tell us where the new images are and then figure out if there are any images in the folder.
        for xFile in getImageFileName:
            getFileDir = mc.getAttr(xFile + '.fileTextureName') 
            thesplit = getFileDir.split('/')
            last = (len(thesplit) - 1) 
            print thesplit[last]
            newRelativeDir = output + thesplit[last]
            mc.setAttr(xFile + '.fileTextureName', newRelativeDir, type= 'string')
        print('The script has just updated all %s image connections' % str(howmany))


#___________________________________SORT THE FILES RELATIVE PATH IN MAYA_______________________________
def copyFileNewDir():
    
    sourceDir = getSrcDir[0] 
    destination = getDesDir[0]
    
    pngAmount = len(fnmatch.filter(os.listdir(sourceDir), '*png'))
    tifAmount = len(fnmatch.filter(os.listdir(sourceDir), '*tif'))
    jpgAmount = len(fnmatch.filter(os.listdir(sourceDir), '*jpg'))
    tgaAmount = len(fnmatch.filter(os.listdir(sourceDir), '*tga'))
    hdrAmount = len(fnmatch.filter(os.listdir(sourceDir), '*hdr'))
    fileAmount = pngAmount + tifAmount + jpgAmount + tgaAmount + hdrAmount
    
    
    windowProgName = 'progwindow'   
    windowTitle = 'Directory Fixer'
        
    if mc.window(windowProgName, exists=True):    
        mc.deleteUI(windowProgName, window=True)
    
    progwindow = mc.window(windowProgName, t=windowTitle, rtf=True, s=False)
    mc.columnLayout()
    mc.text(l="Copying Files")
    progressControl = mc.progressBar(maxValue=fileAmount, width=300, h=50)
    mc.showWindow(windowProgName)
    j=0
    i=1
    for xfile in os.listdir(sourceDir):
        for extensions in ('*jpg', '*png', '*tif', '*tga', '*hdr',):               
            if fnmatch.fnmatch(xfile, extensions):
        
                src_file = os.path.join(sourceDir, xfile)
                des_file = os.path.join(destination, xfile)            
                shutil.copy2(src_file, des_file)
                j += i            
                mc.progressBar(progressControl, edit=True, pr=j)
    
    mc.deleteUI(windowProgName)    
    print 'you have copied %i files to %s, %i tif files, %i png files, %i jpg files, %i tga files and %i hdr files' % (fileAmount, destination, tifAmount, pngAmount, jpgAmount, tgeAmount, hdrAmount)