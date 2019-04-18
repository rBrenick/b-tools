# bTools

import pymel.core as pm
import bTools.constants as k


MENU_NAME = "TechAnim_markingMenu"


class markingMenu():
    '''The main class, which encapsulates everything we need to build and rebuild our marking menu. All
    that is done in the constructor, so all we need to do in order to build/update our marking menu is
    to initialize this class.'''

    def __init__(self):

        removeOldMarkingMenu()
        self._build()

    def _build(self):
        '''Creates the marking menu context and calls the _buildMarkingMenu() method to populate it with all items.'''
        menu = pm.popupMenu(MENU_NAME, markingMenu=True, button=1, allowOptionBoxes=True, ctrlModifier=False, altModifier=False, shiftModifier=False, parent="viewPanes", postMenuCommandOnce=True, postMenuCommand=self._buildMarkingMenu)

    def _buildMarkingMenu(self, menu, parent):
        '''This is where all the elements of the marking menu our built.'''

        # Radial positioned
        pm.menuItem(p=menu, l="ResetAttrs / BindPose", rp="N", image="bt_Reset.png", c=k.Hotkeys.utilsCmdForm.format("resetAttrsOrBindPose()"))
        pm.menuItem(p=menu, l="Select Constraint Source", rp="NW", image="parentConstraint.png", c=k.Hotkeys.utilsCmdForm.format("selectConstraintSource()"))
        pm.menuItem(p=menu, l="Select LODs", rp="NE", image="levelOfDetail.png", c=k.Hotkeys.utilsCmdForm.format("selectLods()"))
        pm.menuItem(p=menu, l="WeightHammer Blender", rp="S", c=k.Hotkeys.utilsCmdForm.format("resetAttrsOrBindPose()"), enable=False)
        
        # Create - Submenu
        subMenu = pm.menuItem(p=menu, l="Create", rp="SW", image="bt_Add.png", subMenu=1)
        pm.menuItem(p=subMenu, l="Locator", rp="N", image="locator.png", command=k.Hotkeys.utilsCmdForm.format("createLocatorAroundSelected()"))
        pm.menuItem(p=subMenu, l="Joint", rp="W", image="kinJoint.png", command=k.Hotkeys.utilsCmdForm.format("createSingleJoint()"))
        pm.menuItem(p=subMenu, l="Joint Chain", rp="NW", image="kinJoint.png", command="JointTool", sourceType="mel")
        pm.menuItem(p=subMenu, l="Control", rp="S", image="circle.png", command=k.Hotkeys.utilsCmdForm.format("createCtrl()"))
        # pm.menuItem(p=subMenu, l="Control Options", optionBox=True, command=k.Hotkeys.utilsCmdForm.format("createCtrl_Options()"))
        pm.menuItem(p=subMenu, l="NURBS Circle", rp="SE", image="circle.png", command="pm.circle(nr=[1,0,0])")
        
        # Save/Load - Submenu
        subMenu = pm.menuItem(p=menu, l="Save/Load", rp="SE", image="bt_File.png", subMenu=1)
        pm.menuItem(p=subMenu, l="Checkout Asset", rp="E", image="mayaIcon.png", enable=False)
        pm.menuItem(p=subMenu, l="Export All To Same Name", rp="SE", image="mayaIcon.png", command=k.Hotkeys.utilsCmdForm.format("exportAllToSameName()"))
        pm.menuItem(p=subMenu, l="Export All Skinweights", rp="SW", image="mayaIcon.png", enable=False)
        
        # Skinning List
        # pm.menuItem(p=menu, image="mayaIcon.png")
        # pm.menuItem(p=menu, l="Skinning Commands", boldFont=True, enable=False)
        pm.menuItem(p=menu, l="Add Influence", image="addWrapInfluence.png", command='pm.mel.skinClusterInfluence(1, "-lw false -wt 0")')
        
        pm.menuItem(p=menu, l="Move Influences", image="removeWrapInfluence.png", command="RemoveInfluence", sourceType="mel", enable=False)
        
        pm.menuItem(p=menu, l="Move Skinned Joints", image="moveSkinnedJoint.png", command="MoveSkinJointsTool", sourceType="mel")
        
        pm.menuItem(p=menu, l="Label Joints by Name", command="labelJointsBasedOnNames", image="menuIconSkeletons.png", sourceType="mel")
        
        pm.menuItem(p=menu, l="Mirror Skin Weights", image="mirrorSkinWeight.png", command="MirrorSkinWeights", sourceType="mel")
        pm.menuItem(p=menu, l="Mirror Skin Weights Options", optionBox=True, command="MirrorSkinWeightsOptions", sourceType="mel")
        
        pm.menuItem(p=menu, l="Copy Skin Weights", image="copySkinWeight.png", command="CopySkinWeights", sourceType="mel")
        pm.menuItem(p=menu, l="Copy Skin Weights Options", optionBox=True, command="CopySkinWeightsOptions", sourceType="mel")
        
        pm.menuItem(p=menu, l="Bind Skin", image="smoothSkin.png", command="SmoothBindSkin", sourceType="mel")
        pm.menuItem(p=menu, l="Bind Skin Options", optionBox=True, command="SmoothBindSkinOptions", sourceType="mel")
        
        # Constraint List
        """
        pm.menuItem(p=menu, divider=True)
        pm.menuItem(p=menu, l="Constraint Commands", boldFont=True, enable=False)
        pm.menuItem(p=menu, l="Parent Constraint", image="parentConstraint.png", command="ParentConstraint", sourceType="mel")
        pm.menuItem(p=menu, l="Parent Constraint Options", optionBox=True, command="ParentConstraintOptions", sourceType="mel")
        
        pm.menuItem(p=menu, l="Point Constraint", image="posConstraint.png", command="PointConstraint", sourceType="mel")
        pm.menuItem(p=menu, l="Point Constraint Options", optionBox=True, command="PointConstraintOptions", sourceType="mel")
        
        pm.menuItem(p=menu, l="Orient Constraint", image="orientConstraint.png", command="OrientConstraint", sourceType="mel")
        pm.menuItem(p=menu, l="Orient Constraint Options", optionBox=True, command="OrientConstraintOptions", sourceType="mel")
        
        pm.menuItem(p=menu, l="Aim Constraint", image="aimConstraint.png", command="AimConstraint", sourceType="mel")
        pm.menuItem(p=menu, l="Aim Constraint Options", optionBox=True, command="AimConstraintOptions", sourceType="mel")
        """
        
def removeOldMarkingMenu():
    if pm.popupMenu(MENU_NAME, ex=1):
        pm.deleteUI(MENU_NAME)
        


