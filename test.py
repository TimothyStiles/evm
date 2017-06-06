import unittest
import numpy as np
import cv2 as cv
import os
import requests
import imageio

import evm.utils as utils
import evm.pyramids as pyramids
import evm.filters as filters

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

    def test_read_stream(self):
        video = utils.read_video('resources/baby.mp4')
        video2 = utils.read_video('resources/baby.mp4')

    def test_read_video(self):
        video = utils.read_video('resources/baby.mp4')
        length, height, width, pixel = video.shape
        self.assertTrue(width == 960 and height == 544 and length == 301 and pixel == 3)

    def test_write_video(self):
        video = utils.read_video('resources/baby.mp4')
        fps = utils.get_fps('resources/baby.mp4')
        utils.write_video(video,'./resources/baby-write-test.avi',fps)
        video_test = utils.read_video('resources/baby-write-test.avi')
        length, height, width, pixel = video_test.shape
        self.assertTrue(width == 960 and height == 544 and length == 301 and pixel == 3)

    def test_video_gaussian(self):
        path = 'resources/baby.mp4'
        fps = utils.get_fps(path)
        laplacians = pyramids.video_gaussian(path)
        utils.write_video(laplacians[0], 'resources/baby-gaussian.mp4', fps)

    def test_video_laplacian(self):
        path = 'resources/baby.mp4'
        fps = utils.get_fps(path)
        laplacians = pyramids.video_laplacian(path)
        utils.write_video(laplacians[0], 'resources/baby-laplacian.mp4', fps)
       # utils.write_laplacians(laplacians, 'resources/baby-lap.mp4', fps)

    def test_temporal_bandpass_filter(self):
        path = 'resources/baby.mp4'
        pyramid = pyramids.video_laplacian(path)
        fps = int(utils.get_fps(path))
        filtered_video= filters.temporal_bandpass_filter(pyramid[3], fps)
        utils.write_video(filtered_video, 'resources/baby-time-filtered.mp4', fps)

    def test_collapse_image_pyramid(self):
        img = cv.imread('resources/slowpoke.png')
        pyramid = pyramids.image_laplacian(img)
        print("pyramid dimesions", len(pyramid), pyramid[4].shape)
        collapsed_pyramid = pyramids.collapse_image_pyramid(pyramid)
        cv.imwrite('resources/slowpoke-pyramid-collapse.png', collapsed_pyramid)

    def test_collapse_video_pyramid(self):
        path = 'resources/baby.mp4'
        fps = utils.get_fps(path)
        laplacian_pyramid = pyramids.video_laplacian(path)
        collapsed_pyramid = pyramids.collapse_video_pyramid(laplacian_pyramid)
        print("pyramid dimensions", len(collapsed_pyramid), collapsed_pyramid[0].shape)
        cv.imwrite('resources/baby-pyramid-collapse.png', pyramids.collapse_image_pyramid(collapsed_pyramid))
    #    utils.write_video(collapsed_pyramid, 'resources/baby-collapse_image_pyramid.mp4', fps)

class TestRequests(unittest.TestCase):

    def test_http_status(self):
        r = requests.get('https://api.github.com/events')
        self.assertTrue(r.status_code == 200)


if __name__ == '__main__':
    unittest.main()
