import re
import sys
import traceback

import b_tools.constants as k
import pymel.core as pm

"""

# Examples

# Simple
for tgt in pm.selected():
    ctrl = createCtrl(tgt)

    
# Chain
previousCtrl = None
for tgt in pm.selected():
    ctrl = createCtrl(tgt)
    
    if previousCtrl:
        ctrl.getParent().setParent(previousCtrl)
    previousCtrl = ctrl

    
# OffsetGrp
createOffsetGrp(pm.selected()[0])





def createCtrl(targetNode=None):
    tgt = pm.selected()[0]                                        # Gets the first selected item and sets it as the target
    ctrlName = tgt.nodeName()+"_CTRL"                             # Creates a nice name for the controller

    ctrl = pm.circle(normal=[1, 0, 0], name=ctrlName)[0]          # Creates a Nurbs Circle as the control
    offsetGrp = pm.group(empty=True, name=ctrlName+"_offsetGrp")  # Creates the offsetGrp
    ctrl.setParent(offsetGrp)                                     # Sets the controllers parent to be the offset Grp
    pm.matchTransform(offsetGrp, tgt)                             # Matches the transform of the offsetGrp and the target
    pm.parentConstraint(ctrl, tgt)                                # Constrains the target to the controller
    
def superBasicControl():
    tgt = pm.selected()[0]
    ctrlName = tgt.nodeName()+"_CTRL"

    ctrl = pm.circle(name=ctrlName)[0]
    offsetGrp = pm.group(empty=True, name=ctrlName+"_offsetGrp")
    ctrl.setParent(offsetGrp)
    pm.matchTransform(offsetGrp, tgt)
    pm.parentConstraint(ctrl, tgt)
        

"""


def get_unique_name(target_name):
    if pm.objExists(target_name) and not target_name[-1].isdigit():
        target_name += "_1"
        
    if pm.objExists(target_name):
        finalDigit = int(re.findall("[0-9]+", target_name)[-1])
        noNumber = target_name[:-len(str(finalDigit))]
        target_name = noNumber + str(finalDigit + 1)
    
    if pm.objExists(target_name):
        target_name = get_unique_name(target_name)
    
    return target_name
    
    
def create_ctrl(node=None):

    tgt = "NAME"
    
    if node:
        tgt = node.name()
        
    else:
        sel = pm.selected(type="transform")
        if sel:
            ctrls = []
            for node in sel:
                ctrls.append(create_ctrl(node))
            return ctrls
        
    ctrl_name = get_unique_name(tgt + "_CTRL")
    ctrl = pm.circle(normal=[1, 0, 0], name=ctrl_name)[0]
    offset_grp = pm.group(empty=True, name=ctrl_name+"_offsetGrp")
    spaces_grp = pm.group(empty=True, name=ctrl_name+"_spacesGrp")
    spaces_grp.setParent(offset_grp)
    ctrl.setParent(spaces_grp)
    if node:
        pm.matchTransform(offset_grp, tgt)
        pm.parentConstraint(ctrl, tgt)
    
    ctrl.setAttr("scaleX", lock=True, keyable=False)
    ctrl.setAttr("scaleY", lock=True, keyable=False)
    ctrl.setAttr("scaleZ", lock=True, keyable=False)
    ctrl.setAttr("visibility", lock=True, keyable=False)
    
    return ctrl


def create_offset_grp(tgt=None):
    if not tgt:
        tgt = pm.selected(type="transform")[0]
    
    offset_grp = pm.group(empty=True, name=tgt.nodeName()+"_offsetGrp")
    offset_grp.setParent(tgt.getParent())
    offset_grp.setTranslation(tgt.getTranslation())
    offset_grp.setRotation(tgt.getRotation())
    tgt.setParent(offset_grp)
    return offset_grp
    
    
def chain_fk():
    # Chain create FK Controls
    previous_ctrl = None
    for tgt in pm.selected():
        ctrl = create_ctrl(tgt)
        
        if previous_ctrl:
            ctrl.getParent().setParent(previous_ctrl)
        previous_ctrl = ctrl
        
    
def connect_skeletons():
    driver, driven = pm.selected()

    driver_skel = driver.getChildren(allDescendents=True, type="joint")
    driven_skel = driven.getChildren(allDescendents=True, type="joint")

    for src, tgt in zip(driver_skel, driven_skel):
        src.r >> tgt.r
        src.t >> tgt.t
        src.s >> tgt.s


# Marking Menu Things

def create_locator_around_selected():
    sel_transforms = pm.selected(type="transform")
    loc = pm.spaceLocator()
    
    if sel_transforms:
        loc.rename(get_unique_name(sel_transforms[0].name() + "_LOC"))
        consts = []
        for node in sel_transforms:
            consts.append(pm.parentConstraint(node, loc))
        pm.delete(consts)
        
    return loc

    
