# Animation DNA 2.0
# ASSET MANAGER

import pymel.core as pm
import os, sys

attrList = ['mColor','mDisp','mMat']
sceneNameLong = pm.sceneName()
sPath = os.path.dirname(sceneNameLong)
assDir = 'ASS'
assVer = '_001N.ass'
siVer = '001'


def addMTOAAttr():
    pm.pickWalk( d = "down" )# get shapes of selection
    sel = pm.ls( sl=1 )
    for i in sel:
        if len(i.split('_Prx')) == 1: # EXCLUDE PROXY OBJECT FROM ADD ATTR
            for n in attrList:
                if pm.attributeQuery( "mtoa_constant_" + n, node = i, exists = True ):
                    print 'Attribute ' + n + ' exist!'
                else:
                    pm.addAttr(i, ln = "mtoa_constant_" + n, nn = n, dt = 'string')
        else:
            print 'No attr for proxy'        
           
def copyMTOAAttr(): # COPY ATTRIBUTES FROM LAST SELECTED OBJECTS
    pm.pickWalk( d = "down" ) # get shapes of selection 
    tagert = pm.ls( sl=1 ) 
    source = tagert.pop(-1)
    for m in attrList: # for each MTOA attribute
        attrLong = source + '.mtoa_constant_' + m
        for i in tagert: # copy value for each object
            attrValue = pm.getAttr(attrLong)
            if not pm.attributeQuery( "mtoa_constant_" + m, node = i, exists = True ):
                pm.addAttr(i, ln = "mtoa_constant_" + m, nn = m, dt = 'string')
            if not attrValue == None:
                pm.setAttr(i + ".mtoa_constant_" + m, attrValue ,type = 'string')

def getColor(obj, attr): # get texture name from asigned material
    shadingGroup = pm.listConnections(obj, type='shadingEngine')
    if not pm.listHistory(shadingGroup, type='alSurface'): # GET TEXTURE FROM ALL SHADERS but alSurface
        if attr == 'mtoa_constant_mColor':
            imageFile = pm.listHistory(shadingGroup, type='file')
        else:
            imageDisp = pm.listHistory(shadingGroup, type='displacementShader')
            if imageDisp:
                imageFile = pm.listHistory(imageDisp, type='file')
            else:
                imageFile = None
        if imageFile:
            texture = imageFile[0].attr('fileTextureName').get().replace('\\','/')
            return texture
    else: # Get texture from alSurface
        shader = pm.listHistory(shadingGroup, type='alSurface')
        imf = pm.listConnections( shader[0].diffuseColor )
        if imf:
            texture = imf[0].attr('fileTextureName').get().replace('\\','/')
            return texture
        
def getTXShape(obj): # get texture name from custom attribute on shapes
    string =  obj.attr('mtoa_constant_mColor').get()
    if string: # Check, if attribute has value
        texturePath = string.replace('\\','/').replace('.tx','.jpg') # get JPG full path 
        textureName = texturePath.split('/')[-1].split('.jpg')[0] # get TEXTURE NAME without extension
        return texturePath, textureName      

def txGet(attr, ext): # GET TEXTURE FROM MATERIAL AND ASIGN TO CUSTOM ATTR
    pm.pickWalk( d = "down" ) # get shapes of selection
    sel = pm.ls( sl=1 ) 
    for i in sel: 
        if not pm.attributeQuery(attr, ex = 1, node = i): # check if attribute exists
            for n in attrList: # add  mtoa custom attributes to ASS
                pm.addAttr(i , ln = "mtoa_constant_" + n, nn = n, dt = 'string')
        texture = getColor(i, attr)
        if texture: # Check, if attribute has value
            if not os.path.exists(texture.replace(ext,'.tx')): # check if there is TX TEXTURE exists
                txWarning = pm.confirmDialog( title='Warning', message = 'There is NO TX texture for' + str(i) + '!' , button=['Cancel' , 'Get anyway'], cancelButton='OK' )
                if txWarning == 'Cancel':
                    sys.exit('Convert to TX textures for' + str(i))
            if texture: # SET custom attribute with TEXTURE NAME
                texture = texture.split('sourceimages/')[1].replace(ext,'.tx') 
                i.attr(attr).set(texture)
            else:
                pm.warning('There is NO TEXTURE asigned for ' + str(i))
           
