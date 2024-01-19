from flask import Flask, render_template, url_for
import numpy as np
import imageio
import json
import cv2
import os
import pandas as pd

CAMERA_IDX = 0 # 0, 1, 2

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
    return render_template('crop.html', video_path=video_path)


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
