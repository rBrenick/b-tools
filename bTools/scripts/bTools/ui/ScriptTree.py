try:
  from PySide2.QtCore import * 
  from PySide2.QtGui import * 
  from PySide2.QtWidgets import *
  from shiboken2 import wrapInstance
except ImportError:
  from PySide.QtCore import * 
  from PySide.QtGui import * 
  from shiboken import wrapInstance
  
  
import os
import stat
import pymel.core as pm
import json
from maya import OpenMayaUI as omui 
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin


SETTINGS_FILEPATH = os.path.join(pm.internalVar(upd=True), "ScriptFileTree.ini")


def printArguments(*args):
    print("Args", args)

def doNothing(*args):
    pass

    
def deleteControl(control):
    if pm.workspaceControl(control, q=True, exists=True):
        pm.workspaceControl(control, e=True, close=True)
        pm.deleteUI(control, control=True)


def main(dock=True):
    # First create the script editor and dock it to something first, otherwise it displays strange
    if dock:
        pm.mel.eval("ScriptEditor")
        pm.workspaceControl("scriptEditorPanel1Window", edit=True, dockToControl=["Outliner", "left"])
        pm.workspaceControl("scriptEditorPanel1Window", edit=True, floating=True)
    
    name = "ScriptTree"
    workspaceName = name + "WorkspaceControl"
    deleteControl(workspaceName)
    dockableWidget = ScriptTreeDockableWindow(name=name)
    
    if dock:        
        # Dock it to the script editor
        pm.workspaceControl(workspaceName, edit=True, dockToControl=["scriptEditorPanel1Window", "left"])
       

    return dockableWidget

class ScriptTreeDockableWindow(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, rootWidget=None, name="Script FileTree", *args, **kwargs):
        super(ScriptTreeDockableWindow, self).__init__(*args, **kwargs)
        # Destroy this widget when closed.  Otherwise it will stay around
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        self.setObjectName(name)
        self.setWindowTitle(name)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        self.initUI()
        
        self.show(dockable=True, area='left', allowedArea="left",  floating=True)
        self.treeWidgets.loadSettings()
    
    def initUI(self):
        
        self.treeWidgets = ScriptFileTreeWidgets()
        self.setCentralWidget(self.treeWidgets)
        
        self.myQMenuBar = self.menuBar()
        
        fileMenu = self.myQMenuBar.addMenu('File')
        self.createAction(name="Open", command=self.openFile, hotkey="Ctrl+O", menu=fileMenu)
        self.createAction(name="Save", command=self.treeWidgets.saveSelected, hotkey="Ctrl+S", menu=fileMenu)
        self.createAction(name="Save As...", command=self.treeWidgets.saveAsSelected, hotkey="Ctrl+Shift+S", menu=fileMenu)
        self.createAction(name="Save Preferences", command=self.treeWidgets.saveSettings, hotkey="Alt+Shift+S", menu=fileMenu)
        self.createAction(name="Reload Tab", command=self.treeWidgets.reloadTab, hotkey="F5", menu=fileMenu)
        self.createAction(name="Save Script Editor", command=pm.mel.syncExecuterBackupFiles, menu=fileMenu)
        
        # edit menu
        editMenu = self.myQMenuBar.addMenu('Edit')
        self.createAction(name="Clear Output", command=self.clearScriptOutput, hotkey="Alt+Shift+D", menu=editMenu)
    
    def createAction(self, name="Action", command=doNothing, hotkey=None, menu=None):
        action = QAction(name, self)
        action.triggered.connect(command)
        if hotkey:
            action.setShortcut(hotkey)
        menu.addAction(action)
    
    def openFile(self):
        fileQuery = pm.fileDialog2(fileMode=4, fileFilter="*.py", dialogStyle=1)
        if not fileQuery:
            return
            
        path = fileQuery[0]
            
        scriptTab = addScriptToEditor(path)
        if scriptTab:
            addScriptTabToSettings(scriptTab)
    
    def clearScriptOutput(self):
        pm.scriptEditorInfo(clearHistory=True)
        
    def dockCloseEventTriggered(self):
        pass
        # pm.mel.syncExecuterBackupFiles()
        # self.deleteInstances()
    

