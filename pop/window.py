import copy
import struct
import threading

from genlib.udp import MulticastSender
from genlib.udp import MulticastReceiver


class Window:
    ACT_Window = 0x0041
    BRD_Window = 0x0020
    
    def __init__(self, group=None):
        if group is None:
            self._sender = MulticastSender(group='239.4.2.0', port=7323)
            self._receiver = MulticastReceiver(group='239.4.2.0', port=7322)
        else:
            self._sender = MulticastSender(group=group)
            self._receiver = MulticastReceiver(group=group)
            
        self._receiver.onRecv(self._on_async_recv, unpickling=True)
        self._receiver.loopStart()
        
        self._value = 1000
                
    def _encode(self, value):
        data = []
        data.append(Window.ACT_Window)
        data.append(0x01)        
        hex_value = int(hex(value), 16)
        data.append(hex_value)
        
        return data
        
    def _on_async_recv(self, sender, message):
        _data = copy.deepcopy(message)
        if len(_data.payload) > 0:
            try:
                _data = list(struct.unpack(f'{_data.payload[1]+2}B', _data.payload))
                if _data[0] == Window.BRD_Window:
                    _value = (_data[2] << 8) + _data[3]
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
        elif _value >= 500:
            _value = 120
        else:
            _value = round(_value * 0.24) # 120 / 500

        return _value
