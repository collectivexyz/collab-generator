import os
from moviepy.editor import VideoFileClip

def strip_audio_from_many(input_dir, output_dir):
    # Get a list of all files in the directory
    files = os.listdir(input_dir)
    
    # Filter out non-video files
    video_files = [f for f in files if f.endswith(('.mp4', '.flv', '.mkv', '.webm', '.avi'))]
    
    for video_file in video_files:
        # Create the full input file path
        input_file_path = os.path.join(input_dir, video_file)
        
        # Create VideoFileClip object
        video = VideoFileClip(input_file_path)
        
        # Remove audio
        video = video.without_audio()
        
        # Create the full output file path, even if it doesnt exist
        output_file_path = os.path.join(output_dir, video_file)
        
        # Write the result to a file
        video.write_videofile(output_file_path)

input_directory = "./data"
output_directory = "./output/stripped_audio"

if __name__ == "__main__":
    strip_audio_from_many(input_directory, output_directory)
