# 256 pipeline tools
# Data publisher 2.0
# NO FTRACK EDITION

import pymel.core as pm
import  os, sys
from setupProject import *
import dnaCore as dna
reload(dna)
      
        
def anilizeCurrent(assetField,textPublisher,fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA):
    print '<<  ANALIZING CURRENT ASSET  >>'  
    fileNameFull = pm.sceneName()
    dataFileName = dna.fileActs(fileNameFull) # Get filename details (name, ver, ext etc) 
    phase = dataFileName['filePhase'] # Get PHASE (MODELLING, RENDER, LOOKDEV etc)
    key = dataFileName['filePrefix']
    # Get asset DATA from FTRACK
    assetName = dataFileName['assetName']
    assetType = dataFileName['assetType']
    assetCat = dataFileName['assetCat']    
    # RUN SETUP
    if phase == 'ASSETS': # SETUP ASSETS
        if key == 'ENV': # SETUP <<  ENVIRONMENT  >>
            print 'assetType: <<  ENVIRONMENT  >>'
            value = dataFileName['fileNameFull'] 
            textPublisher(assetName, 'GEO', value, type, assetField, fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA)                
        elif key == 'FUR' or key == 'GEO' or key == 'RIG': # SETUP <<  CHARACTERS + DYNAMIC PROPS + EDA  >>
            if assetType == 'characters':
                print 'assetType: <<  CHARACTERS  >>'
                value = dataFileName['fileNameFull'] 
                textPublisher(assetName,key,value,type,assetField,fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA)
            elif assetType == 'props':
                print 'assetType: <<  DYNAMIC PROPS  >>'
                value = '{0}/{1}/{2}'.format(assetCat, key, dataFileName['fileNameFull'])
                textPublisher(assetName,key,value,type,assetField,fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA)
            elif assetType == 'eda':
                print 'assetType: <<  ENVIRONMENT DYNAMIC ASSET  >>'
                value = fileNameFull.split('{0}{1}'.format(rootScene, envPath))[-1]
                textPublisher(assetName,key,value,type,assetField,fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA)
                        
    elif phase == 'LOOKDEV': # SETUP MATERIALS
        print 'assetType: <<  MTERIAL LIBRARY  >>'  
        value = dataFileName['fileNameFull'] 
        textPublisher(assetName,key,value,type,assetField,fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA)

def textPublisher(assetName, key, value, type, assetField, fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA):
    pm.textField(assetField, edit = True, tx = assetName) 
    if key == 'GEO':
        pm.textField(fieldGEO, edit = True, tx = value) 
    elif key =='RIG':
        pm.textField(fieldRIG, edit = True, tx = value) 
    #elif key =='FUR':
        #pm.textField(fieldFUR, edit = True, tx = value) 
    elif key =='MAT':
        pm.textField(fieldMAT, edit = True, tx = value)
    elif key =='EDA':
        pm.textField(fieldEDA, edit = True, tx = value) 

def pubKEY(fieldKEY, assetField, key):
    dna.addMetaAsset( fieldKEY.getText(), assetField.getText(), key )
               
def baseUI (): 
    if pm.window('DTP', exists = 1):
        pm.deleteUI('DTP')
    baseWin = pm.window('DTP', t = 'Data Publisher', w = 280, h = 100)
    with baseWin:
        mainLayout = pm.columnLayout()
        
        currentLayout = pm.rowColumnLayout(nc=1, parent = mainLayout)
        anilizeCur = pm.button(l = 'ANALIZE CURRENT ASSET', w = 280, h = 45)
        
        assetLayout = pm.rowColumnLayout(nc=1, parent = mainLayout) 
        assetField = pm.textField(tx = '', w= 280, h = 30)
        pm.separator(h = 5 , style = 'none')
        
        assetLayout = pm.rowColumnLayout(nc=2, parent = mainLayout) 
        fieldGEO = pm.textField( w= 240, h= 30)
        publishGEO = pm.button(l = 'GEO', w = 40)
        publishGEO.setCommand(pm.Callback (pubKEY, fieldGEO, assetField, 'GEO'))
        
        fieldRIG = pm.textField( w= 240, h= 30)
        publishRIG = pm.button(l = 'RIG', w = 40)
        publishRIG.setCommand(pm.Callback (pubKEY, fieldRIG, assetField, 'RIG'))
        
        fieldFUR = pm.textField( w= 240, h= 30)
        publishFUR = pm.button(l = 'FUR', w = 40)
        publishFUR.setCommand(pm.Callback (pubKEY, fieldFUR, assetField, 'FUR'))
        
        fieldMAT = pm.textField( w= 240, h= 30)
        publishMAT = pm.button(l = 'MAT', w = 40)
        publishMAT.setCommand(pm.Callback (pubKEY, fieldMAT, assetField, 'MAT'))
              
        fieldEDA= pm.textField( w= 240, h= 30)
        publishEDA = pm.button(l = 'EDA', w = 40)
        publishEDA.setCommand(pm.Callback (pubKEY, fieldEDA, assetField, 'EDA'))
         
        anilizeCur.setCommand(pm.Callback (anilizeCurrent,assetField,textPublisher,fieldGEO, fieldRIG, fieldFUR, fieldMAT, fieldEDA))
        
    baseWin.show()  
# baseUI()
