# Animation DNA 2.0
# NO FTRACK EDITION
# <<  DNA CORE 2.0 >>

import pymel.core as pm
from datetime import datetime
import os, sys, json, glob
from setupProject import *

frameStart = 101
version = 1

print 'dnaCore [ projectRoot ]: {}'.format(projectRoot)

# INPUT FILE PATH MANIPULATION. 
def fileActs(filePath): # INPUT : Full file path. (P:/PIRATES/PROD/3D/scenes/ASSETS/CHARACTERS/HOKKINS/GEO/GEO_HOKKINS_001.mb)
    filePath = str(filePath)
    dataFileName = {} # create OUTPUT DIC
    print 'dnaCore.fileActs [ INPUT ]: {}'.format(filePath)
    # Disassemble path:
    fileBrunch = filePath.split('{}'.format(rootProd))[1].split('/')[0]
    if fileBrunch == '3D': # Brunches: PREPRODUCTION, 3D, COMP, EDIT and GRADING      
        filePhase = filePath.split(rootScene)[1].split('/')[0]
        if filePhase == 'ASSETS':
            assetType = filePath.split('{0}ASSETS/'.format(rootScene))[1].split('/')[0]
            dataFileName ['assetType'] = assetType.lower()
            if assetType.lower() == 'environments': # Define EDA
                rootEnv = '{0}{1}'.format(rootScene, envPath)
                if len(filePath.split(rootEnv)[1].split('/')) == 2:
                    dataFileName ['assetType'] = 'environments'
                elif len(filePath.split(rootEnv)[1].split('/')) == 4:
                    dataFileName ['assetType'] = 'eda'    
        elif filePhase == 'LOOKDEV':
            dataFileName ['assetType'] = 'MAT'         
    else:
        filePhase = 'UNKNOWN'  
        assetType = 'XXX'  
        print '<<  Unknown PHASE!  >>'
    fileExt = '.' + filePath.split('/')[-1].split('.')[1] # << .mb >>
    fileVresion = filePath.split('/')[-1].split('.')[0].split('_')[-1] # << 001 >>
    assetCat = filePath.split('/')[-3] # Get category of DYNAMIC PROPS
    fileNameFull = filePath.split('/')[-1] # << GEO_HOKKINS_001.mb >>
    filePrefix = fileNameFull.split('_')[0] # << GEO >>
    assetName = fileNameFull.split('{0}_'.format(filePrefix))[1].split('_{0}{1}'.format(fileVresion, fileExt))[0] # << HOKKINS >>
    fileNameNoVer = fileNameFull.split(fileExt)[0][:-3] # << GEO_HOKKINS_ >>
    fileDirPath = filePath.replace(fileNameFull, '') # get directory of file from path   
    dataFileName ['filePhase'] = filePhase
    dataFileName ['assetName'] = assetName
    dataFileName ['assetCat'] = assetCat
    dataFileName ['fileExt'] = fileExt
    dataFileName ['fileVresion'] = fileVresion
    dataFileName ['fileNameFull'] = fileNameFull
    dataFileName ['filePrefix'] = filePrefix  
    dataFileName ['fileNameNoVer'] = fileNameNoVer
    dataFileName ['fileDirPath'] = fileDirPath
    return dataFileName
# X = fileActs('F:/projects/FUTURAMA/PROD/3D/scenes/LOOKDEV/MATLIB/ASSETS/CHARACTERS/BENDER/MAT_BENDER_001.mb')

def export(fileNameFull, fileExt): # Export FILE (mb, ABC, ASS, XGen etc)
    if fileExt == 'mb':
        pm.saveAs(fileNameFull)
        pm.mel.addRecentFile (fileNameFull, "mayaBinary")

