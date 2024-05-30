from krita import (DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Extension,
                   QLabel, QComboBox, QCheckBox, QDoubleSpinBox, QPushButton, QListView,
                   QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, pyqtSlot)

from .Jitter import Jitter, formulaeNames






DOCKER_NAME = 'Color Jitter'
DOCKER_ID = 'pyKrita_ColorJitter'

class ColorJitter(DockWidget):

    def __init__(self):
        
        super().__init__()
        '''
            Sets up the Docker and instantiates the Extension
        '''
        self.setWindowTitle(DOCKER_NAME) 
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
        mainWidget.setLayout(QVBoxLayout())
        self.setup_complete = False # Refers to if a base color was ever set/self.toggleGeneration ever run

        self.setupGenerationCheck(mainWidget)
        self.setupOptions(mainWidget)

        #initing the extension here means you can't jitter before being on a canvas, 
        # which is good cause that would break it.
        self.extension = ColorJitterEx(parent=Krita.instance()) # This should be the only ColorJitterEx
        Krita.instance().addExtension(self.extension) 
        


    def setupOptions(self, mainWidget):
        '''
            creates 3 seperate options to configure for color jittering: Hue, Saturation, and Value.
            It adds this to the provided mainWidget.

            mainWidget: QWidget
        '''
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
        '''
            creates a checkbox and label for toggling color jitter, also
            attaching a listener to update the value of the checkbox when it
            changes. It adds this to the provided mainWidget.

            mainWidget: QWidget
        '''
        

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
        '''
            creates an option section with range text box and distribution dropdown
            and a label for it with the 'option' specified
            Injects generated option into optionWidget at index specified (0 lowest)
            Also connects the appropriate listeners where applicable. Since all are 
            generated with this function, they all update when one is changed.

            option: String
            optionWidget: QWidget (with QGridLayout as setLayout)
            index: Integer
        '''

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
        '''
            Toggles color jittering based on the self.active value
            If active, reset to base and become inactive.
            If inactive, set new base color and generate a random color from that base
            If never run sets up the listener for switching to new jittered color
        '''
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
        '''
            ignores which distribution was changed, new_val, and updates all of the distributions
            in jitter based on whatever is currently selected in the docker
        '''
        jitter.setDistributions([self.opts[0][1].currentIndex(),
                                 self.opts[1][1].currentIndex(),
                                 self.opts[2][1].currentIndex()])
        
    def updateRanges(self):
        '''
            Updates values in jitter to reflect values in docker
        '''
        jitter.setRanges([self.opts[0][0].value() / 100,
                          self.opts[1][0].value() / 100,
                          self.opts[2][0].value() / 100])


    def canvasChanged(self, canvas):
        '''
            Required for class
        '''
        pass


    def generate(self):
        '''
            Generates a new jitter color if jittering is active
        '''
        if self.active:
            self.newColor()





    def setupGeneration(self):

        '''
            this function is pretty much entirely from 
            https://krita-artists.org/t/how-can-i-listen-to-foregroundcolorchanged/40889/13
            bless you seguso, you da bomb

            it searches through the dockers to find the Undo object and attaches a listener to it
            which generates a new color whenever something happens that can be undone. This means that
            it generates new colors after every stroke and also after every fill, selection, or any other
            undo-able action.
        '''

        history_docker = next((d for d in Krita.instance().dockers() if d.objectName() == 'History'), None)
        kis_undo_view = next((v for v in history_docker.findChildren(QListView) if v.metaObject().className() == 'KisUndoView'), None)
        s_model = kis_undo_view.selectionModel()
        s_model.currentChanged.connect(self.generate)
                


    @pyqtSlot()
    def resetColor(self):
        '''
            Uses the active extension to set the active color back to the base
        '''
        self.extension.resetColor()


    @pyqtSlot()
    def newColor(self):
        '''
            Uses the active extension to generate a new jittered color
        '''
        self.extension.newColor()


    @pyqtSlot()
    def changeColor(self):
        '''
            Uses the active extension to set a new base color
        '''
        self.extension.changeColor()






class ColorJitterEx(Extension):
    '''
        ColorJitterEx is the extension. It contains:
        - shortcuts
        - dirrect interaction with the Jitter object
    '''

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        print("Color jitter setup running...")
        

    def createActions(self, window):
        '''
            Creates shortcuts from the jitter.action file
        '''
        
        new = window.createAction("NewJitteredColor", 'New Jittered Color', "tools/scripts")
        ret = window.createAction("ResetColor", 'Return to Base Color', "tools/scripts")
        bas = window.createAction("SetAsBase", 'Set as Base Color', "tools/scripts")
        new.triggered.connect(self.newColor)
        ret.triggered.connect(self.resetColor)
        bas.triggered.connect(self.changeColor)


    def newColor(self):
        '''
            Generates a new jittered color
        '''
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.newColor(self.activeColor()))
        pass


    def resetColor(self):
        '''
            Sets the active color to the current base color
        '''
        Krita.instance().activeWindow().activeView().setForeGroundColor(jitter.resetColor())
    
    
    def changeColor(self):
        '''
            Sets the current color as the new base color
        '''
        jitter.setBase(self.activeColor())
        

    def activeColor(self):
        '''
            Gets the current foreground color
        '''
        return Krita.instance().activeWindow().activeView().foregroundColor().colorForCanvas(
            Krita.instance().activeWindow().activeView().canvas())





jitter = Jitter() # Singleton; only use this instance of Jitter


instance = Krita.instance()

dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
    DockWidgetFactoryBase.DockLeft, 
    ColorJitter)
instance.addDockWidgetFactory(dock_widget_factory)

