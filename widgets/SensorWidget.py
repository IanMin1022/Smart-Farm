from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from serial import Serial
from threading import Lock
from .ui.page_sensing import Ui_Form


lock = Lock()

class SensorWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setup()
        self.config = config
        self.flag = False
        self.ser = config['port']
        
        self._waterlevel_data = 0
        self._light_data = 0            
        self._co2_data = 0
        self._temp_data = 0
        self._humi_data = 0
        self._soil_data = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateUI)
        self.updateUI()
    
    def updateUI(self):
        self.ui.sensor_in_light_value.setText(str(self._light_data) + ' lx')
        self.ui.sensor_co2_value.setText(str(self._co2_data) + ' ppm')
        self.ui.sensor_in_temp_value.setText(('%d' % (self._temp_data)) + ' ℃')
        self.ui.sensor_in_humi_value.setText(('%d' % (self._humi_data)) + ' %')
        self.ui.sensor_soil_value.setText(str(int(float(self._soil_data))) + ' %')
        
        if self._waterlevel_data == 1:
            result = 'Full'
        else:
            result = 'Dried'
            
        self.ui.sensor_waterlevel_value.setText(result)
    
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
        
        data = []
        
        while self.flag:
            try:              
                self.ser._ser.flush()
                byte = ord(self.ser._ser.read())
                if byte == 0x76:
                    data.clear()
                    data.append(byte)                    
                elif byte == 0x3e:
                    data.append(byte)
                    break
                else:
                    data.append(byte)
            except:
                pass
                
        if len(data) == 7:
            lock.acquire()
            id =  data[1]
            payload = data[2]                                    
            lock.release()
                                
            if id == 0x05:
                self._waterlevel_data = payload
            # elif id == 0x06:
                # self._Door(payload)                
        elif len(data) == 8:
            lock.acquire()
            id =  data[1]
            payload = [data[2] , data[3]]                    
            lock.release()
            
            if id == 0x01:
                self._light_data = ((payload[0] & 0xff) << 8)  + payload[1]
            elif id == 0x02:
                self._co2_data = ((payload[0] & 0xff) << 8)  + payload[1]
            elif id == 0x03:
                self._temp_data = payload[0]
                self._humi_data = payload[1]
            elif id == 0x04:
                self._soil_data = ((payload[0] & 0x0f) << 8)  + payload[1] 
        
    def _Door(self):
        if data == 1:
            data = 'Opened'
        else:
            data = 'Closed'

        self.ui.sensor_waterlevel_value.setText(data)

    def setup(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)