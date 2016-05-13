# 256 pipeline tools
# COMPOSITING branch
# Shot Assembler

import os,glob,nuke,nukescripts, json

version = 1
frameStart = 101
rootProject = os.path.dirname(__file__).split('PREP/PIPELINE/DNA/2D')[0]
rootComp = '{}PROD/2D/COMP/'.format(rootProject)
root3D = '{}PROD/RENDER_3D/RENDER/'.format(rootProject)
rootRND = '{}PROD/RENDER_2D/'.format(rootProject)
rootDic = '{}PREP/PIPELINE/DNA/DIC/'.format(rootProject)
print 'rootProject = {}'.format(rootProject)


def buildShotDic(): # Get data from project database
    global dataShotDic
    dataFile = '{0}dataProject.json'.format(rootDic)
    dataProject = json.load(open(dataFile)) # Build FULL ASSET DICTIONARY of project   
    dataShotDic = {'EXR' : [ ], 'endFrame' : []} # Build shot dic template
    dataShotDic['endFrame'] = dataProject['SHOTS'][codePart][codeSequence]['SHOT_{}'.format(codeShot)]['endFrame']
    dataShotDic['EXR'] = dataProject['SHOTS'][codePart][codeSequence]['SHOT_{}'.format(codeShot)]['EXR']
    return dataShotDic 

def saveNK():# Save Scene and build Nuke scene
    global saveScene
    pathNK  = '{3}{0}/{1}/SHOT_{2}/'.format(codePart, codeSequence, codeShot, rootComp)
    sceneNameFull = '{0}{1}'.format(pathNK, sceneName) 
    print 'saveNK [sceneNameFull] = {}'.format(sceneNameFull) 
    if os.path.isdir(pathNK):
        nuke.scriptSaveAs(sceneNameFull)
        buildScene()
    else:
        os.makedirs(pathNK)
        nuke.scriptSaveAs(sceneNameFull)
        buildScene()

def buildScene(): # Assemble NK scene
    dataShotDic = buildShotDic() 
    exrPath = dataShotDic['EXR']
    endFrame = dataShotDic['endFrame']
    
    # Define Pathes for  Write Nodes
    exrPathFull = '{0}{1}/{2}/SHOT_{3}/MASTER/{4}'.format(root3D, codePart, codeSequence, codeShot, exrPath)
    dpxPathFull = '{3}{4}/{0}/{1}/SHOT_{2}/v{5}/E{1}_S{2}_v{5}.%04d.dpx'.format(codePart, codeSequence, codeShot, rootRND, 'DPX', '[knob VERSION.label]')
    movPathFull = '{3}{4}/{0}/{1}/SHOT_{2}/E{1}_S{2}_v{5}.mov'.format(codePart, codeSequence, codeShot, rootRND, 'MOV','[knob VERSION.label]' )
    nameBase = 'E{0}_S{1}'.format(codeSequence, codeShot)
    reader = nuke.nodes.Read(name = 'REA_E{0}_S{1}'.format(codeSequence, codeShot), file = exrPathFull, first = 101, last = endFrame, xpos = 0, ypos = 0) #creating Reader Node

    dot_A = nuke.nodes.Dot(name = 'DOT', xpos = 34, ypos = 250)
    dot_A.setInput(0, reader)
    dot_B = nuke.nodes.Dot(name = 'DOT', xpos = 184, ypos = 250)
    dot_B.setInput(0, dot_A)

    verser = nuke.nodes.StickyNote(name = "VERSION", xpos = 0, ypos = 380) # Node to DRIVE VESIONS of Nuke renders
    verser['label'].setValue('001')
    # Create WRITE nodes
    writeDPX = nuke.nodes.Write( name ='DPX_E{0}_S{1}'.format(codeSequence, codeShot),file = dpxPathFull, file_type = 'dpx', colorspace='Cineon', first = 101, last = endFrame, xpos = 0, ypos = 300)
    writeDPX.setInput(0, dot_A)
    writeDPX['beforeRender'].setValue("if not os.path.isdir(os.path.dirname(nuke.thisNode()['file'].evaluate())):os.makedirs(os.path.dirname(nuke.thisNode()['file'].evaluate()))") # Create folder for writer output, if its not exists
    writeMOV = nuke.nodes.Write( name ='MOV_E{0}_S{1}'.format(codeSequence, codeShot),file = movPathFull, file_type = 'dpx', colorspace='sRGB', first = 101, last = endFrame, xpos = 150, ypos = 300)
    writeMOV.setInput(0, dot_B)
    writeMOV['beforeRender'].setValue("if not os.path.isdir(os.path.dirname(nuke.thisNode()['file'].evaluate())):os.makedirs(os.path.dirname(nuke.thisNode()['file'].evaluate()))") # Create folder for writer output, if its not exists
    # Setup NK scene
    view = nuke.toNode('Viewer1')
    view['xpos'].setValue( -140 )
    view['ypos'].setValue( 30 )
    nuke.knob('root.first_frame', str(frameStart) )
    nuke.knob('root.last_frame', endFrame)
    nuke.connectViewer(0, reader)
    
