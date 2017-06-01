import unittest
import numpy as np
import cv2 as cv
import os
import requests

import evm.utils as utils

class TestTruth(unittest.TestCase):

    def test_mult(self):
        self.assertTrue(True)


class TestNumpyMatrix(unittest.TestCase):

    def test_module_existence(self):
        self.assertTrue(callable(np.identity))
        
    def test_mult_identity(self):
        a = np.random.rand(3,3)
        i = np.identity(3)
        self.assertTrue(np.array_equal(np.matmul(a, i), a))


class TestCv(unittest.TestCase):

    def test_image_identity(self):
        self.assertTrue(callable(cv.imread))

    def test_imread(self):
        img = cv.imread('resources/slowpoke.png')
        px = img[0, 0, 0]
        self.assertTrue(px == 0)

    def test_imwrite(self):
        img = cv.imread('resources/slowpoke.png')
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imwrite('resources/slowpokegray.png', gray)
        self.assertTrue(os.path.isfile('resources/slowpokegray.png'))

    def test_video_identity(self):
        self.assertTrue(callable(cv.VideoCapture))

    def test_videocapture(self):
        cap = cv.VideoCapture('resources/baby.mp4')
        ret, frame = cap.read()
        px = frame[0, 0, 0]
        self.assertTrue(px == 7)

    def test_get_vid_height(self):
        self.assertTrue(utils.get_vid_height('resources/baby.mp4') == 544.0)

    def test_get_vid_width(self):
        self.assertTrue(utils.get_vid_width('resources/baby.mp4') ==  960.0)

    def test_get_fps(self):
        self.assertTrue(utils.get_fps('resources/baby.mp4') == 30.0)

    def test_get_length(self):
        self.assertTrue(utils.get_vid_length('resources/baby.mp4') == 301.0)

    def test_get_dimensions(self):
        width, height, length, fps = utils.get_vid_dimensions('resources/baby.mp4')
        self.assertTrue(width == 960.0 and height == 544.0 and length == 301.0 and fps == 30.0)

class TestRequests(unittest.TestCase):

    def test_http_status(self):
        r = requests.get('https://api.github.com/events')
        self.assertTrue(r.status_code == 200)


if __name__ == '__main__':
    unittest.main()
