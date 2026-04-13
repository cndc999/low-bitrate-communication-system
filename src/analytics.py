import numpy as np
import time

def calculate_snr(original, reconstructed):
    """Calculating SNR"""
    min_len = min(len(original), len(reconstructed))
    original = original[:min_len]
    reconstructed = reconstructed[:min_len]
    
    noise = original - reconstructed
    signal_power = np.mean(original**2)
    noise_power = np.mean(noise**2)
    
    if noise_power == 0: return float('inf')
    return 10 * np.log10(signal_power / (noise_power + 1e-10))

def calculate_compression_ratio(original_bits, target_bits):
    """Calculating compression rate"""
    return original_bits / target_bits if target_bits > 0 else 0

def get_quality_label(snr):
    """Đánh giá chất lượng cảm tính."""
    if snr > 15: return "Good"
    if snr > 5: return "Average"
    return "Bad"