def txShow(): # GET TEXTURE FROM CUSTOM ATTR AND ASIGN MATERIAL TO OBJ WITH TEXTURE 
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1) # get shapes of selection 
    for i in sel:
        if getTXShape(i): # Check, if attribute has value
            texturePath, textureName  = getTXShape(i) # get texture name with path, texture name
            if textureName: # Check, if attribute has value
                if pm.objExists ('PREV_' + textureName):
                    pm.sets(('PREV_' + str(textureName) + 'SG'), forceElement = i)
                else:
                    previewShader = pm.shadingNode ('lambert', asShader = True, n = 'PREV_' + textureName) 
                    previewIF = pm.shadingNode ('file',asTexture = True, n = 'PREV_IF_' + textureName)
                    previewSG = pm.sets (renderable = True, noSurfaceShader = True, empty = True, n = previewShader  + 'SG')
                    previewIF.fileTextureName.set('sourceimages/' + str(texturePath))
                    previewIF.outColor >> previewShader.color
                    previewShader.outColor >> previewSG.surfaceShader
                    pm.sets(previewSG, forceElement = i) 

def txClean(): # DELETE ALL PREVIEW SHADERS
    previewShaders = pm.select("PREV_*", allDagObjects=False, noExpand=True)
    meshes = pm.hyperShade(objects="")
    pm.hyperShade(assign= 'lambert1' )
    pm.select(cl =1)
    previewShaders = pm.select("PREV_*", allDagObjects=False, noExpand=True)
    pm.delete()     

def setMAT(attrField):
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1)
    for i in sel:
        i.mtoa_constant_mMat.set(attrField.getText())

def getMAT(*args):
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1)
    for i in sel:
        shadingGroup = pm.listConnections(i ,type='shadingEngine')
        if shadingGroup:
            i.mtoa_constant_mMat.set(shadingGroup[0].split('SG')[0])


def checkAttr(*args): 
    # CHECK MTOA CUSTOM ATTR                                       
    attrList = [ 'mColor' , 'mMat' ] # attributes to check LIST 
    list = pm.ls(type = 'geometryShape') # select all geo shapes
    setNo = pm.sets(em = 1, name = 'NO_CUSTOM_ATTR' ) # create SET for objecs without custom attributes
    for e in attrList:
        set = pm.sets(em = 1, name = 'EMPTY_' + str(e) ) # create SET for blank ATTR
        for i in list:
            if pm.attributeQuery('mtoa_constant_%s' % e , node = i , ex = 1): # check if attribute exists
                if not i.attr('mtoa_constant_%s' % e ).get(): # check if attribute has any value
                    set.add(i)
            else:
                if not len(i.split('_Prx'))== 2:
                    setNo.add(i)
    # CHECK ATTRIBUTES ON TRANSFORMS                
    transform =  pm.ls(type = 'transform') # select all transforms
    setTRS =  pm.sets(em = 1, name = 'ATTR_TRANS' ) 
    for i in transform:
        if pm.attributeQuery('mtoa_constant_mMat' , node = i , ex = 1): # check if attribute exists
            setTRS.add(i)
    # CHECK BLANK SUBD
    setSBD = pm.sets(em = 1, name = 'NO_SUBDIV' ) 
    listAtrSBD = pm.ls('*.aiSubdivType')
    for i in listAtrSBD:
        if not i.split('.')[0].split('_')[-1] == 'Prx': # remove PROXY object from check
            if i.get() == 0:
                object = pm.PyNode(i.split('.')[0])
                setSBD.add(object)
    # Check SG
    listSG = pm.ls(type = 'shadingEngine')
    listSG.remove('initialParticleSE')
    listSG.remove('initialShadingGroup')
    listFile = pm.ls(type = 'file')
    listSHN =  listFile + listSG
    if listSHN:
        setSHN = pm.sets(em = 1, name = '__(SHN)__' )
    # Check TX
    listAtr = pm.ls('*.mtoa_constant_mColor')
    if listAtr:
        setJPG = pm.sets(em = 1, name = 'ERROR_IN_mColor' )
        for i in listAtr:
            txt = i.get()
            if txt:
                if not txt.split('.')[-1] == 'tx':
                    object = pm.PyNode(i.split('.')[0])
                    setJPG.add(object)
                
                                  
