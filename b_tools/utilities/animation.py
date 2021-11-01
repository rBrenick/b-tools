import pymel.core as pm
import random
import sys


def reset_transform(nodes=None, translation=False, rotation=False, scale=False, all_keyable=False):
    """
    Resets the transform values on the selected nodes
    """
    if not nodes:
        nodes = pm.selected(type="transform")
    
    for node in nodes:
        attrs = []
        if translation:
            attrs += ["translate"+axis for axis in "XYZ"]
            
        if rotation:
            attrs += ["rotate"+axis for axis in "XYZ"]
            if list(node.rotate.get()) == [0.0, 0.0, 0.0] and node.hasAttr("jointOrient"):
                attrs += ["jointOrient"+axis for axis in "XYZ"]
                sys.stdout.write("{}.JointOrient set to [0, 0, 0]\n".format(node))

        if scale:
            attrs += ["scale"+axis for axis in "XYZ"]
        
        for attr_name in attrs:
            if node.hasAttr(attr_name) and node.getAttr(attr_name, settable=True):
                default_value = pm.attributeQuery(attr_name, listDefault=True, node=node.name())[0]
                node.setAttr(attr_name, default_value)
            
    return nodes


def reset_translation():
    reset_transform(translation=True)


def reset_rotation():
    reset_transform(rotation=True)


def reset_scale():
    reset_transform(scale=True)


def reset_attrs(node=None):
    if not node:
        for node in pm.selected():
            reset_attrs(node)
        return
    
    attrs = []
    sel_attrs = pm.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)
    if sel_attrs:
        attrs += sel_attrs
    
    sel_attrs = pm.channelBox('mainChannelBox', q=True, selectedShapeAttributes=True)
    if sel_attrs:
        attrs += sel_attrs
        
    sel_attrs = pm.channelBox('mainChannelBox', q=True, selectedHistoryAttributes=True)
    if sel_attrs:
        attrs += sel_attrs
    
    sel_attrs = pm.channelBox('mainChannelBox', q=True, selectedOutputAttributes=True)
    if sel_attrs:
        attrs += sel_attrs
        
    keyable_attrs = [a.attrName() for a in node.listAttr(keyable=True, shortNames=True)]
    if not attrs:
        attrs = keyable_attrs
    
    for attr in attrs:
        if attr in keyable_attrs:
            if node.getAttr(attr, settable=True):
                default_value = pm.attributeQuery(attr, listDefault=True, node=node.name())[0]
                node.setAttr(attr, default_value)

            
def reset_attrs_or_bind_pose():
    connections = []
    for node in pm.selected():
        connections += node.connections(type="skinCluster")
        try:
            if node.getShape():
                connections += node.getShape().connections(type="skinCluster")
        except Exception as e:
            pass
            
    if connections:
        try:
            pm.mel.gotoBindPose()
        except Exception as e:
            pass
    else:
        reset_attrs()
    
    
def toggle_nurbs_in_viewport():
    """
    Toggles the visibility of NURBS Curves/Surfaces in the viewport
    """
    focused_panel = pm.getPanel(withFocus=True)
    
    if "modelPanel" in focused_panel:
        current_state = pm.modelEditor(focused_panel, q=True, nurbsCurves=True)
        
        pm.modelEditor(focused_panel, e=True, nurbsCurves=not current_state)
        pm.modelEditor(focused_panel, e=True, nurbsSurfaces=not current_state)
        
        
def toggle_controls_visibility():
    toggle_nurbs_in_viewport()
    
    
def get_frame_range():
    """
    Gets the selected frame range
    If nothing selected, gets the timeslider start end
    
    :return [start_frame, end_frame]
    
    """
    frame_range = [0, 1]
    
    selected_frame_range_slider = pm.mel.eval('$temp=$gPlayBackSlider')
    if pm.timeControl(selected_frame_range_slider, query=True, rangeVisible=True):
        frame_range = pm.timeControl(selected_frame_range_slider, query=True, rangeArray=True)
    else:
        start_frame = pm.playbackOptions(query=True, min=True)
        end_frame = pm.playbackOptions(query=True, max=True)
        frame_range = [start_frame, end_frame]

    return frame_range


def generate_random_vector(length=3, weights=(1, 1, 1)):
    """
    Creates a Vector of length with the weight values as min and max
    Defaults to a vec3
    
    :param length: 
    :param weights: 
    
    :return: []
    
    """
    vector = []
    for i in range(0, length):
        weight = 1
        if i < len(weights):
            weight = weights[i]
            
        vector.append(random.uniform(-weight, weight))
        
    return vector


