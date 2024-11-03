import torchaudio
import torchaudio.transforms as T
import torch
import random
import base64
import io
from io import BytesIO
import soundfile as sf
import numpy as np

def load_audio(file_path):
    waveform, sr = torchaudio.load(file_path)
    return waveform, sr

def audio_to_base64(waveform, sample_rate=16000):
    # Detach if the tensor requires grad
    if isinstance(waveform, torch.Tensor):
        waveform = waveform.detach().squeeze().numpy()

    if waveform.ndim == 1:
        waveform = np.expand_dims(waveform, axis=0)

    waveform = waveform.astype(np.float32)

    buffer = BytesIO()
    sf.write(buffer, waveform.T, sample_rate, format="WAV")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

# Time Stretching with Stereo to Mono Down-mixing
def time_stretch(audio_file, rate=1.2):
    waveform, sample_rate = load_audio(audio_file)
    
    # Down-mix to mono if stereo
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Convert waveform to spectrogram
    spectrogram_transform = T.Spectrogram(n_fft=400)  # Adjust `n_fft` as needed
    spectrogram = spectrogram_transform(waveform)

    # Apply time stretching to the magnitude of the spectrogram
    stretch_transform = T.TimeStretch()
    stretched_spec = stretch_transform(spectrogram, rate)
    
    # Use only the magnitude (real-valued) part of the stretched spectrogram for Griffin-Lim
    stretched_spec_magnitude = stretched_spec.abs()

    # Convert the stretched magnitude spectrogram back to waveform
    griffin_lim = T.GriffinLim(n_fft=spectrogram_transform.n_fft)
    stretched_waveform = griffin_lim(stretched_spec_magnitude)

    return audio_to_base64(stretched_waveform, sample_rate)

# Pitch Shifting with Stereo to Mono Down-mixing
def pitch_shift(audio_file, n_steps=2):
    waveform, sample_rate = load_audio(audio_file)

    # Down-mix to mono if stereo
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    pitch_transform = T.PitchShift(sample_rate=sample_rate, n_steps=n_steps)
    shifted_waveform = pitch_transform(waveform)

    return audio_to_base64(shifted_waveform, sample_rate)

# Adding Random Noise
def add_noise(audio_file, noise_factor=0.005):
    waveform, sample_rate = load_audio(audio_file)
    noise = noise_factor * torch.randn_like(waveform)
    noisy_waveform = waveform + noise
    return audio_to_base64(noisy_waveform, sample_rate)

# Random Volume Adjustment
def random_volume_adjustment(audio_file, factor_range=(0.5, 1.5)):
    waveform, sample_rate = load_audio(audio_file)
    factor = random.uniform(*factor_range)
    adjusted_waveform = waveform * factor
    return audio_to_base64(adjusted_waveform, sample_rate)

# Time Shifting
def time_shift(audio_file, shift_limit=0.2):
    waveform, sample_rate = load_audio(audio_file)
    shift_amt = int(waveform.size(1) * shift_limit)
    shift = random.randint(-shift_amt, shift_amt)
    shifted_waveform = torch.roll(waveform, shifts=shift, dims=1)
    return audio_to_base64(shifted_waveform, sample_rate)
