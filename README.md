# bTools
Maya Tools Module

Includes some convenience stuff for Technical Animation folk (mostly made this for me so I'd have access to all my convenience things wherever)

# Install options

<pre>
Run install_maya_mod.bat (will create a .mod file in your maya/modules folder)
Restart Maya
</pre>


# Start the tool
<pre>

# The following lines are in the userSetup.py so no startup script is required.

import bTools.ui.menu
bTools.ui.menu.setup()

</pre>

bTools menu is now in Mayas menu bar

![image showing where to find the bTools menu in the menubar](https://raw.githubusercontent.com/rBrenick/bTools/master/docs/example_image.png)
