import torchaudio
import torchaudio.transforms as T
import torch
import random
import base64
import io

def load_audio(file_path, target_sr=16000):
    waveform, sample_rate = torchaudio.load(file_path)
    if sample_rate != target_sr:
        resampler = T.Resample(orig_freq=sample_rate, new_freq=target_sr)
        waveform = resampler(waveform)
    return waveform, target_sr

def audio_to_base64(waveform, sample_rate=16000):
    # Ensure waveform is 2D and float32
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)
    waveform = waveform.float()

    # Save waveform to an in-memory bytes buffer
    buffer = io.BytesIO()
    torchaudio.save(buffer, waveform, sample_rate=sample_rate, format="wav")
    
    # Convert buffer to base64
    buffer.seek(0)
    audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return audio_base64

def compress(audio_file, threshold=-20, ratio=4):
    """Dynamic Range Compression: Reduces the volume of loud sounds."""
    waveform, sample_rate = load_audio(audio_file)

    # Convert threshold from dB to linear scale
    threshold_linear = 10 ** (threshold / 20)

    # Create a copy of the waveform for output
    compressed_waveform = waveform.clone()

    # Apply compression
    # Calculate the gain reduction for signals above the threshold
    gain_reduction = torch.where(compressed_waveform > threshold_linear,
                                 (threshold_linear + (compressed_waveform - threshold_linear) / ratio),
                                 compressed_waveform)

    # Ensure that the output does not exceed 1.0
    compressed_waveform = gain_reduction / torch.max(gain_reduction.abs())

    return audio_to_base64(compressed_waveform, sample_rate)

# Resampling
def resample(audio_file, target_sr=16000):
    """Resampling: Standardizes the sample rate across files."""
    waveform, sample_rate = load_audio(audio_file, target_sr)
    return audio_to_base64(waveform, sample_rate)

# Normalization
def normalize(audio_file):
    """ Normalization: Adjusts the amplitude to avoid clipping or extreme values."""
    waveform, sample_rate = load_audio(audio_file)
    
    # Normalize by the maximum absolute value
    normalized_waveform = waveform / waveform.abs().max()
    return audio_to_base64(normalized_waveform, sample_rate)

# Trimming Silence
def trim_silence(audio_file, top_db=20):
    """Trimming Silence: Removes silence from the start and end."""
    waveform, sample_rate = load_audio(audio_file)
    
    # Down-mix to mono if stereo
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Use Voice Activity Detection (VAD) to trim silence
    trimmed_waveform = T.Vad(sample_rate=sample_rate)(waveform)
    
    return audio_to_base64(trimmed_waveform, sample_rate)
