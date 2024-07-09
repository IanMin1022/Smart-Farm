import copy
import struct
import threading

from genlib.udp import MulticastSender
from genlib.udp import MulticastReceiver

from . import crc16_table, crc16_modbus


class Window:
    ACT_Window = 0x20
    BRD_Window = 0x41
    
    def __init__(self, group=None):
        if group is None:
            self._sender = MulticastSender(group='239.4.18.0')
            self._receiver = MulticastReceiver(group='239.4.18.0')            
        else:
            self._sender = MulticastSender(group=group)
            self._receiver = MulticastReceiver(group=group)
            
        self._receiver.onRecv(self._on_async_recv, unpickling=True)
        self._receiver.loopStart()
        
        self._value = 1000
                
    def _encode(self, value):
        data = [0x76]
        data.append(Window.ACT_Window)
        data.append(0x01)        
        hex_value = int(hex(value), 16)
        data.append(hex_value)        
        crc_value = crc16_modbus(bytes([data[2], data[3]]))
        data.append(crc_value >> 8)
        data.append(crc_value & 0x0FF)
        data.append(0x3e)
        
        return data
        
    def _on_async_recv(self, sender, message):
        _data = copy.deepcopy(message)
        if len(_data.payload) == 8:
            try:
                _data = list(struct.unpack('8B', _data.payload))
                if _data[1] == Window.BRD_Window:
                    _value = (_data[3] << 8) + _data[4]
                    self._value = _value
            except TypeError:
                pass
            
    def destroy(self):
        self._receiver.loopStop()
    
    def open(self, value=100):
        if not 100 >= value >= 0:
            raise ValueError("value must be in [0, 100]")
        
        data = self._encode(value)
        self._sender.sendTo(data)
            
    def close(self):
        data = self._encode(0)
        self._sender.sendTo(data)
        
    def read(self):
        _value = 1000 - self._value
        if _value <= 0:
            _value = 0
        elif _value >= 375:
            _value = 90
        else:
            _value = round(_value * 0.24) # 90 / 375

        return _value
