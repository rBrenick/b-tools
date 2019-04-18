import pymel.core as pm
import sys
import re
import bTools.constants as k

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


def getUniqueName(targetName):
    if pm.objExists(targetName) and not targetName[-1].isdigit():
        targetName += "_1"
        
    if pm.objExists(targetName):
        finalDigit = int(re.findall("[0-9]+", targetName)[-1])
        noNumber = targetName[:-len(str(finalDigit))]
        targetName = noNumber + str(finalDigit+1)
    
    if pm.objExists(targetName):
        targetName = getUniqueName(targetName)
    
    return targetName
    
    
def createCtrl(node=None):

    tgt = "NAME"
    
    if node:
        tgt = node.name()
        
    else:
        sel = pm.selected(type="transform")
        if sel:
            ctrls = []
            for node in sel:
                ctrls.append(createCtrl(node))
            return ctrls
        
    ctrlName = getUniqueName(tgt+"_CTRL")
    ctrl = pm.circle(normal=[1, 0, 0], name=ctrlName)[0]
    offsetGrp = pm.group(empty=True, name=ctrlName+"_offsetGrp")
    spacesGrp = pm.group(empty=True, name=ctrlName+"_spacesGrp")
    spacesGrp.setParent(offsetGrp)
    ctrl.setParent(spacesGrp)
    if node:
        pm.matchTransform(offsetGrp, tgt)
        pm.parentConstraint(ctrl, tgt)
    
    ctrl.setAttr("scaleX", lock=True, keyable=False)
    ctrl.setAttr("scaleY", lock=True, keyable=False)
    ctrl.setAttr("scaleZ", lock=True, keyable=False)
    ctrl.setAttr("visibility", lock=True, keyable=False)
    
    return ctrl


def createOffsetGrp(tgt=None):
    if not tgt:
        tgt = pm.selected(type="transform")[0]
    
    offsetGrp = pm.group(empty=True, name=tgt.nodeName()+"_offsetGrp")
    offsetGrp.setParent(tgt.getParent())
    offsetGrp.setTranslation(tgt.getTranslation())
    offsetGrp.setRotation(tgt.getRotation())
    tgt.setParent(offsetGrp)
    return offsetGrp
    
    
def chainFK():
    # Chain create FK Controls
    previousCtrl = None
    for tgt in pm.selected():
        ctrl = createCtrl(tgt)
        
        if previousCtrl:
            ctrl.getParent().setParent(previousCtrl)
        previousCtrl = ctrl
        
    
def connectSkeletons():
    driver, driven = pm.selected()

    driverSkel = driver.getChildren(allDescendents=True, type="joint")
    drivenSkel = driven.getChildren(allDescendents=True, type="joint")

    for src, tgt in zip(driverSkel, drivenSkel):
        src.r >> tgt.r
        src.t >> tgt.t
        src.s >> tgt.s



        
# Marking Menu Things

def createLocatorAroundSelected():
    selTransforms = pm.selected(type="transform")
    loc = pm.spaceLocator()
    
    if selTransforms:
        loc.rename(getUniqueName(selTransforms[0].name()+"_LOC"))
        consts = []
        for node in selTransforms:
            consts.append(pm.parentConstraint(node, loc))
        pm.delete(consts)
        
    return loc

    
def createSingleJoint():
    jnt = pm.joint()
    jnt.rename("Left")
    jnt.setAttr("jointOrientX", keyable=True)
    jnt.setAttr("jointOrientY", keyable=True)
    jnt.setAttr("jointOrientZ", keyable=True)


def selectLods():
    lodSteps = pm.ls("lod*")
    lod0s = pm.ls("lod0*")
    pm.select([x for x in lodSteps if x not in lod0s])

    
def selectConstraintSource(node=None):
    if not node:
        for node in pm.ls(sl=True):
            selectConstraintSource(node)
        return

    conTypes = ["pointConstraint", "parentConstraint", "orientConstraint", "aimConstraint", "scaleConstraint"]
    selectTarget = node
    if node.type() in conTypes:
        selectTarget = pm.listConnections(node+".target[0].targetParentMatrix")
    else:
        selectTarget = pm.listConnections(node+".parentInverseMatrix")
        
    if not selectTarget:
        selectTarget = pm.listConnections(type="constraint")
    
    if not selectTarget:
        selectTarget = node.translate.connections()
        
    if not selectTarget:
        selectTarget = node.rotate.connections()
    
    if selectTarget:
        pm.select(selectTarget)

    
    
