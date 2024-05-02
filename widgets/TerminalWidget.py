from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from serial import Serial
from .ui.page_terminal import *

class TerminalWidget(QWidget):
    msgDelegate = pyqtSignal(str)
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.msgDelegate.connect(self.onMessage)
        self.setup()
        self.ser = config['port']
        self.waitForResponse = False
    
    def onMessage(self, msg):
        if self.waitForResponse:
            self.ui.plain.appendPlainText(msg)

    def setup(self):
        self.ui.input.installEventFilter(self)
        self.ui.input.returnPressed.connect(self.onReturn)

    def showEvent(self, e):
        if self.ser.isConnected():
            self.ui.plain.setPlainText('Enter python code and excute here...')
            
    def hideEvent(self, e):
        self.waitForResponse = False
        if self.ser.isConnected():
            self.ser.write(b'\x03')

    def eventFilter(self, obj, event):
        if obj is self.ui.input:
            if type(event) is QKeyEvent:
                if event.modifiers() == Qt.ControlModifier:
                    key = event.key()
                    if key == Qt.Key_C:
                        self.ser.write(b'\x03')
                        self.ui.input.clear()                
        return super().eventFilter(obj, event)

    def onReturn(self):
        if not self.ser.isConnected():
            self.ui.input.clear()
            return
        msg = self.ui.input.text()
        if msg == 'clear':
            self.ui.plain.clear()
            self.ui.input.clear()
            return
        self.ser.write((msg + '\r\n').encode())
        self.waitForResponse = True
        self.ui.input.clear()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
