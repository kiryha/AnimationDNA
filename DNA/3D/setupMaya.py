# 256 pipeline tools
# NO FTRACK EDITION
# Setup Maya Settings
# This file runs from userSetup.mel 

import pymel.core as pm
import os
from setupProject import *

print '<<  setupMaya [ projectName ]: {0}  >>'.format(projectName)

# Set project in Maya
pm.mel.eval(' setProject "{0}PROD/3D/"'.format(projectRoot)) 