def buildNameNk(codePart, codeSequence, codeShot, version): # Build name of Nuke script
    global sceneName
    sceneName = 'E{0}_S{1}_v{2:03d}.nk'.format(codeSequence, codeShot, version)
    print 'buildNameNk [ sceneName ] = {}'.format(sceneName)
    return sceneName

def checkVersion():# Check existed version, return latest version
    sceneName = buildNameNk(codePart, codeSequence, codeShot, version)
    sceneNameFull = '{0}{1}/{2}/SHOT_{3}/{4}'.format(rootComp, codePart, codeSequence, codeShot, sceneName)
    if os.path.exists(sceneNameFull):
        listExisted = glob.glob('{0}{1}/{2}/SHOT_{3}/*.nk'.format(rootComp, codePart, codeSequence, codeShot)) 
        listVersions = []
        for i in listExisted:
            ver = i.split('\\')[-1].split('.nk')[0].split('_v')[-1]   
            listVersions.append(ver)
        global versionCurrent
        versionCurrent = int(max(listVersions))      
        sceneName = buildNameNk(codePart, codeSequence, codeShot, versionCurrent)
    else:
         versionCurrent = 0
         return versionCurrent
    return versionCurrent

def assemble(): # Run assemble procedure: check if NK file exists
    if checkVersion() > 0: 
        if nuke.ask('{}\nEXISTS!\nSave next version?'.format(sceneName)):
            buildNameNk(codePart, codeSequence, codeShot, versionCurrent+1)
            saveNK()
        else:
            saveNK()
    else:
        buildNameNk(codePart, codeSequence, codeShot, 1)
        saveNK()


class assUI( nukescripts.PythonPanel): # UI

    def __init__( self ):
        nukescripts.PythonPanel.__init__( self, 'Shot assembler', 'panel')
        self.reel = nuke.String_Knob("REEL","REEL","REEL_01")
        self.addKnob(self.reel)
        self.seq = nuke.String_Knob("SEQ","SEQ","010")
        self.addKnob(self.seq)
        self.shot = nuke.String_Knob("SHOT","SHOT","010")
        self.addKnob(self.shot)

        self.push = nuke.PyScript_Knob("ASSEMBLE","ASSEMBLE")
        self.addKnob(self.push)

    def knobChanged(self,knob):
        if nuke.thisKnob().name() == "ASSEMBLE":
            global codePart,codeSequence,codeShot #set codePart,codeSequence.codeShot as global variables
            codePart =  self.reel.getValue()
            codeSequence =  self.seq.getValue()
            codeShot =  self.shot.getValue()
            buildShotDic() 
            assemble() 
                             

def assembleRun():
    assUI().show()
# assembleRun()

