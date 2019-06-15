
class Module:
    name = "b_tools"


class Hotkeys:
    utils_cmd_form = "import b_tools.utilities; b_tools.utilities.{}"


class MarkingMenus:
    category = Module.name+"_MarkingMenus"
    cmd_form = "import b_tools.ui.marking_menus; b_tools.ui.marking_menus.{}"


class OptionVars:
    SavedSelection = "b_tools_SavedSelection"
    SelectVerticesBelowInfluence = "b_tools_SelectVerticesBelowInfluence"