def create_single_joint():
    jnt = pm.joint()
    jnt.rename("Left")
    jnt.setAttr("jointOrientX", keyable=True)
    jnt.setAttr("jointOrientY", keyable=True)
    jnt.setAttr("jointOrientZ", keyable=True)


def select_lods():
    lod_steps = pm.ls("lod*")
    lod0s = pm.ls("lod0*")
    pm.select([x for x in lod_steps if x not in lod0s])

    
def select_constraint_source(node=None):
    if not node:
        for node in pm.ls(sl=True):
            select_constraint_source(node)
        return

    con_types = ["pointConstraint", "parentConstraint", "orientConstraint", "aimConstraint", "scaleConstraint"]

    if node.type() in con_types:
        select_target = pm.listConnections(node+".target[0].targetParentMatrix")
    else:
        select_target = pm.listConnections(node+".parentInverseMatrix")
        
    if not select_target:
        select_target = pm.listConnections(type="constraint")
    
    if not select_target:
        select_target = node.translate.connections()
        
    if not select_target:
        select_target = node.rotate.connections()
    
    if select_target:
        pm.select(select_target)


# Hotkey Things

def is_skinning():
    state = False
    ctx = pm.currentCtx()
    if pm.contextInfo(ctx, q=True, c=True) == "artAttrSkin":
        return True
    return False

    
def component_is_selected():
    sel = pm.selected()[0]
    skinComps = [pm.general.MeshVertex, pm.general.MeshFace, pm.general.MeshEdge]
    return sel.__class__ in skinComps

    
def freeze_translation():
    pm.mel.channelBoxCommand(freezeTranslate=None)
    
    
def freeze_rotation():
    pm.mel.channelBoxCommand(freezeRotate=None)
    
    
def freeze_scale():
    pm.mel.channelBoxCommand(freezeScale=None)
    
    
# Curves
def get_curve_params(crv):
    params = dict()
    params["knot"] = crv.getKnots()
    params["point"] = [list(c) for c in crv.getCVs()]
    params["degree"] = crv.degree()
    if crv.form() == "periodic":
        params["periodic"] = True
    return params


def scale_curve(crv, vec3_mult=(1, 1, 1)):
    if not isinstance(crv, pm.nt.NurbsCurve):
        return 
        
    info = get_curve_params(crv)
    
    cvs = crv.getCVs()
    
    for i, cv in enumerate(cvs):
        cvs[i] = cv * vec3_mult
        
    info["point"] = cvs
    
    pm.curve(crv, replace=True, **info)
    

def scale_selected_curve(vec3_mult=(1, 1, 1), scale_mult=1):
    crvs = []
    for node in pm.selected():
        if not isinstance(node, pm.nt.NurbsCurve):
            for shp in node.getShapes():
                crvs.append(shp)
        else:
            crvs.append(node)
    
    vec3_mult = list(vec3_mult)
    for i, point in enumerate(vec3_mult):
        vec3_mult[i] = point * scale_mult
    
    for crv in crvs:
        scale_curve(crv, vec3_mult=vec3_mult)

        
def mirror_selected_curves():
    scale_selected_curve(vec3_mult=[1, 1, -1])


def increment_scale_selected_curve(positive=True):
    if positive:
        scale_selected_curve(scale_mult=1.1)
    else:
        scale_selected_curve(scale_mult=0.9)
        
        
# Display

def toggle_joints_in_viewport():
    focused_panel = pm.getPanel(withFocus=True)
    
    if "modelPanel" in focused_panel:
        set_value = not pm.modelEditor(focused_panel, q=True, joints=True)
        pm.modelEditor(focused_panel, e=True, joints=set_value)
        

def toggle_joints_x_ray():
    focused_panel = pm.getPanel(withFocus=True)
    
    if "modelPanel" in focused_panel:
        set_value = not pm.modelEditor(focused_panel, q=True, jointXray=True)
        pm.modelEditor(focused_panel, e=True, jointXray=set_value)
        if set_value:
            pm.modelEditor(focused_panel, e=True, joints=set_value)
            

# Skinning

def copy_vertex_weight_or_key():
    if component_is_selected():
        pm.mel.artAttrSkinWeightCopy()
    else:
        pm.mel.timeSliderCopyKey()


def paste_vertex_weight_or_key():
    if component_is_selected():
        pm.mel.artAttrSkinWeightPaste()
    else:
        pm.mel.timeSliderPasteKey(False)


def set_key_or_scale_skinweights(weight_value=1.1):
    if is_skinning():
        ctx = pm.currentCtx()
        pm.artAttrSkinPaintCtx(ctx, e=True, selectedattroper="scale")
        if weight_value > 1:
            pm.artAttrSkinPaintCtx(ctx, e=True, maxvalue=weight_value)
        pm.artAttrSkinPaintCtx(ctx, e=True, value=weight_value)
        pm.artAttrSkinPaintCtx(ctx, e=True, clear=True)
        
    else:
        pm.mel.SetKey()
        

