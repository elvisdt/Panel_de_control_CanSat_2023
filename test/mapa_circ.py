import numpy as np
import matplotlib.pyplot as plt

# Datos del sistema planetario
planetas = ['P Lan', 'C1', 'C2' ]
distancias = [0, 0.72, 1, ]  # Distancias promedio en UA
tamaños = [0.5, 0.5, 0.5 ]  # Tamaños relativos al de la Tierra (Radio)

# Crear figura y ejes polar
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Configurar el tamaño del gráfico polar
fig.set_size_inches(8, 8)

# Convertir las distancias a ángulos
angulos = np.radians(np.linspace(0, 360, len(planetas) + 1))

# Crear las órbitas
for i in range(len(planetas)):
    ax.plot([0, angulos[i]], [0, distancias[i]], marker='', linewidth=2)

# Mostrar los planetas como puntos
for i in range(len(planetas)):
    ax.scatter(angulos[i], distancias[i], s=tamaños[i] * 100, label=planetas[i])

# Configurar el título del gráfico
#ax.set_title('Sistema Planetario')

# Configurar el aspecto del gráfico polar
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)


# Mostrar las etiquetas de los planetas
for i in range(len(planetas)):
    ax.text(angulos[i], distancias[i] + 0.1, planetas[i], ha='center', va='center')


# Configurar el tamaño de los planetas en la leyenda
legend = ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))

# Ajustar el tamaño de los puntos en la leyenda
for handle in legend.legend_handles:
    handle.set_sizes([20])

# Mostrar el gráfico
plt.show()

