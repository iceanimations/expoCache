import site
site.addsitedir(r"R:/Pipe_Repo/Users/Qurban/mayaize")
import mayaize2013
site.addsitedir(r"R:/Python_Scripts")
from PyQt4.QtGui import *
import sys
import os.path as osp
selfPath = sys.modules[__name__].__file__

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pixmap = QPixmap(r'%s\icons\splash.png'%osp.dirname(osp.dirname(selfPath)))
    spScreen = QSplashScreen(pixmap)
    spScreen.mousePressEvent = lambda event: None
    spScreen.show()
    spScreen.showMessage('Loading...')
    import window as win
    w = win.Window()
    spScreen.deleteLater()
    sys.exit(app.exec_())