def exportFileLV( fileNameFull ): # Save LAST VERSION of INPUT file. Inputs(fileNameFull)
    print  'dna.exportFileLV [ INPUT FILE ]: {0}'.format(fileNameFull)
    # Analize FILE PATH
    fileParts = fileNameFull.split('/')
    fileName = fileParts.pop(-1)
    fileExt = fileName.split('.')[-1]
    fileVer = fileName.split('.')[0].split('_')[-1]
    fileNameNoVer = fileName.split('{0}.{1}'.format(fileVer, fileExt))[0]
    filePath = '' # Rebuild full path to a FILE
    for i in fileParts:
        filePath += i + '/' 
    # print filePath, fileNameNoVer, fileVer, fileExt
    if os.path.exists(fileNameFull): # IF FILE EXISTS 
        listExisted = glob.glob('{0}{1}*.{2}'.format(filePath, fileNameNoVer, fileExt ))
        listVersions = []
        for i in listExisted:
            version = i.split('\\')[-1].split('.{}'.format(fileExt))[0].split('_')[-1]
            listVersions.append(version)   
        versionCurrent = int(max(listVersions)) # create number for latest version

        confirm = pm.confirmDialog ( title = 'File exists!', message =  '{0}{1:03d}.{2}'.format(fileNameNoVer, versionCurrent, fileExt), button=['SAVE NEXT VERSION', 'CANCEL'], cancelButton= 'CANCEL', dismissString= 'CANCEL' )
        if confirm == 'SAVE NEXT VERSION':
            fileNameFullNextVer = '{0}{1}{2:03d}.{3}'.format(filePath, fileNameNoVer, versionCurrent + 1, fileExt)
            export(fileNameFullNextVer, fileExt)
            print 'CREATED NEXT VERSION: {}'.format(fileNameFullNextVer)      
        else:
            sys.exit('CANCELED!')
    else: # IF FILE NOT EXISTS
        if not os.path.exists(filePath):
            os.makedirs (filePath)
        else:
            export(fileNameFull, fileExt)
            print 'FILE CREATED: {}'.format(fileNameFull) 

# DATABASE OPERATIONS
def buildAssetDic ( assetNameFull ): #  Create Propertys DIC for ASSET.
    print 'dnaCore.buildAssetDic [ INPUT ]: {0}'.format(assetNameFull)
    dataFile = '{0}dataProject.json'.format(rootDic, charPath)
    dataAssetDicFull = json.load(open (dataFile) ) # Build FULL SHOT DIC of project         
    if assetNameFull in dataAssetDicFull['ASSETS']['characters']:
        dataAssetDic = dataAssetDicFull['ASSETS']['characters'][assetNameFull]
        dataAssetDic['assetType'] = 'characters'  
    elif assetNameFull in dataAssetDicFull['ASSETS']['environments']:
        dataAssetDic = dataAssetDicFull['ASSETS']['environments'][assetNameFull]
        dataAssetDic['assetType'] = 'environments'   
    elif assetNameFull in dataAssetDicFull['ASSETS']['props']:
        dataAssetDic = dataAssetDicFull['ASSETS']['props'][assetNameFull]
        dataAssetDic['assetType'] = 'props' 
    elif assetNameFull in dataAssetDicFull['ASSETS']['eda']:
        dataAssetDic = dataAssetDicFull['ASSETS']['eda'][assetNameFull]
        dataAssetDic['assetType'] = 'eda' 
    else:
        print 'ERROR! No <<  {}  >> in database!'.format(assetNameFull)
        dataAssetDic =   None 
    return dataAssetDic
# X = buildAssetDic('NYC')

def buildShotDic( codePart, codeSequence, codeShot ):
    print 'dnaCore.buildShotDic [ INPUTS ] = {0}:{1}:{2}'.format(codePart, codeSequence, codeShot)
    dataFile = '{0}dataProject.json'.format(rootDic)
    dataShotDic = {'assets' : [], 'characters' : [ ], 'props' : [] , 'environments' : [] , 'eda' : [] , 'endFrame' : []} 
    dataFullDic = json.load(open (dataFile) ) # Build FULL project DIC
    dataShotDicSRC = dataFullDic['SHOTS'][codePart][codeSequence][codeShot] # Build SHOT DIC
    # Rebuild LISTS
    dataShotDic['endFrame'] = dataShotDicSRC['endFrame']
    dataShotDic['environments'] = []
    for i in dataShotDicSRC['environments'].split(' '):
        dataShotDic['environments'].append(i)
    dataShotDic['characters'] = []
    for i in dataShotDicSRC['characters'].split(' '):
        dataShotDic['characters'].append(i)
    dataShotDic['props'] = []
    for i in dataShotDicSRC['props'].split(' '):
        dataShotDic['props'].append(i)    
    # Add EDA data to shot dictionary
    dataShotDic['eda'] = []
    listEnv = dataShotDic['environments']
    listEDA = dataFullDic['ASSETS']['environments'][listEnv[0]]['EDA'].split(' ')
    if listEDA:
        for i in listEDA:
            dataShotDic['eda'].append(i)      
    dataShotDic['assets'] = dataShotDic['characters'] + dataShotDic['props'] +  dataShotDic['environments'] +  dataShotDic['eda']
    print 'dnaCore.buildShotDic [ dataShotDic ] = {0}'.format(dataShotDic)
    return dataShotDic