def mayaSmoothOff(geo): # turn MAYA SMOOTH OFF
    pm.setAttr(geo + ".useSmoothPreviewForRender", lock = 0)
    pm.setAttr(geo + ".renderSmoothLevel", lock = 0)
    geo.useSmoothPreviewForRender.set(0)
    geo.smoothLevel.set(2)
    geo.renderSmoothLevel.set(0)   
    pm.setAttr(geo + ".renderSmoothLevel", lock = 1)
    pm.setAttr(geo + ".useSmoothPreviewForRender", lock = 1)

def setSBD(value):
    pm.pickWalk( d = "down" )
    sel = pm.ls( sl=1 )
    for i in sel:
        if value == 'off':
            mayaSmoothOff(i)
        elif value == 0:
            i.aiSubdivType.set(0)
        else: 
            mayaSmoothOff(i)
            i.aiSubdivType.set(1)
            i.aiSubdivIterations.set(value)  
# ORGANIZE ASSET
def lockTRS(asset): # lock TRANSFORM for input asset
    asset.translate.lock() 
    asset.rotate.lock()
def buildNameAsset (sel):  # GET ASSET NAME AND VARIATION. Support <name>, <name_A>,  <name_A_part>
    if len(sel[0].split('_')) == 1: # if name is <name>
        assetName = sel[0] 
        assetVar = ''
    elif len(sel[0].split('_')) == 2: # if name is <name_part> or <name_A>
        if len(sel[0].split('_')[1]) == 1: # <name_A>
            assetName = sel[0].split('_')[0] 
            assetVar = '_' + str(sel[0].split('_')[1])    
        else: #  <name_part>
            assetName = sel[0].split('_')[0] 
            assetVar = ''
    else: # if  <name_A_part>
        assetName = sel[0].split('_')[0] 
        assetVar = '_' + str(sel[0].split('_')[1])        

        
    return assetName, assetVar

def assetOrganize():
    sel = pm.ls(sl = 1)
    assetName, assetVar = buildNameAsset(sel)
    grpGeo = pm.group( sel, n = assetName + assetVar + '_Geo') # CREATE HIERARCITY
    grpAsset =  pm.group( grpGeo , n = assetName + assetVar + '_001')
    lockTRS(grpGeo) # LOCK transform
    for i in sel:
        lockTRS(i)

def assetPrxOrganize():
    sel = pm.ls(sl = 1)
    prx = sel.pop(-1)
    assetName, assetVar = buildNameAsset(sel)
    prx.rename(assetName + assetVar + '_001') # rename proxy
    prx.getShape().rename(assetName + assetVar + '_Prx') # rename proxy shape
    grpGeo = pm.group( sel, n = assetName + assetVar + '_Geo') # CREATE HIERARCITY
    pm.parent(grpGeo , prx)
    lockTRS(grpGeo) # LOCK transform
    for i in sel:
        lockTRS(i)        

def assetDynOrganize():
    sel = pm.ls(sl = 1)
    assetName, assetVar = buildNameAsset(sel)
    # CREATE HIERARCITY        
    grpGeo = pm.group( sel, n = assetName + assetVar + '_GEO')
    grpRig = pm.group( em=True, n = assetName + assetVar + '_RIG')
    grpAsset =  pm.group( grpGeo , n = assetName + assetVar )
    lockTRS(grpGeo) # LOCK transform
    pm.parent(grpRig, grpAsset)
    
