import os
import re
import cv2
from tqdm import tqdm
from pathlib import Path

img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']  # acceptable image suffixes
vid_formats = ['mov', 'avi', 'mp4', 'mpg', 'mpeg', 'm4v', 'wmv', 'mkv']  # acceptable video suffixes

class LoadImagesAndLabels():
    def __init__(self, path):
        # load all images and videos (with multiple extensions) from a directory using OpenCV
        IMAGE_PATH_LIST = []
        VIDEO_NAME_DICT = {}
        pbar = tqdm(sorted(Path(path).glob('**/*.*')))
        # for f in sorted(os.listdir(INPUT_DIR), key = natural_sort_key):
        desc='scaning images:{} and videos:{}'
        for f in pbar:
            if not f.is_file:
                continue
            if f.suffix and f.suffix[1:] in img_formats:
                # check if it is an image
                test_img = cv2.imread(str(f))
                if test_img is not None:
                    IMAGE_PATH_LIST.append(str(f))
            elif f.suffix and f.suffix[1:] in vid_formats:
                # test if it is a video
                test_video_cap = cv2.VideoCapture(str(f))
                n_frames = int(test_video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
                test_video_cap.release()
                if n_frames == 0:
                    continue
                # it is a video
                desired_img_format = '.jpg'
                video_frames_path, video_name_ext = video2images(str(f), n_frames, desired_img_format)
                # add video frames to image list
                frame_list = sorted(os.listdir(video_frames_path), key = natural_sort_key)
                ## store information about those frames
                first_index = len(IMAGE_PATH_LIST)
                last_index = first_index + len(frame_list) # exclusive
                indexes_dict = {}
                indexes_dict['first_index'] = first_index
                indexes_dict['last_index'] = last_index
                VIDEO_NAME_DICT[video_name_ext] = indexes_dict
                IMAGE_PATH_LIST.extend((os.path.join(video_frames_path, frame) for frame in frame_list))
            pbar.set_description(desc.format(len(IMAGE_PATH_LIST), len(VIDEO_NAME_DICT)))
            
        print(f"found {len(IMAGE_PATH_LIST)} images and {len(VIDEO_NAME_DICT)} videos")
        self.IMAGE_PATH_LIST = IMAGE_PATH_LIST
        self.VIDEO_NAME_DICT = VIDEO_NAME_DICT

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]

def video2images(video_path, n_frames, desired_img_format):
    # create folder to store images (if video was not converted to images already)
    file_path, file_extension = os.path.splitext(video_path)
    # append extension to avoid collision of videos with same name
    # e.g.: `video.mp4`, `video.avi` -> `video_mp4/`, `video_avi/`
    file_extension = file_extension.replace('.', '_')
    file_path += file_extension
    video_name_ext = os.path.basename(file_path)
    if not os.path.exists(file_path):
        print(' Converting video to individual frames...')
        cap = cv2.VideoCapture(video_path)
        os.makedirs(file_path)
        # read the video
        for i in tqdm(range(n_frames)):
            if not cap.isOpened():
                break
            # capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                # save each frame (we use this format to avoid repetitions)
                frame_name =  '{}_{}{}'.format(video_name_ext, i, desired_img_format)
                frame_path = os.path.join(file_path, frame_name)
                cv2.imwrite(frame_path, frame)
        # release the video capture object
        cap.release()
    return file_path, video_name_ext