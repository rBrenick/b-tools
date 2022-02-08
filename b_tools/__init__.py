import os
import sys


def main():
    import b_tools.ui.menu
    return b_tools.ui.menu.setup()


def unload_module():
    pkg_dir = os.path.abspath(os.path.dirname(__file__))

    def _is_part_of_pkg(module_):
        mod_path = getattr(module_, "__file__", os.sep)
        if mod_path:
            mod_dir = os.path.abspath(os.path.dirname(mod_path))
            return mod_dir.startswith(pkg_dir)

    to_unload = [name for name, module in sys.modules.items() if _is_part_of_pkg(module)]

    for name in to_unload:
        print("Clearing from sys.modules: {}".format(name))
        sys.modules.pop(name)
