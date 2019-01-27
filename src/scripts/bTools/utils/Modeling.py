import pymel.core as pm


def pivotSwitch():
    def NextPivotState(obj):
        # Returns a string of what the next state of input obj should be
        
        pivot = pm.xform(obj, q=True, rp=True, ws=True)
        bbox = pm.xform(obj,q=True, ws=True, bb=True)
        center = [(bbox[0] + bbox[3])/2, (bbox[1] + bbox[4])/2, (bbox[2] + bbox[5])/2]
        bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
                
        for i in range(0,3):
            pivot[i] = round(pivot[i],4)
            center[i] = round(center[i],4)
            bottom[i] = round(bottom[i],4)
                
        if pivot == bottom and bottom != [0.0, 0.0, 0.0]:
            return("origo")
        elif pivot == center:
            return("bottom")
        else:
            return("center")

    def TogglePivotPositions(objList):
        lastObj = objList[-1]  # selects last obj of list
        pivot = pm.xform(lastObj, q=True, rp=True, ws=True)
        
        state = NextPivotState(lastObj)  # Gets the next state for last selected obj
        
        for obj in objList:
            bbox = pm.xform(obj,q=True, ws=True, bb=True)
            center = [(bbox[0] + bbox[3])/2, (bbox[1] + bbox[4])/2, (bbox[2] + bbox[5])/2]
            bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
                
            for i in range(0,3):
                pivot[i] = round(pivot[i],4)
                center[i] = round(center[i],4)
                bottom[i] = round(bottom[i],4)
                
            # Setting the pivot to match whatever state the last selected obj has
            if state == "origo":
                newSel = pm.ls(obj)
                pm.move(0, 0, 0, (newSel[0]+".scalePivot"), (newSel[0]+".rotatePivot"), absolute=True)  # Sets pivot to origo
            if state == "bottom":
                pm.xform(obj, piv=bottom, ws=True,absolute=True)  # Sets pivot to bottom of Bounding Box
            if state == "center":
                pm.xform(obj, piv=center, ws=True,absolute=True)  # Sets pivot to center
                
            pm.select(objList)
        
    def moveObjectPivotToSelectedComponent(component):
        obj = pm.PyNode(component.split(".")[0]).getParent()
        loc = pm.spaceLocator()
        
        pm.select(component)
        pm.select(loc, add=True)
        
        pm.mel.eval('doCreatePointOnPolyConstraintArgList 1 {"0" ,"0" ,"0" ,"1" ,"" ,"1"};')
        polyConstraint = pm.listRelatives(loc, type="constraint")
        pm.delete(polyConstraint)
        pm.rotate(loc, [0, 0, '-180deg'], r=True,fo=True,os=True)
        
        objParent = pm.listRelatives(obj, p=True)
        
        pivotTranslate = pm.xform(loc, q = True, ws = True, rotatePivot=True)
        obj.setParent(loc)
        pm.makeIdentity(obj, a=True, t=True, r=True, s=True)  # Freeze transform to match rotation of locator
        pm.xform(obj, pivots=pivotTranslate, ws=True)
        pm.manipPivot(o=(0, 0, 180))  # Rotate pivot to face inwards
        
        if objParent:
            obj.setParent(objParent)
        else:
            obj.setParent(world=True)
            
        pm.delete(loc)
        
        for component in componentArray:  # Select objects of faces when done
            toSelect = obj
            selectArray.append(toSelect)
            pm.select(selectArray)

    sel = pm.ls(sl=True)
    dagNodes = pm.selectedNodes(dagObjects=True)
    counter = 0
    objArray = []
    componentArray = []
    selectArray = []

    for selection in sel:
        if pm.nodeType(selection) == "mesh":
            componentArray.append(selection)
            pm.select(selection,d=True)  # Remove faces from selection to remove confusion when selecting faces again
        else:
            objArray.append(dagNodes[counter])
            
        if pm.nodeType(selection) == "transform" or pm.nodeType(selection) == "mesh": # If object is a poly cube or something else then don't add to counter
            counter += 1

    if len(componentArray):
        for component in componentArray:
            moveObjectPivotToSelectedComponent(component)
            
    if len(objArray) > 0:
        TogglePivotPositions(objArray)

        


        



