import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def generate_cansat_vertices(length, diameter, cone_height, cone_angle):
    # Calcular las dimensiones del CanSat
    total_height = length + cone_height

    # Generar los vértices del CanSat
    vertices = np.array([
        # Cuerpo del CanSat
        [-diameter / 2, -diameter / 2, 0],  # Vértice 0
        [diameter / 2, -diameter / 2, 0],   # Vértice 1
        [diameter / 2, diameter / 2, 0],    # Vértice 2
        [-diameter / 2, diameter / 2, 0],   # Vértice 3
        [-diameter / 2, -diameter / 2, length],  # Vértice 4
        [diameter / 2, -diameter / 2, length],   # Vértice 5
        [diameter / 2, diameter / 2, length],    # Vértice 6
        [-diameter / 2, diameter / 2, length],   # Vértice 7

        # Cono del CanSat
        [0, 0, total_height],  # Vértice 8
    ])

    # Calcular las coordenadas del vértice 8 del cono
    cone_height_offset = length + (cone_height / np.tan(np.deg2rad(cone_angle)))
    vertices[8] = [0, 0, cone_height_offset]

    return vertices

# Parámetros del CanSat
length = 4  # Longitud del cuerpo del CanSat
diameter = 4  # Diámetro del cuerpo del CanSat
cone_height = 10  # Altura del cono del CanSat
cone_angle = 30  # Ángulo del cono del CanSat

# Generar los vértices del CanSat
vertices = generate_cansat_vertices(length, diameter, cone_height, cone_angle)

# Crear la figura y los ejes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Definir las caras del CanSat
caras = [
    # Caras del cuerpo del CanSat
    [vertices[0], vertices[1], vertices[2], vertices[3]],
    [vertices[4], vertices[5], vertices[6], vertices[7]],
    [vertices[0], vertices[1], vertices[5], vertices[4]],
    [vertices[1], vertices[2], vertices[6], vertices[5]],
    [vertices[2], vertices[3], vertices[7], vertices[6]],
    [vertices[3], vertices[0], vertices[4], vertices[7]],

    # Caras del cono del CanSat
    [vertices[8], vertices[0], vertices[1]],
    [vertices[8], vertices[1], vertices[2]],
    [vertices[8], vertices[2], vertices[3]],
    [vertices[8], vertices[3], vertices[0]]
]

# Dibujar el CanSat
for cara in caras:
    poly = Poly3DCollection([cara], linewidths=1, edgecolors='black',alpha=0.5 )
    ax.add_collection3d(poly)

#Configurar los límites de los ejes
ax.set_xlim([-diameter, diameter])
ax.set_ylim([-diameter, diameter])
ax.set_zlim([0, vertices[8][2]])

#Etiquetas de los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#Mostrar la gráfica
plt.show()