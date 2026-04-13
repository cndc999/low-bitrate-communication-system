import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read, write

def record_audio(duration=3, fs=16000):
    print(f"\n--- Đang ghi âm trong {duration} giây... ---")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Ghi âm xong.")
    return audio.flatten(), fs

def load_audio(path):
    try:
        fs, audio = read(path)
        audio = audio.astype(np.float32)
        # Chuyển Mono nếu là Stereo
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        # Chuẩn hóa về dải [-1, 1]
        if np.max(np.abs(audio)) > 1.0:
            audio /= 32768.0
        return audio, fs
    except FileNotFoundError:
        return None, None

def save_audio(filename, audio, fs):
    # Đảm bảo dữ liệu không bị vượt ngưỡng trước khi ép kiểu int16
    out_audio = np.clip(audio, -1.0, 1.0)
    out_audio_int16 = (out_audio * 32767).astype(np.int16)
    write(filename, fs, out_audio_int16)