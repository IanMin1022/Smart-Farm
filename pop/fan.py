from genlib.udp import MulticastSender

from . import crc16_table, crc16_modbus


class Fan:
    ACT_LFan = 0x45
    ACT_RFan = 0x46
    
    def __init__(self, position=None, group=None):
        if group is None:
            self._sender = MulticastSender(group='239.4.18.0')
        else:
            self._sender = MulticastSender(group=group)
            
        self._toggle = False
        
        if position == None:
            self._position = [Fan.ACT_LFan, Fan.ACT_RFan]
        elif position.lower() == "left":
            self._position = Fan.ACT_LFan
        elif position.lower() == "right":
            self._position = Fan.ACT_RFan
        else:
            raise ValueError("position must be left or right ")
                
    def _encode(self, value):
        data = [0x76]
        data.append(self._position)
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
