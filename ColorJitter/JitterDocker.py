from krita import (DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Extension,
                   QLabel, QComboBox, QCheckBox, QDoubleSpinBox, QPushButton, QListView,
                   QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, pyqtSlot)

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
        self.setup_complete = False

        self.setupGenerationCheck(mainWidget)
        self.setupOptions(mainWidget)
        #self.setupButtons(mainWidget) # might be cluttery

        self.extension = ColorJitterEx(parent=Krita.instance())
        Krita.instance().addExtension(self.extension)
        

    def setupButtons(self, mainWidget):


        buttoncontrols = QWidget(mainWidget)
        buttoncontrols.setLayout(QHBoxLayout())

        newBaseColorButton = QPushButton("Set as Base", mainWidget)
        newBaseColorButton.clicked.connect(self.changeColor)

        resetColorButton = QPushButton("Reset to Base", mainWidget)
        resetColorButton.clicked.connect(self.resetColor)


        buttoncontrols.layout().addWidget(newBaseColorButton)
        buttoncontrols.layout().addWidget(resetColorButton)
        mainWidget.layout().addWidget(buttoncontrols)
        


    def setupOptions(self, mainWidget):
        options = QWidget(mainWidget)
        options.setLayout(QGridLayout())

        self.opts = [self.generateOption("Hue", options, 0), 
                    self.generateOption("Saturation", options, 1), 
                    self.generateOption("Value", options, 2)]
        
        for dists in formulaeNames:
            for opt in self.opts:
                opt[1].addItem(dists)
        options.layout().setVerticalSpacing(0)

        mainWidget.layout().addWidget(options)



    def setupGenerationCheck(self, mainWidget):

        checkbos = QWidget(mainWidget)
        checkbos.setLayout(QHBoxLayout())
        generateLabel = QLabel("Stroke Color Jitter: ", checkbos)
        autoGenerate = QCheckBox(checkbos)
        checkbos.layout().addWidget(generateLabel)
        checkbos.layout().addWidget(autoGenerate)
        mainWidget.layout().addWidget(checkbos)
        autoGenerate.stateChanged.connect(self.toggleGeneration)

        self.active = False
        


    

    def generateOption(self, option, optionWidget, index):

        label = QLabel(option + " Range:", self)
        padd = QLabel("\n\n", self)
        dist = QComboBox(self)
        dist.currentIndexChanged.connect(self.updateDistributions)

        variation = QDoubleSpinBox()
        variation.setMinimum(0)
        variation.setMaximum(200)
        variation.setSingleStep(5)
        variation.setValue(25)
        variation.setSuffix("%")
        variation.valueChanged.connect(self.updateRanges)

        optionWidget.layout().addWidget(label, index * 2, 0)
        optionWidget.layout().addWidget(padd, (index * 2) + 1, 0)
        optionWidget.layout().addWidget(variation, index * 2, 1)
        optionWidget.layout().addWidget(dist, (index * 2) + 1, 1)

        return [variation, dist] #i love structs
    

    def toggleGeneration(self):
        if self.active:
            self.resetColor()

        else:
            self.changeColor()
            self.newColor()
            if not self.setup_complete:
                try:
                    self.setupGeneration()
                    print("Color change listener attached.")
                    self.setup_complete = True

                except:
                    print("Couldn't attach color change listener.")
                    pass
        
        self.active = not self.active




    def updateDistributions(self, new_val):
        #ignore which one was changed, newe_val, and update all
        jitter.setDistributions([self.opts[0][1].currentIndex(),
                                 self.opts[1][1].currentIndex(),
                                 self.opts[2][1].currentIndex()])
        
    def updateRanges(self):
        jitter.setRanges([self.opts[0][0].value() / 100,
                          self.opts[1][0].value() / 100,
                          self.opts[2][0].value() / 100])


    def canvasChanged(self, canvas):
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

    def generate(self):
        if self.active:
            self.newColor()



    # this function is almost entirely from https://krita-artists.org/t/how-can-i-listen-to-foregroundcolorchanged/40889/13
    # bless you seguso, you da bomb

    def setupGeneration(self):
        history_docker = next((d for d in Krita.instance().dockers() if d.objectName() == 'History'), None)
        kis_undo_view = next((v for v in history_docker.findChildren(QListView) if v.metaObject().className() == 'KisUndoView'), None)
        s_model = kis_undo_view.selectionModel()
        s_model.currentChanged.connect(self.generate)
                


    @pyqtSlot()
    def resetColor(self):
        self.extension.resetColor()

    @pyqtSlot()
    def newColor(self):
        self.extension.newColor()

    @pyqtSlot()
    def changeColor(self):
        self.extension.changeColor()



    def getExtension(self):
        return self.extension






class ColorJitterEx(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        print("Color jitter setup running...")
        

    def createActions(self, window):
        
        new = window.createAction("NewJitteredColor", 'New Jittered Color', "tools/scripts")
        ret = window.createAction("ResetColor", 'Return to Base Color', "tools/scripts")
        bas = window.createAction("SetAsBase", 'Set as Base Color', "tools/scripts")
        new.triggered.connect(self.newColor)
        ret.triggered.connect(self.resetColor)
        bas.triggered.connect(self.changeColor)


    def newColor(self):
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.newColor(self.activeColor()))
        pass


    def resetColor(self):
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.resetColor())
    
    
    def changeColor(self):
        jitter.setBase(self.activeColor())
        
    def activeColor(self):
        return Krita.instance().activeWindow().activeView().foregroundColor().colorForCanvas(
            Krita.instance().activeWindow().activeView().canvas())





jitter = Jitter()


instance = Krita.instance()

dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
    DockWidgetFactoryBase.DockLeft, 
    ColorJitter)
#instance.addExtension(extension)
instance.addDockWidgetFactory(dock_widget_factory)

