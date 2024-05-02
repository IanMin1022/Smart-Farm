from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import widgets.ui.res_rc

from widgets.ui.page_main import *
from widgets.SensorWidget import SensorWidget
from widgets.ActuatorWidget import ActuatorWidget
from widgets.SettingWidget import SettingWidget
from threading import Thread
from PortConnection import PortConnection
from time import sleep
import json
import RPi.GPIO as GPIO

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) # for big screen.


class Main(QWidget):
    portDelegate = pyqtSignal(str, bool)
    def __init__(self):
        super().__init__()
                
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.showFullScreen()
        
        self.serial = PortConnection()
        self.config = {'port' : self.serial, 'lcd': [20, 4], 'period' : 5, 'font': 10, 'conn_state' : self.portDelegate}
        
        self.sensor = SensorWidget(self.config)
        self.ui.widgets.addWidget(self.sensor)
        self.setDisabledStyle(self.ui.sen_button)

        self.actuator = ActuatorWidget(self.config)
        self.ui.widgets.addWidget(self.actuator)
        self.setDisabledStyle(self.ui.act_button)
  
        self.setting = SettingWidget(self.config)
        self.ui.widgets.addWidget(self.setting)
        self.setToggledStyle(self.ui.set_button)
        
        self.portDelegate.connect(self.onPressConnectButton)
        self.ui.widgets.setCurrentIndex(2)
        self.ui.pow_button.clicked.connect(lambda : self.__shutdown())            

        self.flag = True
        self.th = Thread(target=self.main_Thread, daemon=True)
        self.th.start()
        
    def __shutdown(self):
        self.close()
        print("Shutting down...")

    def closeEvent(self, ev):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Closing")
        msgBox.setText("Really close?")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)

        # Apply stylesheet
        msgBox.setStyleSheet("""
            QLabel { min-width: 300px; font-size: 24px; }
            QPushButton {
            }
        """)

        # Iterate through buttons and set size
        for button in msgBox.buttons():
            button.setFont(QFont("Arial", 16))
            button.setMaximumWidth(150)  # Adjust the width as needed
            button.setMinimumHeight(35) 
        
        # Display the message box and handle the user's response
        if msgBox.exec() == QMessageBox.Yes:
            self.flag = False
            self.actuator.shutdown()
            # self.serial.write(b"window.close()\r\n")
            # self.serial.write(b"fan.off()\r\n")
            # self.serial.write(b"led.off()\r\n")
            # self.serial.write(b"pump.off()\r\n")
            # self.serial.write(b"lcd.clear()\r\n")
            GPIO.cleanup()
            ev.accept()
        else:
            ev.ignore()

    def onPressConnectButton(self, port, isConnect):        
        self.ui.port_label.setText(port)
        if isConnect:
            if self.setting.return_checkbox_value():                
                with open(self.setting.config_path, "r") as json_file:
                    data = json.load(json_file)
                
                self.setting.update_freq_value(data["freq_value"])
                act_value = [
                    data["pump_value"], 
                    data["lfan_value"], 
                    data["rfan_value"], 
                    data["window_value"], 
                    data["heater_value"], 
                    data["cooler_value"],
                ]
                led_value = [
                    data["r_value"],
                    data["g_value"],
                    data["b_value"],
                ]
                json_file.close()                
                self.actuator.update_slide(act_value)
                self.actuator.update_led(led_value)
                
            self.setDefaultStyle(self.ui.sen_button)
            self.setDefaultStyle(self.ui.act_button)
            self.signals()
        else:
            self.actuator.shutdown()
            self.ui.widgets.currentChanged.disconnect()
            self.ui.sen_button.clicked.disconnect()
            self.ui.act_button.clicked.disconnect()
            self.ui.set_button.clicked.disconnect()
            self.setDisabledStyle(self.ui.sen_button)
            self.setDisabledStyle(self.ui.act_button)

    def main_Thread(self):
        while self.flag:
            if not self.serial.isConnected():
                sleep(0.01)
                continue
            
            widget = self.ui.widgets.currentWidget()
            
            if widget is self.sensor:
                self.sensor.work()
            elif widget is self.actuator:
                self.actuator.work()
    
    def onPaging(self, idx):
        if idx == 0:
            self.sensor.flag = True
        elif idx == 1:
            self.sensor.flag = False
            self.setting.reconnect()
        elif idx == 2:
            self.sensor.flag = False
            self.setting.reconnect()
            self.setting.update_saved_value([
                self.actuator.pump_value,
                self.actuator.lfan_value,
                self.actuator.rfan_value,
                self.actuator.window_value,
                self.actuator.heater_value,
                self.actuator.cooler_value,
                self.actuator.r_value,
                self.actuator.g_value,
                self.actuator.b_value,
                ])
        for i, button in enumerate([self.ui.sen_button,self.ui.act_button, self.ui.set_button]):
            self.setDefaultStyle(button) if i != idx else self.setToggledStyle(button)            

    def signals(self):
        self.ui.widgets.currentChanged.connect(self.onPaging)
        self.ui.sen_button.clicked.connect(lambda : self.ui.widgets.setCurrentIndex(0))
        self.ui.act_button.clicked.connect(lambda : self.ui.widgets.setCurrentIndex(1))
        self.ui.set_button.clicked.connect(lambda : self.ui.widgets.setCurrentIndex(2))        
        
    def setDisabledStyle(self, button):
        button.setStyleSheet("QPushButton\n"
        "{ \n"
        "    background-color: rgba(0, 0, 0, 0%);\n"
        "    border-radius: 15px;\n"
        "    border: 4px solid rgb(255,255,255);\n"
        "    font: 75 25pt \"Arial\";\n"
        "    color: rgb(255,255,255);\n"
        "}\n"
        "\n") 

    def setDefaultStyle(self, button):
        button.setStyleSheet("QPushButton\n"
        "{ \n"
        "    background-color: rgba(0, 0, 0, 0%);\n"
        "    border-radius: 15px;\n"
        "    border: 4px solid rgb(255,255,255);\n"
        "    font: 75 25pt \"Arial\";\n"
        "    color: rgb(255,255,255);\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{ \n"
        "    background-color: rgb(255, 255, 255);\n"
        "    border-radius: 15px;\n"
        "    color: rgb(0, 135, 68);\n"
        "    font: 75 17pt \"Arial\";\n"
        "}\n"
        "\n"
        "QPushButton:focus:checked\n"
        "{ \n"
        "    background-color: rgb(255, 255, 255);\n"
        "    border-radius: 15px;\n"
        "    color: rgb(0, 135, 68);  \n"
        "    font: 75 17pt \"Arial\";\n"
        "}\n"
        "\n")

    def setToggledStyle(self, button):
        button.setStyleSheet(
        "QPushButton\n"
        "{ \n"
        "    background-color: rgb(255, 255, 255);\n"
        "    border-radius: 15px;\n"
        "    color: rgb(0, 135, 68);\n"
        "    font: 75 17pt \"Arial\";\n"
        "}\n"
        "\n")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = Main()
    widget.setWindowTitle('SmartFarm UI')
    widget.setWindowIcon(QIcon(':/images/images/icon.png'))
    widget.show()
    sys.exit(app.exec_())
