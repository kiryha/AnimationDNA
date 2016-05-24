# Animation DNA 2.0
# NO FTRACK EDITION
# Set-up current project PATHES and SETTINGS

import os

# Get ROOT of project from this file ('P:/PIRATES/')
projectRoot = os.path.dirname(__file__).split('PREP\PIPELINE\DNA')[0].replace("\\", "/") 
# Get project NAME (PIRATES)
projectName = projectRoot.split('/')[-2]
codeProject = projectName.upper()
print '<<  setupProject [ projectRoot ]: {0} >>'.format(projectRoot)

# SETUP PATHES
rootScene = '{0}PROD/3D/scenes/'.format(projectRoot)
rootProd = '{0}PROD/'.format(projectRoot)
charPath = 'ASSETS/CHARACTERS/'
assetPath = 'ASSETS/PROPS/'
envPath = 'ASSETS/ENVIRONMENTS/'
mlPath = 'LOOKDEV/LIBRARY/MATERIALS/'
llPath = 'LOOKDEV/LIBRARY/LIGHTS/'
rootPB = '{0}PROD/RENDER_3D/BLAST/'.format(projectRoot)
rootABC = '{0}PROD/3D/cache/alembic/'.format(projectRoot)
rootDic = '{}PREP/PIPELINE/DNA/DIC/'.format(projectRoot)

# SETUP LISTS
listAttr = ['mColor','mDisp','mMat']
listShaders = [ 'aiStandard' , 'aiSkin' , 'aiHair' , 'aiUtility' , 'alSurface', 'jf_nested_dielectric', 'K_SSS', 'alHair', 'aiRaySwitch'] 
# ASSEMBLER LISTS
listANM = ['RIG' , 'ANIMATION/' , 'ANM_' ]
listRND = ['GEO', 'RENDER/' , 'RND_' ]
