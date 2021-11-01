# b_tools
import b_tools.constants as k

import pymel.core as pm

from . import mm_tech_anim


def create_marking_menu_command(rtc, command):
    if pm.runTimeCommand(rtc, exists=True):
        pm.runTimeCommand(rtc, edit=True, delete=True)
    pm.runTimeCommand(rtc, category=k.MarkingMenus.category, command=k.MarkingMenus.cmd_form.format(command), commandLanguage="python")
    nc = pm.nameCommand(rtc+"NameCommand", annotation=rtc+'NameCommand generated', command=rtc)
    return nc


# TechAnim MarkingMenu
def setup_tech_anim_marking_menu(key="t"):
    press = create_marking_menu_command("TechAnimMarkingMenu_Press", "tech_anim_marking_menu_press()")
    release = create_marking_menu_command("TechAnimMarkingMenu_Release", "tech_anim_marking_menu_release()")
    pm.hotkey(k=key, name=press)
    pm.hotkey(k=key, releaseName=release)


def tech_anim_marking_menu_press():
    mm_tech_anim.remove_old_marking_menu()
    mm_tech_anim.Markingmenu()


def tech_anim_marking_menu_release():
    mm_tech_anim.remove_old_marking_menu()



