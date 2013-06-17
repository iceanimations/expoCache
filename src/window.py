from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import window
import os
import os.path as osp
import logic

form, base = uic.loadUiType(r'%s\ui\mainWindow.ui'%osp.dirname(osp.dirname(window.__file__)))
class Window(form, base):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        
        # initialize the variables
        self.initVariables()
        
        #set the connections between gui elements
        self.setConnections()
        
        self.show()
        
    def initVariables(self):
        '''
        initializes the variables
        '''
        self.camerasButtons = []
        self.setsButtons = []
        self.sourceFilePath = ''
        self.targetFolderPath = ''
        self.startEndFrame = False
        self.startFrame = 1.00
        self.endFrame = 10.00
        self.keepKeysAtCurrentFrame = False
        self.fps = 24

    def setConniections(self):
        '''
        sets the connections between the ui elements
        '''
        self.selectAllButton.clicked.connect(self.selectAll)
        self.sourceBox.returnPressed.connect(self.listObjects)
        self.targetBox.returnPressed.connect(self.export)
        self.sourceButton.clicked.connect(self.showFileDialog)
        self.targetButton.clicked.connect(self.showFolderDialog)
        self.exportButton.clicked.connect(self.export)
        self.cancelButton.clicked.connect(self.closeWindow)
        self.timeSliderButton.clicked.connect(self.switchStartEndBoxes)
        self.startEndButton.clicked.connect(self.switchStartEndBoxes)
        self.fpsBox.textChanged.connect(self.setFps)
        self.startFrameBox.textChanged.connect(self.setStartEndFrame)
        self.endFrameBox.textChanged.connect(self.setStartEndFrame)
        
    def setValidators(self):
        '''
        sets validators for input fields on the ui
        '''
        pass
        
    def setStartEndFrame(self):
        self.startFrame = int(self.startFrameBox.text())
        self.endFrame = int(self.endFrameBox.text())
        
    def setFps(self, text):
        '''
        set the self.fps
        '''
        self.fps = int(text)
    
    def showHideCams(self, flag = True):
        '''
        shows or hides the cams box and cams label
        when their is no depending on the value of the flag
        '''
        if flag: self.camBox.show(); self.camLabel.show()
        else: self.camBox.hide(); self.camLabel.hide()
        
    def listObjects(self):
        '''
        calls the list cams and list sets
        '''
        pass
    
    def listCams(self, cams):
        '''
        lists the cameras on the ui
        '''
        pass
    
    def listSets(self, _sets):
        '''
        lists the object sets on the ui
        '''
        pass
    
    def export(self):
        '''
        exports the caches of the selected sets
        '''
        self.setSettings()
    
    def closeWindow(self):
        '''
        closes the main window
        '''
        self.close()
        self.deleteLater()
        
    def setSettings(self):
        '''
        sets the values of variables for the export options
        '''
    
    def handleRemoveBox(self):
        '''
        handles the combox box if the current index is changed
        '''
        pass
    
    def remove(self):
        '''
        handles if the remove button is clicked
        '''
        pass
    
    def switchStartEndBoxes(self):
        '''
        enables and disables the start/end frame boxes
        '''
        flag = self.startEndButton.isChecked()
        self.startBox.setEnabled(flag)
        self.endBox.setEnabled(flag)
        self.startEndFrame = flag
        
    def switchSelectAllButton(self):
        '''
        switches the select all button if the user checks all the
        buttons in the setsBox
        '''
        pass
    
    def selectAll(self):
        '''
        selects all the objects in the setsBox
        '''
        pass
    
    def showFileDialog(self):
        '''
        shows the file dialog to select a source file
        '''
        pass
    
    def showFolderDialog(self):
        '''
        shows the folder dialog to select a target folder
        '''
        pass
    
    def setTextForNoSetsLabel(self, text = ''):
        '''
        sets the text string for the label on the sets box
        '''
        if text:
            self.noSetsLabel.setText(text)
    
    def showHideNoSetsLabel(self, flag = True):
        '''
        show or hides the label on the sets box
        '''
        if flag: self.noSetsLabel.show()
        else: self.noSetsLabel.hide()