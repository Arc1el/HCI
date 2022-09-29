import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QImage, QPainter
import os
import time
from PySide6 import QtTest

def get_animation(_path):
    path = _path
    file_list = os.listdir(path)
    
    images_lst = []
    for file in file_list:
        image = QImage()
        image.load(path + file)
        images_lst.append(image)
        
    return images_lst

class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QImage()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        
    def initUI(self):
        self.setWindowTitle('Test')
        
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
            
        self.image = image
        
        if image.size() != self.size():
            self.setFixedSize(image.size())
        
        self.repaint()


app = QApplication(sys.argv)

mywidget = ImageViewer()
imglist = get_animation("./animation/animation1/")



main_window = QMainWindow()
main_window.setCentralWidget(mywidget)

main_window.show()

for img in imglist:
    mywidget.setImage(img)
    #time.sleep(0.06)
    QtTest.QTest.qWait(6)


sys.exit(app.exec())