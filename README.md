# ezwav

A minimal, user focused Python library for analyzing WAV audio files.

## Features

- Load WAV files
- Inspect audio properties (duration, sample rate, channels)
- Split and normalize audio channels
- Generate amplitude lists
- Easily gather volume data

## Install
_(Once released on PyPi)_
```bash
pip install ezwav
```

## Usage
```python
from ezwav import Wav

mywav = Wav("example.wav")      # Create Wav object
print(mywav.duration)           # Print audio length in seconds
mywav.init_amplitude_list('s')  # Initialize list of peak amplitude each second
print(mywav.amplitude_list)     # Print amplitude list
```

More features and documentation coming soon.