
import os
import json
import collections

import pymel.core as pm
from maya import cmds
import b_tools.constants as k


MENU_NAME = k.Module.name
MAYA_MENU_JSON = os.path.join(os.path.dirname(__file__), "maya_menu.json")


def create_command(path="b_tools", command="main()"):
    return 'exec("import {modulePath}; reload({modulePath}); {modulePath}.{cmd}")'.format(modulePath=path, cmd=command)


def read_menu_json():
    with open(MAYA_MENU_JSON, "r+") as fp:
        data = json.load(fp, object_pairs_hook=collections.OrderedDict)
    return data


def create_menu():
    pm.menu(MENU_NAME, parent="MayaWindow", allowOptionBoxes=True, tearOff=True)

    all_menu_data = read_menu_json()
    for item_name, item_data in all_menu_data.get("menu_items", {}).items():
        setup_menu_item(item_name, item_data)

    print("b_tools menu built")


def setup_menu_item(item_name, item_data):
    item_is_divider = item_data == "-----"
    if item_is_divider:
        pm.menuItem(label=item_name, divider=True)
        return

    item_is_sub_menu = item_data.get("sub_menu", "False") == "True"
    if item_is_sub_menu:
        pm.menuItem(subMenu=True, label=item_name)
        item_data.pop("sub_menu")
        for item_name, item_data in item_data.items():
            setup_menu_item(item_name, item_data)  # recursive
        pm.setParent('..', menu=True)
        return

    item_module = item_data.get("module")
    item_command = item_data.get("command")
    item_is_option_box = item_data.get("option_box", "False") == "True"
    item_language = item_data.get("language")

    menu_item_kwargs = dict()
    menu_item_kwargs["command"] = create_command(item_module, item_command)
    menu_item_kwargs["optionBox"] = item_is_option_box

    pm.menuItem(item_name, **menu_item_kwargs)


def setup():
    if pm.menu(MENU_NAME, q=True, exists=True):
        cmds.evalDeferred('cmds.deleteUI("' + MENU_NAME + '")')

    cmds.evalDeferred('import b_tools.ui.menu; b_tools.ui.menu.create_menu()')


def delete_menu(menu_name=MENU_NAME):
    """
    This is not used anywhere, but is being kept for posterity
    
    """
    menu_map = {}
    for m in pm.lsUI(m=True):
        if m.getLabel():
            menu_map[m.getLabel()] = m

    pm.deleteUI(menu_map.get(menu_name))


