import pymel.core as pm
import random
import sys


def resetTransform(nodes=None, translation=False, rotation=False, scale=False, allKeyable=False):
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
        
        for attrName in attrs:
            if node.hasAttr(attrName) and node.getAttr(attrName, settable=True):
                defaultValue = pm.attributeQuery(attrName, listDefault=True, node=node.name())[0]
                node.setAttr(attrName, defaultValue)
            
    return nodes
    
def resetTranslation():
    resetTransform(translation=True)

def resetRotation():
    resetTransform(rotation=True)

def resetScale():
    resetTransform(scale=True)

def resetAttrs(node=None):
    if not node:
        for node in pm.selected():
            resetAttrs(node)
        return
    
    attrs = []
    selAttrs = pm.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)
    if selAttrs:
        attrs += selAttrs
    
    selAttrs = pm.channelBox('mainChannelBox', q=True, selectedShapeAttributes=True)
    if selAttrs:
        attrs += selAttrs
        
    selAttrs = pm.channelBox('mainChannelBox', q=True, selectedHistoryAttributes=True)
    if selAttrs:
        attrs += selAttrs
    
    selAttrs = pm.channelBox('mainChannelBox', q=True, selectedOutputAttributes=True)
    if selAttrs:
        attrs += selAttrs
        
    keyableAttrs = [a.attrName() for a in node.listAttr(keyable=True, shortNames=True)]
    if not attrs:
        attrs = keyableAttrs
    
    for attr in attrs:
        if attr in keyableAttrs:
            if node.getAttr(attr, settable=True):
                defaultValue = pm.attributeQuery(attr, listDefault=True, node=node.name())[0]
                node.setAttr(attr, defaultValue)

            
def resetAttrsOrBindPose():
    connections = []
    for node in pm.selected():
        connections += node.connections(type="skinCluster")
        try:
            if node.getShape():
                connections += node.getShape().connections(type="skinCluster")
        except StandardError, e:
            pass
            
    if connections:
        try:
            pm.mel.gotoBindPose()
        except StandardError, e:
            pass
    else:
        resetAttrs()
    
    
def toggleNurbsInViewport():
    """
    Toggles the visibility of NURBS Curves/Surfaces in the viewport
    """
    focusedPanel = pm.getPanel(withFocus=True)
    
    if "modelPanel" in focusedPanel:
        currentState = pm.modelEditor(focusedPanel, q=True, nurbsCurves=True)
        
        pm.modelEditor(focusedPanel, e=True, nurbsCurves=not currentState)
        pm.modelEditor(focusedPanel, e=True, nurbsSurfaces=not currentState)
        
        
def toggleControlsVisibility():
    toggleNurbsInViewport()
    
    
def frameRange():
    """
    Gets the selected frame range
    If nothing selected, gets the timeslider start end
    
    :return [startFrame, endFrame]
    
    """
    frameRange = [0, 1]
    
    selectedFrameRangeSlider = pm.mel.eval('$temp=$gPlayBackSlider')
    if pm.timeControl(selectedFrameRangeSlider, query=True, rangeVisible=True):
        frameRange = pm.timeControl(selectedFrameRangeSlider, query=True, rangeArray=True)
    else:
        startFrame = pm.playbackOptions(query=True, min=True)
        endFrame = pm.playbackOptions(query=True, max=True)
        frameRange = [startFrame, endFrame]

    return frameRange


def generateRandomVector(length=3, weights=(1, 1, 1)):
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


