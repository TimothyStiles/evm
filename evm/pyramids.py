import numpy as np
import cv2 as cv

import evm.utils as utils

def gaussian_image_pyramid(img):
    """Computes image gaussian pyramid from frame or image."""
    gaussian = img.copy() #needs better name
    pyramid = [gaussian]
    for i in range(6):
        gaussian = cv.pyrDown(gaussian)
        pyramid.append(gaussian)
    return pyramid

def laplacian_image_pyramid(img): # may have an extra layer that isn't being used.
    """Computes image laplacian pyramid from frame or image."""
    laplacian_pyramid = [gaussian_image_pyramid(img)[5].copy()]
    gaussian_pyramid = gaussian_image_pyramid(img)
    for i in range(5, 0, -1):
        gaussian = cv.pyrUp(gaussian_pyramid[i])
        laplacian = cv.subtract(gaussian_pyramid[i -1], gaussian)
        laplacian_pyramid.append(laplacian)
    return laplacian_pyramid


def gaussian_video_pyramid(path):
    """Computes video laplacian pyramid from video."""
    video = utils.read_video(path)
    gaussian = []

    for im in video:
        gaussian.append(np.array(gaussian_image_pyramid(im)))

    gaussian = np.array(gaussian)
    video_length = len(gaussian)
    pyramid_height = len(gaussian[0])
    pyramid_videos = []

    for vid in range(pyramid_height):
        frames = []
        for im in range(video_length):
            frames.append(gaussian[:, vid][im])
        pyramid_videos.append(np.array(frames))

    return pyramid_videos

def laplacian_video_pyramid(path): #may also have an image layer that isn't used.
    """Computes video laplacian pyramid from video."""
    video = utils.read_video(path)
    laplacian = []

    for im in video:
        laplacian.append(np.array(laplacian_image_pyramid(im)))

    laplacian = np.array(laplacian)
    video_length = len(laplacian)
    pyramid_height = len(laplacian[0]) - 1
    pyramid_videos = []

    for vid in range(pyramid_height, 0, -1):
        frames = []
        for im in range(video_length):
            frames.append(laplacian[:, vid][im])
        pyramid_videos.append(np.array(frames))

    return pyramid_videos

def collapse_image_pyramid(pyramid):
    """Collapses an image pyramid into a single image."""
    height = len(pyramid)
    collapsed_image = pyramid[0]
    for im in range(1, height):
        collapsed_image = cv.pyrUp(collapsed_image)
        collapsed_image = cv.add(collapsed_image, pyramid[im])
    return collapsed_image

def collapse_video_pyramid(video_pyramid): #gaussian pyramid may need to be reversed for this.
    """Collapses a video pyramid into a single video."""
    video = []
    pyramid_height = len(video_pyramid)
    video_length = len(video_pyramid[0])

    for frame in range(0, video_length):
        pyramid = []
        for pyramid_level in range(0, pyramid_height):
            pyramid.append(video_pyramid[pyramid_level][frame])
        pyramid.reverse()
        collapsed_video_pyramid_frame = np.array(collapse_image_pyramid(pyramid))
        video.append(collapsed_video_pyramid_frame)
    return video
