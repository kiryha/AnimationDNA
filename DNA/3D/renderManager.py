# Animation DNA 2.0
# NO FTRACK EDITION
# <<  RENDER MANAGER 2.0  >>

import pymel.core as pm
import mtoa.aovs as aovs
from maya.mel import eval
import sys
from setupProject import *
import dnaCore as dna
reload(dna)

frameStart = 101

def checkArnold(*args): #Set current render to <<  ARNOLD  >>
    if( pm.getAttr( 'defaultRenderGlobals.currentRenderer' ) != 'arnold' ):
        print 'SWITCH RENDER TO ARNOLD'
        pm.setAttr('defaultRenderGlobals.currentRenderer', 'arnold')
checkArnold()

# Check arnold drivers
driver = pm.ls('defaultArnoldDriver')
if not driver:
    eval('RenderGlobalsWindow;')  

def aiDrivers(): # Create Default arnold nodes
    add = pm.createNode('aiAOVDriver', name = 'defaultArnoldDisplayDriver')
    add.outputMode.set(0)
    ad = pm.createNode('aiAOVDriver', name = 'defaultArnoldDriver')
    ad.outputMode.set(2)
    pm.createNode('aiAOVFilter', name = 'defaultArnoldFilter')
    pm.createNode('aiOptions', name = 'defaultArnoldRenderOptions')

# Build SHOT data. Check NAME OF CURRENT SCENE. If its RENDER scene >> setup scenes variables. (codePart codeSequence codeShot codeVersion)
scenePrefix = pm.sceneName().split('/')[-1].split('_')[0]
if scenePrefix == 'RND':
    fileNameFull = pm.sceneName()
    fileName =  fileNameFull.split('/')[-1]
    codePart = fileNameFull.split('/')[-4] # get PART NAME from file path (REEL_01, etc)
    codeSequence = fileNameFull.split('/')[-3] # get SEQUENCE NUMBER from scene name
    codeShot = fileNameFull.split('/')[-2].split('SHOT_')[1] # get SHOT NUMBER from scene name
    codeVersion = fileNameFull.split('/')[-1].split('.')[0].split('_')[-1] # get FILE VERSION from scene name 
    fnPrefix = '{4}RENDER_3D/RENDER/{0}/{1}/SHOT_{2}/MASTER/v{3}/E{1}_S{2}_{3}'.format(codePart, codeSequence, codeShot, codeVersion, rootProd) 
def getEnd():
    if scenePrefix == 'RND':
        dataShotDic = dna.buildShotDic(codePart, codeSequence, 'SHOT_' + str(codeShot))
        frameEnd = int(dataShotDic['endFrame'])
    else:
        frameEnd = 101
    return frameEnd

# Render GLOBALS
rgArnold = pm.PyNode('defaultArnoldDriver')
rgArnoldRO =  pm.PyNode('defaultArnoldRenderOptions')
rgCommon = pm.PyNode('defaultRenderGlobals')
rgRes = pm.PyNode('defaultResolution')
# Define GENERALL data
shaderIDsPref = 'IDS_'
objectIDsPref = 'IDO_'
listAOV = ['beauty' , 'N' , 'P' , 'Z' , 'direct_diffuse' , 'direct_specular' , 'indirect_diffuse' , 'indirect_specular' , 'refraction' , 'sss' , 'sheen' , 'specular', 'diffuse_color',  'direct_specular_2', 'indirect_specular_2', 'direct_backlight', 'indirect_backlight', 'volume']
listColors = {'R':( 1, 0, 0 ) , 'G':( 0, 1, 0 ) , 'B':( 0, 0, 1 ) }
SET_GEN = '{}SETS/SET_GENERAL_001.mb'.format(mlPath)
OUT = '{}OUTDOOR/LIT_OUTDOOR_001.mb'.format(llPath)

def ldAdd():
    print 'REFERENCE MATERIALS AND LIGHTS'
    dna.referenceItem(SET_GEN, 'GEN')
    dna.referenceItem(OUT, 'OUT')

# AOVs       
def addAOV(aovName): # Creates AOV render pass
    aov = aovs.AOVInterface().addAOV( aovName )
    return aov

def addObjAOV( prefix, index ): # Creates AOV render pass for object ID
    aovName = str(prefix) + str(index)
    aovs.AOVInterface().addAOV( aovName )
    return aovName

