Low-Bitrate Speech Communication System (DPCM)
## Overview
This project implements a low-bitrate speech communication system using Differential Pulse Code Modulation (DPCM). Our goal is to transmit high-quality voice data over limited bandwidth by reducing data redundancy and utilizing Voice Activity Detection (VAD).

## Project Structure
Organizing code into modules ensures the project is easy to maintain and scale.

Create a folder with  sub-folder: "input", "src" as the following picture here. Then, plug in all the source code provided.
<img width="291" height="481" alt="image" src="https://github.com/user-attachments/assets/f8937d9c-217c-4b74-a061-5972ab4ac3dc" />

## Methodology
The system uses a feedback-loop DPCM architecture to minimize quantization noise.

Preprocessing: Segmenting audio into 20ms frames.

VAD: Skipping "silent" frames to save bandwidth.

Encoding: Calculating the difference between the actual sample and a predicted value.

Quantization: Reducing the bit-depth (e.g., from 16-bit to 4-bit).

Reconstruction: Re-integrating the difference at the receiver side.

## Getting Started
1. Environment Setup
We recommend using a virtual environment (Python 3.8+):
Bash
python -m venv .venv

source .venv/bin/activate  # Mac/Linux

.\.venv\Scripts\activate   # Windows

2. Install Dependencies
Bash
pip install -r requirements.txt
pip install pyaudio sounddevice scipy numpy librosa matplotlib streamlit 

3. Run the Application
Launch the interactive dashboard:

Bash
streamlit run src/app.py
## Evaluation & Metrics
The system is tested against several key performance indicators (KPIs):

Signal-to-Noise Ratio (SNR): Quantifying the clarity of reconstructed audio.

Compression Ratio: Measuring bandwidth savings (Target: 4:1 or 8:1).

Spectrogram Analysis: Visual comparison of frequency loss using librosa.

Latency: Measuring the delay in real-time processing mode.

## Technologies
Processing: numpy, scipy, librosa

Audio I/O: pyaudio, sounddevice

VAD: webrtcvad-wheels

UI: streamlit, matplotlib
