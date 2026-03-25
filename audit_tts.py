import numpy as np
from scipy import signal

# TTS Theory Constants
ALPHA_TTS = 0.0146  # Friction constant in s/Mpc
VACUUM_LIMIT = 1e120  # Omega: Fabric rupture threshold in Hz

def clean_maintenance_noise(raw_strain_data, sampling_rate=4096):
    """
    Removes terrestrial interference and maintenance noise from LIGO/Virgo raw data.
    Designed to preserve the high-frequency 'Snap' signature of the TTS fabric.
    """
    # 1. Notch Filter: Remove 60Hz power line noise and its harmonics
    for freq in [60, 120, 180]:
        quality_factor = 30.0
        b, a = signal.iirnotch(freq, quality_factor, sampling_rate)
        raw_strain_data = signal.filtfilt(b, a, raw_strain_data)
    
    # 2. High-Pass Filter: Eliminate human/mechanical vibrations (< 15Hz)
    # This keeps the 'Snap' (Dirac impulse) while removing maintenance activity
    b_hp, a_hp = signal.butter(4, 15, 'highpass', fs=sampling_rate)
    clean_data = signal.filtfilt(b_hp, a_hp, raw_strain_data)
    
    return clean_data

def predict_friction_delay(distance_mpc):
    """
    Calculates the expected radio delay (Delta_t) based on TTS friction.
    Formula: Delta_t = alpha_TTS * Distance
    """
    return ALPHA_TTS * distance_mpc

# Target: FRB 20180916B
# Distance: 149 Mpc
# Expected Delay: ~2.18s
