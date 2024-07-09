import board
import neopixel


class RgbLedBar:
    def __init__(self):
        DATA_PIN = board.D12
        self._color = [0, 0, 0]
        self._pixel = neopixel.NeoPixel(DATA_PIN, 80, brightness=0.2, pixel_order="GRB")
        
    def setColor(self, color):        
        self._color = color
        self._pixel.fill(self._color)
    
    def read(self):
        return self._color
    
    def on(self):
        self._pixel.fill(self._color)
        
    def off(self):
        self._pixel.fill([0, 0, 0])
