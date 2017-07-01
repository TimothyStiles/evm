import unittest
import numpy as np
import cv2 as cv
import os
import requests
import imageio

import evm.utils as utils
import evm.pyramids as pyramids
import evm.filters as filters

test_image_input_path = 'resources/test_input/slowpoke.png'
test_video_input_path = 'resources/test_input/baby.mp4'
test_output_path = 'resources/test_output/'


class TestTruth(unittest.TestCase):

    def test_truth(self):
        self.assertTrue(True)


class TestNumpyMatrix(unittest.TestCase):

    def test_module_existence(self):
        self.assertTrue(callable(np.identity))

    def test_mult_identity(self):
        a = np.random.rand(3,3)
        i = np.identity(3)
        self.assertTrue(np.array_equal(np.matmul(a, i), a))


class TestOs(unittest.TestCase):

    def test_dirname(self):
        dirname = os.path.dirname(os.path.abspath("test.py"))
        self.assertTrue(os.path.exists(dirname))


class TestCv(unittest.TestCase):

    def test_image_identity(self):
        self.assertTrue(callable(cv.imread))

    def test_imread(self):
        img = cv.imread(test_image_input_path)
        px = img[0, 0, 0]
        self.assertTrue(px == 0)

    def test_imwrite(self):
        img = cv.imread(test_image_input_path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imwrite(test_output_path + 'slowpoke-gray.png', gray)
        self.assertTrue(os.path.isfile(test_output_path + 'slowpoke-gray.png'))

    def test_video_identity(self):
        self.assertTrue(callable(cv.VideoCapture))

    def test_videocapture(self):
        cap = cv.VideoCapture(test_video_input_path)
        ret, frame = cap.read()
        px = frame[0, 0, 0]
        cap.release()
        self.assertTrue(px == 7)


class TestUtils(unittest.TestCase):

    def test_get_vid_height(self):
        self.assertTrue(utils.get_vid_height(test_video_input_path) == 544.0)

    def test_get_vid_width(self):
        self.assertTrue(utils.get_vid_width(test_video_input_path) ==  960.0)

    def test_get_fps(self):
        self.assertTrue(utils.get_fps(test_video_input_path) == 30.0)

    def test_get_length(self):
        self.assertTrue(utils.get_vid_length(test_video_input_path) == 301.0)

    def test_get_dimensions(self):
        width, height, length, fps = utils.get_vid_dimensions(test_video_input_path)
        self.assertTrue(width == 960.0 and height == 544.0 and length == 301.0 and fps == 30.0)

    def test_read_stream(self):
        video = utils.read_video(test_video_input_path)
        video2 = utils.read_video(test_video_input_path)

    def test_read_video(self):
        video = utils.read_video(test_video_input_path)
        length, height, width, pixel = video.shape
        self.assertTrue(width == 960 and height == 544 and length == 301 and pixel == 3)

    def test_write_video(self):
        video = utils.read_video(test_video_input_path)
        fps = utils.get_fps(test_video_input_path)
        utils.write_video(video, test_output_path + 'baby-write-test.mp4',fps)
        video_test = utils.read_video(test_output_path + 'baby-write-test.mp4')
        length, height, width, pixel = video_test.shape
        self.assertTrue(width == 960 and height == 544 and length == 301 and pixel == 3)


class TestPyramids(unittest.TestCase):

    def test_gaussian_image_pyramid(self):
        img = cv.imread(test_image_input_path)
        pyramid = pyramids.gaussian_image_pyramid(img)
        utils.save_image_pyramid(pyramid, test_output_path + 'slowpoke-gaussian-pyramid.png')

    def test_laplacian_image_pyramid(self):
        img = cv.imread(test_image_input_path)
        pyramid = pyramids.laplacian_image_pyramid(img)
        utils.save_image_pyramid(pyramid, test_output_path + 'slowpoke-laplacian-pyramid.png')

    def test_gaussian_video_pyramid(self):
        fps = utils.get_fps(test_video_input_path)
        laplacians = pyramids.gaussian_video_pyramid(test_video_input_path)
        utils.write_video(laplacians[0], test_output_path + 'baby-gaussian.mp4', fps)

    def test_laplacian_video_pyramid(self):
        fps = utils.get_fps(test_video_input_path)
        laplacians = pyramids.laplacian_video_pyramid(test_video_input_path)
        utils.write_video(laplacians[0], test_output_path + 'baby-laplacian.mp4', fps)

    def test_collapse_image_pyramid(self):
        img = cv.imread(test_image_input_path)
        pyramid = pyramids.laplacian_image_pyramid(img)
        collapsed_pyramid = pyramids.collapse_image_pyramid(pyramid)
        cv.imwrite(test_output_path + 'slowpoke-pyramid-collapse.png', collapsed_pyramid)

    def test_collapse_video_pyramid(self):
        fps = utils.get_fps(test_video_input_path)
        laplacian_pyramid = pyramids.laplacian_video_pyramid(test_video_input_path)
        collapsed_pyramid = pyramids.collapse_video_pyramid(laplacian_pyramid)
        utils.write_video(collapsed_pyramid, test_output_path + 'baby-collapse-video-pyramid.mp4', fps)

class TestFilters(unittest.TestCase):

    def test_temporal_bandpass_filter(self):
        pyramid = pyramids.laplacian_video_pyramid(test_video_input_path)
        fps = int(utils.get_fps(test_video_input_path))
        filtered_video= filters.temporal_bandpass_filter(pyramid[3], fps)
        utils.write_video(filtered_video, test_output_path + 'baby-time-filtered.mp4', fps)

    def test_filter_video_pyramid(self):
        fps = utils.get_fps(test_video_input_path)
        laplacian_pyramid = pyramids.laplacian_video_pyramid(test_video_input_path)
        filtered_pyramid = filters.filter_video_pyramid(laplacian_pyramid[1:-1], fps, 0.4, 3, 0, 10)
        collapsed_pyramid = pyramids.collapse_video_pyramid(filtered_pyramid)
        utils.write_video(collapsed_pyramid, test_output_path + 'baby-collapse-filtered-video-pyramid.mp4', fps)

class TestRequests(unittest.TestCase):

    def test_http_status(self):
        r = requests.get('https://api.github.com/events')
        self.assertTrue(r.status_code == 200)


if __name__ == '__main__':
    unittest.main()
