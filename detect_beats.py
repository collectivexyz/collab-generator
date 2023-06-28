import librosa

def detect_beats(song_path):
    # Load the audio file
    y, sr = librosa.load(song_path)

    # Use Librosa's beat detect function
    # This will return an array of frame numbers that represent beat events
    tempo, beats = librosa.beat.beat_track(y, sr=sr)

    # Convert beat frames to time values (seconds)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    return beat_times

# Usage
song_path = "path_to_your_song.mp3"
beat_times = detect_beats(song_path)

for i, beat_time in enumerate(beat_times):
    print(f"Beat {i+1}: {beat_time} seconds")
