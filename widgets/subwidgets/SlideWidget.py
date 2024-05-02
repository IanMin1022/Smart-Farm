from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QBrush, QColor, QCursor
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal, QTimer

class SlideWidget(QLabel):
    clicked = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            self.resize(parent.size())
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_continuous_press)
        self.pos_x = 0
        self.value = 0
        # self.isOn = False

    # def isOn(self):
    #     return isOn

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        half_height = int(self.height() / 2)
        radius = half_height - half_height // 15
        
        value = ((self.pos_x - half_height)/ (self.width() - 2 * half_height)) * 100
        if value <= 0:
            self.value = 0
        elif value >= 100:
            self.value = 100
        else:
            self.value = value
        
        if 100 > self.value > 0:
            qp.setBrush(QBrush(QColor('#00A000')))
            qp.setPen(Qt.NoPen)

            qp.drawEllipse(QPoint(half_height, half_height), half_height, half_height)
            qp.drawRect(QRect(half_height, 0, self.pos_x - half_height, self.height()))
            
            qp.setBrush(QBrush(QColor('#C0C0C0')))
            qp.setPen(Qt.NoPen)
            
            qp.drawEllipse(QPoint(self.width() - half_height, half_height), half_height, half_height)
            qp.drawRect(QRect(self.pos_x, 0, self.width() - self.pos_x - half_height, self.height()))
            
            qp.setBrush(QBrush(QColor('#FFFFFF')))
            qp.drawEllipse(QPoint(self.pos_x, half_height), radius, radius)
        elif self.value == 0:
            qp.setBrush(QBrush(QColor('#C0C0C0')))
            qp.setPen(Qt.NoPen)

            qp.drawEllipse(QPoint(half_height, half_height), half_height, half_height)
            qp.drawEllipse(QPoint(self.width() - half_height, half_height), half_height, half_height)
            qp.drawRect(QRect(half_height, 0, self.width() - self.height(), self.height()))
            
            qp.setBrush(QBrush(QColor('#FFFFFF')))
            qp.drawEllipse(QPoint(half_height, half_height), radius, radius)
        elif self.value == 100:
            value = self.width() - half_height
            qp.setBrush(QBrush(QColor('#00A000')))
            qp.setPen(Qt.NoPen)

            qp.drawEllipse(QPoint(half_height, half_height), half_height, half_height)
            qp.drawEllipse(QPoint(self.width() - half_height, half_height), half_height, half_height)
            qp.drawRect(QRect(half_height, 0, self.width() - self.height(), self.height()))
            
            qp.setBrush(QBrush(QColor('#FFFFFF')))
            qp.drawEllipse(QPoint(self.width() - half_height, half_height), radius, radius)
                
        qp.end()
        
        return super().paintEvent(e)
    
    def mousePressEvent(self, e):
        self.timer.start(50)
    
    def mouseReleaseEvent(self, e):
        self.clicked.emit(True)
        self.timer.stop() 

    def handle_continuous_press(self):        
        mouse_pos = self.mapFromGlobal(QCursor.pos())
        self.pos_x = mouse_pos.x()
        
        self.clicked.emit(False)
        self.update()
        
    def update_value(self, value):
        half_height = int(self.height() / 2)
        radius = half_height - half_height // 15
        
        self.pos_x = 0.01 * (self.width() - 2 * radius) * value + radius
        self.value = value
        self.update()
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(400, 200)
    w.setStyleSheet('QWidget { background-color: white }')
    s = SlideWidget(w)

    w.show()
    
    sys.exit(app.exec_())