import webrtcvad
import collections
import contextlib
import wave
import numpy as np
import soundfile as sf

def vad_segment(wav_path, aggressiveness=3):
    vad = webrtcvad.Vad(aggressiveness)
    audio, sample_rate = sf.read(wav_path)
    audio = (audio * 32768).astype(np.int16)
    frame_duration = 30  # ms
    frame_size = int(sample_rate * frame_duration / 1000)
    num_frames = len(audio) // frame_size
    voiced = []
    for i in range(num_frames):
        frame = audio[i * frame_size:(i + 1) * frame_size].tobytes()
        if vad.is_speech(frame, sample_rate):
            voiced.extend(audio[i * frame_size:(i + 1) * frame_size])
    return np.array(voiced)
