from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import serial
from time import sleep
from .ui.page_setting import Ui_Form
import sys
import glob
import json

class SettingWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setup()
        self.timer = QTimer(self)
        self.config = config
        self.smartfarm_mode = 'normal'
        self.config_path = './widgets/config/config.json'
        self.ui.refresh_button.clicked.connect(self.onRefresh)
        self.ui.save_button.clicked.connect(self.onSave)
        self.ui.conn_button.clicked.connect(self.onConnect)
        self.act_data_flag = False
        self.once = True
        
        self.window_value = 0
        self.heater_value = 0
        self.cooler_value = 0
        self.pump_value = 0
        self.lfan_value = 0
        self.rfan_value = 0
        
        self.r_value = 0
        self.g_value = 0
        self.b_value = 0

    def onRefresh(self):
        if sys.platform.startswith('win'):   
            ports = ['COM%s' % (i + 1) for i in range(256)]   
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):   
            ports = glob.glob('/dev/tty[A-Za-z]*')   
        elif sys.platform.startswith('darwin'):   
            ports = glob.glob('/dev/tty.*')   
        else:   
            raise EnvironmentError('Unsupported platform')   
        result = []   
        for port in ports:   
            try:   
                if port != '/dev/ttyS0':
                    s = serial.Serial(port)   
                    s.close()   
                    result.append(port)   
                else:
                    result.insert(0, port)
            except (OSError, serial.SerialException):  
                pass
        self.ui.port_combo.clear()
        for port in result:
            self.ui.port_combo.addItem(port)
    
    def hideEvent(self, e):
        self.config['period'] = int(self.ui.set_freq_spin.value())
        #self.config['lcd'] = (self.ui.set_lcd_spin_row.value(), self.ui.set_lcd_spin_col.value())
        #self.config['font'] = self.ui.set_font_spin.value()
        
    def return_checkbox_value(self):
        return self.ui.activate_box.isChecked()
    
    def update_freq_value(self, value):
        self.ui.set_freq_spin.setValue(value)
    
    def update_saved_value(self, value):
        self.act_data_flag = True
        self.pump_value = value[0]
        self.lfan_value = value[1]
        self.rfan_value = value[2]
        self.window_value = value[3]
        self.heater_value = value[4]
        self.cooler_value = value[5]
        self.r_value = value[6]
        self.g_value = value[7]
        self.b_value = value[8]        

    def showEvent(self, e):
        if self.once:
            self.onRefresh()
            self.once = False

    def setup(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def onConnect(self):
        con = self.config['port']
        port = self.ui.port_combo.currentText()
        if len(port) == 0:
            QMessageBox.warning(self, 'Error!','input port name and connect')
            return

        if con.connect(port):
            self.ui.port_combo.setEnabled(False)
            self.ui.refresh_button.setEnabled(False)
            self.ui.port_label.setText(f'Connected: {port}')
            self.ui.conn_button.clicked.disconnect()
            self.ui.conn_button.setText('Disconnect')
            self.ui.conn_button.clicked.connect(self.onDisconnect)
            self.config['conn_state'].emit('Online', True)
            self.ui.activate_box.setEnabled(False)
            self.ui.activate_label.setStyleSheet("font: 75 28pt \"나눔스퀘어 Bold\";\n"
"color: rgb(135, 135, 135);")
        else:
            QMessageBox.warning(self, 'Error!','Wrong port name')

    def onDisconnect(self):
        # name = self.config['port']._ser.name
        port = self.config['port']
        port.disconnect()
        self.ui.port_combo.setEnabled(True)
        self.ui.refresh_button.setEnabled(True)
        self.ui.port_label.setText(f'Disconnected')
        self.config['conn_state'].emit('No connection...', False)
        self.ui.conn_button.clicked.disconnect()
        self.ui.conn_button.clicked.connect(self.onConnect)
        self.ui.conn_button.setText('Connect')
        self.ui.activate_box.setEnabled(True)
        self.ui.activate_label.setStyleSheet("font: 75 28pt \"나눔스퀘어 Bold\";\n"
"color: rgb(0, 135, 68);")
        
    def reconnect(self):
        con = self.config['port']
        port = self.ui.port_combo.currentText()
        con.disconnect()
        con.connect(port)

    def onSave(self):
        self.save_data()
        self.ui.save_button.setText('Saved')
        self.timer.setSingleShot(True) 
        self.timer.timeout.connect(self.save_reset)
        self.timer.start(1000)                 

    def save_reset(self):
        self.ui.save_button.setText('Save')
        
    def save_data(self):
        try:
            with open(self.config_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}
            
        data["freq_value"] = self.ui.set_freq_spin.value()
        # print(self.ui.set_freq_spin.value())
        
        if self.act_data_flag:
            data["pump_value"] = self.pump_value
            data["lfan_value"] = self.lfan_value
            data["rfan_value"] = self.rfan_value
            data["window_value"] = self.window_value
            data["heater_value"] = self.heater_value
            data["cooler_value"] = self.cooler_value
            data["r_value"] = self.r_value
            data["g_value"] = self.g_value
            data["b_value"] = self.b_value
        
        json_data = json.dumps(data, indent=4)
        
        with open(self.config_path, "w") as json_file:
            json_file.write(json_data)
            
        json_file.close()