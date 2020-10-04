from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QAction, QFileDialog
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import sys
import numpy as np

from PyQt5 import QtGui

image = QImage("123.jpg").scaled(600, 600, Qt.IgnoreAspectRatio)
objects = []

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    rect = QRect()

    def mousePressEvent(self,event):
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self,event):
        p = QPainter(image)
        p.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        p.drawRect(self.rect)
        self.setPixmap(QPixmap(image))
        objects.append(self.rect)

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0

    def mouseMoveEvent(self,event):
        self.x1 = event.x()
        self.y1 = event.y()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        self.rect = QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(self.rect)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Manual object detection')
        self.lb = MyLabel(self)
        global image

        self.lb.setFixedSize(600,600)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        newLoad = QAction('Load', self)
        saveImg = QAction('Save', self)
        cleanB = QAction('Clean', self)

        newLoad.triggered.connect(self.updatePic)
        cleanB.triggered.connect(self.cleanImage)
        saveImg.triggered.connect(self.saveImage)

        fileMenu.addAction(newLoad)
        fileMenu.addAction(saveImg)
        fileMenu.addAction(cleanB)

        self.lb.setPixmap(QPixmap(image))
        self.setFixedSize(600,600)
        self.lb.setCursor(Qt.CrossCursor)
        self.show()

    def saveImage(self):
        fname = ''
        while (fname==''):
            fname = QFileDialog.getSaveFileName(self, 'Open file',
                                                '', "Image files (*.jpg *.png)")[0]

        image.save(fname)
        np.savetxt('objects.txt', np.array(objects), fmt="%s")

    def cleanImage(self):
        global image
        image = QImage(self.size(), QImage.Format_RGB32)
        image.fill(Qt.white)
        pix = QtGui.QPixmap(image)
        objects.clear()
        self.lb.setPixmap(pix)

    def updatePic(self):
        fname = ''
        while (fname == ''):
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '', "Image files (*.jpg *.png *.jpeg)")[0]
        global image
        image = QImage(fname).scaled(600, 600, Qt.IgnoreAspectRatio)
        pix = QtGui.QPixmap(image)
        objects.clear()
        self.lb.setPixmap(pix)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = MainWindow()
    sys.exit(app.exec_())