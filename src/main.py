import os
import time
import numpy as np
import sounddevice as sd
from audio_io import record_audio, load_audio, save_audio
from codec_engine import DPCMCodec
from vad_handler import apply_vad

BITRATES = [2, 4, 6, 8]

def calculate_snr(original, processed):
    noise = original - processed[:len(original)]
    signal_power = np.mean(original**2)
    noise_power = np.mean(noise**2)
    return 10 * np.log10(signal_power / (noise_power + 1e-10))

def main():
    os.makedirs("../input", exist_ok=True)
    os.makedirs("../output", exist_ok=True)

    print("1: Recording | 2: Load sample.wav")
    choice = input("Select: ")

    if choice == "1":
        audio, fs = record_audio()
    else:
        audio, fs = load_audio("../input/sample.wav")
        if audio is None:
            print("File not found! Recording instead...")
            audio, fs = record_audio()

    # Chuẩn hóa chung
    audio = audio / (np.max(np.abs(audio)) + 1e-9)
    original_clean = audio.copy()

    if input("Use VAD? (y/n): ").lower() == 'y':
        audio = apply_vad(audio)

    codec = DPCMCodec(step_size=0.01)
    results = []

    for bits in BITRATES:
        print(f"\n--- Testing {bits}-bit ---")
        
        # Benchmarking
        t0 = time.time()
        encoded = codec.encode(audio, bits)
        t1 = time.time()
        decoded = codec.decode(encoded)
        t2 = time.time()

        snr = calculate_snr(original_clean, decoded)
        save_audio(f"../output/reconstructed_{bits}bit.wav", decoded, fs)
        
        print(f"SNR: {snr:.2f} dB | Enc: {(t1-t0)*1000:.1f}ms")
        results.append((bits, snr))

    print("\n" + "="*20 + "\nFINAL REPORT\n" + "="*20)
    for b, s in results:
        status = "Good" if s > 15 else "Bad"
        print(f"{b}-bit: {s:.2f} dB ({status})")

if __name__ == "__main__":
    main()