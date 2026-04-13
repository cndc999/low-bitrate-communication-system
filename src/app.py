import streamlit as st
import numpy as np
import scipy.io.wavfile as wav
import time

# Nguyen Le Quang Anh
from codec_engine import dpcm_encode,dpcm_decode
from vad_handler import apply_vad 
from audio_io import record_audio  # If you are using your microphone 

# Nguyen Dang Anh Dung

from analytics import calculate_snr, calculate_compression_ratio, get_quality_label
from visualizer import plot_combined_analysis

def mock_process(audio, bits):
    levels = 2**bits
    return np.round(audio * (levels/2)) / (levels/2)

# Design
st.set_page_config(page_title="DPCM Speech System", layout="wide", initial_sidebar_state="expanded")

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR  ---
with st.sidebar:
    st.title("Settings")
    st.info("Assignment 1: Developing a Low-Bitrate Speech Communication System\n\nMember: Nguyen Le Quang Anh & Nguyen Dang Anh Dung")
    
    st.divider()
    bit_depth = st.select_slider(" Target Bitrate", options=[2, 4, 6, 8], value=4, help="Số bit càng cao chất lượng càng tốt")
    use_vad = st.toggle(" VAD Optimization", value=True)
    
    st.divider()
    st.warning("Note: DPCM uses predictive coding to reduce redundancy.")

# --- MAIN CONTENT ---
st.title("Low-Bitrate Speech Communication System")
st.markdown("---")

# Bước 1: Selecting for test (input or recording)
st.subheader("Step 1: Input Source")
col_up, col_rec = st.columns(2)

with col_up:
    uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

with col_rec:
    st.write("Or use your microphone:")
    if st.button("Start Recording"):
        with st.spinner("Recording..."):
            audio_data, fs_rec = record_audio(duration=10)
            # Lưu vào session_state để không bị mất khi chỉnh slider
            st.session_state['audio'] = audio_data
            st.session_state['fs'] = fs_rec
            st.success("Recording finished!")

# Xử lý logic chọn nguồn dữ liệu
audio_to_process = None
fs = 16000

if uploaded_file:
    fs, audio_to_process = wav.read(uploaded_file)
    if audio_to_process.dtype == np.int16: audio_to_process = audio_to_process / 32768.0
    if len(audio_to_process.shape) > 1: audio_to_process = np.mean(audio_to_process, axis=1)
elif 'audio' in st.session_state:
    audio_to_process = st.session_state['audio']
    fs = st.session_state['fs']

# Processing and Display
if audio_to_process is not None:
    # Chuẩn hóa biên độ tín hiệu
    audio_to_process = audio_to_process / (np.max(np.abs(audio_to_process)) + 1e-9)
    
    # 1. VAD (If selected)
    processed_input = apply_vad(audio_to_process) if use_vad else audio_to_process
    
    # 2. DPCM Compression 
    start_time = time.time()
    encoded, step = dpcm_encode(processed_input, bit_depth)
    reconstructed = dpcm_decode(encoded, step)
    latency = (time.time() - start_time) * 1000

    # 3. Display on Dashboard
    tab1, tab2 = st.tabs(["Performance Dashboard", "Technical Analysis"])
    
    with tab1:
        snr_val = calculate_snr(audio_to_process, reconstructed)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SNR", f"{snr_val:.2f} dB")
        c2.metric("Ratio", f"{calculate_compression_ratio(16, bit_depth):.1f}:1")
        c3.metric("Latency", f"{latency:.2f} ms")
        c4.metric("Quality", get_quality_label(snr_val))

        st.divider()
        p1, p2 = st.columns(2)
        p1.write("**Original Audio**")
        p1.audio(audio_to_process, sample_rate=fs)
        p2.write(f"**Compressed ({bit_depth}-bit)**")
        p2.audio(reconstructed, sample_rate=fs)

    with tab2:
        st.pyplot(plot_combined_analysis(audio_to_process, reconstructed, fs))
else:
    st.info("Please upload a file or click record to start.")