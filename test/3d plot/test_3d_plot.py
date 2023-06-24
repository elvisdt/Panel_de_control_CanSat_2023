import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Crear la figura y los ejes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Definir los puntos del cubo
vertices = np.array([ [1, -1, -1], [1, 1, -1],
                      [-1, 1, -1], [-1, -1, -1],
                      [1, -1, 1],  [1, 1, 1],
                      [-1, 1, 1],  [-1, -1, 1]])

# Factor de escala para modificar las dimensiones del cubo (valor flotante)
factor_escala = 1

# Modificar las dimensiones del cubo
#vertices_f = factor_escala *vertices 
vertices_f = vertices / factor_escala

# Definir las caras del cubo
caras = [
    [vertices_f[0], vertices_f[1], vertices_f[2], vertices_f[3]],
    [vertices_f[4], vertices_f[5], vertices_f[6], vertices_f[7]],
    [vertices_f[0], vertices_f[1], vertices_f[5], vertices_f[4]],
    [vertices_f[1], vertices_f[2], vertices_f[6], vertices_f[5]],
    [vertices_f[2], vertices_f[3], vertices_f[7], vertices_f[6]],
    [vertices_f[3], vertices_f[0], vertices_f[4], vertices_f[7]]
]

# Dibujar el cubo
for cara in caras:
    poly = Poly3DCollection([cara], linewidths=1, edgecolors='black', alpha=0.5)
    #poly.set_facecolor('blue')
    ax.add_collection3d(poly)

# Configurar el rango de los ejes
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-3, 3])

# Mostrar el gráfico 3D
plt.show()