class ScriptFileTreeWidgets(QWidget):
    def __init__(self, parent=None):
        super(ScriptFileTreeWidgets, self).__init__(parent)
        self.scripts = []
        
        self.fileWatcher = QFileSystemWatcher()
        self.fileWatcher.fileChanged.connect(self.scriptUpdated)
        
        self.networkTree = None
        self.localTree = None
        self.splitterHeight = 0
        
        self.setObjectName('ScriptFileTreeWidget')
        
        self.initUI()
        self.loadSettings()
        self.readCurrentTabs()
        
    def initUI(self):
        
        # saveButton = QPushButton("Save Selected Tab")
        # saveButton.clicked.connect(self.saveSelected)
        
        self.networkTree = ScriptTreeWidget(FileTreeSettings.kNetworkFolder, parent=self)
        self.localTree = ScriptTreeWidget(FileTreeSettings.kLocalFolder, parent=self)
        
        # Add to main layout
        self.mainLayout = QVBoxLayout()
        # self.mainLayout.addWidget(saveButton)
        
        # Add File trees to a splitter
        self.split = QSplitter()
        self.split.setOrientation(Qt.Vertical)
        self.split.addWidget(self.networkTree)
        self.split.addWidget(self.localTree)
        self.split.splitterMoved.connect(self.setSplitterHeight)
        
        self.connectCurrentTabCheck()
        
        self.mainLayout.addWidget(self.split)        
        self.mainLayout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.mainLayout)
       
    def loadSettings(self):
        settings = FileTreeSettings()
        
        # Set folders on file trees
        self.networkTree.loadSettings()
        self.localTree.loadSettings()
        
        # Restore Splitter Height from settings
        storedSplitterHeight = settings.data.get(FileTreeSettings.kSplitter, {}).get(FileTreeSettings.kSplitterHeight, 1000)
        self.split.moveSplitter(storedSplitterHeight, 1)
        
    def saveSettings(self):
        self.networkTree.saveSettings()
        self.localTree.saveSettings()
        self.saveSplitterSettings()
        print("ScriptTree: Preferences Saved")
    
    def saveSplitterSettings(self):
        settings = FileTreeSettings()
        settings.data[FileTreeSettings.kSplitter][FileTreeSettings.kSplitterHeight] = self.splitterHeight
        settings.save()
    
    def setSplitterHeight(self, *args):
        self.splitterHeight = args[0]
        
    def readCurrentTabs(self):
        self.scripts = []
        settings = FileTreeSettings()
        tabFilePaths = settings.data.get(FileTreeSettings.kTabPaths, {})
        
        melTabsLayout = pm.melGlobals["$gCommandExecuterTabs"]
        tabLayout = pm.ui.TabLayout(melTabsLayout)
        
        tabsChildArray = tabLayout.getChildArray()
        tabNames = pm.tabLayout(melTabsLayout, q=True, tabLabel=True)
        
        for tab, tabName in zip(tabsChildArray, tabNames):
            scriptTab = ScriptTab(tab=tab)
            self.scripts.append(scriptTab)
            
            # Get saved info
            tabFilePath = tabFilePaths.get(tabName)
            
            if tabFilePath:
                scriptTab.setFileInfo(tabFilePath)
                if tabFilePath not in self.fileWatcher.files():
                    self.fileWatcher.addPath(tabFilePath)
    
    def scriptUpdated(self, *filePaths):
        scriptTabs = self.scripts
        
        for path in filePaths:
            for scriptTab in scriptTabs:
                if scriptTab.selected and scriptTab.filePath == path:
                    scriptTabs.pop(scriptTabs.index(scriptTab))
                    scriptTab.promptReload()
                    
        self.readCurrentTabs()
    
    def connectCurrentTabCheck(self):
        melTabsLayout = pm.melGlobals["$gCommandExecuterTabs"]
        tabLayout = pm.ui.TabLayout(melTabsLayout)
        tabLayout.changeCommand(self.checkCurrentTabUpdated)
        
    def disconnectCurrentTabCheck(self):
        melTabsLayout = pm.melGlobals["$gCommandExecuterTabs"]
        tabLayout = pm.ui.TabLayout(melTabsLayout)
        tabLayout.changeCommand(doNothing)
    
    def checkCurrentTabUpdated(self, *args):
        self.readCurrentTabs()
        selTab = self.getSelectedTab()
        
        if not selTab or not selTab.filePath:
            return
        
        tabContent = selTab.textArea.toPlainText()
        with open(selTab.filePath, "r") as f:
            fileContents = f.read()
        
        if tabContent != fileContents:
            selTab.promptReload()

    def getSelectedTab(self):
    
        # melTab = pm.mel.getCurrentExecuterControl()
        tabLayout = pm.ui.TabLayout(pm.melGlobals["$gCommandExecuterTabs"])
        selectedTabLayout = pm.ui.FormLayout(tabLayout.getSelectTab())
        
        selTab = ScriptTab(tab=selectedTabLayout)
        tabFilePaths = FileTreeSettings().data.get(FileTreeSettings.kTabPaths, {})
        tabFilePath = tabFilePaths.get(selTab.label)
        if tabFilePath:
            selTab.setFileInfo(tabFilePath)
            
        return selTab
    
    def saveSelected(self):
        self.disconnectCurrentTabCheck()
        tab = self.getSelectedTab()
        if tab.filePath:
            self.fileWatcher.removePath(tab.filePath)
            
        tab.save()
        
        if tab.filePath:
            self.fileWatcher.addPath(tab.filePath)
        self.connectCurrentTabCheck()
    
    def saveAsSelected(self):
        self.disconnectCurrentTabCheck()
        tab = self.getSelectedTab()
        if tab.filePath:
            self.fileWatcher.removePath(tab.filePath)
            
        tab.save(promptFile=True)
        
        if tab.filePath:
            self.fileWatcher.addPath(tab.filePath)
        self.connectCurrentTabCheck()
            
    def reloadTab(self):
        self.loadSettings()
        tab = self.getSelectedTab()
        tab.reload()
        