def checkObjID(prefix):#check existing ids to create proper nubers for next ids
    if pm.objExists('aiAOV_' + str(prefix) + '*'): 
        pm.select('aiAOV_' + str(prefix) + '*')
        exist = pm.ls(sl = True)[-1]
        exist = int(exist.split('_')[2]) + 1
        pm.select (d = True)
    else: 
        exist = 0
    return exist

def runIDS(createMatID_X): # Run SETUP SHADER IDS. INPUT: creation method  << aiWriteColor >> or << aiUtility >>
    shadingGroup = pm.ls(sl = 1, type='shadingEngine') # check if any Shading Group selected or not
    if shadingGroup: # for MANUALY SELECTED SG
        createMatID_X(shadingGroup)
    else: # for ALL SG IN SCENESzz
        confirm = pm.confirmDialog ( title='WARNING', message='CREATE IDS FOR ALL SHADERS?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if confirm == 'Yes':
            shadingGroup = pm.ls(type='shadingEngine')
            shadingGroup.remove('initialParticleSE')
            shadingGroup.remove('initialShadingGroup')
            createMatID_X(shadingGroup)  
        else:
            sys.exit()  

# MATERIAL SETUP
# select shading Groups of selected objects
def selSG(condition):
    if condition == 'ALL':
        list = pm.ls(type = 'geometryShape')
    else:
        list =  pm.ls(dag=1,o=1,s=1,sl=1) # get shapes of selection:
    shadingGrps = pm.listConnections(list,type='shadingEngine') # get shading groups from shapes:
    if 'initialShadingGroup' in shadingGrps:
        shadingGrps.remove('initialShadingGroup')
    pm.select(clear = True)
    SGS = pm.select(shadingGrps, ne = 1)

def matAsign(): # ASIGN MATERIAL FOR ALL OBJECTS
    listAtrRoot = pm.ls('*.mtoa_constant_mMat')
    listAtrRef = pm.ls('*:*.mtoa_constant_mMat')
    listAtr = set(listAtrRef + listAtrRoot) # combine lists for REFERENCED and ROOT geo
    for i in listAtr: 
        object = pm.PyNode(i.split('.')[0]) # Create object based on <<  mMat >>
        ins = pm.ls(object, ap = 1, dag = 1 ) # select instances
        if i.get():
            if pm.objExists((i.get()+ 'SG')):
                pm.sets((i.get()+ 'SG'), forceElement = ins)

def matAsignSel(): # ASIGN MATERIAL FOR SELECTED OBJECTS
    sel = pm.ls(dag=1,o=1,s=1,sl=1)
    print sel
    for i in sel:
        if pm.attributeQuery( 'mtoa_constant_mMat' , node = i , exists = 1):
            mat = i.mtoa_constant_mMat.get()
            print mat
            if mat:
                asign = pm.sets(str(mat) + 'SG', forceElement = i)  
                      
                   
# SHADER AOVS aiWriteColor
def setupNetwork(shader, shaderInOBJ, shderInATTR ):
    print 'setupNetwork [INPUTS] = {0} : {1} : {2}'.format(shader, shaderInOBJ, shderInATTR)
    aiAOVName =  'aiAOV_{0}{1}'.format(shaderIDsPref, shader)
    shaderAOVName = str(shaderIDsPref) + str(shader)
    if not pm.objExists(aiAOVName): #check if AOV exists
        aiWCAOV =  addAOV('IDS_%s' % shader) #create AOV for material
        aiWC = pm.shadingNode('aiWriteColor', asShader = True, name = 'WRC_{}'.format(shader) ) #create aiWriteColor node
        aiWC.blend.set(1) # set blemd ON
        if shaderInOBJ: # if connection to COLOR of shader exists
            if pm.nodeType(shaderInOBJ[0]) == 'gammaCorrect':
                shaderInOBJ[0].outValue >> aiWC.beauty
            else:
                shaderInOBJ[0].outColor >> aiWC.beauty # connect INPUT of shader to arWriteColor
            aiWC.input.set(listColors['R'] , type = 'double3') # set MASK COLOR
            aiWC.aovName.set(shaderAOVName, type = 'string') # connect aiWriteColor to  AOV 
            pm.connectAttr( aiWC.outColor, str(shader) + str(shderInATTR), force = True ) # connect aiWriteColor to SHADER
        else: # if COLOR has no input
            color = pm.getAttr(str(shader) + str(shderInATTR)) # get COLOR
            aiWC.beauty.set(color) # set INPUT COLOR of aiWriteColor
            aiWC.input.set(listColors['R'] , type = 'double3') # set MASK COLOR
            aiWC.aovName.set(shaderAOVName, type = 'string') # connect aiWriteColor to  AOV 
            pm.connectAttr( aiWC.outColor, str(shader) + str(shderInATTR), force = True ) # connect aiWriteColor to SHADER
    else:
        print str(shader) + ' AOV already exists!'

def createMatID_WC (shadingGroup): # CREATE IDs
    for i in shadingGroup:
        shader = pm.listConnections(i,  d = False , s = True, type= [ 'aiStandard' , 'aiSkin' , 'aiHair' , 'aiUtility' , 'alSurface', 'jf_nested_dielectric', 'K_SSS', 'alHair', 'aiRaySwitch'] ) #get shader from SG 
        if shader:
            shader = shader[0]
            if pm.nodeType(shader) == 'aiStandard' or pm.nodeType(shader) == 'aiUtility': # for THIS shader type
                shaderInOBJ = shader.color.inputs(d=False, s=True) # get INPUT from shader
                shderInATTR = '.color'
                setupNetwork(shader, shaderInOBJ, shderInATTR )  # insert WRITE COLOR                        
            elif pm.nodeType(shader) == 'aiSkin' or pm.nodeType(shader) == 'K_SSS':
                shaderInOBJ = shader.shallowScatterColor.inputs(d=False, s=True) 
                shderInATTR = '.shallowScatterColor'
                setupNetwork(shader, shaderInOBJ, shderInATTR)
            elif pm.nodeType(shader) == 'aiHair':
                shaderInOBJ = shader.tipcolor.inputs(d=False, s=True) 
                shderInATTR = '.tipcolor'
                setupNetwork(shader, shaderInOBJ, shderInATTR)
            elif pm.nodeType(shader) == 'alSurface' or pm.nodeType(shader) == 'alHair':
                shaderInOBJ = shader.diffuseColor.inputs(d=False, s=True)
                shderInATTR = '.diffuseColor'
                setupNetwork(shader, shaderInOBJ, shderInATTR)
            elif pm.nodeType(shader) == 'jf_nested_dielectric':
                shaderInOBJ = shader.mediumTransmittance.inputs(d=False, s=True) 
                shderInATTR = '.mediumTransmittance'
                setupNetwork(shader, shaderInOBJ, shderInATTR)
            elif pm.nodeType(shader) == 'aiRaySwitch':
                shaderInOBJ = shader.camera.inputs(d=False, s=True) 
                shderInATTR = '.camera'
                setupNetwork(shader, shaderInOBJ, shderInATTR)
            else:
                print 'Unexpected shader type'
                shader = pm.listConnections(i,  d = False , s = True)
                print 'SHADER:  '  + str(shader)
        else:
            print 'ERROR FINDING SHADER IN SG: ' + str(i)
    print 'SHADERS IDs DONE!'
  
           
# SHADER AOVs aiUtility
def addSGAOV(shadingGroup):
    for sg in shadingGroup:
        sg = sg.split('SG')[0]
        aovName = str(shaderIDsPref) + str(sg)
        aiAOVName =  'aiAOV_%s%s' % (shaderIDsPref, sg)
        if not pm.objExists(aiAOVName): #check if AOV exists
            addAOV(aovName)
        else:
            print str(sg) + ' AOV already exists!'
            
def addUT(sg):
    if not pm.objExists('UT_%s' % sg): #check if AOV exists
        UTL = pm.shadingNode('aiUtility', asShader = True, name = 'UT_%s' % sg ) #create aiUtility node
        UTL.shadeMode.set(2)
        UTL.color.set(1,0,0)
        return UTL
    else:
        print str(sg) + ' AOV already exists!'
       
def createMatID_UT(shadingGroup):
    addSGAOV(shadingGroup)    
    for sg in shadingGroup:
        sgAttr = sg.aiCustomAOVs
        dicAOVs, nextIndex = aovs.getShadingGroupAOVMap(sgAttr) # build AOV dictionary
        UTL = addUT(sg.split('SG')[0])
        UTL.outColor >> dicAOVs[str(shaderIDsPref) + str(sg.split('SG')[0])].aovInput
        
          
# OBJECT AOVS
def setupID(prefix, index):
    if type(index) == int:
        index = str('%02d' % index)
    mskObjectMat = pm.shadingNode('aiUserDataColor', asShader = True, name = 'UDC_' + str(prefix) + str(index) )
    mskObjectMat.colorAttrName.set(str(prefix)+ str(index))
    objectID  = addObjAOV (prefix,index)
    objectIDFull = 'aiAOV_' + str(objectID)
    ID = pm.PyNode(objectIDFull)
    mskObjectMat.outColor >> ID.defaultValue  


def addColor(prefix, list, index): #create color attribute for asset IDs
    colorAttrName = prefix + index
    colorAttrNameLong = 'mtoa_constant_' + str(colorAttrName)
    for i in list:
        pm.addAttr(i, longName= colorAttrNameLong , niceName = colorAttrName , usedAsColor=True, attributeType='float3' )
        pm.addAttr(i, longName='R' +  str(colorAttrName), attributeType='float', parent=colorAttrNameLong )
        pm.addAttr(i, longName='G' +  str(colorAttrName), attributeType='float', parent=colorAttrNameLong )
        pm.addAttr(i, longName='B' +  str(colorAttrName), attributeType='float', parent=colorAttrNameLong )
        i.attr(colorAttrNameLong).set(listColors['R'])
    return colorAttrNameLong     

def createObjID(*agrs):
    print 'OBJ IDs'
    prefix = 'IDO_'
    sel = pm.ls(sl = 1) # get list of selected OBJECT GROUPS 
    index = checkObjID('IDO_')
    for i in sel:
        list = pm.listRelatives(i, ad = True)
        setupID(prefix, index)
        indexStr = str('%02d' % index)
        addColor(prefix, list, indexStr)
        index += 1
        
def assetIDs():
    prefix = 'IDA_'
    dataShotDic = dna.buildShotDic(codePart, codeSequence , 'SHOT_{}'.format(codeShot) )
    listAssets = dataShotDic['props'] + dataShotDic['characters']
    listEnv =  dataShotDic['environments'] +  dataShotDic['eda']    
    # Create IDs for <<  characters  >>
    print 'assetIDs [ listAssets ] = {}'.format(listAssets)
    for i in listAssets: 
        asset = pm.ls('{0}:{0}'.format(i), type = 'transform')
        if not pm.objExists( 'aiAOV_IDA_{}'.format(i)): # check existing IDs
            print 'Add asset ID for: {}'.format(i)
            objList = pm.listRelatives(asset[0], ad = True) # select ALL OBJECTS in each ITEM(i) 
            setupID(prefix, i)
            addColor(prefix, objList, i)
        else:
            print 'ID exists'
    print '<<  ADDING ID FOR ASSETS DONE!  >>'   

    # Create IDs for <<  ENV and EDA  >>
    if listEnv:
        print 'assetIDs [ listEnv ] = {}'.format(listEnv)
        code = 'ENVIRONMENT'
        objList = []
        for i in listEnv:
            print 'Add asset ID for: {}'.format(i)
            assets = pm.ls('{0}:{0}'.format(i), type = 'transform')           
            for i in assets:
                objList.append( pm.listRelatives(i, ad = True, shapes  = True))
        if not pm.objExists( 'aiAOV_IDA_{}'.format(code)): # check existing IDs
            setupID(prefix, code)
            for i in objList:
                addColor(prefix, i, code)
        else:
                print 'ID exists'
        print '<<  ADDING ID FOR ENVIRONMENTS DONE!  >>' 
    print '<< ASSETS IDS DONE!  >>'

# PASSES AOVS
def addOcc(*args): #Create Occlution pass with shader
    if not pm.objExists( 'aiAOV_%s' % 'AO' ): #check AO already exists
        shdrAO = pm.shadingNode('aiAmbientOcclusion', asShader = True, name = 'GEN_AO')
        shdrAO.farClip.set(50)
        shdrAO.samples.set(2)
        aovAO = aovs.AOVInterface().addAOV('AO')
        aovAO = pm.PyNode('aiAOV_AO')
        shdrAO.outColor >> aovAO.defaultValue
        print 'AO AOV DONE!'

def addZ(*args): #Create DEPTH pass with shader
    if not pm.objExists( 'aiAOV_%s' % 'ZDEPTH' ): #check AOV already exists
        aovZ = aovs.AOVInterface().addAOV('ZDEPTH')
        aovZ = pm.PyNode('aiAOV_ZDEPTH')
        sin = pm.shadingNode('samplerInfo', asShader = True, name = 'INFO_Z')
        sin.pointCamera.pointCameraZ >> aovZ.defaultValue
        pm.setAttr ('aiAOV_ZDEPTH.type', 4)
        print 'ZDEPTH AOV DONE!'

def addUV(*args): #Create UV pass with shader
    if not pm.objExists( 'aiAOV_UV' ): #check if UV AOV already exists
        shdrUV = pm.shadingNode('aiUtility', asShader = True, name = 'GEN_UV')
        shdrUV.shadeMode.set(2)
        shdrUV.color.set(0,0,0)
        siUV = pm.shadingNode('samplerInfo', asShader = True, name = 'INFO_UV')
        siUV.uvCoord.uCoord >> shdrUV.color.colorR
        siUV.uvCoord.vCoord >> shdrUV.color.colorG
        aovUV = aovs.AOVInterface().addAOV('UV')
        aovUV = pm.PyNode('aiAOV_UV')
        shdrUV.outColor >> aovUV.defaultValue
        print 'UV AOV DONE!'

def addNorm():
    if not pm.objExists( 'aiAOV_NRM' ): #check AO already exists
        shdrNorm = pm.shadingNode('aiUtility', asShader = True, name = 'GEN_NRM')   
        shdrNorm.shadeMode.set(2) 
        shdrNorm.colorMode.set(3) 
        aovNorm = aovs.AOVInterface().addAOV('NRM')
        aovNorm = pm.PyNode('aiAOV_NRM')
        shdrNorm.outColor >> aovNorm.defaultValue
        print 'NORMAL AOV DONE!'
            
def addAOVSet(*args): #create BASE sat of AOVs
    rgArnold.mergeAOVs.set(1) 
    addOcc() # create Ocllution pass
    addZ()
    addUV()
    addNorm()
    n = 0
    for i in listAOV: # create standard set of AOVs from listAOV
        if not pm.objExists( 'aiAOV_%s' % listAOV[n] ): #check if AOV already exists
            addAOV(i)
        n += 1
    print 'PASSES CREATION DONE!'

# DELETE SHADER IDs
def deleteIDS(nodesWC): # DELETE SHADER IDS AND aiWriteColor NODES    
    for i in nodesWC:
        IN = i.inputs(p=1)
        OUT = i.outputs(p=1, type = [ 'aiStandard' , 'aiSkin' , 'aiHair' , 'aiUtility' , 'alSurface', 'jf_nested_dielectric', 'K_SSS', 'alHair', 'aiRaySwitch'])
        AOV = 'aiAOV_IDS_' + str(i.split('WRC_')[1])
        if IN:
            IN[0] >> OUT[0]
            pm.delete(i)
            pm.delete(AOV)
        else:
            color = i.getAttr('beauty')
            pm.delete(i)
            pm.delete(AOV)
            OUT[0].set(color)

def runDelIDs(): # RUN procedure of DELETE SHADER IDS AND aiWriteColor NODES
    nodesWC = pm.ls( sl = True )
    if nodesWC: # delete selected shader IDs
        confirm = pm.confirmDialog ( title='WARNING', message='DELETE SELECTED IDS?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if confirm == 'Yes':
            deleteIDS(nodesWC)
    else: # delete ALL shader IDS
        confirm = pm.confirmDialog ( title='WARNING', message='DELETE ALL SHADER IDS?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if confirm == 'Yes':
            nodesWC = pm.ls('WRC_*', type = 'aiWriteColor') # select all aiWriteColors for IDs
            nodeAOV =  pm.ls('aiAOV_IDS_*', type = 'aiAOV') # select all AOVs for shader IDs
            deleteIDS(nodesWC)

# RENDER SETTINGS
def setupRG():    
    # Set ARNOLD RG
    rgArnold.mergeAOVs.set(1)  
    rgArnold.aiTranslator.set('exr')
    rgArnoldRO.use_existing_tiled_textures.set(1)
    rgArnoldRO.textureMaxMemoryMB.set(4096)
    rgArnoldRO.bucketSize.set(16)
    # Set MAYA RG
    rgCommon.imageFilePrefix.set(fnPrefix) # IMAGE FILE
    rgCommon.startFrame.set(frameStart) # START / END FRAMES
    rgCommon.endFrame.set(getEnd()) 
    rgCommon.outFormatControl.set(0) # NAME.###.EXT
    rgCommon.animation.set(1)
    rgCommon.putFrameBeforeExt.set(1)
    rgCommon.extensionPadding.set(4)
    cams = pm.ls(type = 'camera') # Set rendereble CAMERA
    for i in cams:
        i.renderable.set(0)
    camName = 'E{0}_S{1}Shape'.format(codeSequence, codeShot)
    if pm.ls(camName):
        shotCam = pm.PyNode(camName)
        shotCam.renderable.set(1)
    else:
        pm.warning('No render camera found!')
    # set resolution
    rgRes.width.set(1998)
    rgRes.height.set(1080)
    rgRes.deviceAspectRatio.set(1.85)
    rgRes.pixelAspect.set(1)

    
def setupRES(preset, AA, DIF, GLS, REF, SSS): # Setup HIGH/LOW PRESETS
    if preset == 'HI':
        print 'F I N A L    R E S O L U T I O N'  
        rgRes.width.set(1998)
        rgRes.height.set(1080)
        rgRes.deviceAspectRatio.set(1.85)
        rgRes.pixelAspect.set(1)
    else:
        print 'D R A F T    R E S O L U T I O N'
        rgRes.width.set(720)
        rgRes.height.set(390)
        rgRes.deviceAspectRatio.set(1.85)
        rgRes.pixelAspect.set(1)

    rgArnoldRO.AASamples.set(AA)
    rgArnoldRO.GIDiffuseSamples.set(DIF)
    rgArnoldRO.GIGlossySamples.set(GLS)
    rgArnoldRO.GIRefractionSamples.set(REF)
    rgArnoldRO.GISssSamples.set(SSS)  

def exportAss(frameStart, frameEnd): # codePart codeSequence codeShot codeVersion(FROM FILE VERSION)
    camName = 'E{0}_S{1}Shape'.format(codeSequence, codeShot)
    #frameEnd = getEnd()
    if pm.ls(camName):
        eval('arnoldExportAss -f "{7}3D/data/{0}/{1}/SHOT_{2}/{3}/E{1}_S{2}_{3}.ass" -startFrame {4} -endFrame {5} -cam {6}'.format(codePart, codeSequence, codeShot, codeVersion, frameStart, frameEnd, camName, rootProd))    
    else:
        pm.warning('No render camera found!')
def renderShot(frameStart, frameEnd): # EXPORT ASS SEQUENCE
    frameStart = frameStart.getText() 
    frameEnd = frameEnd.getText() 
    # EXPORT SCENE
    exportAss(frameStart, frameEnd)
    #publishRND() # Publish to FTrack EXR PATH

def publishRND(): # Set path to EXR RENDER in FTRACK
    exr = 'v{2}/E{0}_S{1}_{2}.%04d.exr'.format( codeSequence, codeShot, codeVersion) # Build EXR META DATA for FTrack (v005/E000_S010_005)                
    dna.addMetaShot('EXR', exr, codePart, codeSequence, codeShot) # Add rendered file to FTrack metadata (EXR: v006/E000_S010_006.%04d.exr)         
    
# SMALL UTILITIES
def createDOF(): # Create DOF setup for CAMERA
    i = pm.ls(sl = 1, type = 'transform')
    if i:
        if pm.nodeType(i[0].getShape()) == 'camera':
            pm.pickWalk( d = "down" )# get shapes of selection
            dist = pm.createNode('distanceDimShape')
            dist.getParent().rename('DISTANCE')
            loc = pm.spaceLocator( n = 'FOCUS' )
            loc.scale.set( 100,100,100 )
            print i
            i[0].tx >> dist.startPointX
            i[0].ty >> dist.startPointY
            i[0].tz >> dist.startPointZ
            loc.tx >> dist.endPointX
            loc.ty >> dist.endPointY
            loc.tz >> dist.endPointZ
            dist.distance >> i[0].aiFocusDistance
            print '<<  Created DOF for {}  >>'.format(i[0])
        else:
            print 'SELECT CAMERA!'
    else:
        print 'SELECT CAMERA TRANSFORM!'

def renameNetwork( prefix, name, index): # Rename SHADER NETWORK
    prefix = prefix.getText()
    name = name.getText()
    index = index.getText()
    nameShader = '{0}_{1}_{2}'.format( prefix, name, index)
    if pm.ls(nameShader):
        confirm = pm.confirmDialog ( title = 'Warning!', message = '[ {} ] exists!'.format( nameShader ), button = ['Rename anyway', 'CANCEL'], cancelButton= 'CANCEL', dismissString= 'CANCEL' )
        if confirm == 'CANCEL':
            sys.exit('CANCELED!')
    print 'renameNetwork [shader name]: {}'.format( nameShader )
    SG = pm.ls(sl = 1, type = 'shadingEngine')
    if SG:
        if len(SG) > 1:
            print 'Select Only ONE shading group!'
        else:
            SG = SG[0]
            IN = pm.listHistory(SG) # Create LIST OF SHADING NODES
            mesh = []
            for i in IN: # Remove geometry shapes
                if pm.nodeType(i) == 'mesh':
                    mesh.append(i) 
            for i in mesh:
                IN.remove(i)
            print 'INPUTS: {0}'.format(IN)
            # START RENAME
            SG.rename('{0}SG'.format(nameShader)) # Rename SG
            IN.remove(SG)
            for i in IN: 
                # Rename SHADER
                for m in listShaders:
                    if pm.nodeType(i) == m:
                        i.rename( nameShader )
                        IN.remove(i)
                        bump = pm.listConnections(i, d = False , s = True, type = 'bump2d')
                        if bump:
                            IN.append(bump[0]) # Add BUMP to node list
                if  pm.nodeType(i) == 'displacementShader': 
                    i.rename('DSP_{0}'.format( nameShader))                   
                    IN.remove(i)
                    # Rename DISPLACEMENT INPUT
                    dispIN = i.inputs()
                    if dispIN: # Check id DSP has an input
                        if pm.nodeType(dispIN[0]) == 'file':
                            dispIN[0].rename('IFL_{}_DSP'.format(nameShader))
                            IN.remove(dispIN[0])
                        elif pm.nodeType(dispIN[0]) == 'ramp':
                            dispIN[0].rename('LEV_{}_DSP'.format(nameShader))
                            IN.remove(dispIN[0])
            print 'REST IN: {}'.format( IN )
            for i in IN:                                
                if  pm.nodeType(i) == 'file': # Rename Image File
                    a = i.rename('IFL_{}_CLR'.format(nameShader))                
                elif  pm.nodeType(i) == 'place2dTexture': # Rename Placement
                    i.rename('P2D_{}'.format(nameShader)) 
                elif  pm.nodeType(i) == 'bump2d': # Rename Placement
                    i.rename('BMP_{}'.format(nameShader)) 
                    bumpIN = i.inputs()
                    if bumpIN: # Check id DSP has an input
                        if pm.nodeType(bumpIN[0]) == 'ramp':
                            bumpIN[0].rename('LEV_{}_BMP'.format(nameShader))
                elif  pm.nodeType(i) == 'gammaCorrect': # Rename GAMMA
                        if i.outputs( p = 1 )[0].split('.')[1] == 'color':
                            i.rename('GCR_{}_CLR'.format(nameShader)) 
                        else:
                            i.rename('GCR_{0}_{1}'.format(nameShader, i.outputs( p = 1 )[0].split('.')[1][0:3].upper() )) # LAST 3 LETTERS of connected ATTR
                elif  pm.nodeType(i) == 'ramp': # Rename RAMPS
                    if i.outputs( p = 1 )[0].split('.')[1] == 'specularRoughness':
                        i.rename('LEV_{}_SPR'.format(nameShader)) 
                    elif i.outputs( p = 1 )[0].split('.')[1] == 'KsColor':
                        i.rename('LEV_{}_SPC'.format(nameShader)) 
                    elif i.outputs( p = 1 )[0].split('.')[1] == 'Ks':
                        i.rename('LEV_{}_SPW'.format(nameShader))                     
                    elif i.outputs( p = 1 )[0].split('.')[1] == 'Kd':
                        i.rename('LEV_{}_DIF'.format(nameShader)) 
                    elif i.outputs( p = 1 )[0].split('.')[1] == 'diffuseRoughness':
                        i.rename('LEV_{}_RPH'.format(nameShader)) 
                    else:
                        i.rename('LEV_{0}_{1}'.format( nameShader,i.outputs( p = 1 )[0].split('.')[1][0:3].upper() )) 
                else: # Rename UNSORTED
                    i.rename ('UNS_{}_000'.format(nameShader))
    else:
        print 'Select SHADING GROUP!'
def setupCam():
    cam = pm.ls(sl = 1)[0]
    dna.camSetup(cam)

def baseUI(*args):
    
    if pm.window('RNDManager', q = 1, ex = 1):
        pm.deleteUI('RNDManager')
    win = pm.window('RNDManager', t= 'Render Manager', rtf=True, w = 280, h = 100 )
    with win:
        mainLayout = pm.columnLayout()
        '''
        inputLayout = pm.rowColumnLayout(nc=6, parent = mainLayout) 
        pm.text (l = '  PART  ')
        partField = pm.textField(tx = 'REEL_01', w= 60, h = 30)
        pm.text (l = '    SEQ ')
        sequenceField = pm.textField(tx = '010', w= 45, h = 30)
        pm.text (l = '    SHOT ')
        shotField = pm.textField(tx = '010', w= 45, h = 30)
        pm.separator(h = 5 , style = 'none')        
        createLayout = pm.rowColumnLayout(nc = 1, parent = mainLayout) 
        OPRND = pm.button(l = 'OPEN RENDER SCENE', w = 280, h = 35)
        OPRND.setCommand(pm.Callback (dna.shotOpen, partField, sequenceField, shotField, listRND ))
        pm.separator(h = 6 , style = 'none') 
        '''
        lookdevLayout = pm.rowColumnLayout(nc = 3, parent = mainLayout)
        LD = pm.button(l = 'REF LOOKDEV DATA', w = 200, h = 35)
        LD.setCommand(pm.Callback(ldAdd))
        CAM = pm.button(l = 'CAM', w = 40, h = 35)
        CAM.setCommand(pm.Callback(setupCam))
        DOF = pm.button(l = 'DOF', w = 40, h = 35)
        DOF.setCommand(pm.Callback(createDOF))
        renameLayout = pm.rowColumnLayout(nc = 4, parent = mainLayout)
        prefix = pm.textField(tx = 'GEN', w = 40, h = 30)
        name = pm.textField(tx = 'METAL', w = 80)
        index = pm.textField(tx = 'A', w = 25)
        RN =  pm.button(l = 'RENAME MATERIAL', w = 135)
        RN.setCommand(pm.Callback( renameNetwork, prefix, name, index))
        
        pm.separator(h = 5 , style = 'none')
        matLayout = pm.rowColumnLayout(nc=2, parent = mainLayout)
        ADMAT = pm.button(l = 'ASSIGN MATERIALS', w = 180, h = 45)
        ADMATSEL = pm.button(l = 'FOR SELECTED', w = 100 )
        pm.separator(h = 5 , style = 'none')
        sevrviceLayout = pm.rowColumnLayout(nc=2, parent = mainLayout)
        SELSG = pm.button(l = 'SELECT SG ALL GEO', w = 140, h = 25)
        SELSGSEL = pm.button(l = 'SELECT SG SEL', w = 140 )
        layoutTwo = pm.rowColumnLayout(nc=3, parent = mainLayout)
        createSHW = pm.button(l = 'ADD SHADER ID', w = 90, h = 40)
        deleteSHW = pm.button(l = 'DEL SHADER ID', w = 90, h = 40)
        createOBJ = pm.button(l = 'OBJECT ID', w = 100, h = 40)
        createSHW.setCommand(pm.Callback(runIDS, createMatID_WC))
        deleteSHW.setCommand(pm.Callback(runDelIDs))
        createOBJ.setCommand(createObjID)
        
        assetIDLayout = pm.rowColumnLayout(nc = 1, parent = mainLayout)
        ASTID = pm.button(l = 'ADD ASSETS ID', w = 280, h = 40)
        ASTID.setCommand(pm.Callback(assetIDs))
        pm.separator(h = 5 , style = 'none')
             
        passesLayout = pm.columnLayout(parent = mainLayout)
        createPSS = pm.button(l = 'ADD PASSES', w = 280, h = 30)
        createPSS.setCommand(addAOVSet)
        pm.separator(h = 5 , style = 'none')
        
        settingsLayout = pm.rowColumnLayout(nc =2, parent = mainLayout)
        rsL = pm.columnLayout( parent = settingsLayout)
        RNDSET = pm.button(l = 'RENDER SETTINGS', w = 196, h = 50)
        RNDSET.setCommand(pm.Callback(setupRG))
        hlL = pm.columnLayout( parent = settingsLayout)
        HI = pm.button(l = 'HIGH', w = 80, h = 25)
        HI.setCommand(pm.Callback(setupRES,'HI', 10,1,1,1,3 ))
        LO = pm.button(l = 'LOW', w = 80, h = 25)
        LO.setCommand(pm.Callback(setupRES, 'LO', 4,1,1,1,1 ))
        
        renderLayout = pm.rowColumnLayout(nc = 4, parent = mainLayout)
        start = pm.textField(tx = '101', w = 40)
        endframe = pm.textField(tx = str(getEnd()), w = 40)
        RND =  pm.button(l = 'RENDER SHOT', w = 160, h = 40)
        RND.setCommand(pm.Callback(renderShot, start, endframe))
        PUB =  pm.button(l = 'PUB', w = 40)
        PUB.setCommand(pm.Callback( publishRND ))
        
        ADMAT.setCommand(pm.Callback(matAsign))
        ADMATSEL.setCommand(pm.Callback( matAsignSel ))
        
        SELSG.setCommand(pm.Callback(selSG, 'ALL'))
        SELSGSEL.setCommand(pm.Callback(selSG, 'SEL'))
        
    win.show()

baseUI()
