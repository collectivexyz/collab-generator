import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

# stitches videos together

def stitch_many(input_dir, output_dir):
    # Get a list of all files in the directory
    files = os.listdir(input_dir)
    
    # Filter out non-video files
    video_files = [f for f in files if f.endswith(('.mp4', '.flv', '.mkv', '.webm', '.avi'))]

    # Sort the files by name
    video_files.sort()

    # Create a list of video clips
    clips = [VideoFileClip(os.path.join(input_dir, video_file)) for video_file in video_files]

    # Concatenate the clips into a single video
    final_clip = concatenate_videoclips(clips)

    # Write the final clip to a file
    final_clip.write_videofile(output_dir + "/final.mp4")