# X = buildShotDic( 'REEL_01', '010', 'SHOT_010' )

# METADATA AND NOTES OPERATIONS
def addMetaAsset(value, assetNameFull, key ): # Add(change) METADATA value for KEY. INPUT: VALUE for KEY (001), saaet full name (C05:KIRILLA), KEY (GEO) FROM TEXT FIELDS 
    print 'dnaCore.addMetaAsset INPUT:  [ value ] = {0}, [ assetNameFull ] = {1}, [ key ] = {2}'.format(value, assetNameFull, key)
    if type(value) == pm.uitypes.TextField: # Check if INPUT VALUE is a string or TEXT FIELD
        value = value.getText() # Get PURE VALUE   
    if type(assetNameFull) == pm.uitypes.TextField: # Check if INPUT ASSET NAME is a string or TEXT FIELD
        assetNameFull = assetNameFull.getText() # Get PURE VALUE    
    dataFile = '{0}dataProject.json'.format(rootDic, charPath)
    dataProject = json.load(open(dataFile)) # Build FULL ASSET DICTIONARY of project      
    if assetNameFull in dataProject['ASSETS']['characters'].keys():
        dataProject['ASSETS']['characters'][assetNameFull][key] = value
        json.dump(dataProject, open(dataFile, 'w'), indent = 4)
        print '<<  PUBLISHED ASSET [ {0} ]: {1} = {2}  >>'.format(assetNameFull, key, value)
    elif assetNameFull in dataProject['ASSETS']['environments'].keys():
        dataProject['ASSETS']['environments'][assetNameFull][key] = value
        json.dump(dataProject, open(dataFile, 'w'), indent = 4)
        print '<<  PUBLISHED ASSET [ {0} ]: {1} = {2}  >>'.format(assetNameFull, key, value)
    elif assetNameFull in dataProject['ASSETS']['eda'].keys():
        dataProject['ASSETS']['eda'][assetNameFull][key] = value
        json.dump(dataProject, open(dataFile, 'w'), indent = 4)
        print '<<  PUBLISHED ASSET [ {0} ]: {1} = {2}  >>'.format(assetNameFull, key, value)
    elif assetNameFull in dataProject['ASSETS']['props'].keys():
        dataProject['ASSETS']['props'][assetNameFull][key] = value
        json.dump(dataProject, open(dataFile, 'w'), indent = 4)
        print '<<  PUBLISHED ASSET [ {0} ]: {1} = {2}  >>'.format(assetNameFull, key, value)
    else:
        print 'dna.Core.addMetaAsset: NO {} IN DATABASE!'.format(assetNameFull)
# X = addMetaAsset('LOC_NYC_001.mb', 'NYC', 'RIG' )   

def addMetaShot(key, value, codePart, codeSequence, codeShot ): # Add(change) METADATA value for KEY. INPUT: KEY , VALUE,  codePart, codeSequence, codeShot
    #print 'dnaCore.addMetaShot [ E{0}_S{1} ] =  {2} : {3}'.format(codeSequence, codeShot, key, value)
    dataFile = '{0}dataProject.json'.format(rootDic, charPath)
    dataProject = json.load(open(dataFile)) # Build FULL ASSET DICTIONARY of project  
    dataProject['SHOTS'][codePart][codeSequence]['SHOT_{}'.format(codeShot)][key] = value
    json.dump(dataProject, open(dataFile, 'w'), indent = 4)
    print '<<  PUBLISHED SHOT [ {2}:E{3}:S{4} ]: {0} = {1}  >>'.format(key, value, codePart, codeSequence, codeShot)
# X = addMetaShot('EXR', 'v002/E010_S010_002.%04d.exr', 'REEL_01', '010', '010' )
    
