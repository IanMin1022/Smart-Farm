import copy
import struct
import threading

from genlib.udp import MulticastReceiver


class SoilMoisture:
    BRD_SoilMoisture = 0x0004
    
    TYPE_NORMAL = 1
    TYPE_CALC = 2
    
    MODE_INCLUSIVE = 1
    MODE_EXCLUSIVE = 2
    MODE_FULL = 3
    
    ADC_MAX = 4096 - 1
    
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
        self._type = None
        self._mode = None
        self._min = None
        self._max = None
        self._value = None
                
    def __callback(self):
        while not self._stop:
            _value = self.read()
            
            if _value is None:
                continue
            else:
                if self._type == SoilMoisture.TYPE_NORMAL:
                    _value_proc = _value
                elif self._type == SoilMoisture.TYPE_CALC:
                    _value_proc = self.calcSoilMoisture(_value)
                else:
                    raise ValueError("Type is wrong. Please use either TYPE_NORMAL or TYPE_CALC.")
                                
                if self._mode == SoilMoisture.MODE_INCLUSIVE:
                    if self._min <= _value <= self._max:
                        if self._param is None:
                            self._func(_value_proc)
                        else:
                            self._func(_value_proc, self._param)
                    else:
                        pass
                elif self._mode == SoilMoisture.MODE_EXCLUSIVE:
                    if self._min > _value or _value > self._max:
                        if self._param is None:
                            self._func(_value_proc)
                        else:
                            self._func(_value_proc, self._param)
                    else:
                        pass
                elif self._mode == SoilMoisture.MODE_FULL:
                    if self._param is None:
                        self._func(_value_proc)
                    else:
                        self._func(_value_proc, self._param)
                else:
                    raise ValueError("Mode is wrong. Please use either MODE_INCLUSIVE, MODE_EXCLUSIVE or MODE_FULL.")

    def _on_async_recv(self, sender, message):
        _data = copy.deepcopy(message)
        if len(_data.payload) > 0:
            try:
                _data = list(struct.unpack(f'{_data.payload[1]+2}B', _data.payload))
                if _data[0] == SoilMoisture.BRD_SoilMoisture:
                    _value = ((_data[2] & 0x0F) << 8)  + _data[3]
                    self._value = _value
            except TypeError:
                pass
            
    def destroy(self):
        self._receiver.loopStop()
            
    def read(self):
        return self._value
    
    def calcSoilMoisture(self, value):
        if type(value) == int:
            _value = value
            _value = round(100 * _value / SoilMoisture.ADC_MAX)
            return _value
            
    def setCallback(self, func, param=None, type=TYPE_CALC, mode=MODE_FULL, min=0, max=ADC_MAX):
        if func == None:
            self._stop = True
            self._thread = None
        else:
            self._func = func
            self._param = param
            self._stop = False
            self._type = type
            self._mode = mode
            self._min = min
            self._max = max
            self._thread = threading.Thread(target=self.__callback)
            self._thread.start()