def select_skin_vertices_or_play():
    if is_skinning():
        pm.mel.artSkinSelectVertices("artAttrSkinPaintCtx", 0, 0)
    else:
        pm.mel.PlaybackToggle()
        # pm.mel.dR_DoCmd("pointSnapPress")
        
        
def deselect_skin_vertices_or_unsnap_vertices():
    if is_skinning():
        sel_mesh = pm.ls(sl=True, type="transform")
        if not sel_mesh:
            sel_mesh = pm.selected()[0].node().getTransform()
        pm.select(sel_mesh, replace=True)
    else:
        pm.mel.dR_DoCmd("pointSnapRelease")
        
        
def smooth_skin_or_hik_full_body_key():
    if is_skinning():
        ctx = pm.currentCtx()
        pm.artAttrSkinPaintCtx(ctx, e=True, selectedattroper="smooth")
        pm.artAttrSkinPaintCtx(ctx, e=True, clear=True)
    else:
        pm.mel.HIKSetFullBodyKey()


def select_influence_below_or_go_to_min_frame(weight_value=None):
    if is_skinning():
        ctx = pm.currentCtx()

        if not weight_value:
            weight_value = pm.optionVar.get(k.OptionVars.SelectVerticesBelowInfluence, 0.01)

        pm.mel.artSkinSelectVertices("artAttrSkinPaintCtx", 0, 0)  # Select affected vertices

        sel = pm.selected()
        target_joint = pm.artAttrSkinPaintCtx(ctx, q=True, influence=True)
        sel_mesh = sel[0].node().getTransform()
        skincluster = pm.PyNode(pm.mel.findRelatedSkinCluster(sel_mesh))
        
        if not skincluster:
            pm.warning("No Skin Cluster found from selection")
            return
        
        get_data = skincluster.getPointsAffectedByInfluence(target_joint)
        weight_data = get_data[1]
        vert_data = []
        if len(get_data[0]) > 0:
            for each in get_data[0][0]:
                 vert_data.append(each.currentItemIndex())
                 
        sel_list = []
        for vert, weight in zip(vert_data, weight_data):
            if weight < weight_value:
                sel_list.append(sel_mesh.name()+".vtx[{}]".format(vert))
                
        if not sel_list:
            sys.stdout.write("No Vertices found below value: {}\n".format(weight_value))
            deselect_skin_vertices_or_unsnap_vertices()
            return

        pm.select(sel_list, replace=True)
        
    else:
        pm.mel.GoToMinFrame()

        
def delete_history_or_remove_skinning():
    if is_skinning():
        ctx = pm.currentCtx()
        pm.artAttrSkinPaintCtx(ctx, e=True, selectedattroper="absolute")
        pm.artAttrSkinPaintCtx(ctx, e=True, opacity=1.0)
        pm.artAttrSkinPaintCtx(ctx, e=True, value=0.0)
        pm.artAttrSkinPaintCtx(ctx, e=True, clear=True)
        
    else:
        pm.mel.DeleteHistory()
        
        for node in pm.selected(type="transform"):
            try:
                for attr in node.listAttr(keyable=True):
                    attr.unlock()

                intermediate_shapes = [s for s in node.getShapes() if s.intermediateObject.get()]
                if intermediate_shapes:
                    pm.delete(intermediate_shapes)

            except Exception as e:
                traceback.print_exc()


def increase_manipulator_size_or_increment_select_vertices_below_positive():
    if is_skinning():
        increment_select_vertices_below()
    else:
        pm.mel.IncreaseManipulatorSize()

        
def decrease_manipulator_size_or_increment_select_vertices_below_negative():
    if is_skinning():
        increment_select_vertices_below(positive=False)
    else:
        pm.mel.DecreaseManipulatorSize()

        
def increment_select_vertices_below(positive=True):

    weight_value = pm.optionVar.get(k.OptionVars.SelectVerticesBelowInfluence, 0.01)
    
    if weight_value == 0.0:
        weight_value = 0.01
    
    if weight_value >= 0.1:
        if weight_value > 0.98 and positive:
            sys.stdout.write("SelectVerticesBelowInfluence set to: {}\n".format(weight_value))
            return
            
        if positive:
            weight_value += 0.05
        else:
            weight_value -= 0.05
            
    else:
        if positive and weight_value > 0.049 and weight_value < 0.1:
            weight_value = 0.1
        else:
            if positive:
                weight_value *= 10
            else:   
                weight_value *= 0.1
        
    pm.optionVar[k.OptionVars.SelectVerticesBelowInfluence] = weight_value
    sys.stdout.write("SelectVerticesBelowInfluence set to: {}\n".format(weight_value))
    
    











