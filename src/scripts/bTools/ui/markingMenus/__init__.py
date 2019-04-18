# bTools
import bTools.constants as k

import pymel.core as pm

from . import mm_TechAnim; reload(mm_TechAnim)


def createMarkingMenuCommand(rtc, command):
    if pm.runTimeCommand(rtc, exists=True):
        pm.runTimeCommand(rtc, edit=True, delete=True)
    pm.runTimeCommand(rtc, category=k.MarkingMenus.category, command=k.MarkingMenus.cmdForm.format(command), commandLanguage="python")
    nc = pm.nameCommand(rtc+"NameCommand", annotation=rtc+'NameCommand generated', command=rtc)
    return nc


# TechAnim MarkingMenu
def setupTechAnimMarkingMenu(key="t"):
    press = createMarkingMenuCommand("TechAnimMarkingMenu_Press", "techAnim_MarkingMenu_Press()")
    release = createMarkingMenuCommand("TechAnimMarkingMenu_Release", "techAnim_MarkingMenu_Release()")
    pm.hotkey(k=key, name=press)
    pm.hotkey(k=key, releaseName=release)
    
def techAnim_MarkingMenu_Press():
    reload(mm_TechAnim)
    mm_TechAnim.removeOldMarkingMenu()
    mm_TechAnim.markingMenu()

def techAnim_MarkingMenu_Release():
    mm_TechAnim.removeOldMarkingMenu()