# Hotkey Things

def isSkinning():
    state = False
    ctx = pm.currentCtx()
    if pm.contextInfo(ctx, q=True, c=True) == "artAttrSkin":
        return True
    return False

    
def componentIsSelected():
    sel = pm.selected()[0]
    skinComps = [pm.general.MeshVertex, pm.general.MeshFace, pm.general.MeshEdge]
    return sel.__class__ in skinComps

    
def freezeTranslation():
    pm.mel.channelBoxCommand(freezeTranslate=None)
    
    
def freezeRotation():
    pm.mel.channelBoxCommand(freezeRotate=None)
    
    
def freezeScale():
    pm.mel.channelBoxCommand(freezeScale=None)
    
    
# Curves
def getCurveParams(crv):
    params = {}
    params["knot"] = crv.getKnots()
    params["point"] = [list(c) for c in crv.getCVs()]
    params["degree"] = crv.degree()
    if crv.form() == "periodic":
        params["periodic"] = True
    return params


def scaleCurve(crv, vec3Mult=[1, 1, 1]):
    if not isinstance(crv, pm.nt.NurbsCurve):
        return 
        
    info = getCurveParams(crv)
    
    cvs = crv.getCVs()
    
    for i, cv in enumerate(cvs):
        cvs[i] = cv * vec3Mult
        
    info["point"] = cvs
    
    pm.curve(crv, replace=True, **info)
    

def scaleSelectedCurve(vec3Mult=(1, 1, 1), scaleMult=1):
    crvs = []
    for node in pm.selected():
        if not isinstance(node, pm.nt.NurbsCurve):
            for shp in node.getShapes():
                crvs.append(shp)
        else:
            crvs.append(node)
    
    vec3Mult = list(vec3Mult)
    for i, point in enumerate(vec3Mult):
        vec3Mult[i] = point*scaleMult
    
    for crv in crvs:
        scaleCurve(crv, vec3Mult=vec3Mult)

        
def mirrorSelectedCurves():
    scaleSelectedCurve(vec3Mult=[1, 1, -1])


def increment_ScaleSelectedCurve(positive=True):
    if positive:
        scaleSelectedCurve(scaleMult=1.1)
    else:
        scaleSelectedCurve(scaleMult=0.9)
        
        
# Display

def toggleJointsInViewport():
    focusedPanel = pm.getPanel(withFocus=True)
    
    if "modelPanel" in focusedPanel:
        setValue = not pm.modelEditor(focusedPanel, q=True, joints=True)
        pm.modelEditor(focusedPanel, e=True, joints=setValue)
        

def toggleJointsXRay():
    focusedPanel = pm.getPanel(withFocus=True)
    
    if "modelPanel" in focusedPanel:
        setValue = not pm.modelEditor(focusedPanel, q=True, jointXray=True)
        pm.modelEditor(focusedPanel, e=True, jointXray=setValue)
        if setValue:
            pm.modelEditor(focusedPanel, e=True, joints=setValue)
            

# Skinning

def copyVertexWeightOrKey():
    if componentIsSelected():
        pm.mel.artAttrSkinWeightCopy()
    else:
        pm.mel.timeSliderCopyKey()


def pasteVertexWeightOrKey():
    if componentIsSelected():
        pm.mel.artAttrSkinWeightPaste()
    else:
        pm.mel.timeSliderPasteKey(False)


def setKeyOrScaleSkinweights(weightValue=1.1):
    if isSkinning():
        ctx = pm.currentCtx()
        pm.artAttrSkinPaintCtx(ctx, e=True, selectedattroper="scale")
        if weightValue > 1:
            pm.artAttrSkinPaintCtx(ctx, e=True, maxvalue=weightValue)
        pm.artAttrSkinPaintCtx(ctx, e=True, value=weightValue)
        pm.artAttrSkinPaintCtx(ctx, e=True, clear=True)
        
    else:
        pm.mel.SetKey()
        

