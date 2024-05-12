from krita import (DockWidget, DockWidgetFactory, DockWidgetFactoryBase,
                   QLabel, QIcon, QPainter,
                   QAbstractButton, QApplication, QComboBox,
                   QDockWidget, QHBoxLayout, QLayout, QMainWindow,
                   QPushButton, QStyle, QStyleOptionDockWidget,
                   QStyleOptionToolButton, QStylePainter, QWidget,
                   Extension, ManagedColor)

import colorsys as cs
import random as r
from enum import Enum

instance = Krita.instance()


class Formulae(Enum):
    RANDOM = 0,
    NORMAL = 1,
    LINEARPOSITIVE = 3,
    LINEARNEGATIVE = 4

    def randomize(base, jitter, looped = 0): #Base and Jitter both floats
        if looped:
            return ((base + (float(r.randint(-int(jitter * 100), int(jitter * 100))) / 100)) % 1) + 0.01
        else:
            val =  (base + (float(r.randint(-int(jitter * 100), int(jitter * 100))) / 100))
            if val > 1:
                return 1 - ((val % 1) + 0.01)
            if val < 0:
                return -val
            return val


    def normal(base, jitter, looped = 0): #Base and Jitter both floats
        df = 50
        change = 0
        change += float(r.randint(1, 100) / 100)
        for i in range(0,df):
            change += float(r.randint(1, 100) / 100)
        change /= df + 1

        change -= 0.5
        print("perc change", change)

        change *= float(jitter) * 2.0

        
        print("final change", change)
        if looped:
            return ((base + change) % 1) + 0.01
        else:
            val =  (base + change)
            if val > 1:
                return 1 - ((val % 1) + 0.01)
            if val < 0:
                return -val
            return val
        
        


formulae = [Formulae.randomize, Formulae.normal]


class Jitter():

    def __init__(self):
        self.base = [1.0, 1.0, 1.0]
        self.base_aph = 1
        self.val_jitter = 1.0
        self.hue_jitter = 1.0
        self.sat_jitter = 1.0
        self.aph_jitter = 1.0

        self.jitter_formulas = [
            formulae[1],
            formulae[1],
            formulae[1],
            formulae[1],
        ]


    def resetColor(self):
        print(self.base)
        
        depth = Krita.instance().activeDocument().colorDepth()

        as_rgb = cs.hsv_to_rgb(self.base[0], self.base[1], self.base[2])

        managed_color = ManagedColor("RGBA", depth, "")
        comp = managed_color.components()
        red = as_rgb[0]
        green = as_rgb[1]
        blue = as_rgb[2]
        comp = [blue, green, red, 1]
        managed_color.setComponents(comp)

        return managed_color
    

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
        comp = [blue, green, red, 1]
        managed_color.setComponents(comp)
        print("final finals", comp)

        return managed_color
    
            
    
    
    def setBase(self, color): #Takes in a QColor
        self.base[0] = color.hsvHueF()
        self.base[1] = color.saturationF()
        self.base[2] = color.valueF()




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
        print(jitter.newColor())
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

