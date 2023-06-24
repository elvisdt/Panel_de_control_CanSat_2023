import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Parámetros del cilindro
radius = 0.2
height = 0.4
resolution = 10

# Generar los puntos en el cilindro
theta = np.linspace(0, 2 * np.pi, resolution)
z = np.linspace(0, height, resolution)
theta, z = np.meshgrid(theta, z)
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Crear la figura y los ejes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Dibujar la superficie lateral del cilindro
ax.plot_surface(x, y, z, alpha=0.5)

# Obtener los puntos de la cara superior e inferior del cilindro
top_points = np.stack([x[0], y[0], z[0]], axis=-1)
bottom_points = np.stack([x[-1], y[-1], z[-1]], axis=-1)

# Crear las caras superior e inferior del cilindro
top_face = Poly3DCollection([top_points])
bottom_face = Poly3DCollection([bottom_points])

# Configurar los colores y la transparencia de las caras
#top_face.set_facecolor('blue')
top_face.set_alpha(0.5)
#bottom_face.set_facecolor('blue')
bottom_face.set_alpha(0.5)

# Agregar las caras a los ejes
ax.add_collection3d(top_face)
ax.add_collection3d(bottom_face)

# Configurar los límites de los ejes
# ax.set_xlim(-radius, radius)
# ax.set_ylim(-radius, radius)
# ax.set_zlim(0, height)

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-0.2, 0.5)


# Etiquetas de los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Mostrar la gráfica
plt.show()

