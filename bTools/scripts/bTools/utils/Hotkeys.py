import pymel.core as pm
import bTools.ui as btUI; reload(btUI)
import bTools.constants as k


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
    

MODULE_FORM = "import bTools.utils; bTools.utils.{}"


def setupGeneralHotkeys():

    createHotkey("9", command="HotkeyPreferencesWindow;", name="ShowHotkeyWindow", mel=True)
    createHotkey("Alt+Shift+A", command="ToggleToolSettings;", name="ToggleToolSettingsDisplay", mel=True)

    # Selection
    createHotkey("HOME", command=MODULE_FORM.format("saveSelection()"), name="SaveSelection")
    createHotkey("PgUp", command=MODULE_FORM.format("selectSavedSelection()"), name="SelectSaveSelection")
    createHotkey("PgDown", command=MODULE_FORM.format("deselectSavedSelection()"), name="DeSelectSaveSelection")

    
def setupAnimationHotkeys():
    # Animation
    createHotkey("Alt+W", command=MODULE_FORM.format("resetTranslation()"), name="ResetTranslation")
    createHotkey("Alt+E", command=MODULE_FORM.format("resetRotation()"), name="ResetRotation")
    createHotkey("Alt+R", command=MODULE_FORM.format("resetScale()"), name="ResetScale")
    createHotkey("Alt+C", command=MODULE_FORM.format("toggleControlsVisibility()"), name="ToggleControlsVisibility")
    
    createHotkey("Ctrl+C", command="timeSliderCopyKey;", name="CopyKey", mel=True)
    createHotkey("Ctrl+V", command="timeSliderPasteKey false;", name="PasteKey", mel=True)

    
def setupRiggingHotkeys():
    # Rigging
    createHotkey("Alt+J", command=MODULE_FORM.format("toggleJointsInViewport()"), name="ToggleJointsVisibility")
    createHotkey("Alt+N", command=MODULE_FORM.format("toggleJointsXRay()"), name="ToggleJointsXRay")
    createHotkey("+", command=MODULE_FORM.format("scaleSelectedCurve_Positive_Or_IncrementSelectVerticesBelow_Positive()"), name="ScaleCurvePositive")
    createHotkey("-", command=MODULE_FORM.format("scaleSelectedCurve_Negative_Or_IncrementSelectVerticesBelow_Negative()"), name="ScaleCurveNegative")
    
    # Skinning
    createHotkey("S", command=MODULE_FORM.format("setKeyOrScaleSkinweights()"), name="SetKeyOrScaleSkinWeights")
    createHotkey("Shift+S", command=MODULE_FORM.format("setKeyOrScaleSkinweights(weightValue=0.9)"), name="SetKeyOrScaleSkinWeightsLower")
    createHotkey("Alt+S", command=MODULE_FORM.format("smoothSkinOrHIKFullBodyKey()"), name="SmoothSkinOrHIKFullBodyKey")
    createHotkey("Alt+Shift+D", command=MODULE_FORM.format("deleteHistoryOrRemoveSkinning()"), name="DeleteHistoryOrRemoveSkinning")
    createHotkey("Alt+Shift+X", command=MODULE_FORM.format("moveToOrigoOrWeightHammer()"), name="MoveToOrigo")

    # Skinning - Selection
    createHotkey("Alt+V", command=MODULE_FORM.format("selectSkinVerticesOrPlay()"), name="SelectSkinVerticesOrSnapVertices")
    createHotkey("Shift+V", command=MODULE_FORM.format("deselectSkinVerticesOrUnSnapVertices()"), name="DeselectSkinVerticesOrUnSnapVertices")
    createHotkey("Alt+Shift+V", command=MODULE_FORM.format("selectInfluenceBelowOrGoToMinFrame()"), name="SelectInfluenceBelow")
    

def setupModelingHotkeys():
    # Modeling
    createHotkey("Alt+Shift+W", command=MODULE_FORM.format("freezeTranslation()"), name="FreezeTranslation")
    createHotkey("Alt+Shift+E", command=MODULE_FORM.format("freezeRotation()"), name="FreezeRotation")
    createHotkey("Alt+Shift+R", command=MODULE_FORM.format("freezeScale()"), name="FreezeScale")
    createHotkey("Alt+Shift+C", command=MODULE_FORM.format("pivotSwitch()"), name="PivotSwitch")
    createHotkey("Alt+Shift+C", command=MODULE_FORM.format("pivotSwitch()"), name="PivotSwitch")
    # createHotkey("Alt+Shift+X", command=MODULE_FORM.format("moveToOrigo()", name="MoveToOrigo")
    
    
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
