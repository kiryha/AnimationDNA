# ANIMATION DNA 2.0 
# TYRANT EDITION
# WRAPPER to run Houdini and Setup Houdini Environment
# Run from runHoudini.bat

import os, subprocess
rootProject = os.path.dirname(__file__).split('PREP\PIPELINE')[0].replace("\\", "/") # Get root of project from runMaya file place ('P:/DNA')
print 'runHoudini [rootProject] {0}'.format(rootProject)

houdini = "C:/Program Files/Side Effects Software/Houdini 16.0.504.20/bin/houdinifx.exe"

# Setup  Houdini ENVIRONMENT
# os.environ['HOME'] = '{0}PREP/PIPELINE/DNA/3D/home'.format(rootProject) # Set variable for the user settings
os.environ['HOUDINI_PATH'] = '{0}PREP/PIPELINE/DNA/3D/path;&'.format(rootProject) # Add custom PATH to a standard HOUDINI_PATH variable (;&). To change MENU, SHELVES, SETTINGS etc.
os.environ['JOB'] = '{0}PROD/3D'.format(rootProject) # Set Houdini project root

# Lunch Houdini
subprocess.Popen( houdini ) 

# Prevent closing CMD window
raw_input()
