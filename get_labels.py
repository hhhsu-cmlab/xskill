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

# add episode_index column
# episode_index corresponds to the video at position `episode_index` of data.h5
# episode_index = -1 means the corresponding video is not made yet
if "episode_index" not in dat:
    dat["episode_index"] = -1

dat.to_csv("datasets/data/labels_complete.csv")
