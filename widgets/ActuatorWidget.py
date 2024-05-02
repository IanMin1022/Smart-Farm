from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .ui.page_actuator import *
from .subwidgets.ColorWidget import *
from .subwidgets.SlideWidget import *
from serial import Serial
import RPi.GPIO as GPIO
import board
import neopixel
import time

class ActuatorWidget(QWidget):
    
    def __init__(self, config):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        DATA_PIN = board.D12
        
        self.setup()
        self.config = config
        self.ser = config['port']
        self.addr = [0x41, 0x42, 0x43, 0x44, 0x45, 0x46]
        self.window_value = 0
        self.heater_value = 0
        self.cooler_value = 0
        self.pump_value = 0
        self.lfan_value = 0
        self.rfan_value = 0
                
        self.pixel = neopixel.NeoPixel(DATA_PIN, 8, brightness=0.2, pixel_order="GRB")
        
        self.r_value = 0
        self.g_value = 0
        self.b_value = 0
        
        self.crc16_table = [0x0000, 0xc0c1, 0xc181, 0x0140, 0xc301, 0x03c0, 0x0280, 0xc241, 
            0xc601, 0x06c0, 0x0780, 0xc741, 0x0500, 0xc5c1, 0xc481, 0x0440, 
            0xcc01, 0x0cc0, 0x0d80, 0xcd41, 0x0f00, 0xcfc1, 0xce81, 0x0e40, 
            0x0a00, 0xcac1, 0xcb81, 0x0b40, 0xc901, 0x09c0, 0x0880, 0xc841, 
            0xd801, 0x18c0, 0x1980, 0xd941, 0x1b00, 0xdbc1, 0xda81, 0x1a40, 
            0x1e00, 0xdec1, 0xdf81, 0x1f40, 0xdd01, 0x1dc0, 0x1c80, 0xdc41, 
            0x1400, 0xd4c1, 0xd581, 0x1540, 0xd701, 0x17c0, 0x1680, 0xd641, 
            0xd201, 0x12c0, 0x1380, 0xd341, 0x1100, 0xd1c1, 0xd081, 0x1040, 
            0xf001, 0x30c0, 0x3180, 0xf141, 0x3300, 0xf3c1, 0xf281, 0x3240, 
            0x3600, 0xf6c1, 0xf781, 0x3740, 0xf501, 0x35c0, 0x3480, 0xf441, 
            0x3c00, 0xfcc1, 0xfd81, 0x3d40, 0xff01, 0x3fc0, 0x3e80, 0xfe41, 
            0xfa01, 0x3ac0, 0x3b80, 0xfb41, 0x3900, 0xf9c1, 0xf881, 0x3840, 
            0x2800, 0xe8c1, 0xe981, 0x2940, 0xeb01, 0x2bc0, 0x2a80, 0xea41, 
            0xee01, 0x2ec0, 0x2f80, 0xef41, 0x2d00, 0xedc1, 0xec81, 0x2c40, 
            0xe401, 0x24c0, 0x2580, 0xe541, 0x2700, 0xe7c1, 0xe681, 0x2640, 
            0x2200, 0xe2c1, 0xe381, 0x2340, 0xe101, 0x21c0, 0x2080, 0xe041, 
            0xa001, 0x60c0, 0x6180, 0xa141, 0x6300, 0xa3c1, 0xa281, 0x6240, 
            0x6600, 0xa6c1, 0xa781, 0x6740, 0xa501, 0x65c0, 0x6480, 0xa441, 
            0x6c00, 0xacc1, 0xad81, 0x6d40, 0xaf01, 0x6fc0, 0x6e80, 0xae41, 
            0xaa01, 0x6ac0, 0x6b80, 0xab41, 0x6900, 0xa9c1, 0xa881, 0x6840, 
            0x7800, 0xb8c1, 0xb981, 0x7940, 0xbb01, 0x7bc0, 0x7a80, 0xba41, 
            0xbe01, 0x7ec0, 0x7f80, 0xbf41, 0x7d00, 0xbdc1, 0xbc81, 0x7c40, 
            0xb401, 0x74c0, 0x7580, 0xb541, 0x7700, 0xb7c1, 0xb681, 0x7640, 
            0x7200, 0xb2c1, 0xb381, 0x7340, 0xb101, 0x71c0, 0x7080, 0xb041, 
            0x5000, 0x90c1, 0x9181, 0x5140, 0x9301, 0x53c0, 0x5280, 0x9241, 
            0x9601, 0x56c0, 0x5780, 0x9741, 0x5500, 0x95c1, 0x9481, 0x5440, 
            0x9c01, 0x5cc0, 0x5d80, 0x9d41, 0x5f00, 0x9fc1, 0x9e81, 0x5e40, 
            0x5a00, 0x9ac1, 0x9b81, 0x5b40, 0x9901, 0x59c0, 0x5880, 0x9841, 
            0x8801, 0x48c0, 0x4980, 0x8941, 0x4b00, 0x8bc1, 0x8a81, 0x4a40, 
            0x4e00, 0x8ec1, 0x8f81, 0x4f40, 0x8d01, 0x4dc0, 0x4c80, 0x8c41, 
            0x4400, 0x84c1, 0x8581, 0x4540, 0x8701, 0x47c0, 0x4680, 0x8641, 
            0x8201, 0x42c0, 0x4380, 0x8341, 0x4100, 0x81c1, 0x8081, 0x4040
            ]
        
    def crc16_modbus(self, init_crc, dat, len):
        crc = [init_crc >> 8, init_crc & 0xFF]
        for b in dat:
            tmp = self.crc16_table[crc[0] ^ b]
            crc[0] = (tmp & 0xFF) ^ crc[1]
            crc[1] = tmp>>8
    
        return (crc[0]|crc[1]<<8)
    
    def work(self):
        if not self.ser.isConnected():
            return        
        
    def send(self, order, value):
        if not self.ser.isConnected():
            return  
        
        GPIO.output(17, GPIO.HIGH)
        send_str = [0x76]
        send_str.append(self.addr[order])
        send_str.append(0x01)
        send_str.append(value)
        temp = self.crc16_modbus(0xFFFF,[send_str[3]],1)
        send_str.append(temp>>8)
        send_str.append(temp&0x00FF)
        send_str.append(0x3e)
        self.ser.write(bytes(bytearray(send_str)))
        time.sleep(0.05)
        GPIO.output(17, GPIO.LOW)
    
    def windowClick(self, state):
        self.window_value = int(self.ui.window_toggle.value)
        ui_value = self.window_value
        self.ui.window_value.setText(('%d' % (ui_value)) + ' %')
        if state:            
            self.send(0, self.window_value)
            
    def heaterClick(self, state):
        self.heater_value = int(self.ui.heater_toggle.value)
        ui_value = self.heater_value
        self.ui.heater_value.setText(('%d' % (ui_value)) + ' %')
        if state:
            self.send(1, self.heater_value)
        
    def coolerClick(self, state):
        self.cooler_value = int(self.ui.cooler_toggle.value)
        ui_value = self.cooler_value
        self.ui.cooler_value.setText(('%d' % (ui_value)) + ' %')
        if state:
            self.send(2, self.cooler_value)
            
    def pumpClick(self, state):
        self.pump_value = int(self.ui.water_toggle.value)
        ui_value = self.pump_value
        self.ui.water_value.setText(('%d' % (ui_value)) + ' %')
        if state:
            self.send(3, self.pump_value)

    def lfanClick(self, state):
        self.lfan_value = int(self.ui.lfan_toggle.value)
        ui_value = self.lfan_value
        self.ui.lfan_value.setText(('%d' % (ui_value)) + ' %')
        if state:
            self.send(4, self.lfan_value)

    def rfanClick(self, state):
        self.rfan_value = int(self.ui.rfan_toggle.value)
        ui_value = self.rfan_value
        self.ui.rfan_value.setText(('%d' % (ui_value)) + ' %')
        if state:
            self.send(5, self.rfan_value)

    def ledSetClick(self):
        self.r_value = self.ui.red_slider.value()
        self.g_value = self.ui.green_slider.value()
        self.b_value = self.ui.blue_slider.value()
        self.pixel.fill([self.r_value, self.g_value, self.b_value])
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

        self.ui.water_toggle = SlideWidget(self.ui.water_slide)
        self.ui.water_toggle.clicked.connect(self.pumpClick)

        self.ui.lfan_toggle = SlideWidget(self.ui.lfan_slide)
        self.ui.lfan_toggle.clicked.connect(self.lfanClick)
        
        self.ui.rfan_toggle = SlideWidget(self.ui.rfan_slide)
        self.ui.rfan_toggle.clicked.connect(self.rfanClick)      

        self.ui.window_toggle = SlideWidget(self.ui.window_slide)
        self.ui.window_toggle.clicked.connect(self.windowClick)
        
        self.ui.heater_toggle = SlideWidget(self.ui.heater_slide)
        self.ui.heater_toggle.clicked.connect(self.heaterClick)
        
        self.ui.cooler_toggle = SlideWidget(self.ui.cooler_slide)
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
        
        self.pixel.fill([self.r_value, self.g_value, self.b_value])
                
    def shutdown(self):
        for i in range(len(self.addr)):
            self.send(i, 0)
        self.pixel.fill([0, 0, 0])