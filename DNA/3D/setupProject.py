# ANIMATION DNA 2.0 
# FTrack EDITION
# Set-up current project PATHES and SETTINGS
# FTrack PROJECT NAME should match PROJECT ROOT FOLDER NAME ( pirates  ==  P:/PIRATES/) 

import os, ftrack

# Get ROOT of project from this file ('P:/PIRATES/')
rootProject = os.path.dirname(__file__).split('PREP\PIPELINE\DNA')[0].replace("\\", "/") 
# Get project NAME (PIRATES)
projectName = rootProject.split('/')[-2]
print '<<  setupProject [ rootProject ]: {0} >>'.format(rootProject)

# SETUP PATHES
rootScene = '{0}PROD/3D/scenes/'.format(rootProject)
rootProd = '{0}PROD/'.format(rootProject)
charPath = 'ASSETS/CHARACTERS/'
assetPath = 'ASSETS/PROPS/'
envPath = 'ASSETS/ENVIRONMENTS/'
mlPath = 'LOOKDEV/LIBRARY/MATERIALS/'
llPath = 'LOOKDEV/LIBRARY/LIGHTS/'
rootPB = '{0}PROD/RENDER_3D/BLAST/'.format(rootProject)
rootABC = '{0}PROD/3D/cache/alembic/'.format(rootProject)

# SETUP LISTS
listAttr = ['mColor','mDisp','mMat']
listShaders = [ 'aiStandard' , 'aiSkin' , 'aiHair' , 'aiUtility' , 'alSurface', 'jf_nested_dielectric', 'K_SSS', 'alHair', 'aiRaySwitch'] 
# ASSEMBLER PHASES LISTS
listANM = ['RIG' , 'ANIMATION/' , 'ANM_' ]
listRND = ['GEO', 'RENDER/' , 'RND_' ]

# Setup FTRACK PROJECT
codeProject = projectName.lower() # Get project name in lowercase
project = ftrack.getProject( '{}'.format(codeProject) ) # Get project data from FTrack
