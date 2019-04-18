
from cStringIO import StringIO
import xml.etree.ElementTree as xml
from Qt import QtCompat, QtWidgets, QtCore, QtGui



def getTopWindow():
    return getMayaWindow()


def getMayaWindow():
    from maya import OpenMayaUI as omui
    mayaMainWindowPtr = omui.MQtUtil().mainWindow()
    mayaMainWindow = QtCompat.wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)
    return mayaMainWindow


def launchExampleWindow():
    # WORKS: Widget is fine
    hello = QtWidgets.QLabel("Hello, World", parent=getMayaWindow())
    hello.setObjectName('MyLabel')
    hello.setWindowFlags(QtCore.Qt.Window)  # Make this widget a standalone window even though it is parented
    hello.show()
    return hello


def compileUIFile(uiFilePath=None):
    pyPath = uiFilePath.replace(".ui", ".py")
    with open(pyPath, 'w') as pyFile:
        pysideuic.compileUi(uiFilePath, pyFile, False, 4, False)


## REWRITE THIS
def deleteWindow(object):
    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if "__class__" in dir(widget):
            if str(widget.__class__) == str(object.__class__):
                widget.deleteLater()
                widget.close()


# Sorry
def getQWidget(name, qType=QtWidgets.QWidget):
    import maya.OpenMayaUI as apiUI

    dockPt = apiUI.MQtUtil.findControl(name)  # Find the pointer to the dock control
    if dockPt is not None:
        return QtCompat.wrapInstance(long(dockPt), qType)
    else:
        print("No control found for", name)
        return None

def compileUi(*args, **kvargs):
    """ Run standard compileUi from eater PySide2 or PySide (dependence on which is available)"""
    try:
        import pyside2uic as pysideuic
    except ImportError:
        import pysideuic as pysideuic

    return pysideuic.compileUi(*args, **kvargs)
    
def loadUiType(uiFile):
    """Pyside equivalent for the loadUiType function in PyQt.
    From the PyQt4 documentation:
        Load a Qt Designer .ui file and return a tuple of the generated form
        class and the Qt base class. These can then be used to create any
        number of instances of the user interface without having to parse the
        .ui file more than once.
    Note:
        Pyside lacks the "loadUiType" command, so we have to convert the ui
        file to py code in-memory first and then execute it in a special frame
        to retrieve the form_class.
    Args:
        uifile (str): Absolute path to .ui file
    Returns:
        tuple: the generated form class, the Qt base class
    """

    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtWidgets.%s' % widget_class)
    return form_class, base_class
                

class cameraWindow(QtWidgets.QDialog):
    """
    SOURCE: http://blog.virtualmethodstudio.com/2017/03/embed-maya-native-ui-objects-in-pyside2/
    """
    def __init__(self, parent=getMayaWindow(), **kwargs):
        super(cameraWindow, self).__init__(parent, **kwargs)
        self.resize(500, 500)

        qtLayout = QtWidgets.QVBoxLayout()
        qtLayout.setObjectName('viewportLayout')

        pm.setParent('viewportLayout')
        paneLayoutName = pm.paneLayout()

        modelPanel = pm.modelPanel("embeddedModelPanel#", cam='persp')

        ptr = omui.MQtUtil.findControl(paneLayoutName)
        paneLayoutQt = wrapInstance(long(ptr), QtWidgets.QWidget)

        qtLayout.addWidget(paneLayoutQt)

        self.show()


