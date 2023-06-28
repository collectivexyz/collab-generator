# get_overlay should get the overlay for the community 

def get_overlay(revolution_id):
    pass

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, clips_array
from PIL import Image
import os 
from moviepy.video.fx.all import resize

def add_overlay(clip_path, output_path, overlay_path):
    # Load the overlay image with Pillow to get its size
    overlay_image = Image.open(overlay_path)
    overlay_width, overlay_height = overlay_image.size

    # Load the video clip
    clip = VideoFileClip(clip_path)

    # Calculate the ratio for resizing the video
    ratio = min(overlay_width / clip.w, overlay_height / clip.h)

    # Resize the video to fit within the overlay
    resized_clip = clip.fx(resize, ratio)

    # Create a blurred background
    blur_clip = resized_clip.fx(resize, width=overlay_width, height=overlay_height)
    
    # Position the resized video in the center of the frame
    final_clip = clips_array([[blur_clip, resized_clip.set_position('center')]])

    # Create an ImageClip from the overlay
    overlay_clip = ImageClip(overlay_path, duration=clip.duration)

    # Overlay the image on the video clip
    final_clip = CompositeVideoClip([final_clip, overlay_clip.set_duration(clip.duration)])


    # Write the final clip to a file
    final_clip.write_videofile(output_path)

def add_overlay_to_many(input_dir, output_dir, overlay_path):
    # Get a list of all files in the directory
    files = os.listdir(input_dir)
    
    # Filter out non-video files
    video_files = [f for f in files if f.endswith(('.mp4', '.flv', '.mkv', '.webm', '.avi'))]
    
    for video_file in video_files:
        add_overlay(os.path.join(input_dir, video_file), os.path.join(output_dir, video_file), overlay_path)

input_directory = "./data"
output_directory = "./output/overlayed"
overlay_path = "./assets/overlay.png"

# Usage
if __name__ == "__main__":
    add_overlay_to_many(input_directory, output_directory, overlay_path)
