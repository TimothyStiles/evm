import numpy as np
import cv2 as cv

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

def video_laplacian(path):
    """Computes video laplacian pyramid from video."""
