import serial
import socket
import struct
import json
import RPi.GPIO as GPIO

import threading
import time, sys

import copy
from genlib.udp import MulticastSender
from genlib.udp import MulticastReceiver


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
lock = threading.Lock()

class Multicast:
    with open('config.json', 'r') as file:
        config = json.load(file)
        
    LOCAL_GROUP = config["local_group"]
    EXTERNAL_GROUP = config["external_group"]
    DEFAULT_PORT = 7321 
    
    crc16_table = [
        0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
        0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
        0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
        0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
        0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
        0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
        0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
        0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
        0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
        0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
        0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
        0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
        0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
        0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
        0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
        0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
        0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
        0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
        0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
        0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
        0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
        0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
        0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
        0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
        0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
        0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
        0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
        0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
        0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
        0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
        0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
        0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
    ]
    
    def __init__(self):
        self.Serial = serial.Serial(
            port="/dev/ttyS0",
            baudrate=115200,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )
        self.receiver = None
        self.sender = None
        self.loop = False
        self.connection = "internal"
        self.thread = threading.Thread(target=self._condition)
        self.thread_loop = True
        
    def __del__(self):
        self.Serial.close()

    def _crc16_modbus(self, data, init_crc=0xFFFF):
        crc = [init_crc >> 8, init_crc & 0xFF]
            
        for byte in data:
            tmp = Multicast.crc16_table[crc[0] ^ byte]
            crc[0] = (tmp & 0xFF) ^ crc[1]
            crc[1] = tmp>>8
        
        return (crc[0]|crc[1]<<8)

    def _on_async_recv(self, sender, message): #Multiple Unicast
        data = copy.deepcopy(message)
        value = data.payload

        if len(value) == 7:
            if value[1] in [0x41, 0x42, 0x43, 0x44, 0x45, 0x46]:
                GPIO.output(17, GPIO.HIGH)
                
                time.sleep(0.1)
                self.Serial.write(bytes(bytearray(value)))
                time.sleep(0.1)
                
                GPIO.output(17, GPIO.LOW)
            elif value[1] == [0x45, 0x46]:
                addr = value[1]
                del value[1]
                
                value_1, value_2 = value.copy(), value.copy()
                value_1.insert(1, addr[0])
                value_2.insert(1, addr[1])
                GPIO.output(17, GPIO.HIGH)
                
                time.sleep(0.1)
                self.Serial.write(bytes(bytearray(value_1)))
                self.Serial.write(bytes(bytearray(value_2)))
                time.sleep(0.1)
                
                GPIO.output(17, GPIO.LOW)
                
    def _buf(self, sender, message):
        pass
    
    def _condition(self):
        while self.thread_loop: 
            try:
                sock = socket.create_connection(('8.8.8.8', 53), timeout=1)
                sock.close()
                if self.connection == "internal":
                    self.connection = "external"
                    self.loop = False
            except (socket.timeout, socket.error):
                if self.connection == "external":
                    self.connection = "internal"
                    self.loop = False
                
            time.sleep(1)
    
    def _connect(self):
        try:
            if self.connection == "external":
                self.sender = MulticastSender(group=Multicast.EXTERNAL_GROUP) 
                self.receiver = MulticastReceiver(group=Multicast.EXTERNAL_GROUP)
            else:
                self.sender = MulticastSender(group=Multicast.LOCAL_GROUP) 
                self.receiver = MulticastReceiver(group=Multicast.LOCAL_GROUP)
                
            print(self.connection) 
            Multicast.config["connection"] = self.connection
            with open('config.json', 'w') as file:
                json.dump(Multicast.config, file, indent=4)
                
            self.receiver.onRecv(self._on_async_recv, unpickling=True)
            self.receiver.loopStart()
            self.loop = True
        except OSError:
            pass
        
    def _close(self):
        try:
            self.sender.close()
            self.receiver.loopStop()
            self.receiver.close()
        except:
            pass

    def _loop(self):        
        data = []
        addr = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x20]
        
        while True:
            data.clear()
            if not self.loop:
                self._close()
                time.sleep(0.1)
                self._connect()

            while self.loop:
                try:
                    with lock:
                        self.Serial.flush()
                        byte = self.Serial.read()
                        byte = ord(byte)
                        # print(byte)
                        if byte == 0x76:
                            data.clear()
                            
                        data.append(byte)
                        if not data[0] == 0x76:
                            data.clear()
                        elif len(data) < 3:
                            continue
                        elif data[2] == 0x01:
                            if len(data) == 7 and data[-1] == 0x3e:
                                # print(data)
                                val = self._crc16_modbus(bytes([data[2], data[3]]))
                                val = [val>>8, val&0x0FF]
                                if data[4:6] == val:
                                    packed_data = struct.pack('7B', *data)
                                    if data[1] == addr[4]:
                                        self.sender.sendTo(packed_data)
                                    elif data[1] == addr[5]:
                                        self.sender.sendTo(packed_data)
                                break
                            elif len(data) > 7:
                                data.clear()
                        elif data[2] == 0x02:
                            if len(data) == 8 and data[-1] == 0x3e:
                                # print(data)
                                val = self._crc16_modbus(bytes([data[2], data[3], data[4]]))
                                val = [val>>8, val&0x0FF]
                                if data[5:7] == val:
                                    packed_data = struct.pack('8B', *data)
                                    if data[1] == addr[0]:
                                        self.sender.sendTo(packed_data)
                                    elif data[1] == addr[1]:
                                        self.sender.sendTo(packed_data)
                                    elif data[1] == addr[2]:
                                        self.sender.sendTo(packed_data)
                                    elif data[1] == addr[3]:
                                        self.sender.sendTo(packed_data)
                                    elif data[1] == addr[6]:
                                        self.sender.sendTo(packed_data)
                                    elif data[1] == addr[8]:
                                        self.sender.sendTo(packed_data)                                                                            
                                break
                            elif len(data) > 8:
                                data.clear()
                        elif data[2] == 0x04:
                            if len(data) == 10:
                                # print(data)
                                val = self._crc16_modbus(bytes([data[2], data[3], data[4], data[5], data[6]]))
                                val = [val>>8, val&0x0FF]                                
                                if data[7:9] == val:
                                    packed_data = struct.pack('10B', *data)
                                    if data[1] == addr[7]:
                                        self.sender.sendTo(packed_data)
                                break
                            elif len(data) > 10:
                                data.clear()
                        else:
                            data.clear()
                    time.sleep(0.001)
                except TypeError:
                    pass
                except OSError as e:
                    if e.errno == 101:
                        pass
                except KeyboardInterrupt:
                    self.stop()
                    sys.exit()
                
        self.receiver.loopStop()
        
    def start(self):
        self.thread.start()
        self._loop()
        
    def stop(self):
        self.thread_loop = False
        self.thread.join()

print("Hello World")
multi = Multicast()
multi.start()