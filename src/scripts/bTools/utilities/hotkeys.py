import pymel.core as pm
import bTools.constants as k

import bTools.ui as bt_ui
reload(bt_ui)
from bTools.ui import marking_menus
reload(marking_menus)


def create_hotkey(command_hotkey, command=None, name=None, mel=False, maya_default=False):
    # prev_cmd = pm.hotkey(cmdHotkey, query=True, name=True)
    nice_name_hotkey = command_hotkey
    if pm.hotkeySet(q=True, current=True) == "Maya_Default":
        pm.hotkeySet("bTools", current=True, source='Maya_Default')

    if not name:
        name = command.split(".")[-1]
        
    if maya_default:
        nc = name
    else:
        rtc = name
        nc = name+"NameCommand"
        
        if pm.runTimeCommand(rtc, exists=True):
            pm.runTimeCommand(rtc, edit=True, delete=True)
        
        command_language = "python"
        if mel:
            command_language = "mel"
            
        rtc = pm.runTimeCommand(rtc, annotation=name+' Hotkey generated', category=k.Module.name, command=command, commandLanguage=command_language)
        nc = pm.nameCommand(nc, annotation=name+' nameCommand generated', command=rtc)
    
    hotkey_params = dict()
    hotkey_params["name"] = nc
    
    if "alt" in command_hotkey.lower():
        hotkey_params["altModifier"] = True
        command_hotkey = command_hotkey.lower().replace("alt+", "")
        
    if "ctrl" in command_hotkey.lower():
        hotkey_params["ctrlModifier"] = True
        command_hotkey = command_hotkey.lower().replace("ctrl+", "")
        
    if "shift" in command_hotkey.lower():
        hotkey_params["shiftModifier"] = True
        command_hotkey = command_hotkey.lower().replace("shift+", "")
        
    hotkey_params["keyShortcut"] = command_hotkey.lower()
    pm.hotkey(**hotkey_params)
    print "       {}        {}".format(nice_name_hotkey, rtc)


class HotkeyOptionsMenu(bt_ui.DefaultWindow):

    kSetupGeneralHotkeys = k.Module.name+"_SetupGeneralHotkeys"
    kSetupAnimationHotkeys = k.Module.name+"_SetupAnimationHotkeys"
    kSetupModelingHotkeys = k.Module.name+"_SetupModelingHotkeys"
    kSetupRiggingHotkeys = k.Module.name+"_SetupRiggingHotkeys"
    
    def __init__(self, window_title="HotkeyOptions"):
        super(HotkeyOptionsMenu, self).__init__(window_title)

    @staticmethod
    def set_option_var_general(*args):
        pm.optionVar[HotkeyOptionsMenu.kSetupGeneralHotkeys] = args[0]

    @staticmethod
    def set_option_var_animation(*args):
        pm.optionVar[HotkeyOptionsMenu.kSetupAnimationHotkeys] = args[0]

    @staticmethod
    def set_option_var_modeling(*args):
        pm.optionVar[HotkeyOptionsMenu.kSetupModelingHotkeys] = args[0]

    @staticmethod
    def set_option_var_rigging(*args):
        pm.optionVar[HotkeyOptionsMenu.kSetupRiggingHotkeys] = args[0]
        
    def setup_ui(self):
        with pm.verticalLayout():
            pm.separator(height=40, style="none")
            
            pm.checkBox(label='Setup General Hotkeys',
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupGeneralHotkeys, True),
                        changeCommand=self.set_option_var_general)
            
            pm.checkBox(label='Setup Animation Hotkeys',
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupAnimationHotkeys, True),
                        changeCommand=self.set_option_var_animation)
                        
            pm.checkBox(label='Setup Modeling Hotkeys',
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupModelingHotkeys, True),
                        changeCommand=self.set_option_var_modeling)
                        
            pm.checkBox(label='Setup Rigging Hotkeys',
                        value=pm.optionVar.get(HotkeyOptionsMenu.kSetupRiggingHotkeys, True),
                        changeCommand=self.set_option_var_rigging)

    def main(self):
        setup_default_hotkeys()

            
def show_hotkey_options_menu():
    win = HotkeyOptionsMenu()
    return win
    

def setup_general_hotkeys():
    # General
    create_hotkey("9", command="HotkeyPreferencesWindow;", name="ShowHotkeyWindow", mel=True)
    create_hotkey("Alt+Shift+A", command="ToggleToolSettings;", name="ToggleToolSettingsDisplay", mel=True)
    create_hotkey("Ctrl+DOWN", command="SelectHierarchy;", name="SelHierarchy", mel=True)
    create_hotkey("Ctrl+E", command="ExportSelection;", name="ExportSel", mel=True)
    create_hotkey("Ctrl+Shift+E", command="Export;", name="ExportAll", mel=True)
    
    # Selection
    create_hotkey("HOME", command=k.Hotkeys.utils_cmd_form.format("save_selection()"), name="SaveSelection")
    create_hotkey("PgUp", command=k.Hotkeys.utils_cmd_form.format("select_saved_selection()"), name="SelectSaveSelection")
    create_hotkey("PgDown", command=k.Hotkeys.utils_cmd_form.format("deselect_saved_selection()"), name="DeSelectSaveSelection")

    