# REFERENCE-IMPORT DATA
def importData(fullPath): # IMPORT SINGLE ASSET. INPUT: FULL PATH TO ASSET
    pm.importFile(fullPath)       
def referenceItem (itemPathFull, nameSpace): # REFERENCE SINGLE ASSET. INPUT <P:/TANNER/PROD/3D/scenes/ASSETS/CHARACTERS/KIRILLA/GEO/GEO_KIRILLA_039.mb>, <C01>
    pm.createReference(itemPathFull , sharedNodes =( 'shadingNetworks', 'displayLayers', 'renderLayersByName') , ns = nameSpace )   
    print 'dnaCore.referenceItem: {}'.format(nameSpace)
def referenceItems(listIN, key ): # Reference list of assets. INPUTS: List of assets, KEY (GEO,RIG,MAT,FUR), type of asset  (char, env, prop, eda
    print 'dnaCore.referenceItems [ INPUTS ] = {0}, {1}'.format(listIN, key)
    for i in listIN:
        itemPathFull = buildItemFullPath(i, key) # Build FULL PATH to asset
        referenceItem (itemPathFull, i) # Refernce Item	
def shotOpen(partField, sequenceField, shotField, listBrunch): # Open LAST version of the shot
    codePart = partField.getText()
    codeSequence = sequenceField.getText()
    codeShot = shotField.getText()
    print 'dnaCore.shotOpen [INPUTS] = {3}: {0} E{1} SHOT_{2}'.format(codePart, codeSequence, codeShot, listBrunch[1].split('/')[0])
    fullName = '{0}{1}{2}/{3}/SHOT_{4}/{5}E{3}_S{4}_001.mb'.format(rootScene, listBrunch[1], codePart, codeSequence, codeShot, listBrunch[2]  )
    print 'FILE NAME: {0}{1}{2}/{3}/SHOT_{4}/{5}E{3}_S{4}_001.mb'.format(rootScene, listBrunch[1], codePart, codeSequence, codeShot, listBrunch[2]  )
    if os.path.exists(fullName): # IF FILE EXISTS 
        listExisted = glob.glob ('{0}{1}{2}/{3}/SHOT_{4}/{5}E{3}_S{4}_*.mb'.format(rootScene, listBrunch[1], codePart, codeSequence, codeShot, listBrunch[2]  ) )  # check existed version
        listVersions = []
        print listExisted
        for i in listExisted:
            v = i.split('\\')[-1].split('.mb')[0].split('_')[-1]
            listVersions.append(v)   
        versionCurrent = int(max(listVersions))# create number for latest version
        fullName = '{0}{1}{2}/{3}/SHOT_{4}/{5}E{3}_S{4}_{6:03d}.mb'.format(rootScene, listBrunch[1], codePart, codeSequence, codeShot, listBrunch[2], versionCurrent)
        pm.openFile(fullName, f = 1)
        pm.mel.addRecentFile (fullName, 'mayaBinary')
    else:
        pm.confirmDialog (title = 'Warning!', message = 'NO {2} FILE EXISTS FOR: E{0}_S{1}'.format(codeSequence, codeShot, listBrunch[1].split('/')[0] ))        
def buildItemFullPath(assetName, key): # Build full PATH to ASSET. INPUTS: ( assetName (BENDER), KEY ( GEO, RIG, MAT, FUR, EDA), asste type (char, env, prop, eda) )  
    print 'dnaCore.buildItemFullPath [ assetName ] = {0}'.format(assetName)
    dataAssetDic = buildAssetDic(assetName) # get asset properties from DIC  
    print dataAssetDic
    assetType = dataAssetDic[ 'assetType' ]
    if assetType == 'characters': # Build Path for CHARACTERS (P:/PIRATES/PROD/3D/scenes/ASSETS/CHARACTERS/HOKKINS/GEO/GEO_HOKKINS_001.mb )
        if key == 'GEO' or key == 'RIG':
            itemPathFull = '{0}{1}{2}/{3}/{4}'.format( rootScene, charPath, assetName, key, dataAssetDic [key])
        elif key == 'MAT':
            itemPathFull = '{0}{1}{2}{3}/{4}'.format( rootScene, mlPath, charPath, assetName, dataAssetDic [key])    
    elif assetType == 'props': # Build Path for PROPS ( P:/PIRATES/PROD/3D/scenes/ASSETS/PROPS/WEAPON/RIG/RIG_firGunHorn_001.mb )
        itemPathFull = '{0}{1}{2}'.format( rootScene, assetPath, dataAssetDic [key])
    elif  assetType == 'environments':
        if key == 'GEO' or key == 'RIG':
            itemPathFull = '{0}{1}{2}/{3}'.format( rootScene, envPath, assetName, dataAssetDic['GEO'])  
        elif key == 'MAT':
            itemPathFull = '{0}{1}{2}{3}/{4}'.format( rootScene, mlPath, envPath, assetName, dataAssetDic [key])     
    elif  assetType == 'eda':
        itemPathFull = '{0}{1}{2}'.format( rootScene, envPath, dataAssetDic [key]) 
    else:
        print '<<  ERROR in ASSET setup in FTRACK  >>'
        
    print 'dnaCore.buildItemFullPath [ itemPathFull ] = {}'.format(itemPathFull)
    return itemPathFull
