# 256 pipeline tools
# NO FTRACK EDITION
# Setup Nuke WRAPPER
import os, subprocess

# Get root of project 
rootProject = os.getcwd().split('PREP\PIPELINE')[0].replace("\\", "/") 

# Add DNA menu
os.environ['NUKE_PATH'] = '{0}PREP/PIPELINE/DNA/2D/'.format(rootProject)

# Run Nuke
exe = 'C:/Program Files/Nuke9.0v7/Nuke9.0.exe'
subprocess.Popen( [exe, '--nukex'] )