def selectSkinVerticesOrPlay():
    if isSkinning():
        pm.mel.artSkinSelectVertices("artAttrSkinPaintCtx", 0, 0)
    else:
        pm.mel.PlaybackToggle()
        # pm.mel.dR_DoCmd("pointSnapPress")
        
        
def deselectSkinVerticesOrUnSnapVertices():
    if isSkinning():
        selMesh = pm.ls(sl=True, type="transform")
        if not selMesh:
            selMesh = pm.selected()[0].node().getTransform()
        pm.select(selMesh, replace=True)
    else:
        pm.mel.dR_DoCmd("pointSnapRelease")
        
        
def smoothSkinOrHIKFullBodyKey():
    if isSkinning():
        ctx = pm.currentCtx()
        pm.artAttrSkinPaintCtx(ctx, e=True, selectedattroper="smooth")
        pm.artAttrSkinPaintCtx(ctx, e=True, clear=True)
    else:
        pm.mel.HIKSetFullBodyKey()


def selectInfluenceBelowOrGoToMinFrame(weightValue=None):
    if isSkinning():
        ctx = pm.currentCtx()

        if not weightValue:
            weightValue = pm.optionVar.get(k.OptionVars.SelectVerticesBelowInfluence, 0.01)

        pm.mel.artSkinSelectVertices("artAttrSkinPaintCtx", 0, 0)  # Select affected vertices

        sel = pm.selected()
        targetJoint = pm.artAttrSkinPaintCtx(ctx, q=True, influence=True)
        selMesh = sel[0].node().getTransform()
        skincluster = pm.PyNode(pm.mel.findRelatedSkinCluster(selMesh))
        
        if not skincluster:
            pm.warning("No Skin Cluster found from selection")
            return
        
        getData = skincluster.getPointsAffectedByInfluence(targetJoint)
        weightData = getData[1]
        vertData = []
        if len(getData[0]) > 0:
            for each in getData[0][0]:
                 vertData.append(each.currentItemIndex())
                 
        selList = []   
        for vert, weight in zip(vertData, weightData):
            if weight < weightValue:
                selList.append(selMesh.name()+".vtx[{}]".format(vert))
                
        if not selList:
            sys.stdout.write("No Vertices found below value: {}\n".format(weightValue))
            deselectSkinVerticesOrUnSnapVertices()
            return

        pm.select(selList, replace=True)
        
    else:
        pm.mel.GoToMinFrame()

        
def deleteHistoryOrRemoveSkinning():
    if isSkinning():
        ctx = pm.currentCtx()
        pm.artAttrSkinPaintCtx(ctx, e=True, selectedattroper="absolute")
        pm.artAttrSkinPaintCtx(ctx, e=True, opacity=1.0)
        pm.artAttrSkinPaintCtx(ctx, e=True, value=0.0)
        pm.artAttrSkinPaintCtx(ctx, e=True, clear=True)
        
    else:
        pm.mel.DeleteHistory()
        
        
def increaseManipulatorSize_Or_IncrementSelectVerticesBelow_Positive():
    if isSkinning():
        increment_SelectVerticesBelow()
    else:
        pm.mel.IncreaseManipulatorSize()

        
def decreaseManipulatorSize_Or_IncrementSelectVerticesBelow_Negative():
    if isSkinning():
        increment_SelectVerticesBelow(positive=False)
    else:
        pm.mel.DecreaseManipulatorSize()

        
def increment_SelectVerticesBelow(positive=True):

    weightValue = pm.optionVar.get(k.OptionVars.SelectVerticesBelowInfluence, 0.01)
    
    if weightValue == 0.0:
        weightValue = 0.01
    
    if weightValue >= 0.1:
        if weightValue > 0.98 and positive:
            sys.stdout.write("SelectVerticesBelowInfluence set to: {}\n".format(weightValue))
            return
            
        if positive:
            weightValue += 0.05
        else:
            weightValue -= 0.05
            
    else:
        if positive and weightValue > 0.049 and weightValue < 0.1:
            weightValue = 0.1
        else:
            if positive:
                weightValue *= 10
            else:   
                weightValue *= 0.1
        
    pm.optionVar[k.OptionVars.SelectVerticesBelowInfluence] = weightValue
    sys.stdout.write("SelectVerticesBelowInfluence set to: {}\n".format(weightValue))
    
    











