
# Super secret do not share

import pymel.core as pm
from maya import OpenMaya as om


def getSoftSelectionWeights():
    #get selection
    sel = om.MSelectionList()
    softSelection = om.MRichSelection()
    om.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(sel)

    dagPath = om.MDagPath()
    component = om.MObject()

    iter = om.MItSelectionList(sel, om.MFn.kMeshVertComponent)
    weights = {}
    while not iter.isDone():

        iter.getDagPath(dagPath, component)
        dagPath.pop() #Grab the parent of the shape node
        node = dagPath.fullPathName()
        fnComp = om.MFnSingleIndexedComponent(component)

        for i in range(fnComp.elementCount()):
            weight = 1.0
            if fnComp.hasWeights():
                weight = fnComp.weight(i).influence()

            vtxId = '{}.vtx[{}]'.format(node, fnComp.element(i))
            weights[vtxId] = weight

        iter.next()

    return weights


def softSelectPaint(rgbMult=(1, 1, 1), useMayaAPI=True, asAlpha=False):
    """
    Takes the Soft Selection from current tool and converts it to Vertex Colors
    """
    
    orgSel = pm.ls(sl=True)
    pm.mel.eval("ConvertSelectionToVertices;")
    sel = pm.ls(sl=True, o=True)

    if not sel:
        pm.warning('Please select some vertices or a mesh before executing this tool')
        return
    
    node = sel[0]
    nodeName = sel[0].getParent().longName()
    weights = getSoftSelectionWeights()

    if not weights:
        pm.warning('Unable to find Soft Selection values for the vertices.')
        return
    
    
    # Blend from the currently painted vertices
    vertexColors = {}
    vertexAlphas = {}
    currentColorValues = {}
    currentAlphaValues = {}
    try:
        polyColorList = pm.polyColorPerVertex(weights.keys(), q=True, rgb=True)
    except StandardError:
        # Paint some if unable to find any
        pm.select(weights.keys())
        pm.mel.eval("polyColorPerVertex -r 0 -g 0 -b 0 -a 1 -cdo;")
        polyColorList = pm.polyColorPerVertex(weights.keys(), q=True, rgb=True)
    
    alphaList = pm.polyColorPerVertex(weights.keys(), q=True, alpha=True)
    
    # Lerp between the old and new colors
    for vtxID, vtxColor, alphaValue in zip(weights.keys(), getListChunks(polyColorList, 3), alphaList):
        vtxIDIndex = int(vtxID.split("[")[-1][0:-1])
        vertexColors[vtxIDIndex] = vec3Lerp(vtxColor, rgbMult, weights[vtxID])
        vertexAlphas[vtxIDIndex] = floatLerp(alphaValue, rgbMult[0], weights[vtxID])
        currentColorValues[vtxIDIndex] = tuple(vtxColor)
        currentAlphaValues[vtxIDIndex] = alphaValue
        
    # apply colors using either API or pymel
    if useMayaAPI:
        colorList = vertexColors.values() if not asAlpha else currentColorValues.values()
        alphaList = vertexAlphas.values() if asAlpha else currentAlphaValues.values()
        
        newColors = []
        for vertexColor, alphaValue in zip(colorList, alphaList):
            newColors.append(vertexColor + (alphaValue,))
            
        API_applyVtxColors(newColors, vertexColors.keys(), nodeName)
        
    else:        
        with pm.UndoChunk():
            progressWin = pm.progressWindow(title='Painting Vertex Colors', maxValue=len(weights.keys()), status='_'*150, isInterruptable=True)
            for i, vtxID in enumerate(weights.keys()):
                if pm.progressWindow(query=True, isCancelled=True):
                    break
                    
                pm.progressWindow(edit=True, progress=i, status=('Painting: {}'.format(vtxID)))
                
                vtxIDIndex = int(vtxID.split("[")[-1][0:-1])
                if asAlpha:
                    pm.polyColorPerVertex(vtxID, alpha=vertexAlphas[vtxIDIndex])
                else:
                    pm.polyColorPerVertex(vtxID, rgb=vertexColors[vtxIDIndex], alpha=currentAlphaValues[vtxIDIndex])
                    
            pm.progressWindow(endProgress=True)
            
    pm.select(orgSel)


def API_applyVtxColors(colors, indices, obj):
    from maya.api import OpenMaya as om  # Importing like this is dumb, I am sorry
    colors = [om.MColor(i) for i in colors]
    selectionList = om.MSelectionList()
    selectionList.add(obj)
    nodeDagPath = selectionList.getDagPath(0)
    mfnMesh = om.MFnMesh(nodeDagPath)
    mfnMesh.setVertexColors(colors, indices)


def floatLerp(floatA, floatB, interpVal):
    return floatA + (floatB - floatA) * interpVal
    

def vec3Lerp(vecA, vecB, interpVal=0.5):
    return vecA[0] + (vecB[0] - vecA[0]) * interpVal, vecA[1] + (vecB[1] - vecA[1]) * interpVal, vecA[2] + (vecB[2] - vecA[2]) * interpVal


def getListChunks(longList, chunkLength):
    for i in range(0, len(longList), chunkLength):
        yield longList[i:i + chunkLength]


def SoftSelectPolyColor_UI():
    def launchScript(*args):
        softSelectPaint(rgbMult=colSlider.getRgbValue(), useMayaAPI=useMayaAPICheckBox.getValue(), asAlpha=asAlphaCheckBox.getValue())
    
        
    if pm.window("SoftSelectPolyColorWin", q=True, exists=True):
        pm.deleteUI("SoftSelectPolyColorWin")
    
    
    flatWindow = pm.window("SoftSelectPolyColorWin", title="Soft Select To Poly Color", maximizeButton=False, minimizeButton=False)
    with pm.verticalLayout() as mainLayout:
        colSlider = pm.colorSliderGrp(label="Color: ", rgb=(1, 1, 1))
        
        asAlphaCheckBox = pm.checkBox(label="Paint as Alpha", v=False)
        useMayaAPICheckBox = pm.checkBox(label="Use Maya API (Way faster, but does not allow Undo)", v=False)
        
        pm.separator(style="none", height=20)
        pm.button(label="Soft Select To Poly Color", height=45, command=launchScript)
        pm.separator(style="none", height=20)
        
    mainLayout.redistribute(2, 1, 1, 1, 2)
    pm.showWindow(flatWindow)


def run():
    return SoftSelectPolyColor_UI()
    
    
if __name__ == '__main__':
    run()
