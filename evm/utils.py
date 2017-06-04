import numpy as np
import cv2 as cv
import imageio

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
    """Gets pixel width of video frames."""
    video = cv.VideoCapture(path)
    width = video.get(cv.CAP_PROP_FRAME_WIDTH)
    video.release()
    return width

def get_vid_length(path):
    """Gets number of frames in video."""
    video = cv.VideoCapture(path)
    length = video.get(cv.CAP_PROP_FRAME_COUNT)
    video.release()
    return length

def get_vid_dimensions(path):
    """Gets dimensions of video."""
    width = get_vid_width(path)
    height = get_vid_height(path)
    length = get_vid_length(path)
    fps = get_fps(path)
    return width, height, length, fps

def save_image_pyramid(pyramid, output_basename):
    """Saves image pyramid to files as n images where n is pyramid height."""
    height = len(pyramid) - 1
    name = output_basename.split(".")[0]
    extension = output_basename.split(".")[-1] or "png"
    for i in range(height, 0, -1):
        cv.imwrite(name + '_' + str(i) + '.' + extension, pyramid[i])
    return None

def read_video(path):
    """Load video as 4D numpy array."""
    reader = imageio.get_reader(path)
    images = list()
    for im in reader:
        images.append(im)
    reader.close()
    return np.array(images)

def write_video(output, path, fps):
    """Write 4D numpy array as video"""
    writer = imageio.get_writer(path, fps=fps)
    for im in output:
        writer.append_data(im)
    writer.close()
    return None

def write_laplacians(laplacians, output_basename, fps):
    """Saves laplacians from video_lapcian to file"""
    height = len(laplacians) - 1
    name = output_basename.split(".")[0]
    extension = output_basename.split(".")[-1] or ".mp4"
    for i in range(height, 0, -1):
        write_video(name + '_' + str(i) + '.' + extension, laplacians[i], fps)
    return None
