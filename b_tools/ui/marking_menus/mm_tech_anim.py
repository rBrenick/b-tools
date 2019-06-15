# b_tools

import pymel.core as pm
import b_tools.constants as k


MENU_NAME = "TechAnim_markingMenu"


class Markingmenu():
    '''The main class, which encapsulates everything we need to build and rebuild our marking menu. All
    that is done in the constructor, so all we need to do in order to build/update our marking menu is
    to initialize this class.'''

    def __init__(self):

        remove_old_marking_menu()
        self._build()

    def _build(self):
        '''Creates the marking menu context and calls the _buildMarkingMenu() method to populate it with all items.'''
        menu = pm.popupMenu(MENU_NAME, markingMenu=True, button=1, allowOptionBoxes=True, ctrlModifier=False, altModifier=False, shiftModifier=False, parent="viewPanes", postMenuCommandOnce=True, postMenuCommand=self._build_marking_menu)

    def _build_marking_menu(self, menu, parent):
        '''This is where all the elements of the marking menu our built.'''

        # Radial positioned
        pm.menuItem(p=menu, label="ResetAttrs / BindPose", rp="N", image="bt_Reset.png", c=k.Hotkeys.utils_cmd_form.format("reset_attrs_or_bind_pose()"))
        pm.menuItem(p=menu, label="Select Constraint Source", rp="NW", image="parentConstraint.png", c=k.Hotkeys.utils_cmd_form.format("select_constraint_source()"))
        pm.menuItem(p=menu, label="Select LODs", rp="NE", image="levelOfDetail.png", c=k.Hotkeys.utils_cmd_form.format("select_lods()"))
        pm.menuItem(p=menu, label="WeightHammer Blender", rp="S", c=k.Hotkeys.utils_cmd_form.format("reset_attrs_or_bind_pose()"), enable=False)
        
        # Create - Submenu
        sub_menu = pm.menuItem(p=menu, label="Create", rp="SW", image="bt_Add.png", subMenu=1)
        pm.menuItem(p=sub_menu, label="Locator", rp="N", image="locator.png", command=k.Hotkeys.utils_cmd_form.format("create_locator_around_selected()"))
        pm.menuItem(p=sub_menu, label="Joint", rp="W", image="kinJoint.png", command=k.Hotkeys.utils_cmd_form.format("create_single_joint()"))
        pm.menuItem(p=sub_menu, label="Joint Chain", rp="NW", image="kinJoint.png", command="JointTool", sourceType="mel")
        pm.menuItem(p=sub_menu, label="Control", rp="S", image="circle.png", command=k.Hotkeys.utils_cmd_form.format("create_ctrl()"))
        # pm.menuItem(p=sub_menu, label="Control Options", optionBox=True, command=k.Hotkeys.utilsCmdForm.format("createCtrl_Options()"))
        pm.menuItem(p=sub_menu, label="NURBS Circle", rp="SE", image="circle.png", command="pm.circle(nr=[1,0,0])")
        
        # Save/Load - Submenu
        sub_menu = pm.menuItem(p=menu, label="Save/Load", rp="SE", image="bt_File.png", subMenu=1)
        pm.menuItem(p=sub_menu, label="Checkout Asset", rp="E", image="mayaIcon.png", enable=False)
        pm.menuItem(p=sub_menu, label="Export All To Same Name", rp="SE", image="mayaIcon.png", command=k.Hotkeys.utils_cmd_form.format("export_all_to_same_name()"))
        pm.menuItem(p=sub_menu, label="Export All Skinweights", rp="SW", image="mayaIcon.png", enable=False)
        
        # Skinning List
        # pm.menuItem(p=menu, image="mayaIcon.png")
        # pm.menuItem(p=menu, label="Skinning Commands", boldFont=True, enable=False)
        pm.menuItem(p=menu, label="Add Influence", image="addWrapInfluence.png", command='pm.mel.skinClusterInfluence(1, "-lw false -wt 0")')
        
        pm.menuItem(p=menu, label="Move Influences", image="removeWrapInfluence.png", command="RemoveInfluence", sourceType="mel", enable=False)
        
        pm.menuItem(p=menu, label="Move Skinned Joints", image="moveSkinnedJoint.png", command="MoveSkinJointsTool", sourceType="mel")
        
        pm.menuItem(p=menu, label="Label Joints by Name", command="labelJointsBasedOnNames", image="menuIconSkeletons.png", sourceType="mel")
        
        pm.menuItem(p=menu, label="Mirror Skin Weights", image="mirrorSkinWeight.png", command="MirrorSkinWeights", sourceType="mel")
        pm.menuItem(p=menu, label="Mirror Skin Weights Options", optionBox=True, command="MirrorSkinWeightsOptions", sourceType="mel")
        
        pm.menuItem(p=menu, label="Copy Skin Weights", image="copySkinWeight.png", command="CopySkinWeights", sourceType="mel")
        pm.menuItem(p=menu, label="Copy Skin Weights Options", optionBox=True, command="CopySkinWeightsOptions", sourceType="mel")
        
        pm.menuItem(p=menu, label="Bind Skin", image="smoothSkin.png", command="SmoothBindSkin", sourceType="mel")
        pm.menuItem(p=menu, label="Bind Skin Options", optionBox=True, command="SmoothBindSkinOptions", sourceType="mel")
        
        # Constraint List
        """
        pm.menuItem(p=menu, divider=True)
        pm.menuItem(p=menu, label="Constraint Commands", boldFont=True, enable=False)
        pm.menuItem(p=menu, label="Parent Constraint", image="parentConstraint.png", command="ParentConstraint", sourceType="mel")
        pm.menuItem(p=menu, label="Parent Constraint Options", optionBox=True, command="ParentConstraintOptions", sourceType="mel")
        
        pm.menuItem(p=menu, label="Point Constraint", image="posConstraint.png", command="PointConstraint", sourceType="mel")
        pm.menuItem(p=menu, label="Point Constraint Options", optionBox=True, command="PointConstraintOptions", sourceType="mel")
        
        pm.menuItem(p=menu, label="Orient Constraint", image="orientConstraint.png", command="OrientConstraint", sourceType="mel")
        pm.menuItem(p=menu, label="Orient Constraint Options", optionBox=True, command="OrientConstraintOptions", sourceType="mel")
        
        pm.menuItem(p=menu, label="Aim Constraint", image="aimConstraint.png", command="AimConstraint", sourceType="mel")
        pm.menuItem(p=menu, label="Aim Constraint Options", optionBox=True, command="AimConstraintOptions", sourceType="mel")
        """


def remove_old_marking_menu():
    if pm.popupMenu(MENU_NAME, ex=1):
        pm.deleteUI(MENU_NAME)
        


