from unittest.mock import patch
import unittest
from module_ import ledboard
import serial

class TestYourClass(unittest.TestCase):
    def setUp(self):
        self.led = ledboard()

    @patch('serial.Serial', autospec=True)
    def test_open_device(self,mock_serial):
        self.assertEqual(self.led.open_device(), True)
        # Check that serial.Serial was called with the expected arguments,
        mock_serial.assert_called_once_with(baudrate=self.led.config['baudrate'],
                                             bytesize=eval(self.led.config['bytesize']),
                                             parity=eval(self.led.config['parity']),
                                             port=self.led.config['port'],
                                             stopbits=eval(self.led.config['stopbits']),
                                             timeout=self.led.config['timeout'])

    def test_calculate_checksum(self):
        test_cases = [
                        ([170, 1, 0, 0, 99, 14, 1], 199),
                        ([170, 5, 0, 0, 1, 14, 1], 161),
                        ([170, 2, 0, 1, 99, 14, 0], 196),
                        ([170, 3, 0, 10, 5, 0, 0], 166)
                        ]

        for command, expected_checksum in test_cases:
            actual_checksum = self.led.calculate_checksum(command)
            self.assertEqual(actual_checksum, expected_checksum)

    def test_illumCmd(self):
        self.assertEqual(self.led.illumCmd(),True)
    
    def test_flushCmd(self):
        self.assertEqual(self.led.settings(), True)
    
    def test_trgCmd(self):
        self.assertEqual(self.led.trgCmd(),True)
    
    def test_setDelayCmd(self):
        self.assertEqual(self.led.setDelayCmd(),True)
    
    def test_singleTriggerCmd(self):
        expected_outputs = [b'\xaa\x06\x00\n\x05c\x01\xc1',
                    b'\xaa\x06\x00\n\x05c\x02\xc2',
                    b'\xaa\x06\x00\n\x05c\x03\xc3',
                    b'\xaa\x06\x00\n\x05c\x04\xc4',
                    b'\xaa\x06\x00\n\x05c\x05\xc5',
                    b'\xaa\x06\x00\n\x05c\x06\xc6',
                    b'\xaa\x06\x00\n\x05c\x07\xc7',
                    b'\xaa\x06\x00\n\x05c\x08\xc8',
                    b'\xaa\x06\x00\n\x05c\t\xc9',
                    b'\xaa\x06\x00\n\x05c\n\xca',
                    b'\xaa\x06\x00\n\x05c\x0b\xcb',
                    b'\xaa\x06\x00\n\x05c\x0c\xcc',
                    b'\xaa\x06\x00\n\x05c\r\xcd',
                    b'\xaa\x06\x00\n\x05c\x0e\xce',
                    b'\xaa\x06\x00\n\x05c\x0f\xcf',
                    b'\xaa\x06\x00\n\x05c\x10\xd0',
                    b'\xaa\x06\x00\n\x05c\x11\xd1',
                    b'\xaa\x06\x00\n\x05c\x12\xd2',
                    b'\xaa\x06\x00\n\x05c\x13\xd3',
                    b'\xaa\x06\x00\n\x05c\x14\xd4',
                    b'\xaa\x06\x00\n\x05c\x15\xd5',
                    b'\xaa\x06\x00\n\x05c\x16\xd6',
                    b'\xaa\x06\x00\n\x05c\x17\xd7',
                    b'\xaa\x06\x00\n\x05c\x18\xd8',
                    b'\xaa\x06\x00\n\x05c\x19\xd9',
                    b'\xaa\x06\x00\n\x05c\x1a\xda',
                    b'\xaa\x06\x00\n\x05c\x1b\xdb',
                    b'\xaa\x06\x00\n\x05c\x1c\xdc',
                    b'\xaa\x06\x00\n\x05c\x1d\xdd',
                    b'\xaa\x06\x00\n\x05c\x1e\xde',
                    b'\xaa\x06\x00\n\x05c\x1f\xdf',
                    b'\xaa\x06\x00\n\x05c \xe0',
                    b'\xaa\x06\x00\n\x05c!\xe1',
                    b'\xaa\x06\x00\n\x05c"\xe2',
                    b'\xaa\x06\x00\n\x05c#\xe3',
                    b'\xaa\x06\x00\n\x05c$\xe4',
                    b'\xaa\x06\x00\n\x05c%\xe5',
                    b'\xaa\x06\x00\n\x05c&\xe6',
                    b"\xaa\x06\x00\n\x05c'\xe7",
                    b'\xaa\x06\x00\n\x05c(\xe8',
                    b'\xaa\x06\x00\n\x05c)\xe9',
                    b'\xaa\x06\x00\n\x05c*\xea',
                    b'\xaa\x06\x00\n\x05c+\xeb',
                    b'\xaa\x06\x00\n\x05c,\xec',
                    b'\xaa\x06\x00\n\x05c-\xed',
                    b'\xaa\x06\x00\n\x05c.\xee',
                    b'\xaa\x06\x00\n\x05c/\xef',
                    b'\xaa\x06\x00\n\x05c0\xf0',
                    b'\xaa\x06\x00\n\x05c1\xf1',
                    b'\xaa\x06\x00\n\x05c2\xf2',
                    b'\xaa\x06\x00\n\x05c3\xf3',
                    b'\xaa\x06\x00\n\x05c4\xf4',
                    b'\xaa\x06\x00\n\x05c5\xf5',
                    b'\xaa\x06\x00\n\x05c6\xf6',
                    b'\xaa\x06\x00\n\x05c7\xf7']
        for i in range(1,56):
            actual_output = self.led.singleTriggerCmd(i)
            self.assertEqual(actual_output, expected_outputs[i-1])

    @patch('serial.Serial', autospec=True)
    def test_illumination(self,mock_serial):
        self.assertEqual(self.led.illuminate()[1],8)
    
    @patch('serial.Serial', autospec=True)
    def test_flush(self,mock_serial):
        self.assertEqual(self.led.flush(),True)

    @patch('serial.Serial', autospec=True)
    def test_trigger(self,mock_serial):
        self.assertEqual(self.led.trigger()[1],8)

    @patch('serial.Serial', autospec=True)
    def test_set_delays(self,mock_serial):
        self.assertEqual(self.led.set_daleys(),8)

    # @patch('serial.Serial', autospec=True)
    # def test_single_trigger(self):
    #     # Current led board has a bug on code. 
    #     # if it is not solved this should not pass.
    #     # this failure can be ignored until next version of led board.
    #     for i in range(1,56):
    #         r = self.led.single_trigger(led_number=i)
    #         self.assertEqual(int.from_bytes(r, "big"),i)

        
if __name__ == '__main__':
    # One failure is possible in sinle_trigger. can be ignored for now
    unittest.main()
