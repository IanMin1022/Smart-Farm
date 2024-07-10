from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .ui.page_camera import *
from picamera2 import Picamera2, Preview
import cv2
import time

class CameraWidget(QWidget):    
    def __init__(self):
        super().__init__()       
        self.setup()
        self.image_format = 'color'
        self.ui.grey_button.clicked.connect(self.onGrey)
        self.ui.color_button.clicked.connect(self.onColor)
        self.ui.canny_button.clicked.connect(self.onCanny)
        self.setDisabledStyle(self.ui.color_button)
        
        try:
            self.cam = Picamera2()
            config = self.cam.create_preview_configuration(raw=self.cam.sensor_modes[1])
            self.cam.configure(config)
            self.cam.start()
            # self.cam.set_controls({"AfMode": 1 ,"AfTrigger": 0})
        except Exception as e:
            self.cam =  None
            print(e)

    def showEvent(self, e):
        pass
 
    def hideEvent(self, e):
        pass

    def update_frame(self):
        if self.cam is not None:
            frame = self.cam.capture_array()
            
            if frame is not None:
                frame = frame[:, 80:450]
                if self.image_format == 'grey':
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    frame = cv2.resize(frame, (1344, 756))
                    
                    h, w = frame.shape
                    bytes_per_line = w
                    qt_image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
                elif self.image_format == 'canny':
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
                    frame = cv2.Canny(frame, 100, 300)
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    frame = cv2.resize(frame, (1344, 756))
                    
                    h, w = frame.shape
                    bytes_per_line = w
                    qt_image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
                elif self.image_format == 'color':
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    frame = cv2.resize(frame, (1344, 756))
                    
                    h, w, ch = frame.shape
                    bytes_per_line = ch * w
                    qt_image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    
                self.ui.video_label.setPixmap(QtGui.QPixmap.fromImage(qt_image))
                
        time.sleep(0.05)
                        
    def setup(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        lay = QVBoxLayout()

    def onGrey(self):
        self.image_format = 'grey'
        self.setDisabledStyle(self.ui.grey_button)
        self.setDefaultStyle(self.ui.color_button)
        self.setDefaultStyle(self.ui.canny_button)
    
    def onColor(self):
        self.image_format = 'color'
        self.setDefaultStyle(self.ui.grey_button)
        self.setDisabledStyle(self.ui.color_button)
        self.setDefaultStyle(self.ui.canny_button)
    
    def onCanny(self):
        self.image_format = 'canny'
        self.setDefaultStyle(self.ui.grey_button)
        self.setDefaultStyle(self.ui.color_button)
        self.setDisabledStyle(self.ui.canny_button)
        
    def setDisabledStyle(self, button):
        button.setStyleSheet("QPushButton\n"
                             "{ \n"
                             "    background-color: rgb(0, 135, 68);\n"
                             "    border-radius: 15px;\n"
                             "    font: 75 35pt \"Arial\";\n"
                             "    color: white;  \n"
                             "}\n"
                             "\n") 

    def setDefaultStyle(self, button):
        button.setStyleSheet("QPushButton:hover\n"
                             "{ \n"
                             "    background-color: rgb(0, 135, 68);\n"
                             "    border-radius: 15px;\n"
                             "    font: 75 35pt \"Arial\";\n"
                             "    color: white;  \n"
                             "}\n"
                             "\n"
                             "QPushButton\n"
                             "{ \n"
                             "    border-radius: 15px;\n"
                             "    border: 4px solid rgb(0, 135, 68);\n"
                             "    font: 75 35pt \"나눔스퀘어 Bold\";\n"
                             "    color: rgb(0, 135, 68);\n"
                             "}\n"
                             "")
        