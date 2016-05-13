# 256 pipeline tools
# ANIMATION MANAGER 2.0
# NO FTRACK EDITION

import pymel.core as pm
import os, sys, glob
from datetime import datetime
from setupProject import *
import dnaCore as dna
reload(dna)

listLens = [12, 18, 27, 40, 65, 75, 100, 135, 180]
version = 1
frameStart = 101

def buildName(version, type):
    filePath = '{0}{1}/{2}/SHOT_{3}/{4}/'.format(rootPB, codePart, codeSequence, codeShot, prefix)    
    if type == 'mov':
        fileName = '{3}_E{0}_S{1}_{2}_'.format(codeSequence, codeShot, codeVersion, prefix)    
    elif type == 'jpg':
        fileName = 'E{0}_S{1}_'.format(codeSequence, codeShot)    
    version = '{0:03d}'.format(version)
    extension = '.{}'.format(type)
    fileNameFull = filePath + fileName + version + extension
    fileName = fileName + version + extension
    return fileNameFull, fileName
       
def getVersions(fileNameFull, type): # Get 1 version as input <<  fileNameFull  >>  <'P:/TANNER/PROD/RENDER_3D/BLAST/REEL_01/000/SHOT_010/E000_S010_001.mov'> Output last existing version
    # split fullName into parts
    buildName(version, type)
    dataFileName = dna.fileActs(fileNameFull) 
    # get latest version   
    listExisted = glob.glob(dataFileName['fileDirPath'] + dataFileName['fileNameNoVer'] + '*.{}'.format(type))  
    listVersions = []
    for i in listExisted:
        v = i.split('\\')[-1].split('.{}'.format(type))[0].split('_')[-1]
        listVersions.append(v)   
    versionLast = int(max(listVersions))# create number for latest version     
    return versionLast

# EXTRACT DATA FROM FILE NAME
fileNameFull = pm.sceneName()
if fileNameFull:
    dataShotSC = dna.analizeShotSC()
    fileName = dataShotSC['fileName']
    codePart = dataShotSC['codePart']
    codeSequence = dataShotSC['codeSequence'] 
    codeShot = dataShotSC['codeShot']
    codeVersion = dataShotSC['codeVersion']
    frameEnd = dataShotSC['scn_END']
    # Get file PREFIX
    if fileName.split('_')[0] == 'ANM':
        prefix = 'ANM'
    else:
        prefix = fileName.split('_')[0]


def dataFrame(): # Output headUpDisplay information about shot
    user = os.getenv('USERNAME')
    reel = codePart
    seq = codeSequence
    shot = codeShot
    frames = int( frameEnd - 100 )
    frame = int( pm.currentTime( query = True ) )
    out = '[ {0}:E{1}:S{2} ]  Frame:{3:04d}  ({4:04d}) by: {5}'.format(reel, seq, shot, frame, frames, user)
    return out
    
def writePB(fileNameFull, type):
    if type == 'mov':
        # Turn ON HUD
        pm.headsUpDisplay( rp = ( 6 , 1 ) ) # Delete HUD if exists by position
        hud = pm.headsUpDisplay ( 'HUD', section = 6, block = 1, blockSize = 'medium', label = codeProject.upper(), labelFontSize='large', command = dataFrame, attachToRefresh = True)
        if  pm.ls(type = 'audio') == []: # make PB without sound
            pm.playblast(format = 'qt', compression = 'Sorenson Video 3',showOrnaments = 1, quality = 100, percent = 100, f = fileNameFull, width = 999, height = 540, forceOverwrite = 1 ) 
        else: # make PB with sound
            audio = pm.ls(type = 'audio')[0]
            pm.playblast(format = 'qt', compression = 'Sorenson Video 3', s = audio, showOrnaments = 1, offScreen = 1, quality = 100, percent = 100, f = fileNameFull, width = 999, height = 540, forceOverwrite = 1 )
        print 'PLAYBLAST DONE: ' + str(fileNameFull)   
    elif type == 'jpg':
        pm.playblast(frame = pm.env.getTime(), format = 'image', compression = 'jpg', viewer = 0, showOrnaments = 0, quality = 100, percent = 100, completeFilename = fileNameFull, width = 999, height = 540, forceOverwrite = 1 )
        shot = ftrack.getShotFromPath([codeProject, codePart, codeSequence, 'SHOT_' + str(codeShot) ])
        thumbnail = shot.createThumbnail(fileNameFull)
        shot.setThumbnail(thumbnail)
        print 'SCREENSHOT SET IN FTRACK: ' + str(fileNameFull)
        
