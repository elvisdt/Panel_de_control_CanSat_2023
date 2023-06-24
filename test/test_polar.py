import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def update(frame):
    ax.clear()
    ax.set_title('Radar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Mostrar los planetas como puntos
    for i in range(0, len(frame), 2):
        distancia_1 = frame[i]
        angulo_1 = frame[i + 1]
        distancia_2 = frame[i + 2]
        angulo_2 = frame[i + 3]
        
        ax.scatter(np.radians(angulo_1), distancia_1, s=tamaños[0] * 100, label=planetas[0])
        ax.scatter(np.radians(angulo_2), distancia_2, s=tamaños[1] * 100, label=planetas[1])

    # Mostrar las etiquetas de los planetas
    for i in range(len(planetas)):
        distancia_1 = frame[i * 2]
        angulo_1 = frame[i * 2 + 1]
        distancia_2 = frame[i * 2 + 2]
        angulo_2 = frame[i * 2 + 3]
        
        ax.text(np.radians(angulo_1), distancia_1 + 0.1, planetas[i], ha='center', va='center')

    # Configurar el tamaño de los planetas en la leyenda
    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    for handle in legend.legend_handles:
        handle.set_sizes([20])

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
fig.set_size_inches(8, 8)

# Matriz generada
arr = np.array([[0.19, 2.88073116, 0.19, 2.88],
                [0.27, 1.06334043, 0.32, 1.07],
                [0.61, 3.12141943, 0.66, 3.13],
                [0.16, 4.23646019, 0.21, 4.24],
                [0.98, 1.52392655, 0.03, 1.53],
                [0.79, 1.10816017, 0.84, 1.11],
                [0.96, 2.59738825, 0.01, 2.6],
                [0.39, 0.86964172, 0.44, 0.87],
                [0.57, 5.15657274, 0.62, 5.16],
                [0.71, 2.92436551, 0.76, 2.93]])

valores = arr.flatten()[:10]  # Tomar los primeros 10 valores de arr
planetas = ['Mercurio', 'Venus']
tamaños = [0.5, 0.5]

ani = FuncAnimation(fig, update, frames=valores, interval=1000)
plt.show()