import numpy as np
import cv2 as cv

import evm.utils as utils

def image_gaussian(img):
    """Computes image gaussian pyramid from frame or image."""
    gaussian = img.copy() #needs better name
    pyramid = [gaussian]
    for i in range(6):
        gaussian = cv.pyrDown(gaussian)
        pyramid.append(gaussian)
    return pyramid

def image_laplacian(img): # may have an extra layer that isn't being used.
    """Computes image laplacian pyramid from frame or image."""
    laplacian_pyramid = [image_gaussian(img)[5].copy()]
    gaussian_pyramid = image_gaussian(img)
    for i in range(5, 0, -1):
        gaussian = cv.pyrUp(gaussian_pyramid[i])
        laplacian = cv.subtract(gaussian_pyramid[i -1], gaussian)
        laplacian_pyramid.append(laplacian)
    return laplacian_pyramid


def video_gaussian(path):
    """Computes video laplacian pyramid from video."""
    video = utils.read_video(path)
    gaussian = list()

    for im in video:
        gaussian.append(np.array(image_gaussian(im)))

    gaussian = np.array(gaussian)
    video_length = len(gaussian) - 1
    pyramid_height = len(gaussian[0]) -1
    pyramid_videos = list()

    for vid in range(pyramid_height):
        frames = list()
        for im in range(video_length):
            frames.append(gaussian[:, vid][im])
        pyramid_videos.append(np.array(frames))

    return pyramid_videos

def video_laplacian(path):
    """Computes video laplacian pyramid from video."""
    video = utils.read_video(path)
    laplacian = list()

    for im in video:
        laplacian.append(np.array(image_laplacian(im)))

    laplacian = np.array(laplacian)
    video_length = len(laplacian) - 1
    pyramid_height = len(laplacian[0]) - 1
    pyramid_videos = list()

    for vid in range(pyramid_height, 0, -1):
        frames = list()
        for im in range(video_length):
            frames.append(laplacian[:, vid][im])
        pyramid_videos.append(np.array(frames))

    return pyramid_videos

def collapse_image_pyramid(pyramid):
    height = len(pyramid) - 1
    collapsed_image = pyramid[0]
    for im in range(1, height):
        collapsed_image = cv.pyrUp(collapsed_image)
        collapsed_image = cv.add(collapsed_image, pyramid[im])
    return collapsed_image

def collapse_video_pyramid(video_pyramid):
    frames = list()
    pyramid_height = len(video_pyramid) - 1
    video_length = len(video_pyramid[0]) - 1
    pyramid = []
    for im in range(0, pyramid_height):
        pyramid.append(video_pyramid[im][0])
    pyramid.reverse()
    return pyramid
