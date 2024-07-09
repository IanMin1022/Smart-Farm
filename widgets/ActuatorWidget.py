from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .ui.page_actuator import *
from .subwidgets.ColorWidget import *
from .subwidgets.SlideWidget import *
import socket
from pop.window import Window
from pop.fan import Fan
from pop.heater import Heater
from pop.cooler import Cooler
from pop.waterpump import WaterPump
from pop.rgbledbar import RgbLedBar


class ActuatorWidget(QWidget):
    def __init__(self, config):
        super().__init__()        
        self.setup()
        self.config = config
        self.ser = config['port']
        self.addr = [0x41, 0x42, 0x43, 0x44, 0x45, 0x46]
        
        self.windows = Window()
        self.l_fan = Fan(position="left")
        self.r_fan = Fan(position="right")
        self.heater = Heater()
        self.cooler = Cooler()
        self.pump = WaterPump()
        self.rgb = RgbLedBar()
        
        self.window_value = 0
        self.heater_value = 0
        self.cooler_value = 0
        self.pump_value = 0
        self.lfan_value = 0
        self.rfan_value = 0
        
        self.r_value = 0
        self.g_value = 0
        self.b_value = 0
            
    def work(self):
        if not self.ser.isConnected():
            return
                    
    def windowClick(self, state):
        self.window_value = int(self.ui.window_toggle.value)
        ui_value = self.window_value
        self.ui.window_value.setText(('%d' % (ui_value)) + ' %')
        if state:
            if self.window_value == 0:
                self.windows.close()
            else:
                self.windows.open(self.window_value)
            
    def heaterClick(self, state):
        self.heater_value = int(self.ui.heater_toggle.value)
        ui_value = self.heater_value
        
        if state:
            if self.heater_value == 0:
                self.ui.heater_value.setText('Off')
                self.heater.off()
            else:
                self.ui.heater_value.setText('On')
                self.heater.on(self.heater_value)
        
    def coolerClick(self, state):
        self.cooler_value = int(self.ui.cooler_toggle.value)
        ui_value = self.cooler_value
        
        if state:
            if self.cooler_value == 0:
                self.ui.cooler_value.setText('Off')
                self.cooler.off()
            else:
                self.ui.cooler_value.setText('On')
                self.cooler.on(self.cooler_value)
            
    def pumpClick(self, state):
        self.pump_value = int(self.ui.water_toggle.value)
        ui_value = self.pump_value
        
        if state:
            if self.pump_value == 0:
                self.ui.water_value.setText('Off')
                self.pump.off()
            else:
                self.ui.water_value.setText('On')
                self.pump.on(self.pump_value)

    def lfanClick(self, state):
        self.lfan_value = int(self.ui.lfan_toggle.value)
        ui_value = self.lfan_value
        
        if state:
            if self.lfan_value == 0:
                self.ui.lfan_value.setText('Off')
                self.l_fan.off()
            else:
                self.ui.lfan_value.setText('On')
                self.l_fan.on(self.lfan_value)

    def rfanClick(self, state):
        self.rfan_value = int(self.ui.rfan_toggle.value)
        ui_value = self.rfan_value
        
        if state:
            if self.rfan_value == 0:
                self.ui.rfan_value.setText('Off')
                self.r_fan.off()
            else:
                self.ui.rfan_value.setText('On')
                self.r_fan.on(self.rfan_value)

    def ledSetClick(self):
        self.r_value = self.ui.red_slider.value()
        self.g_value = self.ui.green_slider.value()
        self.b_value = self.ui.blue_slider.value()
        self.rgb.setColor([self.r_value, self.g_value, self.b_value])
        # color = self.color.currentColor()
        # self.led_state = f"led.setColor([{self.r_value}, {self.g_value}, {self.b_value}])\r\n".encode()
        # self.led_act = True
    
    def colorChange(self):
        red = self.ui.red_slider.value()
        self.ui.red_label.setText(str(red))
        green = self.ui.green_slider.value()
        self.ui.green_label.setText(str(green))
        blue = self.ui.blue_slider.value()
        self.ui.blue_label.setText(str(blue))
        self.ui.color_label.setStyleSheet("background-color: rgb({},{},{})".format(red,green,blue))

    def setup(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.color = ColorWidget()
        # lay = QVBoxLayout()

        # self.color.currentColorChanged.connect(lambda color : self.ui.color_label.setStyleSheet(f'background-color: {color.name()}'))
        # lay.addWidget(self.color, alignment=Qt.AlignCenter)
        # self.ui.led_area.setLayout(lay)

        self.ui.water_toggle = SlideWidget(self.ui.water_slide, True)
        self.ui.water_toggle.clicked.connect(self.pumpClick)

        self.ui.lfan_toggle = SlideWidget(self.ui.lfan_slide, True)
        self.ui.lfan_toggle.clicked.connect(self.lfanClick)
        
        self.ui.rfan_toggle = SlideWidget(self.ui.rfan_slide, True)
        self.ui.rfan_toggle.clicked.connect(self.rfanClick)      

        self.ui.window_toggle = SlideWidget(self.ui.window_slide)
        self.ui.window_toggle.clicked.connect(self.windowClick)
        
        self.ui.heater_toggle = SlideWidget(self.ui.heater_slide, True)
        self.ui.heater_toggle.clicked.connect(self.heaterClick)
        
        self.ui.cooler_toggle = SlideWidget(self.ui.cooler_slide, True)
        self.ui.cooler_toggle.clicked.connect(self.coolerClick)

        self.ui.red_slider.valueChanged.connect(self.colorChange)
        self.ui.green_slider.valueChanged.connect(self.colorChange)
        self.ui.blue_slider.valueChanged.connect(self.colorChange)

        self.ui.set_button.clicked.connect(self.ledSetClick)
        
    def update_slide(self, data):
        self.ui.water_toggle.update_value(data[0])
        self.ui.lfan_toggle.update_value(data[1])        
        self.ui.rfan_toggle.update_value(data[2])
        self.ui.window_toggle.update_value(data[3])        
        self.ui.heater_toggle.update_value(data[4])        
        self.ui.cooler_toggle.update_value(data[5])
        
        self.pumpClick(True)
        self.lfanClick(True)
        self.rfanClick(True)
        self.windowClick(True)
        self.heaterClick(True)
        self.coolerClick(True)
        
    def update_led(self, data):        
        self.r_value = data[0]
        self.g_value = data[1]
        self.b_value = data[2]
        
        self.ui.red_slider.setValue(self.r_value)
        self.ui.green_slider.setValue(self.g_value)
        self.ui.blue_slider.setValue(self.b_value)
        
        self.ui.color_label.setStyleSheet("background-color: rgb({},{},{})".format(self.r_value,self.g_value,self.b_value))        
        self.rgb.setColor([self.r_value, self.g_value, self.b_value])
                
    def shutdown(self):
        self.windows.close()
        self.l_fan.off()
        self.r_fan.off()
        self.heater.off()
        self.cooler.off()
        self.pump.off()
        self.rgb.setColor([0, 0, 0])
