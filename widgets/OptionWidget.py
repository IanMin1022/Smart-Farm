from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .ui.page_option import *
from .subwidgets.SlideWidget import *
from serial import Serial

class OptionWidget(QWidget):
    
    def __init__(self, config):
        super().__init__()       
        self.config = config
        self.flag = True
        self.ser = config['port']
        self.setup()
        self.ph_state = None
        self.nutrientsolution_state = False
        self.nutrient_state = False
        self.cooler_state = False
        self.heater_state = False
        self.co2_state = False
        self.ph_act = False
        self.nutrientsolution_act = False
        self.nutrient_act = False
        self.cooler_act = False
        self.heater_act = False
        self.co2_act = False
        self.ui.ph_combo.addItems(["pH Pump Stop", "pH Up Pump", "pH Down Pump"])
        self.timer = QTimer()
        self.timer.timeout.connect(self.readyToSensing)      

    def readyToSensing(self):
        self.ser.flush()
        self.flag = True

    def showEvent(self, e):
        if self.ser.isConnected():
            self.timer.setInterval(self.config['period'] * 1000)
            self.timer.start()
 
    def hideEvent(self, e):
        if self.timer.isActive():
            self.timer.stop()

    def work(self):
        if not self.ser.isConnected():
            return
        
        if self.flag:
            self._ph()
            self._ec()  
            self._nutrientlevel()       
            self.flag = False   
        
        if self.co2_act is True:
            self.co2_act = False
            self.ser.write(self.co2_state)
            self.ser.readline()

        if self.cooler_act is True:
            self.cooler_act = False
            self.ser.write(self.cooler_state)
            self.ser.readline()         

        if self.heater_act is True:
            self.heater_act = False
            self.ser.write(self.heater_state)
            self.ser.readline()         

        if self.nutrient_act is True:
            self.nutrient_act = False
            self.ser.write(self.nutrient_state)
            self.ser.readline() 

        if self.nutrientsolution_act is True:
            self.nutrientsolution_act = False
            self.ser.write(self.nutrientsolution_state)
            self.ser.readline()

        if self.ph_act is True:
            self.ph_act = False
            self.ser.write(self.ph_state)
            self.ser.readline() 

    def _ph(self):
        if not self.ser.isConnected():
            return
        self.ser.flush()
        self.ser.write(b"ph.read()\r\n")
        data = self.ser.readline()
        while '>>>' in data:
            data = self.ser.readline()  

        data = data[:-2]
        
        self.ui.sensor_ph_value.setText(data[:6] + 'pH')

    def _ec(self):
        if not self.ser.isConnected():
            return
        self.ser.flush()
        self.ser.write(b"ec.readEC()\r\n")
        data = self.ser.readline()
        while '>>>' in data:
            data = self.ser.readline()            
                
        data = data[:-2]
        
        self.ui.sensor_ec_value.setText(data[:6] + 'dS/m')       

    def _nutrientlevel(self):
        if not self.ser.isConnected():
            return
        self.ser.flush()
        self.ser.write(b"nutrientlevel.read()\r\n")
        data = self.ser.readline()
        while '>>>' in data:
            data = self.ser.readline()            
                
        if '1' in data:
            data = 'Full'
        else:
            data = 'Warning'

        self.ui.sensor_nutrientlevel_value.setText(data)       
        
    def co2_pumpClick(self, state):
        if not state:
            self.co2_state = b"co2_pump.off()\r\n"
        else:
            self.co2_state = b"co2_pump.on()\r\n"
        
        self.co2_act = True

    def nutrient_pumpClick(self, state):
        if not state:
            self.nutrient_state = b"nutrient_pump.off()\r\n"
        else:
            self.nutrient_state = b"nutrient_pump.on()\r\n"
        
        self.nutrient_act = True

    def nutrientsolution_pumpClick(self, state):
        if not state:
            self.nutrientsolution_state = b"nutrientsolution_pump.off()\r\n"
        else:
            self.nutrientsolution_state = b"nutrientsolution_pump.on()\r\n"
        
        self.nutrientsolution_act = True
        
    def coolerClick(self, state):
        if not state:
            self.cooler_state = b"cooler.off()\r\n"
        else:
            self.cooler_state = b"cooler.on()\r\n"
        
        self.cooler_act = True
            
    def heaterClick(self, state):
        if not state:
            self.heater_state = b"heater.off()\r\n"
        else:
            self.heater_state = b"heater.on()\r\n"
        
        self.heater_act = True
    
    def ph_click(self):
        data = self.ui.ph_combo.currentText().lower()
        
        if 'up' in data:
            self.ph_state = b"ph_pump.up()\r\n"
        elif 'down' in data:
            self.ph_state = b"ph_pump.down()\r\n"      
        if 'stop' in data:
            self.ph_state = b"ph_pump.stop()\r\n"       
        
        self.ph_act = True
                        
    def setup(self):      
       
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        lay = QVBoxLayout()

        self.ui.co2_pump_toggle = SlideWidget(self.ui.co2_pump_slide)
        self.ui.co2_pump_toggle.clicked.connect(self.co2_pumpClick)
        self.ui.nutrient_pump_toggle = SlideWidget(self.ui.nutrient_pump_slide)
        self.ui.nutrient_pump_toggle.clicked.connect(self.nutrient_pumpClick)
        self.ui.nutrientsolution_pump_toggle = SlideWidget(self.ui.nutrientsolution_pump_slide)
        self.ui.nutrientsolution_pump_toggle.clicked.connect(self.nutrientsolution_pumpClick)
        self.ui.cooler_toggle = SlideWidget(self.ui.cooler_slide)
        self.ui.cooler_toggle.clicked.connect(self.coolerClick)
        self.ui.heater_toggle = SlideWidget(self.ui.heater_slide)
        self.ui.heater_toggle.clicked.connect(self.heaterClick)
        self.ui.ph_button.clicked.connect(self.ph_click)