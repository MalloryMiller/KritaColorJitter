from krita import (DockWidget, DockWidgetFactory, DockWidgetFactoryBase,
                   QLabel, QComboBox, QDoubleSpinBox,
                   QDockWidget, QHBoxLayout, QLayout, QMainWindow,
                   QPushButton, QStyle, QStyleOptionDockWidget,
                   QStyleOptionToolButton, QStylePainter, QWidget, QColor,
                   Extension, pyqtSlot, QVBoxLayout, QTableView)

from .Jitter import Jitter, formulaeNames






DOCKER_NAME = 'Color Jitter'
DOCKER_ID = 'pyKrita_ColorJitter'

class ColorJitter(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME) 
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
        mainWidget.setLayout(QVBoxLayout())

        self.opts = self.setupOptions(mainWidget)

        for dists in formulaeNames:
            for options in self.opts:
                options[2].addItem(dists)
        for options in self.opts:
            mainWidget.layout().addWidget(options[0])


        buttoncontrols = QWidget(mainWidget)
        buttoncontrols.setLayout(QHBoxLayout())

        self.newBaseColorButton = QPushButton("Set as Base", mainWidget)
        self.newBaseColorButton.clicked.connect(self.changeColor)

        self.resetColorButton = QPushButton("Reset to Base", mainWidget)
        self.resetColorButton.clicked.connect(self.resetColor)

        self.generateColorButton = QPushButton("New Color", mainWidget)
        self.generateColorButton.clicked.connect(self.newColor)



        buttoncontrols.layout().addWidget(self.newBaseColorButton)
        buttoncontrols.layout().addWidget(self.resetColorButton)
        buttoncontrols.layout().addWidget(self.generateColorButton)
        mainWidget.layout().addWidget(buttoncontrols)

        self.active = False

        self.extension = ColorJitterEx(parent=Krita.instance())
        Krita.instance().addExtension(self.extension)
        



    def setupOptions(self, mainWidget):

        return [self.generateOption("Hue", mainWidget), 
                self.generateOption("Saturation", mainWidget), 
                self.generateOption("Value", mainWidget)]
    

    def generateOption(self, option, mainWidget):

        label = QLabel(option + " Range %", self)
        dist = QComboBox(self)
        dist.currentIndexChanged.connect(self.updateDistributions)

        variation = QDoubleSpinBox()
        variation.setMinimum(0)
        variation.setMaximum(100)
        variation.setSingleStep(5)
        variation.valueChanged.connect(self.updateRanges)

        opt = QWidget(mainWidget)
        opt.setLayout(QHBoxLayout())
        opt.layout().addWidget(label)
        opt.layout().addWidget(variation)
        opt.layout().addWidget(dist)

        return [opt, variation, dist] #i love structs



    def updateDistributions(self, new_val):
        #ignore which one was changed, newe_val, and update all
        jitter.setDistributions([self.opts[0][2].currentIndex(),
                                 self.opts[1][2].currentIndex(),
                                 self.opts[2][2].currentIndex()])
        
    def updateRanges(self):
        jitter.setRanges([self.opts[0][1].value() / 100,
                          self.opts[1][1].value() / 100,
                          self.opts[2][1].value() / 100])


    def canvasChanged(self, canvas):
        try:
            self.changeColor() #initialize to current color
            qwin = Krita.instance().activeWindow().qwindow()
            wobj = qwin.findChild(QTableView,'paletteBox')
            wobj.selectionModel().currentChanged.connect(self.changeColor)
            
            print("Color change listener attached.")
        except:
            print("Couldn't attach color change listener.")
            pass


    #def mousePressEvent(self, event):
    #    if not self.active:
    #        Krita.instance().action('mirror_canvas').trigger()
    #        self.active = True
        

    #def mouseReleaseEvent(self, event):
    #    if self.active:
    #        Krita.instance().action('mirror_canvas').trigger()
    #        self.active = False
    #    pass

    @pyqtSlot()
    def newBaseColor(self):
        print("color AUTOMATICALLY changed.")
        if self.active:
            self.changeColor()

    @pyqtSlot()
    def resetColor(self):
        self.extension.resetColor()

    @pyqtSlot()
    def newColor(self):
        self.extension.newColor()

    @pyqtSlot()
    def changeColor(self):
        print("color changed.")
        self.extension.changeColor()



    def getExtension(self):
        return self.extension






class ColorJitterEx(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        print("Colorsetup running...")
        

    def createActions(self, window):
        
        new = window.createAction("NewJitteredColor", 'New Jittered Color', "tools/scripts")
        ret = window.createAction("ResetColor", 'Return to Base Color', "tools/scripts")
        bas = window.createAction("SetAsBase", 'Set as Base Color', "tools/scripts")
        new.triggered.connect(self.newColor)
        ret.triggered.connect(self.resetColor)
        bas.triggered.connect(self.changeColor)


    def newColor(self):
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.newColor())
        pass


    def resetColor(self):
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.resetColor())
    
    
    def changeColor(self):
        jitter.setBase(Krita.instance().activeWindow().activeView()
                       .foregroundColor().colorForCanvas(Krita.instance().activeWindow().activeView().canvas())
                       .toHsv())





jitter = Jitter()


instance = Krita.instance()

dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
    DockWidgetFactoryBase.DockLeft, 
    ColorJitter)
#instance.addExtension(extension)
instance.addDockWidgetFactory(dock_widget_factory)

