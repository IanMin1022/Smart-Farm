from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pop.light import Light
from pop.co2 import CO2
from pop.tphg import Tphg
from pop.soilmoisture import SoilMoisture
from pop.waterlevel import WaterLevel
# from pop.doorstatus import DoorStatus
from .ui.page_sensing import Ui_Form


class SensorWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setup()
        self.config = config
        self.ser = config['port']
        
        self.light = Light()
        self.co2 = CO2()
        self.tphg = Tphg()
        self.soil = SoilMoisture()
        self.waterlevel = WaterLevel()
        # self.doorstatus = DoorStatus()
        
        self._light_data = 0
        self._co2_data = 0
        self._temp_data = 0
        self._press_data = 0
        self._humi_data = 0
        self._gas_data = 0 
        self._soil_data = 0
        self._waterlevel_data = 0
        self._window_data = 0
        # self._doorstatus_data = 0
        self._count = 0
        self._gas_data_old = 0
        self._humi_base = 40.0
        self._gas_base = None
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateUI)
        self.updateUI()
    
    def updateUI(self):
        self._Light()
        self._CO2()
        self._Temp()
        self._Humi()
        self._Gas()
        self._Press()
        self._Soil()
        self._Window()
        self._Water()
    
    def showEvent(self, e):
        if self.ser.isConnected():
            self.timer.setInterval(self.config['period'] * 1000)
            self.timer.start()
            
    def hideEvent(self, e):
        if self.timer.isActive():
            self.timer.stop()
            
    def work(self, value):
        if not self.ser.isConnected():
            return
        
        self._window_data = value
                
        self._light_data = self.light.read()
        self._co2_data = self.co2.read()
        self._temp_data, self._press_data, self._humi_data, self._gas_data = self.tphg.read()
        self._soil_data = self.soil.read()
        self._waterlevel_data = self.waterlevel.read()
        # self._doorstatus_data = self.doorstatus.read()
        
        if self._count < 30:
            if self._gas_data is not None:
                if self._gas_data > self._gas_data_old:
                    self._gas_data_old = self._gas_data
                    self._count = 0
                else:
                    self._count += 1
                    
                    if self._count == 10:
                        self._gas_base = self._gas_data
                        # print(self._gas_base)
            
    def _Light(self):
        if self._light_data:
            self.ui.sensor_in_light_value.setText(f'{self._light_data} lx')
        else:
            self.ui.sensor_in_light_value.setText('None')
        
    def _CO2(self):
        if self._co2_data:
            self.ui.sensor_co2_value.setText(f'{self._co2_data} ppm')
        else:
            self.ui.sensor_co2_value.setText('None')
            
    def _Temp(self):
        if self._temp_data:
            self.ui.sensor_in_temp_value.setText(f'{self._temp_data} ℃')
        else:
            self.ui.sensor_in_temp_value.setText('None')
            
    def _Humi(self):
        if self._humi_data:
            self.ui.sensor_in_humi_value.setText(f'{self._humi_data} %')
        else:
            self.ui.sensor_in_humi_value.setText('None')
            
    def _Gas(self):
        if all([self._humi_data, self._gas_data, self._gas_base]):
            humidity_offset = self._humi_data - self._humi_base
            gas_offset = self._gas_base - self._gas_data

            if humidity_offset > 0:
                humi_score = self._humi_data - self._humi_base
                humi_score /= (100 - self._humi_base)
                humi_score *= 125
            else:
                humi_score = self._humi_base - self._humi_data
                humi_score /= self._humi_base
                humi_score *= 125

            if gas_offset > 0:
                gas_score = gas_offset / (self._gas_base - 10000) * 375
            else:
                gas_score = 0

            # print(humi_score, gas_score)
            air_quality_score = humi_score + gas_score
            
            if air_quality_score <= 50:
                self.ui.sensor_in_gas_value.setText('Excellent')
            elif air_quality_score <= 100:
                self.ui.sensor_in_gas_value.setText('Good')
            elif air_quality_score <= 150:
                self.ui.sensor_in_gas_value.setText('Lightly polluted')
            elif air_quality_score <= 200:
                self.ui.sensor_in_gas_value.setText('Moderately polluted')
            elif air_quality_score <= 250:
                self.ui.sensor_in_gas_value.setText('Heavily polluted')
            elif air_quality_score <= 350:
                self.ui.sensor_in_gas_value.setText('Severely polluted')
            else:
                self.ui.sensor_in_gas_value.setText('Extremely polluted')
        else:
            self.ui.sensor_in_gas_value.setText('None')
                    
    def _Press(self):
        if self._press_data:
            self.ui.sensor_in_press_value.setText(f'{self._press_data} hPa')
        else:
            self.ui.sensor_in_press_value.setText('None')
            
    def _Soil(self):
        if self._soil_data:
            soil_level = round(self._soil_data / 40.95)
            self.ui.sensor_soil_value.setText(f'{soil_level} %')
        else:
            self.ui.sensor_soil_value.setText('None')
            
    def _Window(self):
        if self._window_data is not None:
            if self._window_data == 0:
                self.ui.sensor_in_window_value.setText('Closed')
            else:
                self.ui.sensor_in_window_value.setText(f'Opened - {self._window_data} °')
        else:
            self.ui.sensor_in_window_value.setText('None')
            
    def _Water(self):
        if self._waterlevel_data is not None:
            if self._waterlevel_data == 1:
                self.ui.sensor_waterlevel_value.setText('Filled')
            elif self._waterlevel_data == 0:
                self.ui.sensor_waterlevel_value.setText('Warning')
        else:
            self.ui.sensor_waterlevel_value.setText('None')

    def setup(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)