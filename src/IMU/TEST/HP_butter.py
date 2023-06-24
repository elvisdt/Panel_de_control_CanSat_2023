import numpy as np
from scipy.signal import butter, filtfilt

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Parámetros del filtro
cutoff = 1.0  # frecuencia de corte (Hz)
fs = 10.0     # frecuencia de muestreo (Hz)
order = 5     # orden del filtro

# Datos de ejemplo
t = np.linspace(0, 10, 101)
data = np.sin(0.5 * 2 * np.pi * t) + np.sin(2.0 * 2 * np.pi * t)

# Aplicar el filtro
filtered_data = butter_highpass_filter(data, cutoff, fs, order)

# Ahora 'filtered_data' contiene los datos filtrados con el filtro pasa altas Butterworth

#%%




