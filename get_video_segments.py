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
VIDEO_WIDTH = 160
VIDEO_HEIGHT = 160
dat = pd.read_csv("datasets/data/labels_complete.csv")

####### process videos #######

def extract_frames(input_file, start_time, end_time, num_frames):
    # Load the video clip
    video_clip = VideoFileClip(input_file)

    # resizing
    # without resizing, the script would get killed when it is about 48% complete
    #  Out of memory: Killed process 13933 (python) total-vm:7816116kB, anon-rss:6783396kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:14656kB oom_score_adj:0
    video_clip = resize(video_clip, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)

    # Calculate the time points for the frames
    time_points = np.linspace(start_time, end_time, num_frames)

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

videos = []
nrow = len(dat.index)
for i in tqdm(range(3)):
    videos.append(frames_for(i))
videos = np.array(videos, dtype=np.uint8)

print(f"Shape of all videos: {videos.shape}")

####### save #######

with h5py.File("datasets/data/data.h5", 'w') as f:
    sim_data = f.create_group('sim')
    sim_data.create_dataset('ims', data=videos)  

