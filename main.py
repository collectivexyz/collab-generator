from extract_action import extract_action_from_many
from strip_audio import strip_audio_from_many
from add_overlay import add_overlay_to_many
from stitch_video import stitch_many

def create_compilation(input_dir, output_dir):

    print("Extracting action...")
    # runs extract_action, saves to some intermediate output dir
    extract_action_from_many(input_dir, 120, output_dir + "/extracted_action")

    print("Stripping audio...")
    # runs strip_audio, saves to some intermediate output dir
    strip_audio_from_many(output_dir + "/extracted_action" , output_dir + "/stripped_audio")

    print("Adding overlay...")
    # runs add_overlay, saves to some intermediate output dir
    add_overlay_to_many(output_dir + "/stripped_audio", output_dir + "/overlayed", "./assets/overlay.png")

    print("Stitching videos...")
    stitch_many(output_dir + "/overlayed", output_dir)
    
if __name__ == "__main__":
    print("CREATING COMPILATION")
    create_compilation("./data", "./output")