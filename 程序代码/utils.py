import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import soundfile as sf
import os

def plot_multiple_waveforms(wav_paths, labels, save_path):
    plt.figure(figsize=(12, 3 * len(wav_paths)))
    for i, (wav_path, label) in enumerate(zip(wav_paths, labels), 1):
        y, sr = sf.read(wav_path)
        plt.subplot(len(wav_paths), 1, i)
        plt.title(f"Waveform - {label}")
        librosa.display.waveshow(y, sr=sr)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_multiple_spectrograms(wav_paths, labels, save_path):
    plt.figure(figsize=(12, 3 * len(wav_paths)))
    for i, (wav_path, label) in enumerate(zip(wav_paths, labels), 1):
        y, sr = sf.read(wav_path)
        plt.subplot(len(wav_paths), 1, i)
        plt.title(f"Spectrogram - {label}")
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz')
        plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
