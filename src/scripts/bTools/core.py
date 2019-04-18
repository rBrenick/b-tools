import logging

def Logger(name):
    return logging.getLogger(name)

log = Logger("bTools")

import bTools.ui.qtUtils as qt
from bTools import utilities as utils