def switchProxy(*args):
	sel = pm.ls(sl = 1)
	if sel: #check if any asset selected
		sel = pm.ls(sl = 1)[0]
		child = pm.listRelatives(c = 1)
		
		if child[0].visibility.get() == 1:
			child[0].visibility.set(0)
			child[1].visibility.set(1)
		else:
			child[0].visibility.set(1)
			child[1].visibility.set(0)    
	else:
		geo = pm.ls('*_Ass')+ pm.ls('*:*_Ass') + pm.ls('*_Geo')+ pm.ls('*:*_Geo')
		prx = pm.ls('*_Prx') + pm.ls('*:*_Prx')
		if (geo[0].visibility.get() == 1):
			for (i,e) in zip(geo,prx):
				i.visibility.set(0)
				e.visibility.set(1)
		else:
			for (i,e) in zip(geo,prx):
				i.visibility.set(1)
				e.visibility.set(0)

def switchStandin(*args): # switch STANDIN DISPLAY MODE   BOUNDING BOX/SHADED POLYWIRE
	sel = pm.ls(sl = 1)
	if sel: #check if any asset selected
	    sel = pm.ls(sl = 1)[0]
	    child = pm.listRelatives(c = 1)
	    if (child[0].mode.get()) == 0:
	        for i in child:
	            i.mode.set(5)
	    else:
	        for i in child:
	            i.mode.set(0)

	else:
	    sel = pm.ls(type = 'aiStandIn')
	    if sel[0].mode.get() == 0:
	        for i in sel:
	            i.mode.set(5)
	    else:
	        for i in sel:
	            i.mode.set(0)

def delUnlock(): # UNLOCK node and DEL
    confirm = pm.confirmDialog ( title = 'SURE TO DELETE? ', message = 'Sure you want to DELETE selected?!', 
                                         button=['DELETE', 'CANCEL'],
                                         defaultButton= 'CANCEL',
                                         cancelButton= 'CANCEL',
                                         dismissString= 'CANCEL' )
    if confirm == 'DELETE':
        sel = pm.ls( sl = True )
        for i in sel:
            i.unlock()
            pm.delete(i)
        print 'OBJECT DELETED: ' + str(sel)
    else:
        sys.exit()

        	            				                
