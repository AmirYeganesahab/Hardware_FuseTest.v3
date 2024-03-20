import serial
import yaml


class ledboard:
    def __init__(self) -> None:
        pass

    def settings(self):
        with open('.config/ledboard.yml', 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.config = config
            

    def open_device(self):
        # Configure the serial port settings
        ser = serial.Serial(
            port='/dev/ttyTHS1',   # Replace 'COM1' with the actual serial port name
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0
        )

    def calculate_checksum(self,data_bytes):
        # Calculate the XOR checksum of the data bytes
        checksum = 0
        for byte in data_bytes:
            checksum ^= byte
            #print(type(checksum),type(byte))
        return checksum