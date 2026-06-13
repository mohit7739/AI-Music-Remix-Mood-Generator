import librosa
import numpy as np
from pydub import AudioSegment
import io
import os

def load_audio(file_path_or_bytes):
    """Loads audio file and returns y, sr for librosa processing."""
    y, sr = librosa.load(file_path_or_bytes, sr=None)
    return y, sr

def extract_features(y, sr):
    """Extracts MFCC, Chroma, Spectral Contrast, Tempo, Energy."""
    # 1. MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)

    # 2. Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    # 3. Spectral Contrast
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = np.mean(contrast, axis=1)

    # 4. Tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, np.ndarray):
        tempo = tempo[0]

    # 5. Energy (RMS)
    rms = librosa.feature.rms(y=y)
    energy_mean = np.mean(rms)

    features = {
        'mfcc': mfcc_mean,
        'chroma': chroma_mean,
        'spectral_contrast': contrast_mean,
        'tempo': tempo,
        'energy': energy_mean
    }
    return features

def load_pydub_audio(file_bytes, format="mp3"):
    """Loads audio into pydub AudioSegment."""
    audio = AudioSegment.from_file(io.BytesIO(file_bytes), format=format)
    return audio

def apply_speed_change(audio, speed=1.0):
    """Changes the speed of the audio."""
    # Note: speed_change also changes pitch in pydub easily
    # We can use frame_rate hack for simple speedup
    sound_with_altered_frame_rate = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(audio.frame_rate)

def apply_bass_boost(audio, gain_dB=5):
    """Applies a simple bass boost."""
    # We can do a low shelf filter using pydub's low_pass_filter
    bass = audio.low_pass_filter(150)
    boosted_bass = bass + gain_dB
    return audio.overlay(boosted_bass)

def export_audio(audio, format="mp3"):
    """Exports pydub audio to bytes."""
    buffer = io.BytesIO()
    audio.export(buffer, format=format)
    return buffer.getvalue()
