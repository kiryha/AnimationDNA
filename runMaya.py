# Animation DNA 2.0
# NO FTRACK EDITION
# WRAPPER to RUN MAYA and Setup Maya Environment
# Run from runMaya.bat

import os, subprocess

# Define variables
rootProject = os.path.dirname(__file__).split('PREP\PIPELINE')[0].replace("\\", "/") # Get root of project <P:/FUTURAMA/> from runMaya file 

# Setup  project ENVIRONMENT
os.environ['PYTHONPATH'] = '{0}PREP/PIPELINE/DNA/3D'.format(rootProject)
os.environ['MAYA_SCRIPT_PATH'] = '{0}PREP/PIPELINE/DNA/3D'.format(rootProject) # Setup MEL path to run userSetup.mel
os.environ['MAYA_SHELF_PATH'] = '{0}PREP/PIPELINE/DNA/3D/shelves'.format(rootProject)
os.environ['XBMLANGPATH'] = '{0}PREP/PIPELINE/DNA/3D/icons'.format(rootProject)

# Run MAYA 
cmd = [ 'C:/Program Files/Autodesk/Maya2015/bin/maya.exe', '-hideConsole' ]
subprocess.Popen( cmd ) 

# Prevent closing CMD window
# raw_input()
