# 256 pipeline tools
# INTERFACE MANIPULATIONS
# Create custom menu for NUKE

import nuke, os,sys
import shotAssembler 


# Add favorite dir
nuke.addFavoriteDir('COMP', '{}PROD/2D/COMP'.format(rootProject))

menubar = nuke.menu('Nuke')
dna = menubar.addMenu('DNA')
dna.addCommand('ASSEMBLER',shotAssembler.assembleRun)
