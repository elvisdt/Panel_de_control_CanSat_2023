#%%

import numpy as np
from scipy.signal import iirfilter

# Parámetros del filtro
order = 2  # Orden del filtro biquadrático (2 para un filtro biquadrático)
ftype = 'butter'  # Tipo de filtro (Butterworth en este caso)
cutoff_freq = 0.001  # Frecuencia de corte en Hz
sample_rate = 100  # Tasa de muestreo en Hz

# Diseñar el filtro biquadrático
b, a = iirfilter(order, Wn=cutoff_freq/(sample_rate/2), btype='high', ftype=ftype)
print("-----HP--------")
print("Coeficientes del numerador (b):")
print("{",str(f"{b[0]}, {b[1]}, {b[2]}"),"}")
print("Coeficientes del denominador (a):")
print("{",str(f"{a[0]}, {a[1]}, {a[2]}"),"}")

print()
#%%

import numpy as np
from scipy.signal import iirfilter

# Parámetros del filtro
order = 2  # Orden del filtro biquadrático (2 para un filtro biquadrático)
ftype = 'butter'  # Tipo de filtro (Butterworth en este caso)
cutoff_freq = 5  # Frecuencia de corte en Hz
sample_rate = 100  # Tasa de muestreo en Hz

# Diseñar el filtro biquadrático
b, a = iirfilter(order, Wn=cutoff_freq/(sample_rate/2), btype='low', ftype=ftype)

print("---LP----")

print("Coeficientes del numerador (b):")
print("{",str(f"{b[0]}, {b[1]}, {b[2]}"),"}")
print("Coeficientes del denominador (a):")
print("{",str(f"{a[0]}, {a[1]}, {a[2]}"),"}")

# %%
