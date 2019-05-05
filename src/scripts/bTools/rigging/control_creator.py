import pymel.core as pm


"""
This is a control creator meant for quickly generating basic FK controls for a rig

2019/03/28 - version 1.0 - initial release


INSTALL

1. Put this ControlCreator.py file in C:\Users\USERNAME\Documents\maya\scripts (if the folder does not exist you can just create it)

2. Run these two lines in mayas script editor, (in a python tab)

import ControlCreator
ControlCreator.run()



author: rBrenick
email: RichardBrenick@gmail.com



"""


def create_offset_grp(tgt):
    offset_grp = pm.group(empty=True, name=tgt.nodeName()+"_offset_grp")
    pm.matchTransform(offset_grp, tgt)
    tgt.setParent(offset_grp)
    return offset_grp


def get_constraint_of_node(node):
    const = list(set(node.inputs(type="constraint")))
    if not const:
        return None
        
    return const

def get_ctrl_from_constraint(node):
    const = get_constraint_of_node(node)
    if not const:
        return None
        
    for node in const[0].connections(type="transform", destination=False):
        if node.type() == "transform":
            return node


def node_is_constraint(node):
    return node.type() in ["parentConstraint", "orientConstraint", "pointConstraint", "aimConstraint", "scaleConstraint"]
    
    
def create_constraint(source, target, **kwargs):
    const = None
    connectable_unlocked_attributes = ["{}.{}".format(target, attr) for attr in pm.listAttr(target, unlocked=True, keyable=True)]
    locked_translate_axes = ["x", "y", "z"]
    locked_rotate_axes = ["x", "y", "z"]

    for attr in connectable_unlocked_attributes:
        attr_name = attr.split(".")[-1]

        if "translate" in attr_name:
            locked_translate_axes.remove(attr_name[-1].lower())

        if "rotate" in attr_name:
            locked_rotate_axes.remove(attr_name[-1].lower())

    return pm.parentConstraint(source, target, skipRotate=locked_rotate_axes, skipTranslate=locked_translate_axes, **kwargs)


def create_control(shape="cube"):
    created_controls = []
        
    sel = pm.selected(type="transform")
    
    for target in sel:
        if node_is_constraint(target):
            continue
        
        if get_constraint_of_node(target):
            pm.warning("Existing Constraint found for node, skipping: {}".format(get_constraint_of_node(target)[0]))
            continue
        
        if shape == "cube":
            ctrl = control_cube()
            
        elif shape == "circle":
            ctrl = control_circle()
        
        ctrl = pm.PyNode(ctrl)
        
        for attr in ["scaleX", "scaleY", "scaleZ", "visibility"]:
            ctrl.setAttr(attr, lock=True, keyable=False)
        
        ctrl.rename(target+"_FK_CTRL")
        ctrl_offset_grp = create_offset_grp(ctrl)
        ctrl_offset_grp.setMatrix(target.getMatrix(worldSpace=True), worldSpace=True)
        
        create_constraint(ctrl, target)
        
        if target.getParent():
            
            target_parent_ctrl = get_ctrl_from_constraint(target.getParent())
            
            if target_parent_ctrl:
                ctrl_offset_grp.setParent(target_parent_ctrl)
        
        for target_child in target.getChildren(type="transform"):
            if node_is_constraint(target_child):
                continue
                
            target_child_ctrl = get_ctrl_from_constraint(target_child)
            
            if target_child_ctrl:
                if target_child_ctrl.getParent().getParent() is None: # if target control offset_grp parent is world
                    target_child_ctrl.getParent().setParent(ctrl)
            
        created_controls.append(ctrl)
        
    pm.select(created_controls)


def scale_curve_shape(scale_value=1.1):
    for ctrl in pm.selected(type="transform"):
        if not ctrl.getShape():
            continue
        
        ctrl_shape = ctrl.getShape()
        
        new_points = [cv * scale_value for cv in ctrl_shape.getCVs()]
        
        for i, point in enumerate(ctrl.cv[:]):
            pm.xform(ctrl+".cv[{}]".format(i), absolute=True, translation=new_points[i])


def control_cube():
    return pm.mel.eval('curve -d 1 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15')
    
def control_circle():
    return pm.circle(nr=[1, 0, 0])[0]
    