# X = buildItemFullPath('BOOZER', 'MAT')    

# SCENE SETUP
def rangeSetup(codePart, codeSequence, codeShot): # setup frame range from shot dictionary
    dataShotDic = buildShotDic(codePart, codeSequence, 'SHOT_' + str(codeShot))
    frameEnd = int(dataShotDic['endFrame']) # get end frame
    pm.env.setTime(frameStart)
    pm.env.setMinTime(frameStart)
    pm.env.setAnimStartTime(frameStart)
    pm.env.setMaxTime(frameEnd)
    pm.env.setAnimEndTime(frameEnd)
def camSetup(cam): # SETUP CAMERA
    # Break connections to shape attributes after ABC import
    cam.overscan.disconnect() 
    cam.nearClipPlane.disconnect() 
    cam.farClipPlane.disconnect() 
    cam.horizontalFilmAperture.disconnect() 
    cam.verticalFilmAperture.disconnect()     
    # Setup attributes
    cam.displayResolution.set(1)
    cam.displayGateMaskColor.set(0,0,0)
    cam.overscan.set(1.1)
    cam.displayGateMaskOpacity.set(1)
    cam.nearClipPlane.set(10)
    cam.farClipPlane.set(100000)
    cam.locatorScale.set(50)
def setRes(): # setup RESOLUTION
    rgRes = pm.PyNode('defaultResolution')
    rgRes.width.set(1998)
    rgRes.height.set(1080)
    rgRes.deviceAspectRatio.set(1.85)
    rgRes.pixelAspect.set(1)
    
# CHECK AND UPDATE SCENE DATA
def analizeShotSC(): # Get SHOT DATA from <<  SCENE  >>
    fileNameFull = pm.sceneName()
    fileName =  fileNameFull.split('/')[-1]
    codePart = fileNameFull.split('/')[-4] # get PART NAME from file path (REEL_01, etc)
    codeSequence = fileNameFull.split('/')[-3] # get SEQUENCE NUMBER from scene name
    codeShot = fileNameFull.split('/')[-2].split('SHOT_')[1] # get SHOT NUMBER from scene name
    codeVersion = fileNameFull.split('/')[-1].split('.')[0].split('_')[-1] # get FILE VERSION from scene name 
    prefix = fileNameFull.split('/')[-1].split('_')[0] # get brunch (RIG or GEO) from scene Name
    if prefix == 'ANM':
        brunch = 'RIG'
    elif prefix == 'RND':
        brunch = 'GEO'
    else:
        brunch =  'GEO'         
    dataShotSC = {}
    dataShotSC['scn_END'] = pm.env.getAnimEndTime()
    dataShotSC['fileName'] = fileName
    dataShotSC['prefix'] = prefix
    dataShotSC['brunch'] = brunch
    dataShotSC['codePart'] = codePart
    dataShotSC['codeSequence'] = codeSequence
    dataShotSC['codeShot'] = codeShot
    dataShotSC['codeVersion'] = codeVersion
    dataShotSC['scn_AST'] = pm.getReferences().keys()
    # Build asset dic by category
    listAssets = pm.getReferences().values() # Get list of assets FULL PATH
    print 'listAssets: {}'.format(listAssets)
    dataShotSC['scn_CHR'] = []
    dataShotSC['scn_PRP'] = []
    dataShotSC['scn_ENV'] = []
    dataShotSC['scn_EDA'] = []
    for i in listAssets:
        dataFileName = fileActs( i ) # Get DATA from file PATH
        assetName = dataFileName['assetName']
        assetType = dataFileName['assetType']
        if assetType == 'characters':
           dataShotSC['scn_CHR'].append(assetName)
        elif assetType == 'props':
           dataShotSC['scn_PRP'].append(assetName)  
        elif assetType == 'environments':
           dataShotSC['scn_ENV'].append(assetName)
        elif assetType == 'eda':
           dataShotSC['scn_EDA'].append(assetName)                      
    print 'dnaCore.analizeShotSC [ dataShotSC ]: {}' .format(dataShotSC)
    return dataShotSC
