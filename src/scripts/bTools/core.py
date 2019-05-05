import logging


def Logger(name):
    return logging.getLogger(name)


log = Logger("bTools")

import bTools.ui.qt_utils as qt
from bTools import utilities as utils


