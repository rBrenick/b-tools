import pymel.core as pm
import bTools.constants as k

import bTools.ui as btUI; reload(btUI)
from bTools.ui import markingMenus; reload(markingMenus)


def createHotkey(commandHotkey, command=None, name=None, mel=False, mayaDefault=False):
    # prevCmd = pm.hotkey(cmdHotkey, query=True, name=True)
    niceNameHotkey = commandHotkey
    if pm.hotkeySet(q=True, current=True) == "Maya_Default":
        pm.hotkeySet("bTools", current=True, source='Maya_Default')

    if not name:
        name = command.split(".")[-1]
        
    if mayaDefault:
        nc = name
    else:
        rtc = name
        nc = name+"NameCommand"
        
        if pm.runTimeCommand(rtc, exists=True):
            pm.runTimeCommand(rtc, edit=True, delete=True)
        
        commandLanguage = "python"
        if mel:
            commandLanguage = "mel"
            
        rtc = pm.runTimeCommand(rtc, annotation=name+' Hotkey generated', category=k.Module.name, command=command, commandLanguage=commandLanguage)
        nc = pm.nameCommand(nc, annotation=name+' nameCommand generated', command=rtc)
    
    hotkeyParams = dict()
    hotkeyParams["name"] = nc
    
    if "alt" in commandHotkey.lower():
        hotkeyParams["altModifier"] = True
        commandHotkey = commandHotkey.lower().replace("alt+", "")
        
    if "ctrl" in commandHotkey.lower():
        hotkeyParams["ctrlModifier"] = True
        commandHotkey = commandHotkey.lower().replace("ctrl+", "")
        
    if "shift" in commandHotkey.lower():
        hotkeyParams["shiftModifier"] = True
        commandHotkey = commandHotkey.lower().replace("shift+", "")
        
    hotkeyParams["keyShortcut"] = commandHotkey.lower()
    print "      ", niceNameHotkey, "       ", rtc
    pm.hotkey(**hotkeyParams)


class HotkeyOptionsMenu(btUI.DefaultWindow):

    kSetupGeneralHotkeys = k.Module.name+"_SetupGeneralHotkeys"
    kSetupAnimationHotkeys = k.Module.name+"_SetupAnimationHotkeys"
    kSetupModelingHotkeys = k.Module.name+"_SetupModelingHotkeys"
    kSetupRiggingHotkeys = k.Module.name+"_SetupRiggingHotkeys"
    
    def __init__(self, windowTitle="HotkeyOptions"):
        super(HotkeyOptionsMenu, self).__init__(windowTitle)
        
    def setOptionVar_General(self, *args):
        pm.optionVar[HotkeyOptionsMenu.kSetupGeneralHotkeys] = args[0]
    
    def setOptionVar_Animation(self, *args):
        pm.optionVar[HotkeyOptionsMenu.kSetupAnimationHotkeys] = args[0]
        
    def setOptionVar_Modeling(self, *args):
        pm.optionVar[HotkeyOptionsMenu.kSetupModelingHotkeys] = args[0]
    
    def setOptionVar_Rigging(self, *args):
        pm.optionVar[HotkeyOptionsMenu.kSetupRiggingHotkeys] = args[0]
        
    def setupUI(self):
        with pm.verticalLayout():
            pm.separator(height=40, style="none")
            
            pm.checkBox(label='Setup General Hotkeys', 
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupGeneralHotkeys, True),
                        changeCommand=self.setOptionVar_General)
            
            pm.checkBox(label='Setup Animation Hotkeys', 
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupAnimationHotkeys, True), 
                        changeCommand=self.setOptionVar_Animation)
                        
            pm.checkBox(label='Setup Modeling Hotkeys', 
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupModelingHotkeys, True),
                        changeCommand=self.setOptionVar_Modeling)
                        
            pm.checkBox(label='Setup Rigging Hotkeys', 
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupRiggingHotkeys, True),
                        changeCommand=self.setOptionVar_Rigging)

    def main(self):
        setupDefaultHotkeys()

            
def showHotkeyOptionsMenu():
    win = HotkeyOptionsMenu()
    return win
    

def setupGeneralHotkeys():
    # General
    createHotkey("9", command="HotkeyPreferencesWindow;", name="ShowHotkeyWindow", mel=True)
    createHotkey("Alt+Shift+A", command="ToggleToolSettings;", name="ToggleToolSettingsDisplay", mel=True)
    createHotkey("Ctrl+DOWN", command="SelectHierarchy;", name="SelHierarchy", mel=True)
    createHotkey("Ctrl+E", command="ExportSelection;", name="ExportSel", mel=True)
    createHotkey("Ctrl+Shift+E", command="Export;", name="ExportAll", mel=True)
    
    # Selection
    createHotkey("HOME", command=k.Hotkeys.utilsCmdForm.format("saveSelection()"), name="SaveSelection")
    createHotkey("PgUp", command=k.Hotkeys.utilsCmdForm.format("selectSavedSelection()"), name="SelectSaveSelection")
    createHotkey("PgDown", command=k.Hotkeys.utilsCmdForm.format("deselectSavedSelection()"), name="DeSelectSaveSelection")

    
