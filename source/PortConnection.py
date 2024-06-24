import serial
from threading import Thread
from time import sleep

class PortConnection(object):
    _ser = None
    _personal_port = False
    def connect(self, port, baudrate=115200):
        try:
            if not port == '/dev/ttyS0':
                self._ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1,
                )
                self._personal_port = True
            else:
                self._ser = FakeSerial()
                self._personal_port = False
        except Exception as e:
            print(e)
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

class FakeSerial:
    def close(self):
        pass            
        