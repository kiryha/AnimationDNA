# Animation DNA 2.0
# NO FTRACK EDITION
# Shot Assembler

import pymel.core as pm
import os, sys, glob
from setupProject import *
import dnaCore as dna
reload(dna)

actANM = ['save','add assets', 'create camera']
actRND = ['save','add assets', 'add ML' ] 
frameStart = 101     
    

def shotAssemble(partField, sequenceField, shotField, listPhase, act ):
    # New scene
    pm.newFile(f = True)
    # Extract SHOT NUMBER from UI 
    codePart = partField.getText()
    codeSequence = sequenceField.getText()
    codeShot = shotField.getText()
    # Build SHOT DICTIONARY from FTrack data
    dataShotDic = dna.buildShotDic( codePart, codeSequence, 'SHOT_{0}'.format(codeShot))
    listChars = dataShotDic['characters']
    listProps = dataShotDic['props']
    listEDA = dataShotDic['eda']
    listEnv = dataShotDic['environments']
    
    # START ASSEMBLING   
    for action in act:
        if action == 'save':
            fileNameFull = '{0}{1}{2}/{3}/SHOT_{4}/{5}E{3}_S{4}_001.mb'.format(rootScene, listPhase[1], codePart, codeSequence, codeShot, listPhase[2])
            dna.exportFileLV( fileNameFull ) # Save scene
            dna.rangeSetup(codePart, codeSequence, codeShot) # PLAYBACK START/END RANGE SETUP
            dna.setRes() # Setup RESOLUTION
        elif action == 'add assets':
            dna.referenceItems(listChars, listPhase[0]) # reference ( list of CHARS, RIG-GEO triger, asset type)
            print ' <<  CHARACTERS DONE!  >>'
            dna.referenceItems(listProps, listPhase[0]) # REF PROPS 
            print ' <<  PROPS DONE!  >>'
            if listEnv:
                dna.referenceItems(listEnv, 'GEO' ) # REF ENVIRONMENT 
                print ' <<  ENVIRONMENNT DONE!  >>'
                if listEDA[0]:
                    print listEDA
                    dna.referenceItems(listEDA, listPhase[0] ) # REF EDA  
                    print ' <<  EDA DONE!  >>'
        elif action == 'create camera':
            cam = pm.camera()
            camName =  'E' + codeSequence + '_S' + codeShot
            cam[0].rename(camName)
            cam[1].rename(str(camName) + 'Shape')
            dna.camSetup(cam[1])
        elif action == 'add ML':
            for i in listChars:
                matPath = dna.buildItemFullPath(i, 'MAT')
                dna.importData(matPath) # IMPORT ML for CHAR
                print '<<  IMPORTED MATERIAL FOR: {}  >>'.format(i)
            if listEnv:
                matPath = dna.buildItemFullPath(listEnv[0], 'MAT')
                dna.importData(matPath) # IMPORT ML for ENV
                print '<<  IMPORTED MATERIAL FOR: {}  >>'.format( listEnv[0] )                         
    # SAVE SCENE
    pm.saveFile() 
    # CREATE REPORT
    print 'ASSEMBLING DONE!'


def saveNext():
    dna.SNV()

# ADD ASSETS
def refDataList(listAssets, key): # 1) REFERENCE ASSET LIST
    listAssets = listAssets.getText().split(' ')
    dna.referenceItems (listAssets, key)


def baseUI (): 
    if pm.window('ASSEMBLER', exists = 1):
        pm.deleteUI('ASSEMBLER')
    baseWin = pm.window('ASSEMBLER', t = 'Shot Assembler', w = 280, h = 100)
    with baseWin:
        mainLayout = pm.columnLayout()
        inputLayout = pm.rowColumnLayout(nc=6, parent = mainLayout) 
        pm.text (l = '  PART  ')
        partField = pm.textField(tx = 'REEL_01', w= 60, h = 30)
        pm.text (l = '    SEQ ')
        sequenceField = pm.textField(tx = '010', w= 45, h = 30)
        pm.text (l = '    SHOT ')
        shotField = pm.textField(tx = '010', w= 45, h = 30)
        pm.separator(h = 5 , style = 'none')        
        createLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout) 
        ANM = pm.button(l = 'CREATE\r\nANIMATION SCENE', w = 140, h= 55)
        RND = pm.button(l = 'CREATE\r\nRENDER SCENE', w = 140, h= 55)
        ANM.setCommand(pm.Callback (shotAssemble, partField, sequenceField, shotField, listANM, actANM))
        RND.setCommand(pm.Callback (shotAssemble, partField, sequenceField, shotField, listRND, actRND)) 
        OPANM = pm.button(l = 'OPEN ANIMATION SCENE', w = 140, h = 25)
        OPRND = pm.button(l = 'OPEN RENDER SCENE', w = 140 )
        OPANM.setCommand(pm.Callback (dna.shotOpen, partField, sequenceField, shotField, listANM ))
        OPRND.setCommand(pm.Callback (dna.shotOpen, partField, sequenceField, shotField, listRND )) 
        pm.separator(h = 6 , style = 'none')

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
        pm.separator(h = 8 , style = 'none')
        
        addLayout = pm.rowColumnLayout(nc=2, parent = mainLayout)  
        pm.text (l = '   ADD ASSETS:        ')
        assetListField = pm.textField(tx = 'BENDER', w= 180, h = 30)
          
        createLayout = pm.rowColumnLayout(nc =2, parent = mainLayout)
        addANM = pm.button(l = 'FOR AMIMATION', w = 140, h= 50)
        addRND = pm.button(l = 'FOR RENDER', w = 140)
        addANM.setCommand(pm.Callback (refDataList, assetListField, 'RIG' ))
        addRND.setCommand(pm.Callback (refDataList, assetListField, 'GEO' )) 

    baseWin.show()  
# baseUI()