def setupAnimationHotkeys():
    # Animation
    createHotkey("Alt+W", command=k.Hotkeys.utilsCmdForm.format("resetTranslation()"), name="ResetTranslation")
    createHotkey("Alt+E", command=k.Hotkeys.utilsCmdForm.format("resetRotation()"), name="ResetRotation")
    createHotkey("Alt+R", command=k.Hotkeys.utilsCmdForm.format("resetScale()"), name="ResetScale")
    createHotkey("Alt+C", command=k.Hotkeys.utilsCmdForm.format("toggleControlsVisibility()"), name="ToggleControlsVisibility")
    
    createHotkey("Ctrl+C", command=k.Hotkeys.utilsCmdForm.format("copyVertexWeightOrKey()"), name="CopyVertexWeightOrKey")
    createHotkey("Ctrl+V", command=k.Hotkeys.utilsCmdForm.format("pasteVertexWeightOrKey()"), name="PasteVertexWeightOrKey")

    
def setupRiggingHotkeys():
    # Rigging
    createHotkey("Alt+J", command=k.Hotkeys.utilsCmdForm.format("toggleJointsInViewport()"), name="ToggleJointsVisibility")
    createHotkey("Alt+N", command=k.Hotkeys.utilsCmdForm.format("toggleJointsXRay()"), name="ToggleJointsXRay")
    createHotkey("+", command=k.Hotkeys.utilsCmdForm.format("increaseManipulatorSize_Or_IncrementSelectVerticesBelow_Positive()"), name="increaseManipSize_Or_SelectVertivesBelowPos")
    createHotkey("-", command=k.Hotkeys.utilsCmdForm.format("decreaseManipulatorSize_Or_IncrementSelectVerticesBelow_Negative()"), name="decreaseManipSize_Or_SelectVertivesBelowNeg")
    createHotkey("Ctrl++", command=k.Hotkeys.utilsCmdForm.format("increment_ScaleSelectedCurve()"), name="ScaleCurvePositive")
    createHotkey("Ctrl+-", command=k.Hotkeys.utilsCmdForm.format("increment_ScaleSelectedCurve(positive=False)"), name="ScaleCurveNegative")
    
    # Skinning
    createHotkey("S", command=k.Hotkeys.utilsCmdForm.format("setKeyOrScaleSkinweights()"), name="SetKeyOrScaleSkinWeights")
    createHotkey("Shift+S", command=k.Hotkeys.utilsCmdForm.format("setKeyOrScaleSkinweights(weightValue=0.9)"), name="SetKeyOrScaleSkinWeightsLower")
    createHotkey("Alt+S", command=k.Hotkeys.utilsCmdForm.format("smoothSkinOrHIKFullBodyKey()"), name="SmoothSkinOrHIKFullBodyKey")
    createHotkey("Alt+Shift+D", command=k.Hotkeys.utilsCmdForm.format("deleteHistoryOrRemoveSkinning()"), name="DeleteHistoryOrRemoveSkinning")
    createHotkey("Alt+Shift+X", command=k.Hotkeys.utilsCmdForm.format("moveToOrigoOrWeightHammer()"), name="MoveToOrigo")

    # Skinning - Selection
    createHotkey("Alt+V", command=k.Hotkeys.utilsCmdForm.format("selectSkinVerticesOrPlay()"), name="SelectSkinVerticesOrSnapVertices")
    createHotkey("Shift+V", command=k.Hotkeys.utilsCmdForm.format("deselectSkinVerticesOrUnSnapVertices()"), name="DeselectSkinVerticesOrUnSnapVertices")
    createHotkey("Alt+Shift+V", command=k.Hotkeys.utilsCmdForm.format("selectInfluenceBelowOrGoToMinFrame()"), name="SelectInfluenceBelow")
    
    # Tech Anim marking menu
    markingMenus.setupTechAnimMarkingMenu(key="t")
    
    
def setupModelingHotkeys():
    # Modeling
    createHotkey("Alt+Shift+F", command="FreezeTransformations", name="FreezeTransform", mel=True)
    createHotkey("Alt+Shift+W", command=k.Hotkeys.utilsCmdForm.format("freezeTranslation()"), name="FreezeTranslation")
    createHotkey("Alt+Shift+E", command=k.Hotkeys.utilsCmdForm.format("freezeRotation()"), name="FreezeRotation")
    createHotkey("Alt+Shift+R", command=k.Hotkeys.utilsCmdForm.format("freezeScale()"), name="FreezeScale")
    createHotkey("Alt+Shift+C", command=k.Hotkeys.utilsCmdForm.format("pivotSwitch()"), name="PivotSwitch")
    # createHotkey("Alt+Shift+X", command=k.Hotkeys.utilsCmdForm.format("moveToOrigo()", name="MoveToOrigo")
    
    
def setupDefaultHotkeys():

    print "#"*40
    
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupGeneralHotkeys, True):
        print("    "+k.Module.name+": General Hotkeys Setup")
        setupGeneralHotkeys()
        
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupAnimationHotkeys, True):
        print("    "+k.Module.name+": Animation Hotkeys Setup")
        setupAnimationHotkeys()
        
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupRiggingHotkeys, True):
        print("    "+k.Module.name+": Rigging Hotkeys Setup")
        setupRiggingHotkeys()
        
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupModelingHotkeys, True):
        print("    "+k.Module.name+": Modeling Hotkeys Setup")
        setupModelingHotkeys()
        
    print(k.Module.name+": Hotkeys Setup")