class ScriptTreeWidget(QWidget):
    def __init__(self, name, parent=None):
        super(ScriptTreeWidget, self).__init__(parent)
        
        self.folder = None
        self.name = name
        self.parent = parent
        
        self.initUI()
    
    def initUI(self):
        
        self.folderPathLE = QLineEdit()
        self.folderPathLE.textChanged.connect(self.lineEdit_SetFolder)
        
        self.searchBar = QLineEdit()
        self.searchBar.textChanged.connect(self.filterResults)
        self.searchBar.setPlaceholderText("search")
        
        self.defaultFilter = ["*.py", "*.mel"]
        
        setFolderBTN = QPushButton("...")
        setFolderBTN.clicked.connect(self.button_SetFolder)
        
        self.model = QFileSystemModel()
        self.model.setRootPath(self.folder)
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.AllEntries)
        self.model.setNameFilters(self.defaultFilter)
        self.model.setNameFilterDisables(0)
        
        self.treeView = QTreeView()
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(self.folder))
        self.treeView.doubleClicked.connect(self.addScript)
        # self.treeView.setColumnWidth(0, 300)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.setHeaderHidden(True)
        
        # Add to main layout
        self.mainLayout = QVBoxLayout()
        fileLineLayout = QHBoxLayout()
        fileLineLayout.addWidget(self.folderPathLE)
        fileLineLayout.addWidget(setFolderBTN)
        
        self.mainLayout.addLayout(fileLineLayout)
        self.mainLayout.addWidget(self.searchBar)
        self.mainLayout.addWidget(self.treeView)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.mainLayout)
    
    # Settings
    def loadSettings(self):
        settings = FileTreeSettings()
        folder = settings.data.get(FileTreeSettings.kFolders, {}).get(self.name)
        if folder:
            self.setFolder(folder)
    
    def saveSettings(self):
        settings = FileTreeSettings()
        settings.data[FileTreeSettings.kFolders][self.name] = self.folder
        settings.save()
    
    # Filter Files
    def filterResults(self, *args):
        filterText = args[0]
        if not filterText:
            self.model.setNameFilters(self.defaultFilter)
            self.treeView.collapseAll()
        else:
            filters = []
            for filterString in filterText.split(","):
                filterString = filterString.replace(" ", "")
                filters += ["*" + filterString + "*.py"]
                filters += ["*" + filterString + "*.mel"]
            self.treeView.expandAll()
            self.model.setNameFilters(filters)
    
    # Folder
    def lineEdit_SetFolder(self, folder):
        self.setFolder(folder)
    
    def button_SetFolder(self):
        folderQuery = pm.fileDialog2(fileMode=2, dialogStyle=1, startingDirectory=self.folder)
        if folderQuery:
            folder = folderQuery[0]
            self.setFolder(folder)
            
    def setFolder(self, folder=None):
        if not os.path.exists(folder):
            return
        
        folder = folder.replace("\\", "/")
        
        self.folder = folder
        self.model.setRootPath(self.folder)
        self.treeView.setRootIndex(self.model.index(self.folder))
        self.folderPathLE.setText(folder)
        
        self.saveSettings()
    
    # Add Tab
    def addScript(self, index):
        self.parent.disconnectCurrentTabCheck()
        
        path = self.getFilePath(index)
        scriptTab = addScriptToEditor(path)
        if scriptTab:
            addScriptTabToSettings(scriptTab)
                
        self.parent.connectCurrentTabCheck()
        
    def getFilePath(self, index):
        filePath = self.model.filePath(index)
        filePath = filePath.replace("\\", "/")
        return filePath
    

        

