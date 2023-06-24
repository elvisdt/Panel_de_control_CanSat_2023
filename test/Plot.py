import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Supongamos que tus datos son aleatorios para el ejemplo
datos = np.random.rand(10000)

# Creamos la figura y el eje
fig, ax = plt.subplots()

# Inicializamos una línea vacía
linea, = ax.plot([], [])

# Función de inicialización para configurar el gráfico
def init():
    ax.set_ylim(0, 1) # Ajustamos el eje y al rango de tus datos
    return linea,

# Función de animación que se llama en cada frame
def update(i):
    x = list(range(max(0, i-100), i)) # Creamos el rango del eje x
    y = datos[max(0, i-100):i] # Seleccionamos los datos correspondientes
    ax.set_xlim(max(0, i-100), i) # Ajustamos el eje x al rango actual
    linea.set_data(x, y) # Actualizamos los datos de la línea
    return linea,

# Creamos la animación
ani = animation.FuncAnimation(fig, update, frames=range(0, 10000, 100), init_func=init, blit=True,interval=10)

plt.show()
