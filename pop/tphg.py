import copy
import struct
import threading

from genlib.udp import MulticastReceiver


class Tphg:
    BRD_TH = 0x0003
    BRD_P = 0x0007
    BRD_G = 0x0008
    
    def __init__(self, group=None):
        if group is None:
            self._receiver = MulticastReceiver(group='239.4.18.0', port=7322)
        else:
            self._receiver = MulticastReceiver(group=group)
            
        self._receiver.onRecv(self._on_async_recv, unpickling=True)
        self._receiver.loopStart()
                
        self._func = None
        self._param = None
        self._thread = None 
        self._stop = False
        self._value = 4 * [None]
                
    def __callback(self):
        while not self._stop:
            if self._param:
                self._func(self._value, self._param)
            else:
                self._func(self._value)
            
    def _on_async_recv(self, sender, message):
        _data = copy.deepcopy(message)
        if len(_data.payload) > 0:
            try:
                _data = list(struct.unpack(f'{_data.payload[1]+2}B', _data.payload))
                if _data[0] == Tphg.BRD_TH:
                    if format(_data[3], '08b')[0] == "1":
                        self._value[0], self._value[2] = (_data[3]- 0x80) - 128, _data[2]
                    else:
                        self._value[0], self._value[2] = _data[3], _data[2]
                elif _data[0] == Tphg.BRD_P:
                    self._value[1] = ((_data[3] & 0x0F) << 8) + _data[3]
                elif _data[0] == Tphg.BRD_G:
                    self._value[3] = (_data[2] << 24) + (_data[3] << 16) + (_data[4] << 8) + _data[5]
            except TypeError:
                pass
            
    def destroy(self):
        self._receiver.loopStop()

    def read(self):
        return self._value
            
    def setCallback(self, func, param=None):
        if func == None:
            self._stop = True
            self._thread = None
        else:
            self._func = func 
            self._param = param
            self._stop = False
            self._thread = threading.Thread(target=self.__callback)
            self._thread.start()
