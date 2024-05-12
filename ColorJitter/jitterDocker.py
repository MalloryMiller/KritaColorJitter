from krita import (DockWidget, DockWidgetFactory, DockWidgetFactoryBase,
                   QLabel, QIcon, QPainter,
                   QAbstractButton, QApplication, QComboBox,
                   QDockWidget, QHBoxLayout, QLayout, QMainWindow,
                   QPushButton, QStyle, QStyleOptionDockWidget,
                   QStyleOptionToolButton, QStylePainter, QWidget,
                   Extension, ManagedColor)

import random as r

instance = Krita.instance()


class Jitter():

    def __init__(self):
        self.base = [1.0, 1.0, 1.0]
        self.base_aph = 1
        self.val_jitter = 0.25
        self.hue_jitter = 0.25
        self.sat_jitter = 0.25
        self.aph_jitter = 1.0

        self.jitter_formulas = [
            self.randomizeLooped,
            self.randomize,
            self.randomize,
            self.randomize,
        ]

    def resetColor(self):
        print(self.base)
        
        depth = Krita.instance().activeDocument().colorDepth()

        managed_color = ManagedColor("HSV", depth, "")
        comp = managed_color.components()
        hue = self.base[0]
        sat = self.base[1]
        val = self.base[2]
        comp = [hue, sat, val, 1]
        managed_color.setComponents(comp)

        return managed_color
    

    def newColor(self):
        
        depth = Krita.instance().activeDocument().colorDepth()

        
        new_color = [
            self.jitter_formulas[0](self.base[0], self.hue_jitter / 2),
            self.jitter_formulas[1](self.base[1], self.sat_jitter / 2),
            self.jitter_formulas[2](self.base[2], self.val_jitter / 2)
            ]

        managed_color = ManagedColor("HSV", depth, "")
        comp = managed_color.components()
        hue = new_color[0]
        sat = new_color[1]
        val = new_color[2]
        comp = [hue, sat, val, 1]
        managed_color.setComponents(comp)

        return managed_color
    
    def randomizeLooped(self, base, jitter): #Base and Jitter both floats
        return (base + (float(r.randint(-int(jitter * 100), int(jitter * 100))) / 100)) % 1 + 0.01
    
    def randomize(self, base, jitter): #Base and Jitter both floats
        val =  (base + (float(r.randint(-int(jitter * 100), int(jitter * 100))) / 100))
        if val > 1:
            return 1
        if val < 0:
            return 0
        return val
    
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
        #jitter.base = Krita.instance().activeWindow().activeView().foregroundColor()
        #print(jitter.base)
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.resetColor())
    
    def setAsBase(self):
        jitter.setBase(Krita.instance().activeWindow()
                       .activeView().foregroundColor()
                       .colorForCanvas(Krita.instance().activeWindow().activeView().canvas()).toHsv())
        print(jitter.base)





jitter = Jitter()


dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
    DockWidgetFactoryBase.DockLeft, 
    ColorJitter)
extension=ColorJitterEx(parent=instance)



instance.addExtension(extension)
instance.addDockWidgetFactory(dock_widget_factory)

