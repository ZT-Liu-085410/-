import numpy as np
from scipy.fftpack import dct
from scipy.signal import get_window

def hz_to_mel(hz):
    return 2595 * np.log10(1 + hz / 700.0)

def mel_to_hz(mel):
    return 700 * (10**(mel / 2595.0) - 1)

def get_mel_filterbank(num_filters=26, fft_size=512, sample_rate=16000, low_freq=0, high_freq=None):
    if high_freq is None:
        high_freq = sample_rate / 2
    low_mel = hz_to_mel(low_freq)
    high_mel = hz_to_mel(high_freq)
    mel_points = np.linspace(low_mel, high_mel, num_filters + 2)
    hz_points = mel_to_hz(mel_points)
    bin = np.floor((fft_size + 1) * hz_points / sample_rate).astype(int)

    fbank = np.zeros((num_filters, int(fft_size // 2 + 1)))
    for j in range(1, num_filters + 1):
        for i in range(bin[j - 1], bin[j]):
            fbank[j - 1, i] = (i - bin[j - 1]) / (bin[j] - bin[j - 1])
        for i in range(bin[j], bin[j + 1]):
            fbank[j - 1, i] = (bin[j + 1] - i) / (bin[j + 1] - bin[j])
    return fbank

def compute_mfcc(frames, sample_rate, fft_size=512, num_filters=26, num_ceps=13):
    # 1. FFT
    mag_frames = np.absolute(np.fft.rfft(frames, n=fft_size))  # shape: (num_frames, fft_size//2+1)
    pow_frames = (1.0 / fft_size) * (mag_frames ** 2)          # 功率谱

    # 2. Mel Filterbank
    mel_filters = get_mel_filterbank(num_filters=num_filters, fft_size=fft_size, sample_rate=sample_rate)
    mel_energy = np.dot(pow_frames, mel_filters.T)             # shape: (num_frames, num_filters)
    mel_energy = np.where(mel_energy == 0, np.finfo(float).eps, mel_energy)  # 避免 log(0)

    # 3. Log
    log_mel_energy = np.log(mel_energy)

    # 4. DCT
    mfcc = dct(log_mel_energy, type=2, axis=1, norm='ortho')[:, :num_ceps]
    return mfcc
