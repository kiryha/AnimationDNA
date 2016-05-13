# 256 pipeline tools
# Add custom plugin paths
# Set knob defaults
# Set custom format

import nuke, os
# Get project root (P:/FUTURAMA/)
rootProject = os.path.dirname(__file__).split('PREP/PIPELINE/DNA/2D')[0]


# Set Path to GIZMOS
gizmo = '{}PREP/PIPELINE/DNA/2D/gizmo'.format(rootProject)
nuke.pluginAddPath(gizmo, addToSysPath = False)

# Set paths DNA to scripts 
python  = '{}PREP/PIPELINE/DNA/2D/scripts/'.format(rootProject)
sys.path.append(python)

# Set FORMAT
nuke.addFormat('1998 1080 1.0 KZMRES')
nuke.knobDefault('Root.format', 'KZMRES')
