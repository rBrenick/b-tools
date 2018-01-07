import pymel.core as pm
import random
import sys


def resetTransform(nodes=None, translation=True, rotation=True, scale=True):
    """
    Resets the transform values on the selected nodes
    """
    if not nodes:
        nodes = pm.selected(type="transform")
    
    for node in nodes:
        if translation:
            node.translate.set([0, 0, 0])
        if rotation:
            if list(node.rotate.get()) == [0.0, 0.0, 0.0]:
                node.jointOrient.set([0.0, 0.0, 0.0])
                sys.stdout.write("{}.JointOrient set to [0, 0, 0]\n".format(node))

            node.rotate.set([0, 0, 0])

        if scale:
            node.scale.set([1, 1, 1])
            
    return nodes


def resetTranslation():
    resetTransform(translation=True, rotation=False, scale=False)


def resetRotation():
    resetTransform(translation=False, rotation=True, scale=False)


def resetScale():
    resetTransform(translation=False, rotation=False, scale=True)
    
    
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
