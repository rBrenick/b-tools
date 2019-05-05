
from cStringIO import StringIO
import xml.etree.ElementTree as xml

# Not even going to pretend to have Maya 2016 support
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools


def get_top_window():
    return get_app_window()


def get_app_window():
    top_window = None
    try:
        from maya import OpenMayaUI as omui
        maya_main_window_ptr = omui.MQtUtil().mainWindow()
        top_window = wrapInstance(long(maya_main_window_ptr), QtWidgets.QMainWindow)
    except ImportError, e:
        pass
    return top_window


def launch_example_window():
    hello = QtWidgets.QLabel("Hello, World", parent=get_app_window())
    hello.setObjectName('MyLabel')
    hello.setWindowFlags(QtCore.Qt.Window)  # Make this widget a standalone window even though it is parented
    hello.show()
    return hello


def compile_ui_file(ui_file_path=None):
    py_path = ui_file_path.replace(".ui", ".py")
    with open(py_path, 'w') as pyFile:
        pysideuic.compileUi(ui_file_path, pyFile, False, 4, False)


def delete_window(window_class):
    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if "__class__" in dir(widget):
            if str(widget.__class__) == str(window_class.__class__):
                widget.deleteLater()
                widget.close()


# Sorry
def get_QWidget(name, q_type=QtWidgets.QWidget):
    import maya.OpenMayaUI as apiUI

    dock_pt = apiUI.MQtUtil.findControl(name)  # Find the pointer to the dock control
    if dock_pt is not None:
        return wrapInstance(long(dock_pt), q_type)
    else:
        print("No control found for", name)
        return None


def compile_ui(*args, **kvargs):
    """ Run standard compileUi from eater PySide2 or PySide (dependence on which is available)"""
    try:
        import pyside2uic as pysideuic
    except ImportError:
        import pysideuic as pysideuic

    return pysideuic.compileUi(*args, **kvargs)


def load_ui_type(ui_file):
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

    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        compile_ui(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtWidgets.%s' % widget_class)
    return form_class, base_class
                

class CameraWindow(QtWidgets.QDialog):
    """
    SOURCE: http://blog.virtualmethodstudio.com/2017/03/embed-maya-native-ui-objects-in-pyside2/
    """
    def __init__(self, parent=get_app_window(), **kwargs):
        super(CameraWindow, self).__init__(parent, **kwargs)
        self.resize(500, 500)

        qt_layout = QtWidgets.QVBoxLayout()
        qt_layout.setObjectName('viewportLayout')

        pm.setParent('viewportLayout')
        pane_layout_name = pm.paneLayout()

        model_panel = pm.modelPanel("embeddedModelPanel#", cam='persp')

        ptr = omui.MQtUtil.findControl(pane_layout_name)
        pane_layout_qt = wrapInstance(long(ptr), QtWidgets.QWidget)

        qt_layout.addWidget(pane_layout_qt)

        self.show()