class ScriptTab(object):
    def __init__(self, tab=None, filePath=None):
        
        self.tab = None
        self.index = None
        self.textArea = None
        self.label = None
        
        self.__selected = False
        
        self.filePath = None
        self.extension = None
        self.fileName = None
        
        if tab:
            self.tab = tab
            self.getTabInfo()
        
        if filePath:
            self.setFileInfo(filePath)
    
    @property
    def selected(self):
        self.__selected = False
        
        selectedTab = pm.mel.getCurrentExecuterControl()
        cmdExec = pm.formLayout(self.tab, q=True, ca=True)[0]
        
        if selectedTab == cmdExec:
            self.__selected = True
            
        return self.__selected
    
    def setFileInfo(self, filePath):
        self.filePath = filePath
        self.extension = os.path.splitext(filePath)[-1]
        self.fileName = os.path.basename(self.filePath).replace(self.extension, "")
    
    def createTab(self):
        if not os.path.exists(self.filePath):
            return
            
        # If tab already exists, switch to it
        self.tab = getScriptTabByName(self.fileName)
        
        if self.tab:
            selectTabByName(self.fileName)
        
        if not self.tab:
            # Build tab
            pm.mel.buildNewExecuterTab(-1, self.fileName, "python", 0)
            
            # Get tab settings
            tabs = pm.melGlobals["$gCommandExecuterTabs"]
            tabsLayout = pm.tabLayout(tabs, q=True, ca=True)
            self.tab = tabsLayout[-1]
            
            # Select Created Tab
            tabsLen = pm.tabLayout(tabs, q=True, numberOfChildren=True)
            pm.tabLayout(tabs, e=True, selectTabIndex=tabsLen)
            
        # Indent this if you want to fill tab content from file only if it didn't exist
        cmdExec = pm.formLayout(self.tab, q=True, ca=True)[0]
        with open(self.filePath, "r") as f:
            fileContents = f.read()
        pm.cmdScrollFieldExecuter(cmdExec, e=True, text=fileContents)
        
        self.getTabInfo()
    
    def getTabInfo(self):
        if not self.tab:
            return
        
        reporter = self.tab
        pyReporter = pm.ui.CmdScrollFieldExecuter(reporter)
        reporterQt = pyReporter.asQtObject()
        
        # I am kind of ashamed of the following
        for child in reporterQt.children():
            for qtChild in child.children():
                if "QTextDocument" in str(qtChild):
                    self.textArea = qtChild
                    
                for qtChild2 in qtChild.children():
                    if "QTextDocument" in str(qtChild2):
                        self.textArea = qtChild2
        
        tabLayout = pm.ui.TabLayout(pm.melGlobals["$gCommandExecuterTabs"])
        tabName = self.tab.split("|")[-1]
        self.index = tabLayout.getChildArray().index(tabName)
        self.label = tabLayout.getTabLabel()[self.index]
        
        # self.textArea = reporterQt.findChildren(QTextDocument) # This maybe actually works?
        
        # self.textArea.contentsChanged.connect(self.save) 
        # This will just save constantly on text change. Use this if you want your Hardrive to die an early, glorious, death
    
    def promptReload(self):
        if not self.filePath:
            return
        
        if prompt_reloadFile(self.filePath):
            self.reload()
            
    def reload(self):
        if not self.filePath:
            return
        
        if os.path.exists(self.filePath):
            with open(self.filePath, "r") as f:
                fileContents = f.read()
                
            tabsLayoutChildren = pm.formLayout(self.tab, q=True, ca=True)
            tab = tabsLayoutChildren[0]
            
            pm.cmdScrollFieldExecuter(tab, e=True, text=fileContents)
            
    
    def save(self, promptFile=False, printSaveMessage=True):
        renameTab = False
        if not self.filePath or promptFile:
            multipleFilters = "Python and MEL(*.py *.mel)"
            fileQuery = pm.fileDialog2(fileMode=0, fileFilter=multipleFilters, dialogStyle=1)
            if not fileQuery:
                return
                
            self.setFileInfo(fileQuery[0])
            renameTab = True
            
        script = None
        
        try:
            script = self.textArea.toPlainText()
        except:
            pass
        
        if script and self.filePath and prompt_isWritable(self.filePath):
            with open(self.filePath, "w+") as f:
                f.write(script)
                
            if renameTab:
                pm.mel.eval('tabLayout -e -tabLabelIndex {} {} $gCommandExecuterTabs;'.format(self.index+1, self.fileName))
                
            if printSaveMessage:
                print("ScriptTree: SAVED: {}".format(self.filePath))
                
            addScriptTabToSettings(self)
            pm.mel.syncExecuterTabState()
            

