from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np
import pandas as pd
import h5py
import os
from collections import defaultdict
import json

N_FRAMES = 40

dat = pd.read_csv("datasets/timestamps.csv")
with open("datasets/config/data.json") as f:
    metadata = json.load(f)

####### add info to dat #######
    
# generates task names and append them to dat
dat['stage'] = dat.groupby(['video_folder', 'video_index']).cumcount()
def func(row):
    v_folder = row['video_folder']
    stage_idx = row['stage']
    return metadata['data'][v_folder]['stages'][stage_idx]
dat['Task Name'] = dat.apply(func, axis=1)

# generate env descriptions
def get_env_descriptions(video_folder, task_name):
    env_descriptions_binary = metadata['data'][video_folder]['Env Descriptions'][task_name]
    descriptions_map = metadata['Env Descriptions']
    return [descriptions_map[i][b] for i, b in enumerate(env_descriptions_binary)]

env_d = dat.apply(lambda row: get_env_descriptions(row['video_folder'], row['Task Name']),
          axis=1)
env_d = env_d.apply(pd.Series)

colnames = [f"Env Descriptions: {obj}" for obj in metadata["Env_Objects"]]
env_d.columns = colnames 

dat = pd.concat([dat, env_d], axis=1)

####### ------------------ #######




def extract_frames(input_file, start_time, end_time, num_frames):
    # Load the video clip
    video_clip = VideoFileClip(input_file)

    # Calculate the time points for the frames
    time_points = np.linspace(start_time, end_time, num_frames)

    # Extract frames at the specified time points
    frames = [video_clip.get_frame(t) for t in time_points]

    return frames




# add stages
def addStages(video_folder, video_index):
    stages = metadata['data'][video_folder]['stages']


def transform(start_idx: int, end_idx: int):
    for i in range(start_idx, end_idx):
        v_folder = dat['video_folder'][i]
        v_idx = dat['video_index'][i]
        cam_idx = dat['camera_index'][i]
        video_path = f"datasets/data_v2/{v_folder}/videos/{v_idx}/{cam_idx}/color.mp4"
        frames = extract_frames(video_path, dat['start'], dat['end'], N_FRAMES)

def transform(i: int):
    v_folder = dat['video_folder'][i]
    v_idx = dat['video_index'][i]
    cam_idx = dat['camera_index'][i]
    video_path = f"datasets/data_v2/{v_folder}/videos/{v_idx}/{cam_idx}/color.mp4"
    return extract_frames(video_path, dat['start'], dat['end'], N_FRAMES)


labels_dict = defaultdict(list)
labels_dict['video_folder'].append()




def make_labels(, )
    
with open("datasets/data/labels.csv", "r") as f:


with h5py.File("datasets/data/data.h5", "w") as hf:
    pass


