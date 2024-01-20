from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.resize import resize
import numpy as np
import pandas as pd
import h5py
import os
from collections import defaultdict
import json
from tqdm import tqdm

N_FRAMES = 40
VID_SQUARE_SIZE = 256
labels_complete_csv_path = "datasets/data/labels_complete.csv"
dat = pd.read_csv(labels_complete_csv_path)

cur_episode_idx = dat['episode_index'].max() + 1

class Saver:
    def __init__(self, label, start_idx, max_size=20):
        self.max_size = max_size
        self.start_idx = start_idx
        self.label = label # label on filename of saved h5 data
        self.items = []

    def append(self, item):
        self.items.append(item)
        if len(self.items) >= self.max_size:
            self._save()

    def _save(self):
        end_idx = self.start_idx + self.max_size - 1
        filename = f"data_{self.label}_{self.start_idx}_{end_idx}.h5"
        with h5py.File(f"datasets/data/{filename}", 'w') as f:
            f.create_group("sim")
            f["sim"].create_dataset("ims", data=np.array(self.items, dtype=np.uint8))
        print(f'Videos of size {self.max_size} saved.')

        self.items = []
        self.start_idx = end_idx + 1

saver_full = Saver(label="full", start_idx=cur_episode_idx, max_size=20)
saver_square = Saver(label="square", start_idx=cur_episode_idx, max_size=50)

####### process videos #######

def extract_frames(input_file, start_time, end_time, num_frames):
    # Load the video clip
    video_clip = VideoFileClip(input_file)

    # resizing
    # without resizing, the script would get killed when it is about 48% complete
    #  Out of memory: Killed process 13933 (python) total-vm:7816116kB, anon-rss:6783396kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:14656kB oom_score_adj:0
    #video_clip = resize(video_clip, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)

    # Calculate the time points for the frames
    time_points = np.linspace(start_time, end_time, num_frames)

    '''
    frames = []; square_frames = []
    for t in time_points:
        frm = video_clip.get_frame(t)
        w, h = frm.shape
    '''

    # Extract frames at the specified time points
    frames = [video_clip.get_frame(t) for t in time_points]

    video_clip.close()

    return np.array(frames, dtype=np.uint8)

def frames_for(i: int):
    # i: row i
    v_folder = dat['video_folder'][i]
    v_idx = dat['video_index'][i]
    cam_idx = dat['camera_index'][i]
    video_path = f"datasets/data_v2/{v_folder}/videos/{v_idx}/{cam_idx}/color.mp4"
    return extract_frames(video_path, dat['start'][i], dat['end'][i], N_FRAMES)

undone_rows = np.where(dat['episode_index'] == -1)[0]
for i, r in tqdm(enumerate(undone_rows)):
    saver_full.append(frames_for(r))

    # update index i to done
    dat['episode_index'][r] = cur_episode_idx
    cur_episode_idx += 1

dat.to_csv("datasets/data/test/labels_complete.csv", index=False)
