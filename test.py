import unittest
import numpy as np
import cv2 as cv
import os
import requests
import imageio

import evm.utils as utils
import evm.pyramids as pyramids

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
        cv.imwrite('resources/slowpoke-gray.png', gray)
        self.assertTrue(os.path.isfile('resources/slowpoke-gray.png'))

    def test_video_identity(self):
        self.assertTrue(callable(cv.VideoCapture))

    def test_videocapture(self):
       """Needs to be rewritten to test for multiple image frames."""
        cap = cv.VideoCapture('resources/baby.mp4')
        ret, frame = cap.read()
        px = frame[0, 0, 0]
        cap.release()
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

    def test_image_gaussian(self):
        img = cv.imread('resources/slowpoke.png')
        pyramid = pyramids.image_gaussian(img)
        utils.save_image_pyramid(pyramid, 'resources/slowpoke-gaussian-pyramid.png')

    def test_image_laplacian(self):
        img = cv.imread('resources/slowpoke.png')
        pyramid = pyramids.image_laplacian(img)
        utils.save_image_pyramid(pyramid, 'resources/slowpoke-laplacian-pyramid.png')

    def test_video_in_out(self):
        reader = imageio.get_reader('resources/baby.mp4')
        fps = reader.get_meta_data()['fps']
        writer = imageio.get_writer('resources/baby-gray.mp4', fps=fps)

        for im in reader:
            writer.append_data(im[:, :, 1])
        writer.close()

        gray_reader = imageio.get_reader('resources/baby-gray')
        gray_fps = gray_reader.get_meta_data()['fps']
        self.assertTrue(fps == gray_fps)

class TestRequests(unittest.TestCase):

    def test_http_status(self):
        r = requests.get('https://api.github.com/events')
        self.assertTrue(r.status_code == 200)


if __name__ == '__main__':
    unittest.main()
