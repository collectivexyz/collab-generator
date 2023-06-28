import cv2
import numpy as np
from collections import deque
import os

def calculate_difference(frame1, frame2):
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(frame1_gray, frame2_gray)
    return np.sum(diff)

def extract_action(video_path, window_size, output_path, padding_seconds=3):
    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

    ret, prev_frame = cap.read()

    frame_idx = 0
    diffs = deque(maxlen=window_size)
    total_diff = 0
    max_diff = 0
    max_diff_start_idx = 0
    frames = deque(maxlen=window_size)
    max_diff_frames = []
    padding = []

    while True:
        ret, curr_frame = cap.read()

        if (len(padding) < fps * padding_seconds):
            padding.append(curr_frame)

        if not ret:
            break

        diff = calculate_difference(prev_frame, curr_frame)
        total_diff += diff
        diffs.append(diff)
        frames.append(curr_frame)

        if len(diffs) == window_size:
            if total_diff > max_diff:
                max_diff = total_diff
                max_diff_start_idx = frame_idx - window_size + 1
                max_diff_frames = list(frames)
                padding = [] 

            total_diff -= diffs[0]

        prev_frame = curr_frame
        frame_idx += 1

    cap.release()

    os.makedirs(output_path, exist_ok=True)

    out = cv2.VideoWriter(f'{output_path}/{video_path.split("/")[-1]}', fourcc, fps, (width, height))

    for frame in max_diff_frames:
        out.write(frame)

    for frame in padding:  # write the padding frames
        out.write(frame)

    out.release()

    return max_diff_start_idx, max_diff_start_idx + window_size

def extract_action_from_many(input_dir, total_duration, output_path):

    # clear output_path:
    for f in os.listdir(output_path):
        os.remove(os.path.join(output_path, f))

    video_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]

    for video_path in video_paths:
        fps = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)
        window_size = min(int(total_duration / len(video_paths) * fps), int(fps*2))  # window size in frames
        start_frame, end_frame = extract_action(video_path, window_size, output_path)
        print(f'Video {video_path}: the most action-packed sequence starts at frame {start_frame} and ends at frame {end_frame}')

if __name__ == "__main__":
    video_dir = "./data"
    video_paths = [os.path.join(video_dir, f) for f in os.listdir(video_dir)]
    total_duration = 60  # total duration for all action sequences combined, in seconds
    output_path = './output'
    extract_action_from_many(video_paths, total_duration, output_path)
