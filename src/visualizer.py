import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

def plot_combined_analysis(original, reconstructed, fs):
    """Plotting Diagram[cite: 43, 70]."""
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    
    # Waveform - Tín hiệu gốc
    librosa.display.waveshow(original, sr=fs, ax=ax[0, 0], color='blue')
    ax[0, 0].set_title("Original Waveform")
    
    # Waveform - Tín hiệu sau nén
    librosa.display.waveshow(reconstructed, sr=fs, ax=ax[0, 1], color='orange')
    ax[0, 1].set_title("Reconstructed Waveform")
    
    # Spectrogram - Tín hiệu gốc
    D_orig = librosa.amplitude_to_db(np.abs(librosa.stft(original)), ref=np.max)
    librosa.display.specshow(D_orig, sr=fs, x_axis='time', y_axis='hz', ax=ax[1, 0])
    ax[1, 0].set_title("Original Spectrogram")
    
    # Spectrogram - Tín hiệu sau nén
    D_recon = librosa.amplitude_to_db(np.abs(librosa.stft(reconstructed)), ref=np.max)
    librosa.display.specshow(D_recon, sr=fs, x_axis='time', y_axis='hz', ax=ax[1, 1])
    ax[1, 1].set_title("Reconstructed Spectrogram")
    
    plt.tight_layout()
    return fig