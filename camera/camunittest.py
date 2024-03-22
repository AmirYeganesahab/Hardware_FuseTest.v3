from module_ import camera
import unittest

cam = camera()

class TestCamera(unittest.TestCase):
    def test_camera(self):
        self.assertEqual(cam, "camera")

    def test_open_device(self):
        self.assertEqual(cam.opend_device(), True)
    
    def test_settings(self):
        self.assertEqual(cam.settings(), True)

    def test_apply_settings(self):
        self.assertEqual(cam.apply_settings(), True)

    def test_capture(self):
        self.assertEqual(cam.capture(), True)

    def test_close_device(self):
        self.assertEqual(cam.close_device(), True)

    def test_get_image(self):
        self.assertIsNotNone(cam.get_image())