def setup_animation_hotkeys():
    # Animation
    create_hotkey("Alt+W", command=k.Hotkeys.utils_cmd_form.format("reset_translation()"), name="ResetTranslation")
    create_hotkey("Alt+E", command=k.Hotkeys.utils_cmd_form.format("reset_rotation()"), name="ResetRotation")
    create_hotkey("Alt+R", command=k.Hotkeys.utils_cmd_form.format("reset_scale()"), name="ResetScale")
    create_hotkey("Alt+C", command=k.Hotkeys.utils_cmd_form.format("toggle_controls_visibility()"), name="ToggleControlsVisibility")
    
    create_hotkey("Ctrl+C", command=k.Hotkeys.utils_cmd_form.format("copy_vertex_weight_or_key()"), name="CopyVertexWeightOrKey")
    create_hotkey("Ctrl+V", command=k.Hotkeys.utils_cmd_form.format("paste_vertex_weight_or_key()"), name="PasteVertexWeightOrKey")

    
def setup_rigging_hotkeys():
    # Rigging
    create_hotkey("Alt+J", command=k.Hotkeys.utils_cmd_form.format("toggle_joints_in_viewport()"), name="ToggleJointsVisibility")
    create_hotkey("Alt+N", command=k.Hotkeys.utils_cmd_form.format("toggle_joints_x_ray()"), name="ToggleJointsXRay")
    create_hotkey("+", command=k.Hotkeys.utils_cmd_form.format("increase_manipulator_size_or_increment_select_vertices_below_positive()"), name="increaseManipSize_Or_SelectVertivesBelowPos")
    create_hotkey("-", command=k.Hotkeys.utils_cmd_form.format("decrease_manipulatorSize_Or_IncrementSelectVerticesBelow_Negative()"), name="decreaseManipSize_Or_SelectVertivesBelowNeg")
    create_hotkey("Ctrl++", command=k.Hotkeys.utils_cmd_form.format("increment_scale_selected_curve()"), name="ScaleCurvePositive")
    create_hotkey("Ctrl+-", command=k.Hotkeys.utils_cmd_form.format("increment_scale_selected_curve(positive=False)"), name="ScaleCurveNegative")
    
    # Skinning
    create_hotkey("S", command=k.Hotkeys.utils_cmd_form.format("set_key_or_scale_skinweights()"), name="SetKeyOrScaleSkinWeights")
    create_hotkey("Shift+S", command=k.Hotkeys.utils_cmd_form.format("set_key_or_scale_skinweights(weight_value=0.9)"), name="SetKeyOrScaleSkinWeightsLower")
    create_hotkey("Alt+S", command=k.Hotkeys.utils_cmd_form.format("smooth_skin_or_hik_full_body_key()"), name="SmoothSkinOrHIKFullBodyKey")
    create_hotkey("Alt+Shift+D", command=k.Hotkeys.utils_cmd_form.format("delete_history_or_remove_skinning()"), name="DeleteHistoryOrRemoveSkinning")
    create_hotkey("Alt+Shift+X", command=k.Hotkeys.utils_cmd_form.format("move_to_origo_or_weight_hammer()"), name="MoveToOrigo")

    # Skinning - Selection
    create_hotkey("Alt+V", command=k.Hotkeys.utils_cmd_form.format("select_skin_vertices_or_play()"), name="SelectSkinVerticesOrSnapVertices")
    create_hotkey("Shift+V", command=k.Hotkeys.utils_cmd_form.format("deselect_skin_vertices_or_unsnap_vertices()"), name="DeselectSkinVerticesOrUnSnapVertices")
    create_hotkey("Alt+Shift+V", command=k.Hotkeys.utils_cmd_form.format("select_influence_below_or_go_to_min_frame()"), name="SelectInfluenceBelow")
    
    # Tech Anim marking menu
    marking_menus.setup_tech_anim_marking_menu(key="t")
    
    
def setup_modeling_hotkeys():
    # Modeling
    create_hotkey("Alt+Shift+F", command="FreezeTransformations", name="FreezeTransform", mel=True)
    create_hotkey("Alt+Shift+W", command=k.Hotkeys.utils_cmd_form.format("freeze_translation()"), name="FreezeTranslation")
    create_hotkey("Alt+Shift+E", command=k.Hotkeys.utils_cmd_form.format("freeze_rotation()"), name="FreezeRotation")
    create_hotkey("Alt+Shift+R", command=k.Hotkeys.utils_cmd_form.format("freeze_scale()"), name="FreezeScale")
    create_hotkey("Alt+Shift+C", command=k.Hotkeys.utils_cmd_form.format("pivot_switch()"), name="PivotSwitch")
    # createHotkey("Alt+Shift+X", command=k.Hotkeys.utilsCmdForm.format("moveToOrigo()", name="MoveToOrigo")
    
    
def setup_default_hotkeys():

    print "#"*40
    
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupGeneralHotkeys, True):
        print("    "+k.Module.name+": General Hotkeys Setup")
        setup_general_hotkeys()
        
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupAnimationHotkeys, True):
        print("    "+k.Module.name+": Animation Hotkeys Setup")
        setup_animation_hotkeys()
        
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupRiggingHotkeys, True):
        print("    "+k.Module.name+": Rigging Hotkeys Setup")
        setup_rigging_hotkeys()
        
    if pm.optionVar.get(HotkeyOptionsMenu.kSetupModelingHotkeys, True):
        print("    "+k.Module.name+": Modeling Hotkeys Setup")
        setup_modeling_hotkeys()
        
    print(k.Module.name+": Hotkeys Setup")


