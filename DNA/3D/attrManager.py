# 256 pipeline tools
# ATTRIBUTES MANAGER
# NO FTRACK EDITION
# create, set and delete custom attributes on objects shapes
import pymel.core as pm

#define RGB colors
R = ( 1, 0, 0 )
G = ( 0, 1, 0 )
B = ( 0, 0, 1 )

# SETUP FLOAT ATTRIBUTES
def addFloatAttr(floatField):
    attrName = floatField.getText().split(' ')
    pm.pickWalk( d = "down" ) # select SHAPES of selected objects
    sel = pm.ls(sl=1 , long = 1)
    for m in sel:
        for i in attrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = m, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(m, ln = "mtoa_constant_" + i, nn = i, dv =1)
def delFloatAttr(floatField):
    attrName = floatField.getText().split(' ')
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1,long=1)
    for m in sel:
        for i in attrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = m, exists = True ):
                pm.deleteAttr(m + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'                

# SETUP STRING ATTRIBUTES
def addStringAttr(stringField):
    attrName = stringField.getText().split(' ')
    pm.pickWalk( d = "down" ) # select SHAPES of selected objects
    sel = pm.ls(sl=1 , long = 1)
    for m in sel:
        for i in attrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = m, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(m, ln = "mtoa_constant_" + i, nn = i, dt = 'string')
def delStringAttr(stringField):
    attrName = stringField.getText().split(' ')
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1,long=1)
    for m in sel:
        for i in attrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = m, exists = True ):
                pm.deleteAttr(m + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!' 
# SETUP COLOR ATTRIBUTE
def addColorAttr(colorField):
    attrName = colorField.getText().split(' ')
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1,long=1)
    for m in sel:
        for i in attrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = m, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(m, ln = "mtoa_constant_" + i, nn = i , uac = 1, at ="float3" )
                pm.addAttr(m, ln = "red_" + i, at = "float", p = "mtoa_constant_" + i )
                pm.addAttr(m, ln = "grn_" + i, at = "float", p = "mtoa_constant_" + i )
                pm.addAttr(m, ln = "blu_" + i, at = "float", p = "mtoa_constant_" + i )            
def delColorAttr(colorField):
    attrName = colorField.getText().split(' ')
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1,long=1)
    for m in sel:
        for i in attrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = m, exists = True ):
                pm.deleteAttr(m + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'
# SETUP ALL ATTR
def addAll(floatField , stringField , colorField):
    addFloatAttr(floatField)
    addStringAttr(stringField)
    addColorAttr(colorField)

def delAll(floatField , stringField , colorField):
    delFloatAttr(floatField)
    delStringAttr(stringField)
    delColorAttr(colorField)               

# SET
def setAttrFloat(floatSetField , floatValField):
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1,long=1)
    for i in sel:
       pm.setAttr( i + '.mtoa_constant_' + floatSetField.getText(), float(floatValField.getText()))
def setAttrString(stringSetField , stringValField):
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1,long=1)
    for i in sel:
       pm.setAttr( i + '.mtoa_constant_' + stringSetField.getText(), stringValField.getText())
def setAttrColor(colorSetField , colorValField):
    pm.pickWalk( d = "down" )
    sel = pm.ls(sl=1,long=1)
    for i in sel:
        if colorValField.getText() == 'R':
            print i + '.mtoa_constant_' + colorSetField.getText()
            pm.setAttr( i + '.mtoa_constant_' + colorSetField.getText(), R)
        elif colorValField.getText() == 'G':
            pm.setAttr( i + '.mtoa_constant_' + colorSetField.getText(), G)
        elif colorValField.getText() == 'B':
            pm.setAttr( i + '.mtoa_constant_' + colorSetField.getText(), B)
        else:
            pm.warning( 'Set one of R, G, B colors!' )
    
def baseUI (): 
    if pm.window('ATM', exists = 1):
        pm.deleteUI('ATM')
    baseWin = pm.window('ATM', t = 'Attribute manager', w = 280, h = 100)
    with baseWin:
        
        mainLayout = pm.columnLayout()
        addLayout = pm.rowColumnLayout(nc=3, parent = mainLayout) 
        floatField = pm.textField(tx = 'mTileUV', w= 120, h = 25)
        ADFL = pm.button(l = 'ADD FLOAT', w = 80, h= 25)
        DLFL = pm.button(l = 'DEL FLOAT', w = 80, h= 25)
        stringField = pm.textField(tx = 'mColor mDisp mMat', w= 120, h = 25)
        ADST = pm.button(l = 'ADD STRING', w = 80, h= 25)
        DLST = pm.button(l = 'DEL STRING', w = 80, h= 25)
        colorField = pm.textField(tx = 'mMask_A', w= 120, h = 25)
        ADCL = pm.button(l = 'ADD COLOR', w = 80, h= 25)
        DLCL = pm.button(l = 'DEL COLOR', w = 80, h= 25)
        
        allLayout = pm.rowColumnLayout(nc = 2, parent = mainLayout)
        ADALL = pm.button(l = 'ADD ALL', w = 140, h= 35)
        DLALL = pm.button(l = 'DELETE ALL', w = 140, h= 35)      
        pm.separator(h = 10 , style = 'none')
        
        setLayout = pm.rowColumnLayout(nc=3, parent = mainLayout)
        floatSetField = pm.textField(tx = 'mTileUV', w= 60, h = 25)
        floatValField = pm.textField(tx = '256', w= 150, h = 25)
        SETFL = pm.button(l = 'SET FLOAT', w = 70, h= 25)
        stringSetField = pm.textField(tx = 'mMat', w= 60, h = 25)
        stringValField = pm.textField(tx = 'GEN_BASE_A', w= 150, h = 25)
        SETST = pm.button(l = 'SET STRING', w = 70, h= 25)
        colorSetField = pm.textField(tx = 'mMask_A', w= 60, h = 25)
        colorValField = pm.textField(tx = 'R', w= 150, h = 25)
        SETCL = pm.button(l = 'SET COLOR', w = 70, h= 25)
        
        
        ADFL.setCommand(pm.Callback (addFloatAttr, floatField)) 
        DLFL.setCommand(pm.Callback (delFloatAttr, floatField))
        ADST.setCommand(pm.Callback (addStringAttr, stringField)) 
        DLST.setCommand(pm.Callback (delStringAttr, stringField)) 
        ADCL.setCommand(pm.Callback (addColorAttr, colorField)) 
        DLCL.setCommand(pm.Callback (delColorAttr, colorField))
        ADALL.setCommand(pm.Callback (addAll, floatField , stringField , colorField)) 
        DLALL.setCommand(pm.Callback (delAll, floatField , stringField , colorField))
        
        SETFL.setCommand(pm.Callback (setAttrFloat, floatSetField , floatValField)) 
        SETST.setCommand(pm.Callback (setAttrString, stringSetField , stringValField)) 
        SETCL.setCommand(pm.Callback (setAttrColor, colorSetField , colorValField)) 
        baseWin.show()  
# baseUI()
