from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase

DOCKER_NAME = 'ColorJitter'
DOCKER_ID = 'pyKrita_ColorJitter'

class ColorJitter(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME) 

    def canvasChanged(self, canvas):
        pass

instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
    DockWidgetFactoryBase.DockRight, 
    ColorJitter)

instance.addDockWidgetFactory(dock_widget_factory)