def geoToAsset(): # CONVERT GEO ASSET OO STANDIN ASSET
   
    def SI(asset, siVer): # create name for STAND IN file
        siName = asset[0].split('_') 
        del siName[-1]
        siName = str(siName[0]) + '_' + str(siName[1]) + '_SI_' + siVer + '.mb'
        siSceneExport = os.path.join(sPath + '/SI/', siName).replace('\\' , '/')
        return siSceneExport
     
    def copyMTOAAttr(srcGeo,standIn): # copy mtoa attributes from render geo to standIn
        for n in attrList: # add  mtoa custom attributes to ASS
                pm.addAttr(standIn.getShape(), ln = "mtoa_constant_" + n, nn = n, dt = 'string')
        for m in attrList: # copy custom attribute values to ASS
            attrLong = srcGeo.getShape() + '.mtoa_constant_' + m
            attrValue = pm.getAttr(attrLong)
            if not attrValue == None:
                pm.setAttr(standIn.getShape() + ".mtoa_constant_" + m, attrValue ,type = 'string')
    
    def checkHR(geoName): # setup display of STAND INs
        if geoName.split('_')[-1] == 'Hrs':
            return 4 # POINT COLUD mode for ASS DISPLAY
        else:
            return 2 # POLYWIRE cloud mode for ASS DISPLAY
           
    def switchToStandIn(renderGeometry):
        rndGeoName = (pm.ls(sl = 1)[0]).split('_Geo')
        rndAssName = str(rndGeoName[0]) + '_Ass'
        assList = []
        for geo in list: #export ass from selected group 
            
            assName = geo + assVer
            assExport = os.path.join(sPath, assDir, assName ).replace('\\' , '/')
            mayaSmoothOff(geo)
            pm.select(geo)
            pm.hyperShade(assign= 'lambert1' )
            pm.exportSelected(assExport, force = 1)
            pm.importFile(assExport) #import ass and rename
            standIn = pm.PyNode('ArnoldStandIn')
            
            standIn.rename('ASS_' + geo)
            standIn.mode.set(0) #set standIn display mode
            copyMTOAAttr(geo,standIn) # copy mtoa attributes from render geo to standIn
            assList.append(standIn)
            standIn.translate.lock() # lock TRANSFORM for STANDIN
            standIn.rotate.lock()
        standInGRP = pm.group(assList, n = rndAssName)
        standInGRP.translate.lock()
        standInGRP.rotate.lock()
        pm.parent(standInGRP,asset)
        pm.parent(rndGeo, w=1) #Unparent Render geo
        pm.select(asset)
        if os.path.exists(SI(asset, siVer)):
            confirm = pm.confirmDialog ( title='File exists!', message = str(SI(asset, siVer)).split('/')[-1], 
                                         button=['OVERWRITE', 'CANCEL'],
                                         defaultButton= 'OVERWRITE',
                                         cancelButton= 'CANCEL',
                                         dismissString= 'CANCEL' )
            if confirm == 'OVERWRITE':
                siExport = pm.exportSelected(SI(asset, siVer), force = 1) #export SI file
                print 'ASSET OVERWRITEN TO: ' + str(siExport)
            else:
                print 'CANCELED!'
                sys.exit()
        else:
            siExport = pm.exportSelected(SI(asset, siVer), force = 1) #export SI file
            print 'ASSET CONVERTED TO: ' + str(siExport)
    
    asset = pm.ls(sl = 1)
    rndGeo = pm.listRelatives(c = 1, type = 'transform') #select Render geo group
    pm.select(rndGeo)
    list = pm.listRelatives(c = 1, type = 'transform') #check if selected is a group or single mesh
    if list: #check if render geo is single mesh or group
        switchToStandIn(rndGeo)
    else:
        list = rndGeo
        switchToStandIn(rndGeo)

# SMALL TOOLS
def selectInstances():
    pm.select(pm.ls(ap = 1, dag = 1, sl = 1 ))
def boundingBox():
    pm.pickWalk(d ='down')
    sel = pm.ls(sl = 1, shapes = 1, selection = 1)
    if (sel[0].overrideEnabled.get() == 0):
        for i in sel:
            i.overrideEnabled.set(1) 
            i.overrideLevelOfDetail.set(1)
    else:
        for i in sel:
            i.overrideEnabled.set(0) 
            i.overrideLevelOfDetail.set(0)
            
# CURVE EDITOR     
def shaderAsign(): # Asign SHADER to CURVES
    # select curves, SHIFT select shader, run
    sel = pm.ls( sl=1 )
    mat = sel.pop( -1 ) 
    for i in sel:
        if i.nodeType() == 'transform':
            i = i.getShape()
        mat.outColor >> i.aiCurveShader
        print 'CONNECTED {0} >> {1}'.format( mat,i )
    print 'Connecting shaders DONE!'
def setRND(stat): # Set Render Curve attr on/off (stat = 0/1)
    sel = pm.ls( sl=1 )
    for i in sel:
        if i.nodeType() == 'transform':
            i = i.getShape()
        i.aiRenderCurve.set(stat)    
def setWidth(width): # Set curve width
    sel = pm.ls( sl=1 )
    for i in sel:
        if i.nodeType() == 'transform':
            i = i.getShape()
        i.aiCurveWidth.set(float(width.getText()))    
def setMode(mode): # Set curve render mode
    sel = pm.ls( sl=1 )
    for i in sel:
        if i.nodeType() == 'transform':
            i = i.getShape()
        i.aiMode.set(mode)
def setOpaque(stat): # Set curve transparency
    sel = pm.ls( sl=1 )
    for i in sel:
        if i.nodeType() == 'transform':
            i = i.getShape()
        i.aiOpaque.set(stat)


