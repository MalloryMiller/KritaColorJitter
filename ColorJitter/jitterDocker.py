from krita import (DockWidget, DockWidgetFactory, DockWidgetFactoryBase,
                   QLabel, QIcon, QPainter,
                   QAbstractButton, QApplication, QComboBox,
                   QDockWidget, QHBoxLayout, QLayout, QMainWindow,
                   QPushButton, QStyle, QStyleOptionDockWidget,
                   QStyleOptionToolButton, QStylePainter, QWidget,
                   Extension, ManagedColor)

import colorsys as cs
import random as r

instance = Krita.instance()


class Jitter():

    def __init__(self):
        self.base = [1.0, 1.0, 1.0]
        self.base_aph = 1
        self.val_jitter = 1.0
        self.hue_jitter = 1.0
        self.sat_jitter = 1.0
        self.aph_jitter = 1.0

        self.jitter_formulas = [
            self.randomize,
            self.randomize,
            self.randomize,
            self.randomize,
        ]

    def finishStroke(self):
        print(self.base)
        
        depth = Krita.instance().activeDocument().colorDepth()

        as_rgb = cs.hsv_to_rgb(self.base[0], self.base[1], self.base[2])

        managed_color = ManagedColor("RGBA", depth, "")
        comp = managed_color.components()
        red = as_rgb[0]
        green = as_rgb[1]
        blue = as_rgb[2]
        alpha = self.base_aph
        comp = [blue, green, red, alpha]
        managed_color.setComponents(comp)

        return self.base
    def newColor(self):
        
        depth = Krita.instance().activeDocument().colorDepth()

        
        as_rgb = cs.hsv_to_rgb(self.jitter_formulas[0](self.base[0], self.hue_jitter / 2),
                               self.jitter_formulas[1](self.base[1], self.sat_jitter / 2),
                               self.jitter_formulas[2](self.base[2], self.val_jitter / 2))

        managed_color = ManagedColor("RGBA", depth, "")
        comp = managed_color.components()
        red = as_rgb[0]
        green = as_rgb[1]
        blue = as_rgb[2]
        alpha = self.jitter_formulas[3](self.base_aph, self.aph_jitter)
        comp = [blue, green, red, alpha]
        managed_color.setComponents(comp)

        return managed_color
    
    def randomize(self, base, jitter):
        return (base + (float(r.randint(-int(jitter * 100), int(jitter * 100))) / 100)) % 1 + 0.01
    
    def setBase(self, color):
        self.base = color




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
        new.triggered.connect(self.newColor)
        ret.triggered.connect(self.newColor)
        
    def newColor(self):
        print(jitter.newColor())
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.newColor())
        pass

    def resetColor(self):
        #jitter.base = Krita.instance().activeWindow().activeView().ForeGroundColor()
        #print(jitter.base)
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.finishStroke())




jitter = Jitter()


dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
    DockWidgetFactoryBase.DockLeft, 
    ColorJitter)
extension=ColorJitterEx(parent=instance)



instance.addExtension(extension)
instance.addDockWidgetFactory(dock_widget_factory)

