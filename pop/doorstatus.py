import copy
import struct
import threading

from genlib.udp import MulticastReceiver


class DoorStatus:
    BRD_DoorStatus = 0x0006
    
    def __init__(self, group=None):
        if group is None:
            self._receiver = MulticastReceiver(group='239.4.2.0', port=7322)
        else:
            self._receiver = MulticastReceiver(group=group, port=7322)
            
        self._receiver.onRecv(self._on_async_recv, unpickling=True)
        self._receiver.loopStart()
        
        self._func = None
        self._param = None
        self._thread = None
        self._stop = False
        self._value = None
        
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
                if _data[0] == DoorStatus.BRD_DoorStatus:
                    _value = _data[2]
                    self._value = _value
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
