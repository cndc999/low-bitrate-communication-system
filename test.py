import numpy as np
import sounddevice as sd
import time
import os
from scipy.io.wavfile import read, write

# Cấu hình các mức bit cần test
BITRATES = [2, 4, 6, 8]

def dpcm_encode(signal, bits):
    """
    DPCM Encoder: Sử dụng vòng lặp phản hồi (Feedback Loop) 
    để triệt tiêu sai số tích lũy.
    """
    n = len(signal)
    encoded = np.zeros(n, dtype=np.float32)
    levels = 2 ** bits
    
    # step_size quyết định độ phân giải của sự thay đổi
    # 0.05 là mức cân bằng tốt cho tín hiệu đã chuẩn hóa [-1, 1]
    step_size = 0.01  
    
    predicted = 0.0
    for i in range(n):
        diff = signal[i] - predicted
        
        # Lượng tử hóa sai số và ép kiểu về float đơn lẻ để tránh lỗi sequence
        q = float(np.round(diff / step_size))
        q = float(np.clip(q, -levels/2, levels/2 - 1))
        
        encoded[i] = q
        
        # Cập nhật bộ dự đoán cho mẫu kế tiếp
        dq = q * step_size
        predicted = predicted + dq 
        
    return encoded, step_size

def dpcm_decode(q_signal, step_size):
    """
    DPCM Decoder: Tích lũy lại các sai số đã lượng tử hóa.
    """
    n = len(q_signal)
    decoded = np.zeros(n, dtype=np.float32)
    
    current = 0.0
    for i in range(n):
        dq = q_signal[i] * step_size
        current += dq
        decoded[i] = current
        
    return decoded

def apply_vad(audio, frame_size=256, threshold=0.0005):
    """
    Voice Activity Detection đơn giản dựa trên năng lượng khung.
    """
    output = []
    for i in range(0, len(audio), frame_size):
        frame = audio[i:i+frame_size]
        energy = np.mean(frame ** 2) if len(frame) > 0 else 0
        if energy > threshold:
            output.extend(frame)
        else:
            output.extend([0] * len(frame))
    return np.array(output, dtype=np.float32)

def record_audio(duration=3, fs=16000):
    print(f"\n--- Đang ghi âm trong {duration} giây... ---")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Ghi âm xong.")
    return audio.flatten(), fs

def main():
    # Tạo thư mục lưu trữ nếu chưa có
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("1: Recording from Microphone")
    print("2: Load file from input/sample.wav")
    choice_input = input("Select input: ")

    if choice_input == "1":
        audio, fs = record_audio()
    else:
        try:
            fs, audio = read("input/sample.wav")
            audio = audio.astype(np.float32)
            # Nếu là file Stereo (2 kênh), chuyển về Mono
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)
            # Chuẩn hóa nếu dữ liệu là int16
            if np.max(np.abs(audio)) > 1.0:
                audio /= 32768.0
        except FileNotFoundError:
            print("File not found! Switch to recording.")
            audio, fs = record_audio()

    # Chuẩn hóa biên độ về [-1, 1] để thuật toán chạy ổn định
    audio = audio / (np.max(np.abs(audio)) + 1e-9)
    original = audio.copy()

    choice_vad = input("Using VAD (1: OFF, 2: ON): ")
    if choice_vad == "2":
        print("VAD: ON")
        audio = apply_vad(audio)

    results = []

    for bits in BITRATES:
        print(f"\nProcessing: {bits}-bit DPCM...")

        # Encode
        start_enc = time.time()
        encoded, step = dpcm_encode(audio, bits)
        enc_time = time.time() - start_enc

        # Decode
        start_dec = time.time()
        decoded = dpcm_decode(encoded, step)
        dec_time = time.time() - start_dec

        # Tính toán SNR (Tỷ số tín hiệu trên nhiễu)
        noise = original - decoded[:len(original)]
        signal_power = np.mean(original**2)
        noise_power = np.mean(noise**2)
        snr = 10 * np.log10(signal_power / (noise_power + 1e-10))

        # Giới hạn biên độ và chuyển về định dạng wav chuẩn (int16)
        out_audio = np.clip(decoded, -1.0, 1.0)
        out_audio_int16 = (out_audio * 32767).astype(np.int16)

        # Lưu kết quả
        filename = f"output/reconstructed_{bits}bit.wav"
        write(filename, fs, out_audio_int16)
        
        print(f" > SNR: {snr:.2f} dB")
        print(f" > Enc/Dec Time: {enc_time*1000:.1f}ms / {dec_time*1000:.1f}ms")
        
        # Phát thử âm thanh
        print(f" > Playing {bits}-bit...")
        sd.play(out_audio_int16, fs)
        sd.wait()

        results.append((bits, snr))

    # Tổng kết
    print("\n" + "="*20)
    print("      Conclusion")
    print("="*20)
    for bits, snr in results:
        status = "Tốt" if snr > 15 else "Average"
        if snr < 5: status = "Bad"
        print(f"{bits}-bit: SNR = {snr:.2f} dB ({status})")

if __name__ == "__main__":
    main()