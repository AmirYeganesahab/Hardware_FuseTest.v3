import numpy as np, cython, time
import serial
from ximea import xiapi
import logging
import cv2
logging.basicConfig(level=logging.DEBUG)