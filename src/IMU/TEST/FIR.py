from scipy.signal import firwin, freqz
import matplotlib.pyplot as plt
import numpy as np


# Parámetros del filtro
Fs = 100    # Frecuencia de muestreo
fc = 5      # Frecuencia de corte
num_taps = 30  # Número de coeficientes del filtro

# Diseño del filtro FIR usando ventana de Kaiser
nyq_rate = Fs / 2.0
cutoff_hz = fc
taps = firwin(num_taps, cutoff_hz/nyq_rate, window=('kaiser', 5.0))

# Visualización de la respuesta en frecuencia del filtro
w, h = freqz(taps, worN=8000)
fig, ax1 = plt.subplots()
ax1.set_title('Filtro pasa-bajos FIR')
ax1.plot((Fs * 0.5 / np.pi) * w, abs(h), 'b')
ax1.set_ylabel('Amplitud [dB]', color='b')
ax1.set_xlabel('Frecuencia [Hz]')
plt.show()

np.savetxt('coeficientes.txt', taps)


#%%

