from krita import Extension

MENU_NAME = 'ColorJitter'
EXTENSION_ID = 'pykrita_ColorJitter'
MENU_ENTRY = 'Color Jitter'

class ColorJitter(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(EXTENSION_ID, MENU_NAME, MENU_ENTRY)
        action.triggered.connect(self.action_triggered)
        
    def action_triggered(self):
        # code here.
        pass  

app=Krita.instance()
extension=ColorJitter(parent=app)
app.addExtension(extension)