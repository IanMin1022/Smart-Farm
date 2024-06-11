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
        
        try:
            self.cam = Picamera2()
            config = self.cam.create_preview_configuration(raw=self.cam.sensor_modes[1])
            # config = self.cam.create_preview_configuration(
            #         main={"size":(3248, 2464)}
            #     )
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
