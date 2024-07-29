from genlib.udp import MulticastSender


class Cooler:
    ACT_Cooler = 0x0043
    
    def __init__(self, position=None, group=None):
        if group is None:
            self._sender = MulticastSender(group='239.4.2.0', port=7323)
        else:
            self._sender = MulticastSender(group=group, port=7323)
            
        self._toggle = False
        
    def _encode(self, value):
        data = []
        data.append(Cooler.ACT_Cooler)
        data.append(0x01)        
        hex_value = int(hex(value), 16)
        data.append(hex_value)
        
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