def control_sphere():
    return pm.mel.eval('curve -d 1 -p 0 1.179292 3.57628e-007 -p 0 1.121573 0.364421 -p 0 0.954067 0.693171 -p 0 0.69317 0.954067 -p 0 0.364421 1.121573 -p -2.70084e-008 0 1.179292 -p 0 -0.364421 1.121574 -p 0 -0.69317 0.954067 -p 0 -0.954067 0.693171 -p 0 -1.121573 0.364421 -p 0 -1.179292 1.78814e-007 -p 0 -1.121573 -0.364421 -p 0 -0.954067 -0.69317 -p 0 -0.693171 -0.954067 -p 0 -0.364421 -1.121573 -p -2.79397e-008 0 -1.179292 -p 0 0.364421 -1.121574 -p 0 0.693171 -0.954067 -p 0 0.954068 -0.693171 -p 0 1.121574 -0.364421 -p 0 1.179292 3.57628e-007 -p 0 1 1.78814e-007 -p 0 0.951057 0.309017 -p 0 1.121573 0.364421 -p 0 0.951057 0.309017 -p 0 0.809017 0.587785 -p 0 0.954067 0.693171 -p 0 0.809017 0.587785 -p 0 0.587785 0.809017 -p 0 0.69317 0.954067 -p 0 0.587785 0.809017 -p 0 0.309017 0.951057 -p 0 0.364421 1.121573 -p 0 0.309017 0.951057 -p -2.98023e-008 0 1 -p -2.70084e-008 0 1.179292 -p -2.98023e-008 0 1 -p 0 -0.309017 0.951057 -p 0 -0.364421 1.121574 -p 0 -0.309017 0.951057 -p 0 -0.587785 0.809017 -p 0 -0.69317 0.954067 -p 0 -0.587785 0.809017 -p 0 -0.809017 0.587786 -p 0 -0.954067 0.693171 -p 0 -0.809017 0.587786 -p 0 -0.951057 0.309017 -p 0 -1.121573 0.364421 -p 0 -0.951057 0.309017 -p 0 -1 1.78814e-007 -p 0 -1.179292 1.78814e-007 -p 0 -1 1.78814e-007 -p 0 -0.951057 -0.309017 -p 0 -1.121573 -0.364421 -p 0 -0.951057 -0.309017 -p 0 -0.809017 -0.587785 -p 0 -0.954067 -0.69317 -p 0 -0.809017 -0.587785 -p 0 -0.587785 -0.809017 -p 0 -0.693171 -0.954067 -p 0 -0.587785 -0.809017 -p 0 -0.309017 -0.951057 -p 0 -0.364421 -1.121573 -p 0 -0.309017 -0.951057 -p 0 0 -1 -p -2.79397e-008 0 -1.179292 -p 0 0 -1 -p 0 0.309017 -0.951057 -p 0 0.364421 -1.121574 -p 0 0.309017 -0.951057 -p 0 0.587786 -0.809017 -p 0 0.693171 -0.954067 -p 0 0.587786 -0.809017 -p 0 0.809018 -0.587785 -p 0 0.954068 -0.693171 -p 0 0.809018 -0.587785 -p 0 0.951057 -0.309017 -p 0 1.121574 -0.364421 -p 0 0.951057 -0.309017 -p 0 1 1.78814e-007 -p 0.309017 0.951057 0 -p 0.364421 1.121573 0 -p 0 1.179292 3.57628e-007 -p -0.364421 1.121574 0 -p -0.309017 0.951057 0 -p 0 1 1.78814e-007 -p 0.309017 0.951057 0 -p 0.364421 1.121573 0 -p 0.693171 0.954067 0 -p 0.587785 0.809017 0 -p 0.309017 0.951057 0 -p 0.587785 0.809017 0 -p 0.809017 0.587785 0 -p 0.954067 0.69317 0 -p 0.693171 0.954067 0 -p 0.954067 0.69317 0 -p 1.121573 0.364421 0 -p 0.951057 0.309017 0 -p 0.809017 0.587785 0 -p 0.951057 0.309017 0 -p 1 0 1.78814e-007 -p 1.179292 0 3.57628e-007 -p 1.121573 0.364421 0 -p 1.179292 0 3.57628e-007 -p 1.121574 -0.364421 0 -p 0.951057 -0.309017 0 -p 1 0 1.78814e-007 -p 0.951057 -0.309017 0 -p 0.809017 -0.587785 0 -p 0.587786 -0.809017 0 -p 0.309017 -0.951057 0 -p 0 -1 1.78814e-007 -p -0.309017 -0.951057 0 -p -0.587785 -0.809017 0 -p -0.809017 -0.587785 0 -p -0.951057 -0.309017 0 -p -1 0 1.78814e-007 -p -0.951057 0.309017 0 -p -0.809017 0.587786 0 -p -0.587785 0.809018 0 -p -0.309017 0.951057 0 -p -0.364421 1.121574 0 -p -0.693171 0.954068 0 -p -0.587785 0.809018 0 -p -0.693171 0.954068 0 -p -0.954067 0.693171 0 -p -0.809017 0.587786 0 -p -0.954067 0.693171 0 -p -1.121574 0.364421 0 -p -0.951057 0.309017 0 -p -1.121574 0.364421 0 -p -1.179292 0 1.78814e-007 -p -1 0 1.78814e-007 -p -1.179292 0 1.78814e-007 -p -1.121573 -0.364421 0 -p -0.951057 -0.309017 0 -p -1.121573 -0.364421 0 -p -0.954067 -0.693171 0 -p -0.809017 -0.587785 0 -p -0.954067 -0.693171 0 -p -0.69317 -0.954067 0 -p -0.587785 -0.809017 0 -p -0.69317 -0.954067 0 -p -0.364421 -1.121573 0 -p -0.309017 -0.951057 0 -p -0.364421 -1.121573 0 -p 0 -1.179292 1.78814e-007 -p 0.364421 -1.121573 0 -p 0.309017 -0.951057 0 -p 0.364421 -1.121573 0 -p 0.693171 -0.954067 0 -p 0.587786 -0.809017 0 -p 0.693171 -0.954067 0 -p 0.954067 -0.69317 0 -p 0.809017 -0.587785 0 -p 0.954067 -0.69317 0 -p 1.121574 -0.364421 0 -p 1.179292 0 3.57628e-007 -p 1.121574 0 -0.364421 -p 0.954068 0 -0.693171 -p 0.693171 0 -0.954067 -p 0.364421 0 -1.121574 -p -2.79397e-008 0 -1.179292 -p -0.364421 0 -1.121573 -p -0.693171 0 -0.954067 -p -0.954067 0 -0.69317 -p -1.121573 0 -0.364421 -p -1.179292 0 1.78814e-007 -p -1.121573 0 0.364421 -p -0.954067 0 0.693171 -p -0.69317 0 0.954067 -p -0.364421 0 1.121574 -p -2.70084e-008 0 1.179292 -p 0.364421 0 1.121573 -p 0.69317 0 0.954067 -p 0.954067 0 0.693171 -p 1.121573 0 0.364421 -p 1.179292 0 3.57628e-007 -p 1 0 1.78814e-007 -p 0.951057 0 -0.309017 -p 1.121574 0 -0.364421 -p 0.951057 0 -0.309017 -p 0.809018 0 -0.587785 -p 0.954068 0 -0.693171 -p 0.809018 0 -0.587785 -p 0.587786 0 -0.809017 -p 0.693171 0 -0.954067 -p 0.587786 0 -0.809017 -p 0.309017 0 -0.951057 -p 0.364421 0 -1.121574 -p 0.309017 0 -0.951057 -p 0 0 -1 -p -2.79397e-008 0 -1.179292 -p 0 0 -1 -p -0.309017 0 -0.951057 -p -0.364421 0 -1.121573 -p -0.309017 0 -0.951057 -p -0.587785 0 -0.809017 -p -0.693171 0 -0.954067 -p -0.587785 0 -0.809017 -p -0.809017 0 -0.587785 -p -0.954067 0 -0.69317 -p -0.809017 0 -0.587785 -p -0.951057 0 -0.309017 -p -1.121573 0 -0.364421 -p -0.951057 0 -0.309017 -p -1 0 1.78814e-007 -p -1.179292 0 1.78814e-007 -p -1 0 1.78814e-007 -p -0.951057 0 0.309017 -p -1.121573 0 0.364421 -p -0.951057 0 0.309017 -p -0.809017 0 0.587786 -p -0.954067 0 0.693171 -p -0.809017 0 0.587786 -p -0.587785 0 0.809017 -p -0.69317 0 0.954067 -p -0.587785 0 0.809017 -p -0.309017 0 0.951057 -p -0.364421 0 1.121574 -p -0.309017 0 0.951057 -p -2.98023e-008 0 1 -p -2.70084e-008 0 1.179292 -p -2.98023e-008 0 1 -p 0.309017 0 0.951057 -p 0.364421 0 1.121573 -p 0.309017 0 0.951057 -p 0.587785 0 0.809017 -p 0.69317 0 0.954067 -p 0.587785 0 0.809017 -p 0.809017 0 0.587785 -p 0.954067 0 0.693171 -p 0.809017 0 0.587785 -p 0.951057 0 0.309017 -p 1.121573 0 0.364421 -p 0.951057 0 0.309017 -p 1 0 1.78814e-007 -p 1.179292 0 3.57628e-007 -p 1 0 1.78814e-007 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83 -k 84 -k 85 -k 86 -k 87 -k 88 -k 89 -k 90 -k 91 -k 92 -k 93 -k 94 -k 95 -k 96 -k 97 -k 98 -k 99 -k 100 -k 101 -k 102 -k 103 -k 104 -k 105 -k 106 -k 107 -k 108 -k 109 -k 110 -k 111 -k 112 -k 113 -k 114 -k 115 -k 116 -k 117 -k 118 -k 119 -k 120 -k 121 -k 122 -k 123 -k 124 -k 125 -k 126 -k 127 -k 128 -k 129 -k 130 -k 131 -k 132 -k 133 -k 134 -k 135 -k 136 -k 137 -k 138 -k 139 -k 140 -k 141 -k 142 -k 143 -k 144 -k 145 -k 146 -k 147 -k 148 -k 149 -k 150 -k 151 -k 152 -k 153 -k 154 -k 155 -k 156 -k 157 -k 158 -k 159 -k 160 -k 161 -k 162 -k 163 -k 164 -k 165 -k 166 -k 167 -k 168 -k 169 -k 170 -k 171 -k 172 -k 173 -k 174 -k 175 -k 176 -k 177 -k 178 -k 179 -k 180 -k 181 -k 182 -k 183 -k 184 -k 185 -k 186 -k 187 -k 188 -k 189 -k 190 -k 191 -k 192 -k 193 -k 194 -k 195 -k 196 -k 197 -k 198 -k 199 -k 200 -k 201 -k 202 -k 203 -k 204 -k 205 -k 206 -k 207 -k 208 -k 209 -k 210 -k 211 -k 212 -k 213 -k 214 -k 215 -k 216 -k 217 -k 218 -k 219 -k 220 -k 221 -k 222 -k 223 -k 224 -k 225 -k 226 -k 227 -k 228 -k 229 -k 230 -k 231 -k 232 -k 233 -k 234 -k 235 -k 236 -k 237 -k 238')
    
