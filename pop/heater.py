from genlib.udp import MulticastSender

from . import crc16_table, crc16_modbus


class Heater:
    ACT_Heater = 0x42
    
    def __init__(self, position=None, group=None):
        if group is None:
            self._sender = MulticastSender(group='239.4.18.0')
        else:
            self._sender = MulticastSender(group=group)
            
        self._toggle = False
            
    def _encode(self, value):
        data = [0x76]
        data.append(Heater.ACT_Heater)
        data.append(0x01)        
        hex_value = int(hex(value), 16)
        data.append(hex_value)        
        crc_value = crc16_modbus(bytes([data[2], data[3]]))
        data.append(crc_value >> 8)
        data.append(crc_value & 0x0FF)
        data.append(0x3e)
        
        return data
                
    def on(self, value=100):
        if not 100 >= value >= 0:
            raise ValueError("value must be in [0, 100]")
        
        data = self._encode(value)
        self._sender.sendTo(data)
        self._toggle = True
            
    def off(self):
        data = self._encode(0)
        self._sender.sendTo(data)
        self._toggle = False
    
    def toggle(self):
        self._toggle = not self._toggle        
        if self._toggle:
            data = self._encode(100)
            self._sender.sendTo(data)
        else:
            data = self._encode(0)
            self._sender.sendTo(data)
