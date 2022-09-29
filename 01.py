import sys
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
from PySide6.QtGui import QImage, QPainter
import time
import os



class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QImage()
        
    def paintEvent(self, event):
        print("sdf")
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

def get_animation(_path):
    path = _path
    file_list = os.listdir(path)
    
    images_lst = []
    for file in file_list:
        image = QImage()
        image.load(path + file)
        images_lst.append(image)
        
    return images_lst

app = QApplication(sys.argv)

imglist = get_animation("./animation/animation1/")

main_window = QMainWindow()
mywidget = ImageViewer(main_window)

main_window.setCentralWidget(mywidget)
main_window.setFixedSize(imglist[0].size())
main_window.show()

for img in imglist :
    print(img)
    mywidget.setImage(img)
    time.sleep(1)
    
sys.exit(app.exec())