import json
import os.path
import sys

import pymel.core as pm
import b_tools.constants as k
from maya import cmds

SELECTION_SAVE_JSON = "c:/tmp/saved_selection_maya.json"
if not os.path.exists(os.path.dirname(SELECTION_SAVE_JSON)):
    os.makedirs(os.path.dirname(SELECTION_SAVE_JSON))


def move_to_origo(node=None):
    if not node:
        for node in pm.selected():
            move_to_origo(node)
        return
    
    pm.move(node, [0, 0, 0], rpr=True)
    

def move_to_origo_or_weight_hammer():
    if component_is_selected():
        pm.mel.weightHammerVerts()
    else:
        move_to_origo()


def save_selection():
    with open(SELECTION_SAVE_JSON, "w") as fp:
        json.dump(cmds.ls(sl=True, flatten=True), fp, indent=2)


def select_saved_selection():
    with open(SELECTION_SAVE_JSON, "r") as fp:
        saved_sel = json.load(fp)

    existing_saved_sel = [sel for sel in saved_sel if cmds.objExists(sel)]
    if not existing_saved_sel:
        cmds.warning("Could not find any existing objects in the scene matching the saved selection.")
        return

    cmds.select(existing_saved_sel, add=True)


def deselect_saved_selection():
    with open(SELECTION_SAVE_JSON, "r") as fp:
        saved_sel = json.load(fp)

    existing_saved_sel = [sel for sel in saved_sel if cmds.objExists(sel)]
    if not existing_saved_sel:
        cmds.warning("Could not find any existing objects in the scene matching the saved selection.")
        return

    cmds.select(existing_saved_sel, deselect=True)

        
def export_all_to_same_name():
    if not pm.sceneName():
        pm.warning("No scene name has been set for the maya file")
        return

    fbx_path = pm.sceneName().replace(".ma", ".fbx").replace(".mb", ".fbx").replace("\\", "/")
    pm.mel.FBXExportFileVersion(v="FBX201400")
    pm.mel.eval('file -force -options "v=0;" -type "FBX export" -pr -ea "{}";'.format(fbx_path))
    sys.stdout.write("Exported FBX: {}\n".format(fbx_path))


def open_reference_editor():
    if pm.ls(type="reference"):
        pm.mel.ReferenceEditor()
    else:
        pm.mel.CreateReference()


class ComponentTypes:
    vertex = 31
    edges = 32
    faces = 34


def component_is_selected():
    return any(get_selected_components())


def get_selected_components():
    selected_verts = cmds.filterExpand(expand=True, selectionMask=ComponentTypes.vertex) or []
    selected_edges = cmds.filterExpand(expand=True, selectionMask=ComponentTypes.edges) or []
    selected_faces = cmds.filterExpand(expand=True, selectionMask=ComponentTypes.faces) or []
    return selected_verts + selected_edges + selected_faces
