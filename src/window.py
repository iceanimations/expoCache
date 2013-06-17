from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import window
import os
osp = os.path

form, base = uic.loadUiType(r'%s\ui\mainWindow.ui'%osp.dirname(osp.dirname(window.__file__)))
class Window(form, base):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        
        #set the connections between gui elements
        
        
        self.show()
    
    def showHideCams(self, flag = True):
        '''
        shows or hides the cams box and cams label
        when their is no depending on the value of the flag
        '''
        self.camBox.hide(); self.camLabel.hide()
        if flag: self.camBox.show(); self.camLabel.show()
        
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