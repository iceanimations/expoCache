import site
site.addsitedir(r'R:\Python_Scripts')
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import window
import logic

form, base = uic.loadUiType(r'%s\ui\mainWindow.ui'%logic.dirname(logic.dirname(window.__file__)))
class Window(form, base):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('expoCache')
        icon = QIcon(QPixmap(r'%s\icons\ec.png'%logic.dirname(logic.dirname(window.__file__))))
        self.setWindowIcon(icon)
        self.createSystemTrayIcon()
        self.showCams(False)
        # initialize the variables
        self.initVariables()
        # set the connections between gui elements
        self.setConnections()
        #function calls
        logic.doCreateGeometryCache2()
        self.callInitialFunctions()
        self.show()

    def initVariables(self):
        '''
        initializes the variables
        '''
        self.camerasButtons = []
        self.camera = None
        self.setsButtons = []
        self.sourceFilePath = ''
        self.targetFolderPath = ''
        self.startEndFrame = False
        self.startFrame = 1.00
        self.endFrame = 10.00
        self.keepKeysAtCurrentFrame = False
        self.fps = 'film'
        self.removalType = ''
        self.fpsMapping = {'24 fps (film)': 'film',
                        '25 fps (PAL)': 'pal',
                        '30 fps (ntsc)': 'ntsc'}

    def setConnections(self):
        '''
        sets the connections between the ui elements
        '''
        self.selectAllButton.clicked.connect(self.selectAll)
        self.sourceBox.returnPressed.connect(self.setSourcePath)
        self.targetBox.returnPressed.connect(self.setTargetPath)
        self.sourceButton.clicked.connect(self.showFileDialog)
        self.targetButton.clicked.connect(self.showFolderDialog)
        self.exportButton.clicked.connect(self.setTargetPath)
        self.cancelButton.clicked.connect(self.closeWindow)
        self.timeSliderButton.clicked.connect(self.switchStartEndBoxes)
        self.startEndButton.clicked.connect(self.switchStartEndBoxes)
        self.fpsBox.activated.connect(self.setFps)
        self.startBox.textChanged.connect(self.setStartEndFrame)
        self.endBox.textChanged.connect(self.setStartEndFrame)
        self.keysFrameButton.clicked.connect(self.setKeepkeysAtCurrentFrames)
    
    def createSystemTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(r'%s\icons\ec.png'%logic.dirname(logic.dirname(window.__file__))))
        self.trayIcon.setToolTip('expoCache')
        self.trayIcon.show()
        #self.trayIcon.setContextMenu()
        
        
    def setSourcePath(self):
        '''
        sets the self.sourceFilePath variable and calls self.openScene
        '''
        path = str(self.sourceBox.text())
        path = path.strip("\"")
        if self.sourceFilePath != path:
            self.sourcePath = ''
            if path and logic.exists(path):
                self.sourceFilePath = path
            else:
                self.msgBox(msg = 'The system could not find the path specified\n'+
                              path, icon = QMessageBox.Warning)
                return
            self.openScene()

    def setTargetPath(self):
        '''
        sets the target path and calls self.export
        '''
        self.targetFolderPath = ''
        path = str(self.targetBox.text())
        path = path.strip("\"")
        if path and logic.exists(path):
            self.targetFolderPath = path
        else:
            self.msgBox(msg = 'The system could not find the path specified\n'+
                          path, icon = QMessageBox.Warning)
            return
        self.export()

    def callInitialFunctions(self):
        '''
        calls the functions that should be called when
        the gui gets started
        '''
        self.setValidators()

    def setKeepkeysAtCurrentFrames(self):
        '''
        sets the self.keepKeysAtCurrentFrames to True if the
        corresponding box is checked
        '''
        self.keepKeysAtCurrentFrame = self.keysFrameButton.isChecked()

    def setValidators(self):
        '''
        sets validators for input fields on the ui
        '''
        validator = QIntValidator(self)
        validator.setBottom(0)
        self.startBox.setValidator(validator)
        self.endBox.setValidator(validator)

    def setStartEndFrame(self):
        self.startFrame = self.startBox.text().toInt()[0]
        self.endFrame = self.endBox.text().toInt()[0]
        
    def setFps(self):
        '''
        set the self.fps
        '''
        text = str(self.fpsBox.currentText())
        self.fps = self.fpsMapping[text]
    
    def showCams(self, flag = True):
        '''
        shows or hides the cams box and cams label
        when their is no depending on the value of the flag
        '''
        if flag: self.camBox.show(); self.camLabel.show()
        else: self.camBox.hide(); self.camLabel.hide()
        
    def openScene(self):
        '''
        calls the openScene from the logic module
        '''
        # delete if the buttons are already there
        if self.camerasButtons:
            for cam in self.camerasButtons:
                cam.deleteLater()
            self.camerasButtons[:] = []
        if self.setsButtons:
            for _set in self.setsButtons:
                _set.deleteLater()
            self.setsButtons[:] = []
        self.camera = None
        self.setTextForNoSetsLabel('Please wait...')
        logic.openScene(self.sourceFilePath)
        self.listObjects()
    
    def listObjects(self):
        '''
        calls the list cams and list sets
        '''
        # list the cams if they are more than one
        self.showNoSetsLabel(False)
        cams = logic.objects('camera')
        if len(cams) > 1:
            self.showCams()
            self.listCams([str(cam) for cam in cams])
        else:
            self.camera = cams[0] if len(cams) == 1 else None
            self.showCams(False)
        # list sets
        _sets = logic.objects('objectSet')
        if _sets:
            self.showNoSetsLabel(False)
            self.listSets(_sets)
        else:
            self.showNoSetsLabel()
            self.setTextForNoSetsLabel('No set found...')
        if not cams:
            self.msgBox(msg = 'No camera found in the file')
        self.selectAllButton.setChecked(False)
    
    def listCams(self, cams):
        '''
        lists the cameras on the ui
        '''
        for cam in cams:
            chkBox = QCheckBox(logic.purgeChar(cam, replace = '_'), self)
            chkBox.setObjectName(cam)
            self.camsLayout.addWidget(chkBox)
            self.camerasButtons.append(chkBox)
            
    def listSets(self, _sets):
        '''
        lists the object sets on the ui
        '''
        for _set in _sets:
            chkBox = QCheckBox(logic.purgeChar(_set, replace = '_'), self)
            chkBox.setObjectName(_set)
            self.setsLayout.addWidget(chkBox)
            self.setsButtons.append(chkBox)
            chkBox.clicked.connect(self.switchSelectAllButton)
        self.trayIcon.showMessage('expoCache Objects ready',
                                  'expoCahe is done with the fetching and listing of objects',
                                  QSystemTrayIcon.Information, 5000)
            
    def selectionOnWindow(self):
        '''
        returns True if the user selects an
        object on the window else False
        '''
        for btn in self.setsButtons + self.camerasButtons:
            if btn.isChecked():
                return True
        return False

    def export(self):
        '''
        exports the caches of the selected sets
        '''
        # set the current unit
        if not self.selectionOnWindow():
            self.msgBox(msg = 'System can not find any selection on the window',
                        icon = QMessageBox.Ok)
            return
        logic.setCurrentUnit(self.fps, self.keepKeysAtCurrentFrame)
        # set the export settings
        settings = {}
        settings['time_range_mode'] = 0 if self.startEndFrame else 2
        settings['start_time'] = self.startFrame
        settings['end_time'] = self.endFrame
        settings['cache_dir'] = self.targetFolderPath
        # combine the set as a single mesh
        _sets = []
        for _set in self.setsButtons:
            if _set.isChecked():
                _sets.append(str(_set.objectName()))
        if _sets:
            meshes = logic.combineSet(_sets)
            # select the meshes
            logic.select(meshes)
            # export caches
            logic.export(self.targetFolderPath, settings)
            # delete the meshes
            logic.removeCombinedMeshes(meshes)
        #export cams
        targetPath = ''
        if self.camerasButtons:
            cams = []
            for cam in self.camerasButtons:
                if cam.isChecked():
                    cams.append(logic.pyNode(str(cam.objectName())))
            if cams:
                for cam in cams:
                    targetPath = logic.join(self.targetFolderPath,
                                            logic.purgeChar(str(cam),
                                                            replace = '_') + '.ma')
                    logic.select([cam])
                    logic.exportSelection(targetPath)
        if self.camera:
            targetPath = logic.join(self.targetFolderPath, logic.purgeChar(self.camera))
            logic.select([logic.pyNode(self.camera)])
            logic.exportSelection(targetPath)
        logic.gotoPath(self.targetFolderPath)

    def closeWindow(self):
        '''
        closes the main window
        '''
        self.close()
        self.deleteLater()
    
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
        flag = True
        for btn in self.setsButtons:
            if not btn.isChecked():
                flag = False
                break
        self.selectAllButton.setChecked(flag)
    
    def selectAll(self):
        '''
        selects all the objects in the setsBox
        '''
        checked = self.selectAllButton.isChecked()
        for btn in self.setsButtons:
            btn.setChecked(checked)
    
    def showFileDialog(self):
        '''
        shows the file dialog to select a source file
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Select File', '', '*.ma *.mb')
        if fileName:
            self.sourceBox.setText(fileName)
            self.setSourcePath()
        
    def showFolderDialog(self):
        '''
        shows the folder dialog to select a target folder
        '''
        folderName = QFileDialog.getExistingDirectory(self, 'Select Folder',
                                                      '', QFileDialog.ShowDirsOnly)
        if folderName:
            self.targetBox.setText(folderName)
    
    def setTextForNoSetsLabel(self, text = ''):
        '''
        sets the text string for the label on the sets box
        '''
        if text:
            self.noSetsLabel.show()
            self.noSetsLabel.setText(text)
            self.noSetsLabel.repaint(1,1,1,1)
    
    def showNoSetsLabel(self, flag = True):
        '''
        show or hides the label on the sets box
        '''
        if flag: self.noSetsLabel.show()
        else: self.noSetsLabel.hide()
        
    def msgBox(self, msg = None, btns = QMessageBox.Ok,
               icon = None, ques = None, details = None):
        '''
        dispalys the warnings
        @params:
                args: a dictionary containing the following sequence of variables
                {'msg': 'msg to be displayed'[, 'ques': 'question to be asked'],
                'btns': QMessageBox.btn1 | QMessageBox.btn2 | ....}
        '''
        if msg:
            mBox = QMessageBox(self)
            mBox.setWindowTitle('expoCache')
            mBox.setText(msg)
            if ques:
                mBox.setInformativeText(ques)
            if icon:
                mBox.setIcon(icon)
            if details:
                mBox.setDetailedText(details)
            mBox.setStandardButtons(btns)
            buttonPressed = mBox.exec_()
            return buttonPressed