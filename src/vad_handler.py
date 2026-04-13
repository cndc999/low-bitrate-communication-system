import numpy as np

def apply_vad(audio, frame_size=256, threshold=0.0005):
    """Voice Activity Detection dựa trên năng lượng khung."""
    output = []
    # Vector hóa một phần để tăng tốc
    for i in range(0, len(audio), frame_size):
        frame = audio[i:i+frame_size]
        if len(frame) == 0: continue
        
        energy = np.mean(frame ** 2)
        if energy > threshold:
            output.extend(frame)
        else:
            output.extend(np.zeros(len(frame)))
            
    return np.array(output, dtype=np.float32)