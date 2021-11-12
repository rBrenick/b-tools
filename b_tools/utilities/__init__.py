from b_tools.utilities.animation import *
from b_tools.utilities.rigging import *
from b_tools.utilities.modeling import *
from b_tools.utilities.hotkeys import *
from b_tools.utilities.general import *


def reload_modules():
    import sys
    if sys.version_info.major > 2:
        from importlib import reload
    else:
        from imp import reload
    reload(sys.modules.get("b_tools.utilities.animation"))
    reload(sys.modules.get("b_tools.utilities.rigging"))
    reload(sys.modules.get("b_tools.utilities.modeling"))
    reload(sys.modules.get("b_tools.utilities.hotkeys"))
    reload(sys.modules.get("b_tools.utilities.general"))
    reload(sys.modules.get("b_tools.utilities"))
    reload(sys.modules.get("b_tools.constants"))
    sys.stdout.write("Module Reloaded\n")

