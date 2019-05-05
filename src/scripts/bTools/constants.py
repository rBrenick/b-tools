
class Module:
    name = "bTools"


class Hotkeys:
    utils_cmd_form = "import bTools.utilities; bTools.utilities.{}"


class MarkingMenus:
    category = Module.name+"_MarkingMenus"
    cmd_form = "import bTools.ui.marking_menus; bTools.ui.marking_menus.{}"


class OptionVars:
    SavedSelection = "bTools_SavedSelection"
    SelectVerticesBelowInfluence = "bTools_SelectVerticesBelowInfluence"

