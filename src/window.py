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
    
    def showHideCams(self, flag = True):
        '''
        shows
        '''