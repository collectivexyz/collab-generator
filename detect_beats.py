import librosa
import numpy as np

def detect_beats(audio_path):

    y, sr = librosa.load(audio_path)
    # Compute the onset envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Identify the time frames of the onsets/beat frames
    times = librosa.frames_to_time(np.arange(len(onset_env)), sr=sr)

    # Detect the beats
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Get the beat times
    beat_times = times[beats]

    # Compute the mean onset strength for each beat
    beat_strengths = [np.mean(onset_env[beat]) for beat in beats]

    # Combine the beat times and strengths into a single list
    beat_info = list(zip(beat_times, beat_strengths))

    # Sort the beats by strength in descending order
    beat_info.sort(key=lambda x: x[1], reverse=True)

    return beat_info

def detect_shifts(audio_path):
    y, sr = librosa.load(audio_path)

    # Compute a chromagram of the audio signal
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    # Compute the novelty function from the chromagram
    novelty = librosa.onset.onset_strength(sr=sr, S=chroma)

    # Identify the time frames
    times = librosa.frames_to_time(np.arange(len(novelty)), sr=sr)

    # Combine the times and novelty scores into a single list
    shifts = list(zip(times, novelty))

    # Sort the shifts by novelty score in descending order
    shifts.sort(key=lambda x: x[1], reverse=True)

    return shifts


song_path = "./assets/song.mp3"

if __name__ == "__main__":

    # Detect the beats
    beats = detect_beats(song_path)

    # Print the beat times and strengths
    for beat_time, beat_strength in beats:
        print(f"Beat at {beat_time:.2f}s with strength {beat_strength:.2f}")
    
    # Print the times and novelty scores
    for shift_time, novelty_score in shifts:
        print(f"Shift at {shift_time:.2f}s with novelty score {novelty_score:.2f}")