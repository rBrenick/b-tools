
def startup():
    # DCC startup script
    from maya import cmds
    if cmds.about(batch=True):
        return
        
    # Setup Menu
    import b_tools.ui.menu
    b_tools.ui.menu.setup()
    
    return