def curvesUI(): 
    if pm.window('CRV', exists = 1):
        pm.deleteUI('CRV')
    baseWin = pm.window('CRV', t = 'Curve manager', w = 280, h = 100)
    with baseWin:
        
        mainLayout = pm.columnLayout()
        attrLayout = pm.rowColumnLayout(nc=1, parent = mainLayout) 
        asign = pm.button(l = 'ASIGN MATERIAL', w = 280, h= 50)
        asign.setCommand(pm.Callback ( shaderAsign )) 
        pm.separator(h = 5 , style = 'none')
        
        sbdLayout = pm.rowColumnLayout(nc=2, parent = mainLayout) 
        rndOn = pm.button(l = 'RENDER ON', w = 140, h = 30)
        rndOff = pm.button(l = 'RENDER OFF', w = 140)
        rndOn.setCommand(pm.Callback (setRND, 1))
        rndOff.setCommand(pm.Callback (setRND, 0))
        pm.separator(h = 5 , style = 'none')
        
        colorLayout = pm.rowColumnLayout(nc=3, parent = mainLayout) 
        setRib = pm.button(l = 'RIBON', w = 93, h = 40)
        setThic = pm.button(l = 'THIC', w = 94)
        setOri = pm.button(l = 'ORIENTED', w = 93)
        setRib.setCommand(pm.Callback (setMode, 0))
        setThic.setCommand(pm.Callback (setMode, 1))
        setOri.setCommand(pm.Callback (setMode, 2))
        pm.separator(h = 5 , style = 'none')
        
        matLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout) 
        opOn = pm.button(l = 'OPAQUE ON', w = 140, h = 30)
        opOff = pm.button(l = 'OPAQUE OFF', w = 140)
        opOn.setCommand(pm.Callback (setOpaque, 1))
        opOff.setCommand(pm.Callback (setOpaque, 0))
        pm.separator(h = 5 , style = 'none')
        
        matLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout)   
        attrField = pm.textField(tx = '0.1', w= 90, h = 30) 
        setW = pm.button(l = 'SET WIDTH', w = 190)
        setW.setCommand(pm.Callback (setWidth, attrField))
       
    baseWin.show()  

def lineUp(): # Translate assets along X axix in LINE 
    sel = pm.ls( sl=1 )
    dicAssets = {}     
    dev = 1.5
    transX = 0
    
    for i in sel: # Get name and parameters for all seleceted assets( width,depth,height of boundingBox )
        dicAssets.keys().append(i) 
        dicAssets[i.name()] = {'width':[],'height':[],'depth':[]}
        dicAssets[i.name()]['width'].append(i.getBoundingBox().width())
        dicAssets[i.name()]['height'].append(i.getBoundingBox().height())
        dicAssets[i.name()]['depth'].append(i.getBoundingBox().depth())         
    
    i = 0
    while i < len(sel): 
        nameAsset = sel[i].name()
        if i == 0: # First element should stay at zero point
            value = transX
        else: # Another element will be distributed across x axis
            nameAssetPrev = sel[i-1].name()
            value = transX + dicAssets[nameAsset]['width'][0]/dev + dicAssets[nameAssetPrev]['width'][0]/dev
            transX = value 
        pm.setAttr(nameAsset + '.translateX', value)
        i += 1   
                      
