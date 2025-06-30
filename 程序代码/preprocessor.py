import numpy as np

def pre_emphasis(signal, coeff=0.97):
    return np.append(signal[0], signal[1:] - coeff * signal[:-1])

def frame_signal(signal, sample_rate, frame_size=0.025, frame_stride=0.01):
    frame_length = int(frame_size * sample_rate)
    frame_step = int(frame_stride * sample_rate)
    signal_length = len(signal)
    num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step))
    pad_signal_length = num_frames * frame_step + frame_length
    pad_signal = np.append(signal, np.zeros((pad_signal_length - signal_length)))
    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + \
              np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    return frames

def hamming_window(frames):
    return frames * np.hamming(frames.shape[1])

def preprocess(signal, sample_rate):
    emphasized = pre_emphasis(signal)
    frames = frame_signal(emphasized, sample_rate)
    windowed = hamming_window(frames)
    return windowed
