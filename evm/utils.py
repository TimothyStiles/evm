import numpy as np
import cv2 as cv

def get_fps(path):
    """Gets frames per second of video."""
    video = cv.VideoCapture(path)
    fps = video.get(cv.CAP_PROP_FPS)
    video.release()
    return fps

def get_vid_height(path):
    """Gets pixel height of video frames."""
    video = cv.VideoCapture(path)
    height = video.get(cv.CAP_PROP_FRAME_HEIGHT)
    video.release()
    return height

def get_vid_width(path):
    video = cv.VideoCapture(path)
    """Gets pixel width of video frames."""
    width = video.get(cv.CAP_PROP_FRAME_WIDTH)
    video.release()
    return width

def get_vid_length(path):
    """Gets number of frames in video."""
    video = cv.VideoCapture(path)
    length = video.get(cv.CAP_PROP_FRAME_COUNT)
    video.release()
    return width

def get_vid_dimensions(path):
    """Gets dimensions of video."""
    width = get_vid_width(path)
    height = get_vid_height(path)
    length = get_vid_length(path)
    fps = get_fps(path)
    return width, height, length, fps
