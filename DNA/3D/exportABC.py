# Animation DNA 2.0
# NO FTRACK EDITION
# <<  EXPORT ANIMATION 2.0 >>


import pymel.core as pm
from maya.mel import eval
import os, sys
from setupProject import*
import dnaCore as dna
reload(dna)

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

verABC = 1
frameStart = 101
frameEnd = dna.buildShotDic(codePart,codeSequence,'SHOT_{}'.format(codeShot))['endFrame']
     
def createFolder(path): # create folders for ABC files
    if not os.path.exists(path):
        os.mkdir(path)
def createFolderStr(pathPart, pathSeq , pathShot):   
    createFolder(pathPart)   
    createFolder(pathSeq)
    createFolder(pathShot)
    
def exportABC(asset, prefix):# Export ASSET to ABC     
    if asset in listChars: # if input asset is character, than export ABC from 1 frame 
        frameStart = 1
    else:
        frameStart = 101
    nameABC = '{0}/{1}_{2}_{3:03d}.abc'.format(pathShot, prefix, asset, verABC ) # Build name for ABC file 
    #root =  pm.ls('{0}:{0}_GEO'.format(asset), type = 'transform')[0]
    eval('AbcExport -j " -framerange {2} {3} -uvWrite -root {0}:{0}_GEO -file {1}"'.format(asset, nameABC, frameStart, frameEnd))

def expListABC(list, prefix):# Export LIST of characters to ABC
    for asset in list:
        exportABC(asset, prefix) 

def exportCamABC(listCam):
    nameABC = '{0}/CAM_{1}_{2:03d}.abc'.format(pathShot , listCam[0], verABC)
    eval('AbcExport -j " -framerange {2} {3} -uvWrite -root {0} -file {1}"'.format(listCam[0], nameABC, frameStart, frameEnd))   

def expAllABC(listChars,listCam,listAssets): # EXPORT ALL ANIMATION
    exportCamABC(listCam) # Export camera data
    expListABC(listChars, 'CHR') # Export ALL Character data
    expListABC(listAssets, 'AST') # Export ALL ASSET data
    expListABC(listAssetsEnv, 'EDA') # Export ALL ENV


def checkCam (listCam):
    if len(listCam) > 1:
        confirm = pm.confirmDialog( title='Warning', message = 'There are extra camera in the scene. \r\nDelete or rename extra cameras!' , button=['OK','HELP'], cancelButton='OK' )
        if confirm == 'HELP':
            pm.warning( 'This scene should contain only one camera named E###_S###. You should delete or rename all extra cameras!')
            return []
    else:
        return listCam

checkCam(listCam) # check if THERE IS ONLY ONE SHOT camera       
createFolderStr(pathPart, pathSeq , pathShot) # CREATE FOLDERS FOR ABC export

def exportABCUI(*args):
    
    if pm.window('exportABC', q = 1, ex = 1):
        pm.deleteUI('exportABC')
    win = pm.window('exportABC', t= 'Export ANIMATION', rtf=True, w = 280 )
    with win:
        mainLayout = pm.columnLayout()              
        allLayout = pm.columnLayout(parent = mainLayout) 

        # Export <<  ALL ANIMATION  >>
        exportAll = pm.button(l = 'EXPORT ALL ANIMATION', w = 280, h= 50)
        exportAll.setCommand(pm.Callback (expAllABC, listChars,listCam,listAssets))
        pm.separator(h = 15)
        # Export <<  CAMERA  >> 
        exportCam = pm.button(l = 'EXPORT CAMERA', w = 280, h= 25) 
        exportCam.setCommand(pm.Callback (exportCamABC, listCam))
        pm.separator(h = 10)
        # Export <<  CHARACTERS  >>        
        charLayout = pm.rowColumnLayout(nc=2, parent = mainLayout) 
        if listChars:
           for char in listChars:
                exportChar = pm.button(l = char, w = 140, h= 25)
                exportChar.setCommand(pm.Callback (exportABC, char, 'CHR'))
        else:
            blank = pm.text(l = '     NO CHARACTERS IN SCENE' , h= 40)
        # Export <<  ALL CHARACTERS   >>
        charLayoutAll = pm.columnLayout( parent = mainLayout) 
        exportCharAll = pm.button(l = 'EXPORT ALL CHARACTERS', w = 280, h= 40)
        exportCharAll.setCommand(pm.Callback (expListABC, listChars, 'CHR'))
        # Export <<  ASSETS  >>
        pm.separator(h = 10) 
        assetLayout = pm.rowColumnLayout(nc= 2, parent = mainLayout) 
        if listAssets:
            for asset in listAssets:
                exportAss = pm.button(l = asset, w = 140, h= 25)
                exportAss.setCommand(pm.Callback (exportABC, asset, 'AST'))  
        else:
            a = pm.text(l = '     NO ASSETS IN SCENE', h= 20)               
        assetAllLayout = pm.columnLayout(parent = mainLayout) 
        # Export <<  ALL ASSETS  >>
        exportAssAll = pm.button(l = 'EXPORT ALL ASSETS', w = 280, h= 40)
        exportAssAll.setCommand(pm.Callback (expListABC, listAssets, 'AST'))
        pm.separator(h = 10)
        # Export <<  EDA  >>
        envLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout) 
        if listAssetsEnv:
           for assetEnv in listAssetsEnv:
                exportEnv = pm.button(l = assetEnv, w = 140, h= 25)
                exportEnv.setCommand(pm.Callback (exportABC, assetEnv, 'EDA'))
                
        else:
            blank = pm.text(l = '     NO ANIM in ENVIRONMENT' , h= 40)
        envLayoutAll = pm.columnLayout( parent = mainLayout) # Export ALL EDA   
        exportEnvAll = pm.button(l = 'EXPORT ALL EDA', w = 280, h= 40)
        exportEnvAll.setCommand(pm.Callback (expListABC, listAssetsEnv, 'EDA' ))
        #pm.separator(h = 10)

        
    win.show()    

# exportABCUI()
