from krita import (DockWidget, DockWidgetFactory, DockWidgetFactoryBase,
                   QLabel, QIcon, QPainter,
                   QAbstractButton, QApplication, QComboBox,
                   QDockWidget, QHBoxLayout, QLayout, QMainWindow,
                   QPushButton, QStyle, QStyleOptionDockWidget,
                   QStyleOptionToolButton, QStylePainter, QWidget,
                   Extension, ManagedColor)

from .Jitter import Jitter


instance = Krita.instance()

DOCKER_NAME = 'Color Jitter'
DOCKER_ID = 'pyKrita_ColorJitter'

class ColorJitter(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME) 
        label = QLabel("Hello", self)

        self.setWidget(label)
        self.label = label
        self.active = False
        self.setMouseTracking(True)

    def canvasChanged(self, canvas):
        return

    def mousePressEvent(self, event):
        if not self.active:
            Krita.instance().action('mirror_canvas').trigger()
            self.active = True
        

    def mouseReleaseEvent(self, event):
        if self.active:
            Krita.instance().action('mirror_canvas').trigger()
            self.active = False
        pass






class ColorJitterEx(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        
        new = window.createAction("NewJitteredColor", 'New Jittered Color', "tools/scripts")
        ret = window.createAction("ResetColor", 'Return to Base Color', "tools/scripts")
        bas = window.createAction("SetAsBase", 'Set as Base Color', "tools/scripts")
        new.triggered.connect(self.newColor)
        ret.triggered.connect(self.resetColor)
        bas.triggered.connect(self.setAsBase)
        
    def newColor(self):
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.newColor())
        pass

    def resetColor(self):
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.resetColor())
    
    def setAsBase(self):
        jitter.setBase(Krita.instance().activeWindow().activeView()
                       .foregroundColor().colorForCanvas(Krita.instance().activeWindow().activeView().canvas())
                       .toHsv())





jitter = Jitter()


dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
    DockWidgetFactoryBase.DockLeft, 
    ColorJitter)
extension=ColorJitterEx(parent=instance)



instance.addExtension(extension)
instance.addDockWidgetFactory(dock_widget_factory)

