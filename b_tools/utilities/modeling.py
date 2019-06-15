import pymel.core as pm


def pivot_switch():
    """
    Holy hell this thing is so garbage
    it was very early in my python career

    but I wrote it so long ago and it still works so I'm not going to touch it

    :return:
    """
    def next_pivot_state(obj):
        # Returns a string of what the next state of input obj should be
        
        pivot = pm.xform(obj, q=True, rp=True, ws=True)
        bbox = pm.xform(obj, q=True, ws=True, bb=True)
        center = [(bbox[0] + bbox[3])/2, (bbox[1] + bbox[4])/2, (bbox[2] + bbox[5])/2]
        bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
                
        for i in range(0,3):
            pivot[i] = round(pivot[i], 4)
            center[i] = round(center[i], 4)
            bottom[i] = round(bottom[i], 4)
                
        if pivot == bottom and bottom != [0.0, 0.0, 0.0]:
            return "origo"
        elif pivot == center:
            return "bottom"
        else:
            return "center"

    def toggle_pivot_positions(obj_list):
        last_obj = obj_list[-1]  # selects last obj of list
        pivot = pm.xform(last_obj, q=True, rp=True, ws=True)
        
        state = next_pivot_state(last_obj)  # Gets the next state for last selected obj
        
        for obj in obj_list:
            bbox = pm.xform(obj,q=True, ws=True, bb=True)
            center = [(bbox[0] + bbox[3])/2, (bbox[1] + bbox[4])/2, (bbox[2] + bbox[5])/2]
            bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
                
            for i in range(0,3):
                pivot[i] = round(pivot[i], 4)
                center[i] = round(center[i], 4)
                bottom[i] = round(bottom[i], 4)
                
            # Setting the pivot to match whatever state the last selected obj has
            if state == "origo":
                new_sel = pm.ls(obj)
                pm.move(0, 0, 0, (new_sel[0]+".scalePivot"), (new_sel[0]+".rotatePivot"), absolute=True)  # Sets pivot to origo
            if state == "bottom":
                pm.xform(obj, piv=bottom, ws=True,absolute=True)  # Sets pivot to bottom of Bounding Box
            if state == "center":
                pm.xform(obj, piv=center, ws=True,absolute=True)  # Sets pivot to center
                
            pm.select(obj_list)
        
    def move_object_pivot_to_selected_component(component):
        obj = pm.PyNode(component.split(".")[0]).getParent()
        loc = pm.spaceLocator()
        
        pm.select(component)
        pm.select(loc, add=True)
        
        pm.mel.eval('doCreatePointOnPolyConstraintArgList 1 {"0" ,"0" ,"0" ,"1" ,"" ,"1"};')
        poly_constraint = pm.listRelatives(loc, type="constraint")
        pm.delete(poly_constraint)
        pm.rotate(loc, [0, 0, '-180deg'], r=True, fo=True, os=True)
        
        obj_parent = pm.listRelatives(obj, p=True)
        
        pivot_translate = pm.xform(loc, q=True, ws=True, rotatePivot=True)
        obj.setParent(loc)
        pm.makeIdentity(obj, a=True, t=True, r=True, s=True)  # Freeze transform to match rotation of locator
        pm.xform(obj, pivots=pivot_translate, ws=True)
        pm.manipPivot(o=(0, 0, 180))  # Rotate pivot to face inwards
        
        if obj_parent:
            obj.setParent(obj_parent)
        else:
            obj.setParent(world=True)
            
        pm.delete(loc)
        
        for component in component_array:  # Select objects of faces when done
            to_select = obj
            select_array.append(to_select)
            pm.select(select_array)

    sel = pm.ls(sl=True)
    dag_nodes = pm.selectedNodes(dagObjects=True)
    counter = 0
    obj_array = []
    component_array = []
    select_array = []

    for selection in sel:
        if pm.nodeType(selection) == "mesh":
            component_array.append(selection)
            pm.select(selection,d=True)  # Remove faces from selection to remove confusion when selecting faces again
        else:
            obj_array.append(dag_nodes[counter])
            
        if pm.nodeType(selection) == "transform" or pm.nodeType(selection) == "mesh":  # If object is a poly cube or something else then don't add to counter
            counter += 1

    if len(component_array):
        for component in component_array:
            move_object_pivot_to_selected_component(component)
            
    if len(obj_array) > 0:
        toggle_pivot_positions(obj_array)

        


        