# X = analizeShotSC()
def analizeShotFT(): # Get SHOT DATA from <<  DATABASE  >>
    dataShotSC = analizeShotSC()
    dataShotDic = buildShotDic(dataShotSC['codePart'], dataShotSC['codeSequence'], 'SHOT_{}'.format(dataShotSC['codeShot']) )
    dataShotFT = {} # Build OUTPUT dictionary
    dataShotFT['ftr_END'] = dataShotDic['endFrame']
    dataShotFT['ftr_AST'] = dataShotDic['assets']
    dataShotFT['ftr_CHR'] = dataShotDic['characters']
    dataShotFT['ftr_PRP'] = dataShotDic['props']
    dataShotFT['ftr_ENV'] = dataShotDic['environments']
    dataShotFT['ftr_EDA'] = dataShotDic['eda']    
    print 'dnaCore.analizeShotFT [ dataShotFT ]: {}'.format(dataShotFT)
    return dataShotFT
# dataShotFT = analizeShotFT()     
    
def analizeVersions():
    brunch = analizeShotSC()['brunch']
    # Check ASSETS VERSIONS
    wrongVersions = []
    listRefAssets = pm.getReferences().keys() # Get CODES of referenced FILES in current scene
    print 'dnaCore.analizeVersions [ listRefAssets ]: {}'.format(listRefAssets)
    for i in listRefAssets: # For ecah REFERENCE: Check existing VER, check VER in FTRACK. IF missmatch : ADD to << wrongVersions variable>>  
        pathRef = pm.FileReference(namespace = i)
        dataFileName = fileActs(pathRef) # Get DATA from file PATH
        verLoad = dataFileName['fileVresion'] # Version in SCENE
        assetType = dataFileName['assetType']
        assetNameFull = i
        if assetNameFull: # Check if assetNameFull is NOT empty
            if not buildAssetDic(i) == None: # Check if ASSET exists in DATABASE
                if assetType == 'environments': # Fix KEY for environments
                    brunch = 'GEO'    
                pathRefFT = buildAssetDic(i)[brunch]
                print 'dnaCore.analizeVersions [ pathRefFT ]: {}'.format(pathRefFT)
                verFT = pathRefFT.split('_')[-1].split('.')[0]
                if not verLoad == verFT:
                        wrongVersions.append(i)
    return wrongVersions    
       
def checkScene(): # Analyse scene data and PRINT result
    print 'CHECKING SCENE!'    
    dataShotSC = analizeShotSC() # Get SHOT data from SCENE 
    dataShotFT = analizeShotFT() # Get SHOT data from FTRACK
    missAssets = set(dataShotFT['ftr_AST']) - set(dataShotSC['scn_AST'])
    extraAssets = set(dataShotSC['scn_AST']) - set(dataShotFT['ftr_AST'])
    wrongVersions = analizeVersions()
    # check if scene end frame equal to FTrack end frame
    frameEndFT = int(dataShotFT['ftr_END'])
    frameEndSC = int(dataShotSC['scn_END'])
    missEND = frameEndFT - frameEndSC
    
    print '\r\n<< CREATING SCENE REPORT >>\r\n'
    if extraAssets :
        print 'EXTRA ASSETS: {0}'.format(extraAssets) 
    else:
        print 'NO EXTRA ASSETS IN SCENE!'   
    if missAssets:
        print 'MISSING ASSETS: {0}'.format(missAssets)
    else:
        print 'ALL ASSETS IN SCENE!'
    if wrongVersions:
        print 'WRONG VERSIONS: {0}'.format(wrongVersions)
    else:
        print 'VERSIONS CORRECT!'  
        
    if not missEND == 0:
        print 'FRAME RANGE WRONG! Should be << {0} >> instead of << {1} >>'.format(frameEndFT, frameEndSC)
    else:
        print 'FRAME RANGE OK!'
        
