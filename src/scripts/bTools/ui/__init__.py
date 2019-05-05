import pymel.core as pm


class DefaultWindow(object):
    def __init__(self, window_title="bTools_window"):
        if pm.window(window_title, exists=True):
            pm.deleteUI(window_title)
            
        self.win = pm.window(window_title)
        self.mainLayout = pm.verticalLayout()
        self.setup_ui()
        self.create_execute_buttons()
        self.win.show()
    
    def create_execute_buttons(self):
        hor_layout = pm.rowLayout(numberOfColumns=3, parent=self.mainLayout)
        pm.button(label='Setup', command=self.execute_main)
        pm.button(label='Apply', command=self.execute_apply)
        pm.button(label='Close', command=self.close)
        
    def setup_ui(self):
        pass
        
    def execute_apply(self, *args):
        self.main()
        
    def execute_main(self, *args):
        self.main()
        self.close()
        
    def main(self):
        pass
    
    def close(self, *args):
        pm.deleteUI(self.win)


