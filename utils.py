from pydub import AudioSegment
import random
import os
    
# Load voice files
def load_audio(file_path):
    return AudioSegment.from_file(file_path)

# 1️⃣ Add Silence Around Voice
def add_silence(audio, silence_duration_ms=1000):
    """ Adds silence before and after the audio """
    silence = AudioSegment.silent(duration=silence_duration_ms)
    return silence + audio + silence

# 2️⃣ Overlay One Voice Over Another
def overlay_audio(background_audio, overlay_audio, position_ms=0):
    """
    Overlay `overlay_audio` on `background_audio` starting at `position_ms`
    """
    return background_audio.overlay(overlay_audio, position=position_ms)

# 3️⃣ Reduce Volume in a Segment
def reduce_volume(audio, start_ms, end_ms, reduction_db=10):
    """
    Reduce volume in a specific segment of the audio.
    `start_ms` and `end_ms` define the range.
    `reduction_db` defines how much to reduce (-10 dB means quieter).
    """
    before = audio[:start_ms]
    segment = audio[start_ms:end_ms] - reduction_db
    after = audio[end_ms:]
    return before + segment + after

def fit_random_in_sec(audio, to_sec=6, frame_rate=44100):
    baseline = AudioSegment.silent(duration=to_sec * 1000, frame_rate=frame_rate)
    audio_len = len(audio)
    start_index = random.randint(0, len(baseline) - audio_len)
    output = baseline[:start_index] + audio + baseline[start_index + audio_len :]
    return output

def ensure_exact_samples(audio, target_samples = 6 * 44100, sample_rate=44100):
    """
    Ensures the audio has exactly 'target_samples' by trimming or padding with silence.
    """
    current_samples = len(audio.get_array_of_samples())

    if current_samples < target_samples:
        # Pad with silence
        silence = AudioSegment.silent(duration=(target_samples - current_samples) / sample_rate * 1000)
        audio = audio + silence  # Append silence
    elif current_samples > target_samples:
        # Trim to exact sample count
        audio = audio[:int(target_samples * 1000 // sample_rate)]

    return audio


# Example Usage
if __name__ == "__main__":
    sr = 44100
    offset = 3 * 1000
    segment_length = 6 * 1000
    clean = load_audio('./clean/master.wav').set_frame_rate(sr)
    watermark_0 = load_audio('./watermark/watermark_1.mp3').set_frame_rate(sr)
    watermark_1 = load_audio('./watermark/watermark_2.mp3').set_frame_rate(sr)
    for start in range(0, len(clean), offset):
        watermarks = [fit_random_in_sec(watermark_0), fit_random_in_sec(watermark_1)]
        for idx, watermark in enumerate(watermarks):    
            augmented = overlay_audio(clean[start: start + segment_length], watermark)
            segment_hash = f'start={start//1000},watermark={idx}'
            os.mkdir(f'./dataset/{segment_hash}')
            ensure_exact_samples(augmented).export(f'./dataset/{segment_hash}/mixture.wav', format='wav')
            ensure_exact_samples(watermark).export(f'./dataset/{segment_hash}/watermark.wav', format='wav')
            ensure_exact_samples(clean[start:start+segment_length]).export(f'./dataset/{segment_hash}/background.wav', format='wav')
    