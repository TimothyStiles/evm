import numpy as np
import cv2 as cv

def get_fps(path):
    video = cv.VideoCapture(path)
    fps = video.get(cv.CAP_PROP_FPS)
    video.release()
    return fps

def get_vid_height(path):
    video = cv.VideoCapture(path)
    height = video.get(cv.CAP_PROP_FRAME_HEIGHT)
    video.release()
    return height

def get_vid_width(path):
    video = cv.VideoCapture(path)
    width = video.get(cv.CAP_PROP_FRAME_WIDTH)
    video.release()
    return width

def get_vid_length(path):
    video = cv.VideoCapture(path)
    length = video.get(cv.CAP_PROP_FRAME_COUNT)
    video.release()
    return width
