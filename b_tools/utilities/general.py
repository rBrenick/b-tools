
import sys

import pymel.core as pm
import b_tools.constants as k
from maya import cmds


def move_to_origo(node=None):
    if not node:
        for node in pm.selected():
            move_to_origo(node)
        return
    
    pm.move(node, [0, 0, 0], rpr=True)
    

def move_to_origo_or_weight_hammer():
    selected_components = filter(lambda x: isinstance(x, (pm.MeshVertex, pm.MeshEdge, pm.MeshFace)), pm.selected())
    if not selected_components:
        move_to_origo()
    else:
        pm.mel.weightHammerVerts()


def save_selection():
    pm.optionVar[k.OptionVars.SavedSelection] = cmds.ls(sl=True)


def select_saved_selection():
    saved_sel = pm.optionVar.get(k.OptionVars.SavedSelection)
    if saved_sel:
        cmds.select(saved_sel, add=True)


def deselect_saved_selection():
    saved_sel = pm.optionVar.get(k.OptionVars.SavedSelection)
    if saved_sel:
        cmds.select(saved_sel, deselect=True)

        
def export_all_to_same_name():
    if not pm.sceneName():
        pm.warning("No scene name has been set for the maya file")
        return

    fbx_path = pm.sceneName().replace(".ma", ".fbx").replace(".mb", ".fbx").replace("\\", "/")
    pm.mel.FBXExportFileVersion(v="FBX201400")
    pm.mel.eval('file -force -options "v=0;" -type "FBX export" -pr -ea "{}";'.format(fbx_path))
    sys.stdout.write("Exported FBX: {}\n".format(fbx_path))

