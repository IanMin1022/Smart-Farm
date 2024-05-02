from serial import Serial, STOPBITS_ONE, EIGHTBITS
from threading import Thread
from time import sleep

class PortConnection(object):
    _ser = None
    def connect(self, port, baudrate=115200):
        try:
            self._ser = Serial(port=port, 
                               baudrate=baudrate,
                               stopbits=STOPBITS_ONE,
                                bytesize=EIGHTBITS,
                                timeout=0.05,
                            )
        except Exception as e:
            return False
        return True
    
    def disconnect(self):
        if self._ser is not None:
            self._ser.close()
            self._ser = None
        
    def isConnected(self):
        return self._ser is not None
        
    def write(self, msg):
        return self._ser.write(msg)
        
    def readline(self):
        return self._ser.readline().decode('utf-8')
        
    def flush(self):
        self._ser.flush()
        
                
            
        
            
        