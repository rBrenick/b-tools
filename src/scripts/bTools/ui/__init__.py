import pymel.core as pm

class DefaultWindow(object):
    def __init__(self, windowTitle="bToolsWindow"):
        if pm.window(windowTitle, exists=True):
            pm.deleteUI(windowTitle)
            
        self.win = pm.window(windowTitle)
        self.mainLayout = pm.verticalLayout()
        self.setupUI()
        self.createExecuteButtons()
        self.win.show()
    
    def createExecuteButtons(self):
        horLayout = pm.rowLayout(numberOfColumns=3, parent=self.mainLayout)
        pm.button(label='Setup', command=self.executeMain)
        pm.button(label='Apply', command=self.executeApply)
        pm.button(label='Close', command=self.close)
        
    def setupUI(self):
        pass
        
    def executeApply(self, *args):
        self.main()
        
    def executeMain(self, *args):
        self.main()
        self.close()
        
    def main(self):
        pass
    
    def close(self, *args):
        pm.deleteUI(self.win)


