from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .ui.page_lcd import *
import serial

set_row = 4
set_col = 20

class LcdWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setup()
        self.ser = config['port']
        self.config = config
        self.ui.lcd_button_write.clicked.connect(self.lcdWrite)
        self.ui.lcd_button_clear.clicked.connect(self.lcdClear)

    def showEvent(self, e):
        global set_row, set_col
        set_col, set_row = self.config['lcd']
    
    def setup(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
    def lcdClear(self):
        if not self.ser.isConnected():
            return
        
        self.ser.write("lcd.clear()\r\n".encode())
        
    def lcdWrite(self):
        global set_row, set_col
        if not self.ser.isConnected():
            return
        row=0
        data = self.ui.lcd_text.toPlainText()
        self.ser.write("lcd.clear()\r\n".encode())
        for i in data.split('\n'):
            while(len(i) > set_col):
                self.ser.write(f"lcd.print(\"{i[0:set_col]}\", line={row})\r\n".encode())
                row += 1
                if(row >= set_row): 
                    break
                i = i[set_col:]
            self.ser.write(f"lcd.print(\"{i[0:set_col]}\", line={row})\r\n".encode())
            row += 1
            
            if(row >= set_row):
                break
            
if __name__ == "__main__": 
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = LcdWidget()
    widget.show()
    sys.exit(app.exec_())