def PB(type): # create PLAYBLAST
    fileNameFull = buildName(version, type)[0]
    if not os.path.exists(fileNameFull):
        writePB(fileNameFull, type)
    else:       
        versionLast = getVersions(fileNameFull, type) # get last version
        # build name with LAST version
        fileNameFull, fileName =  buildName(versionLast, type)      
        confirm = pm.confirmDialog ( title = 'WARNING!', message = 'FILE:   ' + str(fileName) + '   EXISTS!' , button=['OVERWRITE', 'SAVE NEXT VERSION' ,'CANCEL'], defaultButton='OVERWRITE', cancelButton='CANCEL', dismissString='CANCEL' )
        if confirm == 'OVERWRITE':
            writePB(fileNameFull, type)
        elif confirm == 'SAVE NEXT VERSION':
            # build name with NEXT version
            fileNameFull =  buildName(versionLast + 1, type)[0]
            writePB(fileNameFull, type)   
        else:
           sys.exit()           
    
# LOCK ACTIVE CAMERA
def lockCam():
    view = pm.PyNode(pm.modelPanel(pm.getPanel(wf=True), q=True, cam=True))
    cam = pm.ls(view)[0]
    
    if (cam.tx.get(l=1) == 1):
            cam.translate.set(l = 0)
            cam.rotate.set(l = 0) 
    else:
            cam.translate.set(l = 1)
            cam.rotate.set(l = 1) 
def lens(focal):
    cam = pm.PyNode('E{0}_S{1}Shape'.format(codeSequence,codeShot))
    cam.horizontalFilmAperture.set(0.825)
    cam.verticalFilmAperture.set(0.446)
    cam.focalLength.set(focal)

def saveNext():
    dna.SNV()

def publishANM(): # PUBLISH ANM DATA TO FTRACK
    dna.addMetaShot ('ANM', fileName, codePart, codeSequence, codeShot) # Publish animation FILE to FTrack
    note = 'PUBLISHED ANM: {0}'.format(fileName)
    dna.addNoteShot(codePart, codeSequence, codeShot, 'Animation', note) # Add NOTE to ANIMATION task


def baseUI(*args):
    
    if pm.window('ANMManager', q = 1, ex = 1):
        pm.deleteUI('ANMManager')
    win = pm.window('ANMManager', t= 'Animation manager', rtf=True, w = 280 )
    with win:
        mainLayout = pm.columnLayout() 
        
        inputLayout = pm.rowColumnLayout(nc=6, parent = mainLayout) 
        pm.text (l = '  PART  ')
        partField = pm.textField(tx = 'REEL_01', w= 60, h = 30)
        pm.text (l = '    SEQ ')
        sequenceField = pm.textField(tx = '010', w= 45, h = 30)
        pm.text (l = '    SHOT ')
        shotField = pm.textField(tx = '010', w= 45, h = 30)
        pm.separator(h = 5 , style = 'none')        
        createLayout = pm.rowColumnLayout(nc = 1, parent = mainLayout) 
        OPANM = pm.button(l = 'OPEN ANIMATION SCENE', w = 280, h = 35)
        OPANM.setCommand(pm.Callback (dna.shotOpen, partField, sequenceField, shotField, listANM ))
        pm.separator(h = 6 , style = 'none')  
                           
        PBLayout = pm.rowColumnLayout(nc = 1, parent = mainLayout) 
        playblast = pm.button(l = 'PLAYBLAST', w = 280, h= 50)       
        playblast.setCommand(pm.Callback (PB, 'mov'))
        pm.separator(h = 5, style = 'none')
        
        camLayout = pm.rowColumnLayout(nc = 10, parent = mainLayout) # 12, 18, 27, 40, 65, 75, 100, 135, 180
        for i in listLens:
            LB = pm.button(l = str(i), w = 25, h= 40)
            LB.setCommand(pm.Callback (lens, i))
        lockCAM = pm.button(l = 'LCM', w = 55)
        lockCAM.setCommand(pm.Callback (lockCam))
        pm.separator(h = 8, style = 'none')
        
        editLayout = pm.rowColumnLayout(nc = 1, parent = mainLayout) 
        check =  pm.button(l = 'CHECK SCENE', w = 280, h= 45)
        check.setCommand(pm.Callback (dna.checkScene))
        
        addLayout = pm.rowColumnLayout(nc = 3, parent = mainLayout)
        add_A = pm.button(l = 'ADD ASSSETS', w = 90, h= 30)
        del_A = pm.button(l = 'DEL ASSETS', w = 90)
        upd = pm.button(l = 'UPDATE REFS', w = 100)
        add_A.setCommand(pm.Callback (dna.addAsset))
        del_A.setCommand(pm.Callback (dna.delAsset))
        upd.setCommand(pm.Callback (dna.updateRefs))       
        updLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout)
        fixALL = pm.button(l = 'FIX ALL', w = 240, h = 30)
        snv =    pm.button(l = 'SNV', w = 40)
        fixALL.setCommand(pm.Callback (dna.fixAll))
        snv.setCommand(pm.Callback (saveNext))
   
    win.show()    

baseUI()
