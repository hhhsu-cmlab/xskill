from flask import Flask, request, render_template, url_for, redirect
import numpy as np
import imageio
import json
import cv2
import os
import pandas as pd
from collections import defaultdict

CAMERA_IDX = 0 # 0, 1, 2


new_timestamps_data = defaultdict(list) # store new timestamps data
# should have keys:
# 'camera_index', 'video_folder', 'video_index', 'stage', 'start', 'end'

timestamps_csv_path = "datasets/timestamps.csv"
def save(new_data: defaultdict):
    '''
    move the timestamps data in new_data into timestamps.csv
    '''
    if os.path.exists(timestamps_csv_path):
        timestamps_df = pd.read_csv(timestamps_csv_path)
        new_data_df = pd.DataFrame(new_data)
        timestamps_df = pd.concat([timestamps_df, new_data_df], ignore_index=True)
    else:
        print(f"Warning: {timestamps_csv_path} does not exist.")
        timestamps_df = pd.DataFrame(new_data)
        
    timestamps_df.to_csv(timestamps_csv_path, index=False)

    new_data.clear() 

with open("datasets/config/data.json", "r") as f:
    data = json.load(f)

app = Flask(__name__, static_folder='datasets')

@app.route('/')
def index():
    data_dir_path = '.' + url_for('static', filename='data_v2')
    video_dirs = [d for d in os.listdir(data_dir_path) if os.path.isdir(os.path.join(data_dir_path, d))]
    return render_template('index.html', directories=video_dirs)

@app.route('/<string:folder>')
def show_crop_page(folder: str):
    videos_path = '.' + url_for('static', filename=f'data_v2/{folder}/videos')
    if not os.path.isdir(videos_path):
        raise Exception("no such directory: videos_path")
    for d in os.listdir(videos_path):
        pass

@app.route('/<string:folder>/<string:video_idx>')
def show_crop(folder: str, video_idx: str):
    video_path = url_for('static', filename=f'data_v2/{folder}/videos/{video_idx}/{str(CAMERA_IDX)}/color.mp4')
    try:
        stages = data['data'][folder]['stages']
        return render_template('crop.html', 
                            video_path=video_path, 
                            stages=stages, 
                            video_folder=folder)
    except:
        print(f"Warning: the video path specified by {folder}/{video_idx} probably does not exist.")
        return redirect(url_for('index'))
    

@app.route('/<string:folder>/<string:video_idx>', methods=['POST'])
def process(folder: str, video_idx: str):
    msg = request.form.get("content")
    if msg is None:
        raise Exception("Something wrong with reading timestamps")
    
    timestamps = json.loads(msg)
    
    for t in timestamps:
        new_timestamps_data['camera_index'].append(CAMERA_IDX)
        new_timestamps_data['video_folder'].append(folder)
        new_timestamps_data['video_index'].append(video_idx)
        new_timestamps_data['start'].append(t['start'])
        new_timestamps_data['end'].append(t['end'])
        
        # deal with stage
        new_timestamps_data['stage'].append(-1)

    save(new_timestamps_data)
    
    return redirect(f'/{folder}/{int(video_idx) + 1}')

def next_video(folder: str):
    '''
    get the next video to crop in the folder

    folder: e.g. draw_cloth_light
    '''
    labels_df_path = '.' + url_for('static', filename='labels.csv')
    labels_df = pd.read_csv(labels_df_path) # what if you cannot read it?

    video_indices = (labels_df.filter(labels_df['video_folder'] == folder))['video_idx']
    pass

def read_video():

    # Path to the video file
    video_path = '.' + url_for('static', filename='data_v2/draw_cloth_light/videos/0/0/color.mp4')

    # Read the video using imageio
    video_reader = imageio.get_reader(video_path)
    print(f"fps: {video_reader.get_meta_data()}")
    return video_reader.get_meta_data()

    '''
    # Initialize an empty list to store video frames
    frames = []

    # Read frames until the video ends
    for frame in video_reader:
        # Convert the frame to a NumPy array
        frame_array = np.array(frame)

        # Append the frame array to the list
        frames.append(frame_array)

    # Convert the list of frames to a NumPy array
    video_array = np.array(frames)

    # Print the shape of the array (height, width, channels, frames)
    print("Shape of the video array:", video_array.shape)

    # Close the video reader
    video_reader.close()

    return video_array.tolist()
    '''

def sample_frames(video_path, num_frames=100):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        raise Exception("Error: Could not open video file.")

    # Get total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the frame indices to sample
    indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

    # Initialize an empty list to store sampled frames
    sampled_frames = []

    # Read and store the sampled frames
    for index in indices:
        # Set the frame position to the current index
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)

        # Read the frame
        ret, frame = cap.read()

        # Check if the frame is read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Append the frame to the list
        sampled_frames.append(frame.tolist())
    
    # Release the video capture object
    cap.release()

    return sampled_frames


if __name__ == '__main__':
    app.run(debug=True)
