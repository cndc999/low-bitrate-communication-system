## Overview
This project implements a low-bitrate speech communication system using DPCM (Differential Pulse Code Modulation). It includes a modular architecture to handle real-time audio I/O, voice activity detection, and signal reconstruction.

## Features
Speech Encoding (DPCM): High-efficiency compression with a feedback loop to eliminate cumulative errors.

Decoding: Accurate signal reconstruction from quantized bitstreams (2, 4, 6, 8-bit support).

VAD (Voice Activity Detection): Energy-based filtering to optimize bitrate during silent periods.

Real-time Processing: Support for live microphone recording and playback.

Performance Metrics: Built-in SNR (Signal-to-Noise Ratio) calculation for quality assessment.

## How to run
Prepare Environment:
pip install -r requirement.txt

## Execute System:
cd src
python main.py

## Technologies
Python 3.8+
NumPy: 
SoundDevice: 
SciPy


Plaintext
numpy
scipy
sounddevice
numba
