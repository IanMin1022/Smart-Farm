class Slip:
    END = b'\xC0'
    ESC = b'\xDB'
    ESC_END = b'\xDC'
    ESC_ESC = b'\xDD'
    
    def __init__(self):
        self.started = False
        self.escaped = False
        self.skip = False
        self.data = b''
        
    def decode(self, chunk):
        dataList = []
        
        for char in chunk:                            
            char = bytes([char])

            if not self.skip:
                if char == self.END:
                    if not self.started:
                        self.started = True
                        self.data = b''
                    else:                                                
                        dataList.append(self.data.decode())
                        self.started = False
                elif char == self.ESC:
                    self.escaped = True
                elif char == self.ESC_END:
                    if self.escaped:
                        self.data += self.END
                        self.escaped = False
                    else:
                        self.data += char
                elif char == self.ESC_ESC:
                    if self.escaped:
                        self.data += self.ESC
                        self.escaped = False
                    else:
                        self.data += char
                else:
                    if self.escaped:
                        raise IOError("Not SLIP data")
                    elif not self.started:
                        self.skip = True
                    else:
                       self.data += char
            else:
                if char == self.END:
                    self.skip = False

        return dataList
    
    def encode(self, payload):
        payload = bytes(payload.encode())
        return self.END + payload.replace(self.ESC, self.ESC + self.ESC_ESC).replace(self.END, self.ESC + self.ESC_END) + self.END