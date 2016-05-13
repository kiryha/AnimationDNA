# Animation DNA 2.0
# NO FTRACK EDITION
# <<  IMPORT ANIMATION 2.0 >>


import pymel.core as pm
from maya.mel import eval
import os, sys, glob
from setupProject import *
import dnaCore as dna
reload(dna)

verABC = 1
frameStart = 101

# EXTRACT DATA FROM FILE NAME
dataScene = dna.analizeShotSC()
codePart = dataScene['codePart']
codeSequence = dataScene['codeSequence']
codeShot = dataScene['codeShot']
# BUILD ASSET LISTS
dataShotDic = dna.buildShotDic(codePart, codeSequence, 'SHOT_{}'.format(codeShot) )
listChars = dataShotDic['characters']
listAssets = dataShotDic['props'] 
listAssetsEnv = dataShotDic['eda']
listCam = pm.ls('E*_S*', type = 'transform')
# BUILD SUB PATHS
pathPart = os.path.join(rootABC , codePart).replace('\\','/') 
pathSeq = os.path.join(pathPart, codeSequence).replace('\\','/') 
pathShot = os.path.join(pathSeq , 'SHOT_{0}'.format(codeShot)).replace('\\','/')

# IMPORT CAMERA SETUP  
def importCamABC(): 
    # Check if camera exists in scene
    cam = pm.ls('E*_S*', type = 'shape')
    if not cam:
        pathABC = '{0}/CAM_E{1}_S{2}_{3:03d}.abc'.format(pathShot, codeSequence, codeShot, verABC) # Build name for <<  CAMERA ABC >>  file
        eval(' AbcImport -m import "{0}" '.format(pathABC)) 
        cam = pm.ls('E*_S*', type = 'shape')[0] # get CAMERA OBJECT
        dna.camSetup(cam) # setup camera DISPLAY               
    else:
        print 'RENDER CAMERA EXIST IN SCENE!'
    
def importABC(asset, pathABC): # IMPORT ALEMBIC
    print 'importABC [ asset ] = {}'.format(asset)
    eval(' AbcImport -ct  "{0}:{0}_GEO" "{1}" '.format(asset, pathABC))
    
def buildPathABC(asset, prefix): # Build   <<  PATH to ABC FILE  >>
    pathABC = '{0}/{1}{2}_{3:03d}.abc'.format(pathShot, prefix, asset, verABC)
    print 'buildPathABC [ pathABC ] = {}'.format(pathABC)
    return pathABC
           
def importCharList(listChars): # IMPORT ALL CHARACTERS
    for char in listChars:
        pathABC = buildPathABC(char, 'CHR_')
        importABC(char, pathABC)
def importAssetList(listAssets): # IMPORT ALL ASSETS
    for asset in listAssets:
        pathABC = buildPathABC(asset, 'AST_')
        importABC(asset, pathABC)
def importEDAList(listAssets): # IMPORT ALL EDA
    for asset in listAssets:
        pathABC = buildPathABC(asset, 'EDA_')
        importABC(asset, pathABC)
def importCltList(listCLT):
    for char in listCLT:
        pathABC = buildPathABC(char, 'CLT/CHR_')
        importABC(char, pathABC)

# IMPORT ALL ANIMATION
def impAllABC(): 
    importCamABC()
    importCharList(listChars)
    importAssetList(listAssets)
    importEDAList(listAssetsEnv)

 
def importABCUI(*args):
    
    if pm.window('importABC', q = 1, ex = 1):
        pm.deleteUI('importABC')
    win = pm.window('importABC', t= 'Import ANIMATION', rtf=True, w = 280 )
    with win:
        mainLayout = pm.columnLayout()
        # Import  <<  ALL ANIMATION  >>        
        allLayout = pm.columnLayout(parent = mainLayout) 
        importAll = pm.button(l = 'IMPORT ALL ANIMATION', w = 280, h= 50)
        importAll.setCommand(pm.Callback (impAllABC))
        pm.separator(h = 15)
        # Import <<  CAMERA  >> 
        importCam = pm.button(l = 'IMPORT CAMERA', w = 280, h= 25) 
        importCam.setCommand(pm.Callback (importCamABC))
        pm.separator(h = 10) 
        # Import <<  CHARACTERS  >>
        charLayout = pm.rowColumnLayout(nc=2, parent = mainLayout) 
        if listChars:
           for char in listChars:
                pathABC = buildPathABC(char, 'CHR_')
                importChar = pm.button(l = char, w = 140, h= 25)
                importChar.setCommand(pm.Callback (importABC, char, pathABC))
        else:
            blank = pm.text(l = '          NO CHARACTERS IN SCENE' , h= 40)
        charLayoutAll = pm.columnLayout( parent = mainLayout)
        # Import <<  ALL CHARACTERS  >> 
        importCharAll = pm.button(l = 'IMPORT ALL CHARACTERS', w = 280, h= 40)
        importCharAll.setCommand(pm.Callback (importCharList, listChars))
        pm.separator(h = 10)
        # Import << ASSETS >>
        assetLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout) 
        if listAssets:
            for asset in listAssets:
                pathABC = buildPathABC(asset, 'AST_')
                importAss = pm.button(l = asset, w = 140, h= 25)
                importAss.setCommand(pm.Callback (importABC, asset, pathABC))
        else:
            pm.text(l = '          NO ASSETS IN SCENE' , h= 20) 
        assetAllLayout = pm.columnLayout(parent = mainLayout) # import <<  ALL ASSET >>  data
        importAssAll = pm.button(l = 'IMPORT ALL ASSETS', w = 280, h= 40)
        importAssAll.setCommand(pm.Callback (importAssetList, listAssets))
        pm.separator(h = 10)
        # Import << EDA >>
        edaLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout) 
        if listAssetsEnv:
            for asset in listAssetsEnv:
                pathABC = buildPathABC(asset, 'EDA_')
                importAss = pm.button(l = asset, w = 140, h= 25)
                importAss.setCommand(pm.Callback (importABC, asset, pathABC))
        else:
            pm.text(l = '          NO ASSETS IN SCENE' , h= 20) 
        assetAllLayout = pm.columnLayout(parent = mainLayout) # import <<  ALL ASSET >>  data
        importAssAll = pm.button(l = 'IMPORT ALL ASSETS', w = 280, h= 40)
        importAssAll.setCommand(pm.Callback (importAssetList, listAssets))
    win.show()    

# importABCUI()
