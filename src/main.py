import site
site.addsitedir(r'R:\Pipe_Repo\Users\Qurban\mayaize')
import mayaize2011
import mayaize2012
import mayaize2013
site.addsitedir(r'R:\Python_Scripts')
from PyQt4.QtGui import *
import sys
import os.path as osp
import main
selfPath = main.__file__

def main(*args):
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("plastique"))
    pixmap = QPixmap(r'%s\icons\splash.png'%osp.dirname(osp.dirname(selfPath)))
    spScreen = QSplashScreen(pixmap)
    spScreen.mousePressEvent = lambda event: None
    spScreen.show()
    spScreen.showMessage('Loading...')
    import window as win
    w = win.Window()
    spScreen.deleteLater()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()