def addAsset():
    brunch = analizeShotSC()['brunch']
    dataShotSC = analizeShotSC() # Get SHOT data from SCENE
    dataShotFT = analizeShotFT() # Get SHOT data from DATABASE
    missAssets = set(dataShotFT['ftr_AST']) - set(dataShotSC['scn_AST'])
    referenceItems(missAssets, brunch )

def delAsset():
    brunch = analizeShotSC()['brunch']
    dataShotSC = analizeShotSC() # Get SHOT data from SCENE
    dataShotFT = analizeShotFT() # Get SHOT data from DATABASE 
    extraAssets = set(dataShotSC['scn_AST']) - set(dataShotFT['ftr_AST'])
    for i in extraAssets:
        a = pm.FileReference(namespace = i).remove()
        print '<<  DELETED ASSET: {}  >>'.format(i)
def fixAll():
    addAsset()
    delAsset()
    updateRefs()

def updateRefs(): # Update versions of SCENE references according to FTrack data.
    brunch = analizeShotSC()['brunch']# Get BRUNCH: RIG or GEO
    listWrongVer = analizeVersions()
    print 'dnaCore.updateRefs [ listWrongVer ]: {}'.format(listWrongVer)
    listReport = []
    if listWrongVer:
        for i in listWrongVer:
            pathRefSC = pm.FileReference(namespace = i) # get current reference path
            dataFileName = fileActs(pathRefSC) # Get DATA from file PATH
            assetType = dataFileName['assetType']
            pathRefFT = buildAssetDic(i)[brunch] # Get asset path from FTrack        
            dataFileName = fileActs(pathRefSC) # Deassemble PATH
            ver = pathRefFT.split('/')[-1].split('.mb')[0].split('_')[-1] # Get version from Metadata
            pathRefUP = dataFileName ['fileDirPath'] + dataFileName ['fileNameNoVer'] + str(ver) + dataFileName ['fileExt'] # Reassemble PATH                   
            pathRefSC.replaceWith(pathRefUP) # REPLACE REFERENCE 
            listReport.append( i ) 
        print '<< UPDATED VERSIONS: {}  >>'.format(listReport) # PRINT REPORT
            
def SNV(*args):
	sceneNameFull = pm.sceneName() # full scene name with path, version, ext
	scenePath = os.path.dirname(sceneNameFull) # scene path
	sceneNameVerExt = sceneNameFull.split('/')[-1] # scene name with version an ext
	sceneNameVer, ext = sceneNameVerExt.split('.') # get EXT
	ver = sceneNameVer.split('_')[-1] # get VERSION
	verNext = int(ver) + 1
	partQnt = len(sceneNameVer.split('_')) - 1 # get quantity of scene name parts, separated with '_'
	sceneNameParts = sceneNameVer.split('_')[0 : partQnt]
	sceneName = '' # recreate scene name from parts
	for i in range (0 , partQnt):
		sceneName += sceneNameParts[i] + '_'

	sceneNameFullNew = '{0}/{1}{2:0>3}.{3}'.format(scenePath, sceneName, verNext, ext)
	if os.path.exists(sceneNameFullNew):
		confirm = pm.confirmDialog ( title = 'File exists!', message=  'Overwrite file?' + '\r\n\r\n' + str('{0}{1:0>3}.{2}'.format( sceneName, verNext, ext)), button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
		if confirm == 'Yes':
			pm.saveAs(sceneNameFullNew)
			pm.mel.addRecentFile (sceneNameFullNew, 'mayaBinary')
			print 'File overrited: ' + str(sceneNameFullNew)
		else:
			sys.exit()
	else:
		pm.saveAs(sceneNameFullNew)
		pm.mel.addRecentFile (sceneNameFullNew, 'mayaBinary')
		print 'File saved: ' + str(sceneNameFullNew)
