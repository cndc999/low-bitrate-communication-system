import numpy as np

def dpcm_encode(signal, bits, step_size=0.01):
    n = len(signal)
    encoded = np.zeros(n, dtype=np.float32)

    levels = 2 ** bits
    limit = levels // 2

    predicted = 0.0
    step = step_size

    for i in range(n):
        diff = signal[i] - predicted
        q = np.round(diff / step)
        q = np.clip(q, -limit, limit - 1)

        encoded[i] = q
        predicted += q * step

    return encoded, step


def dpcm_decode(q_signal, step):
    n = len(q_signal)
    decoded = np.zeros(n, dtype=np.float32)

    predicted = 0.0

    for i in range(n):
        predicted += q_signal[i] * step
        decoded[i] = predicted

    return decoded