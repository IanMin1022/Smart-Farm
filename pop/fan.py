from genlib.udp import MulticastSender


class Fan:
    ACT_LFan = 0x0045
    ACT_RFan = 0x0046
    
    def __init__(self, position=None, group=None):
        if group is None:
            self._sender = MulticastSender(group='239.4.2.0', port=7323)
        else:
            self._sender = MulticastSender(group=group, port=7323)
        
        if position == None:
            self._position = [Fan.ACT_LFan, Fan.ACT_RFan]
        elif position.lower() == "left":
            self._position = [Fan.ACT_LFan]
        elif position.lower() == "right":
            self._position = [Fan.ACT_RFan]
        else:
            raise ValueError("position must be left or right ")
        
        self.length = len(self._position)
        self._toggle = False
                
    def _encode(self, value):
        data = [[] for _ in range(self.length)]
        
        for i in range(self.length):
            data[i].append(self._position[i])
            data[i].append(0x01)        
            hex_value = int(hex(value), 16)
            data[i].append(hex_value)
        
        return data
                    
    def on(self, value=100):
        if not 100 >= value >= 0:
            raise ValueError("value must be in [0, 100]")
        
        data = self._encode(value)
        for i in range(self.length):
            self._sender.sendTo(data[i])
        self._toggle = True
            
    def off(self):
        data = self._encode(0)
        for i in range(self.length):
            self._sender.sendTo(data[i])
        self._toggle = False
    
    def toggle(self):
        self._toggle = not self._toggle        
        if self._toggle:
            data = self._encode(100)
            for i in range(self.length):
                self._sender.sendTo(data[i])
        else:
            data = self._encode(0)
            for i in range(self.length):
                self._sender.sendTo(data[i])
