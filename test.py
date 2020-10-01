from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QAction, QFileDialog
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import sys

from PyQt5 import QtGui

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self,event):
        self.flag = False

    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Manual object detection')
        self.lb = MyLabel(self)

        self.lb.setGeometry(QRect(30, 30, 511, 541))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        newLoad = QAction('Load', self)
        saveImg = QAction('Save', self)
        cleanB = QAction('Clean', self)

        newLoad.triggered.connect(self.updatePic)

        fileMenu.addAction(newLoad)
        fileMenu.addAction(saveImg)
        fileMenu.addAction(cleanB)

        pix = QtGui.QPixmap('123.jpg')

        self.setFixedSize(600,600)

        self.lb.setPixmap(pix)
        self.lb.setCursor(Qt.CrossCursor)
        self.show()

    def updatePic(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif)")[0]
        pix = QtGui.QPixmap(fname)
        self.lb.setPixmap(pix)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = MainWindow()
    sys.exit(app.exec_())