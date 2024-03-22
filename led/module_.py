from __future__ import print_function
import sys
from inspect import currentframe

from ximea import xiapi
import cython
import logging
import os
from typing import *
import serial
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
import random
import numpy as np
import time
import yaml

logging.info('__ ledboard module called __')

# Path: led/module_.py
class ledboard:
    def __init__(self) -> None:
        self.settings()
        self.illumCmd()
        self.flushCmd()
        self.trgCmd()
        self.setDelayCmd()
        self.open_device()

    def settings(self):
        necessary_conf = ['port', 'baudrate', 'bytesize', 'parity', 'stopbits', 'timeout', 'animation_number', 'animation_speed', 'intensity', 'trigger_delay', 'led_delay','timeout']

        with open('../configs/ledboard.yml', 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.config = config
            confok = [key in necessary_conf for key in config.keys()]
            if not all(confok):
                raise Exception(f'Missing configuration in ledboard.yml, all below should be present: \n {necessary_conf}\n {confok}')
            return True

    def open_device(self):
        try:
            # Configure the serial port settings
            self.ser = serial.Serial(
                port = self.config['port'],   # Replace 'COM1' with the actual serial port name
                baudrate = self.config['baudrate'],
                bytesize = eval(self.config['bytesize']),
                parity = eval(self.config['parity']),
                stopbits = eval(self.config['stopbits']),
                timeout = self.config['timeout']
            )
            return True
        except Exception as e:
            raise ConnectionError(e)

    def calculate_checksum(self,data_bytes):
        # Calculate the XOR checksum of the data bytes
        checksum = 0
        for byte in data_bytes:
            checksum ^= byte
            #print(type(checksum),type(byte))
        return checksum
    
    def illumCmd(self)->None:
        """
        Aydınlatma modu
        this module is used to turn 3 central leds on.
        protokol= {'command to be sent':0xaa,
                    'run auto burst':0x01,
                    'N/A':0x00,
                    'N/A':0x00,
                    'led intensity':intensity,
                    'animation speed':animation_speed),
                    'animation number':animation_number,
                    'checksum':0x00}
        """
        command:List[int] = [0xaa,
                             0x01,
                             0x00,
                             0x00,
                             int(hex(self.config['intensity']), 16),
                             int(hex(self.config['animation_speed']),16),
                             int(hex(self.config['animation_number']),16)]
        
        command.append(self.calculate_checksum(command))
        self.illumination_command = bytes(command)
        return True

    def flushCmd(self,trigger_state:int=1)->None:
        """
        trigger_state is a binary value with 1 as active trigger
        all leds off example (animation is on)
        protokol= {'command to be sent':0xaa,
                    'turn all leds off':0x05,
                    'N/A':0x00,
                    'N/A':0x00,
                    'trigger on/off':trigger_state,
                    'animation speed':animation_speed,
                    'animation number':animation_number,
                    'checksum':0x00}
        """
        self.trigger_state=trigger_state
        
        all_off:List[int]= [0xaa,
                            0x05,
                            0x00,
                            0x00,
                            int(hex(trigger_state),16),
                            int(hex(self.config['animation_speed']),16),
                            int(hex(self.config['animation_number']),16)]

        all_off.append(self.calculate_checksum(all_off))
        self.flush_command = bytes(all_off)
        return True

    def trgCmd(self)->None:

        command:List[int] = [0xaa,
                            0x02,
                            0x00,
                            0x01,
                            int(hex(self.config['intensity']), 16),
                            int(hex(self.config['animation_speed']),16),
                            int(hex(0),16)]
        
        command.append(self.calculate_checksum(command))
        self.trigger_command:bytes = bytes(command)
        return True
    
    def setDelayCmd(self)->None:
        command:List[int] = [0xaa,
                             0x03,
                             0x00,
                             int(hex(self.config['trigger_delay']),16),
                             int(hex(self.config['led_delay']),16),
                             0x00,
                             0x00]
        
        command.append(self.calculate_checksum(command))
        self.set_daley_command = bytes(command)
        return True

    def singleTriggerCmd(self,led_number)->None:
        # 0xAA	0x06	0x00	TrigDelay	LedDelay	Parlaklık	IR Led No	Byte1 xor Byte1 xor … xor Byte7
        # protokol = {'command to be sent':0xaa,
        #             'run auto burst':0x06,
        #             'N/A':0x00,
        #             'TrigDelay':int(hex(TrigDelay),16),
        #             'LedDelay':int(hex(LedDelay),16),
        #             'Parlaklık':int(hex(Parlaklık),16),
        #             'IR Led No':ledNum,
        #             'checksum':0x00}
        command = [0xaa,
                   0x06,
                   0x00,
                   int(hex(self.config['trigger_delay']),16),
                   int(hex(self.config['led_delay']),16),
                   int(hex(self.config['intensity']),16),
                   int(hex(led_number),16)]
        
        command.append(self.calculate_checksum(command))
        return bytes(command)

    def illuminate(self) -> None:
        # turns three central leds on. trigger is sent one on every call.
        out = self.ser.write(self.illumination_command)
        return self.ser.read(8), out

    def flush(self, trigger_state:int=1)->None:
        
        if trigger_state!=self.trigger_state:
            self.flushCmd(trigger_state)
        self.ser.write(self.flush_command)
        return True 
    
    def trigger(self)->None:
        out = self.ser.write(self.trigger_command)
        print(out)
        return self.ser.read(8), out

    def set_daleys(self)->None:
        time.sleep(0.05)
        out = self.ser.write(self.set_daley_command)
        time.sleep(0.05)
        return out
        
    def single_trigger(self,led_number)->None:
        # print(command_bytes)
        cmd = self.singleTriggerCmd(led_number=led_number)
        self.ser.write(cmd)
        time.sleep(0.1)
        out = self.ser.read(8)
        return out

if __name__=='__main__':
    led = ledboard()
    time.sleep(1)
    out = led.flush()
    print(out)
    print('led board all of')
    time.sleep(1)
    out = led.trigger()
    print(out)
    print('led board trigger')
    time.sleep(1)
    out = led.illuminate()
    print(out)
    print('led board 3led')
    time.sleep(5)
    out = led.set_daleys()
    print(out)
    print('led board delays set')
    time.sleep(1)
    mylist = [None]*55
    print('led board single illumination')
    for l in range(1,56):
        out = led.single_trigger(led_number=l)
        mylist[l-1]=out
    print(mylist)
    time.sleep(1)
    