class FileTreeSettings(object):
    
    kTabPaths = "Tabs"
    kSplitter = "Splitter"
    kSplitterHeight = "height"
    
    kFolders = "Folders"
    kLocalFolder = "LocalScriptFolder"
    kNetworkFolder = "NetworkScriptFolder"
    
    def __init__(self):
        self.data = {}
        self.load()
        
    def load(self):
        settings = {FileTreeSettings.kFolders:{},
                          FileTreeSettings.kTabPaths:{},
                          FileTreeSettings.kSplitter:{}}
        
        if os.path.exists(SETTINGS_FILEPATH):
            with open(SETTINGS_FILEPATH, "r") as f:
                settingsStr = f.read()
                storedSettings = json.loads(settingsStr)
                
            settings = dict(settings, **storedSettings)
            
        self.data = settings

    def save(self):
        with open(SETTINGS_FILEPATH, "w+") as f:
            f.write(json.dumps(self.data, indent=4))

    
def prompt_reloadFile(filePath):

    doReload = False
    
    fileName = os.path.basename(filePath)
    btn_reloadFiles = "Load File"
    btn_cancel = "Keep Tab"
    
    confirmParams = {}
    confirmParams["title"] = "Load From File"
    confirmParams["message"] = "Tab contents does not match {}".format(fileName)
    confirmParams["messageAlign"] = "center"
    confirmParams["button"] = [btn_reloadFiles, btn_cancel]
    confirmParams["defaultButton"] = btn_reloadFiles
    confirmParams["cancelButton"] = btn_cancel
    confirmParams["dismissString"] = btn_cancel
    
    conReturn = pm.confirmDialog(**confirmParams)
    
    if conReturn == btn_reloadFiles:
        doReload = True
        
    return doReload

    
def prompt_isWritable(filePath):
    if not os.path.exists(filePath):
        return True
        
    writeAccess = os.access(filePath, os.W_OK)
    
    if not writeAccess:
        
        fileName = os.path.basename(filePath)
        btn_makeWrite = "Make Writeable"
        btn_cancel = "Cancel"
        
        confirmParams = {}
        confirmParams["title"] = "File Not Writable"
        confirmParams["message"] = "{} is not writable".format(fileName)
        confirmParams["messageAlign"] = "center"
        confirmParams["button"] = [btn_makeWrite, btn_cancel]
        confirmParams["defaultButton"] = btn_makeWrite
        confirmParams["cancelButton"] = btn_cancel
        confirmParams["dismissString"] = btn_cancel
        
        conReturn = pm.confirmDialog(**confirmParams)
        
        if conReturn == btn_makeWrite:
            os.chmod(filePath, stat.S_IWRITE )
            writeAccess = os.access(filePath, os.W_OK)
            if not writeAccess:
                pm.warning("Unable to make file writeable: {}".format(filePath))
        
    return writeAccess

    
def getScriptTabByName(name):
    melTabs = pm.melGlobals["$gCommandExecuterTabs"]
    tabs = pm.tabLayout(melTabs, q=True, ca=True)
    tabNames = pm.tabLayout(melTabs, q=True, tabLabel=True)
    
    if name in tabNames:
        tabIndex = tabNames.index(name)
        tab = pm.ui.FormLayout(tabs[tabIndex])
        return tab
        
    return None

    
def selectTabByName(name):
    melTabs = pm.melGlobals["$gCommandExecuterTabs"]
    tabs = pm.tabLayout(melTabs, q=True, ca=True)
    tabNames = pm.tabLayout(melTabs, q=True, tabLabel=True)
    
    if name in tabNames:
        tabIndex = tabNames.index(name)
        tab = pm.ui.FormLayout(tabs[tabIndex])
        pm.tabLayout(melTabs, e=True, selectTabIndex=tabIndex+1)
        
        return tab
        
    return None

    
def addScriptToEditor(filePath):
    ext = os.path.splitext(filePath)[-1]
    if ext != ".py" and ext != ".mel":
        return None
    
    scriptTab = ScriptTab(filePath=filePath)
    scriptTab.createTab()
    return scriptTab
    
    
def addScriptTabToSettings(scriptTab):
    fileName = scriptTab.fileName
    settings = FileTreeSettings()
    settings.data[FileTreeSettings.kTabPaths][fileName] = scriptTab.filePath
    settings.save()



if __name__ == "__main__":
    ui = main()