def baseUI (): 
    if pm.window('LDM', exists = 1):
        pm.deleteUI('LDM')
    baseWin = pm.window('LDM', t = 'Asset manager', w = 280, h = 100)
    with baseWin:
        
        mainLayout = pm.columnLayout()
        attrLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout) 
        ADD = pm.button(l = 'ADD ATTR', w = 140, h= 30)
        COP = pm.button(l = 'COPY ATTR', w = 140, h= 30)
        ADD.setCommand(pm.Callback (addMTOAAttr)) 
        COP.setCommand(pm.Callback (copyMTOAAttr))        
        
        smallLayout = pm.rowColumnLayout(nc = 4, parent = mainLayout) 
        LIN = pm.button(l = 'LINE', w = 100, h= 30)
        LIN.setCommand(pm.Callback (lineUp))
        CRV = pm.button(l = 'CRV', w = 60)
        CRV.setCommand(pm.Callback (curvesUI))
        SI = pm.button(l = 'SI', w = 60)
        SI.setCommand(pm.Callback (selectInstances))
        BBOX = pm.button(l = 'BBOX', w = 60)
        BBOX.setCommand(pm.Callback (boundingBox))
        
        pm.separator(h = 5 , style = 'none')
        
        sbdLayout = pm.rowColumnLayout(nc=6, parent = mainLayout) 
        SOF = pm.button(l = 'MAYA SMOOTH OFF', w = 130, h = 40)
        DIV0 = pm.button(l = '0', w = 30, h = 40)
        DIV1 = pm.button(l = '1', w = 30, h = 40)
        DIV2 = pm.button(l = '2', w = 30, h = 40)
        DIV3 = pm.button(l = '3', w = 30, h = 40)
        DIV4 = pm.button(l = '4', w = 30, h = 40)
        pm.separator(h = 5 , style = 'none')
        
        colorLayout = pm.rowColumnLayout(nc=3, parent = mainLayout) 
        TXGET = pm.button(l = 'GET COLOR', w = 80, h = 40)
        DSGET = pm.button(l = 'GET DISPL', w = 80)
        GETMAT = pm.button(l = 'GET MATERIAL', w = 120)
        matLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout) 
        TXSHOW = pm.button(l = 'SHOW TX', w = 140, h = 30)
        TXCLN = pm.button(l = 'CLEAN TX', w = 140)
        matLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout)   
        attrField = pm.textField(tx = 'GEN_BASE_A', w= 90, h = 30) 
        SETMAT = pm.button(l = 'SET MATERIAL', w = 190)
        pm.separator(h = 6 , style = 'none')

        orgLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout)   
        PRG = pm.button(l = 'SETUP STATIC', w = 140, h = 45)
        DYN = pm.button(l = 'SETUP DYNAMIC', w = 140)
        PRG.setCommand(pm.Callback (assetPrxOrganize))
        DYN.setCommand(pm.Callback (assetDynOrganize))
        pm.separator(h = 6 , style = 'none')
              
        checkLayout = pm.rowColumnLayout(nc=4, parent = mainLayout) 
        PRX = pm.button(l = 'PROXY', w = 60, h= 40)
        SI = pm.button(l = 'STANDIN', w = 60, h= 40)
        CHK = pm.button(l = 'CHECK SCENE', w = 130, h= 40)
        DEL = pm.button(l = 'DEL', w = 30, h= 40)
        CHK.setCommand(pm.Callback (checkAttr)) 
        DEL.setCommand(pm.Callback (delUnlock)) 
        pm.separator(h = 15 , style = 'none')
        
        convertLayout = pm.rowColumnLayout(nc=1, parent = mainLayout) 
        GTA = pm.button(l = 'CONVERT TO STANDIN', w = 280, h= 50)
        
        SOF.setCommand(pm.Callback (setSBD, 'off'))
        DIV0.setCommand(pm.Callback (setSBD, 0))
        DIV1.setCommand(pm.Callback (setSBD, 1))
        DIV2.setCommand(pm.Callback (setSBD, 2))
        DIV3.setCommand(pm.Callback (setSBD, 3))
        DIV4.setCommand(pm.Callback (setSBD, 4))
        
        TXGET.setCommand(pm.Callback (txGet, 'mtoa_constant_mColor', '.jpg'))
        DSGET.setCommand(pm.Callback (txGet, 'mtoa_constant_mDisp', '.exr'))
        TXSHOW.setCommand(pm.Callback (txShow))
        TXCLN.setCommand(pm.Callback (txClean))
        SETMAT.setCommand(pm.Callback (setMAT, attrField))
        GETMAT.setCommand(pm.Callback (getMAT))

        
        PRX.setCommand(pm.Callback (switchProxy))
        SI.setCommand(pm.Callback (switchStandin))
        GTA.setCommand(pm.Callback (geoToAsset))
    baseWin.show()  
# baseUI()
