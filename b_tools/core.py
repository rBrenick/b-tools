import logging


def Logger(name):
    return logging.getLogger(name)


log = Logger("b_tools")

import b_tools.ui.ui_utils as qt
from b_tools import utilities as utils


