import pymel.core as pm
from maya import cmds
import bTools.constants as k


MENU_NAME = k.Module.name


def createCommand(path="bTools", command="main()"):
    return 'exec("import {modulePath}; reload({modulePath}); {modulePath}.{cmd}")'.format(modulePath=path, cmd=command)


def createMenu():
    pm.menu(MENU_NAME, parent="MayaWindow", allowOptionBoxes=True, tearOff=True)
    pm.menuItem("Rebuild Menu", command=createCommand(path="bTools.ui.menu", command="setup()"))
    pm.menuItem("Setup Hotkeys", command=createCommand(path="bTools.utilities.hotkeys", command="setupDefaultHotkeys()"))
    pm.menuItem("HotkeyOptions", command=createCommand(path="bTools.utilities.hotkeys", command="showHotkeyOptionsMenu()"), optionBox=True)
    pm.menuItem(label="Tools", divider=True)
    pm.menuItem("ScriptTree", command=createCommand(path="ScriptTree.ScriptTree", command="main()"))
    # pm.menuItem('Allow Model Thing 1', checkBox=True)
    # pm.menuItem(label="Texturing", divider=True)
    # pm.menuItem("Texture Tool 1", command=createCommand(path="JKeys.rigging", command="main()"))


def setup():
    if pm.menu(MENU_NAME, q=True, exists=True):
        cmds.evalDeferred('cmds.deleteUI("' + MENU_NAME + '")')

    cmds.evalDeferred('import bTools.ui.menu; bTools.ui.menu.createMenu()')





def deleteMenu(menuName):
    """
    This is not used anywhere, but is being kept for posterity
    
    """
    mDict = {}
    for m in pm.lsUI(m=True):
        if m.getLabel():
            mDict[m.getLabel()] = m

    pm.deleteUI(mDict.get(MENU_NAME))


