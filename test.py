import unittest
import numpy as np
import cv2 as cv

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

    def test_video_identity(self):
        self.assertTrue(callable(cv.VideoCapture))

    def test_videocapture(self):
        cap = cv.VideoCapture('resources/baby.mp4')
        ret, frame = cap.read()
        px = frame[0, 0, 0]
        self.assertTrue(px == 7)

if __name__ == '__main__':
    unittest.main()