def control_target():
    return pm.mel.eval('curve -d 1 -p 4.875141 19.999998 0 -p 4.875151 11.76965 0 -p 7.077621 10.592403 0 -p 9.008102 9.008097 0 -p 10.592406 7.077615 0 -p 11.76965 4.875144 0 -p 20 4.875144 0 -p 19.999998 -4.875141 0 -p 11.76965 -4.875151 0 -p 10.592403 -7.077621 0 -p 9.008097 -9.008102 0 -p 7.077615 -10.592406 0 -p 4.875144 -11.76965 0 -p 4.875144 -20 0 -p -4.875141 -19.999998 0 -p -4.875151 -11.76965 0 -p -7.077621 -10.592403 0 -p -9.008102 -9.008097 0 -p -10.592406 -7.077615 0 -p -11.76965 -4.875144 0 -p -20 -4.875144 0 -p -19.999998 4.875141 0 -p -11.76965 4.875151 0 -p -10.592403 7.077621 0 -p -9.008097 9.008102 0 -p -7.077615 10.592406 0 -p -4.875144 11.76965 0 -p -4.875144 20 0 -p 4.875141 19.999998 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 ;')


class ControlCreatorWindow(object):
    def __init__(self):
        
        # Make a new window
        win_title = "Control Creator"
        win_title_safe = win_title.replace(" ", "_")
        if pm.window(win_title_safe, q=True, exists=True):
            pm.deleteUI(win_title_safe)
            
        window = pm.window(win_title_safe, title=win_title, toolbox=True, backgroundColor=(0.158, 0.254, 0.290))
        window.show()
        
        with pm.verticalLayout():
            pm.text("1. Select joint in scene\n\n 2. Click controller shape that you want for it")
            pm.button("Cube", command=lambda x: create_control("cube"))
            pm.button("Circle", command=lambda x: create_control("circle"))
            with pm.horizontalLayout() as scale_layout:
                self.scale_float = pm.floatSliderGrp(field=True, maxValue=2, value=1.1, step=0.01)
                pm.button("Scale Control", command=self.increment_scale)
            scale_layout.redistribute(4, 2)
            
    
    def increment_scale(self, *args):
        scale_curve_shape(scale_value = self.scale_float.getValue())
        
    
def run():
    return ControlCreatorWindow()



if __name__ == "__main__":
    run()

















