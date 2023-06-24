import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation

# Reutilizar las funciones create_cube y plot_cube del ejemplo anterior
def create_cube(rotation_matrix, translation_vector):
    # Define los vértices del cubo
    vertices = [
                [0, 0, 0],
                [0.1, 0, 0],
                [0.1, 0.1, 0],
                [0, 0.1, 0],
                [0, 0, 0.2],
                [0.1, 0, 0.2],
                [0.1, 0.1, 0.2],
                [0, 0.1, 0.2],]


    # Aplica la rotación y traslación a los vértices
    transformed_vertices = np.dot(vertices, rotation_matrix.T) + translation_vector

    # Define las caras del cubo
    faces = [
        [transformed_vertices[0], transformed_vertices[1], transformed_vertices[5], transformed_vertices[4]],
        [transformed_vertices[7], transformed_vertices[6], transformed_vertices[2], transformed_vertices[3]],
        [transformed_vertices[0], transformed_vertices[4], transformed_vertices[7], transformed_vertices[3]],
        [transformed_vertices[1], transformed_vertices[2], transformed_vertices[6], transformed_vertices[5]],
        [transformed_vertices[0], transformed_vertices[3], transformed_vertices[2], transformed_vertices[1]],
        [transformed_vertices[4], transformed_vertices[5], transformed_vertices[6], transformed_vertices[7]]
    ]

    return faces

def plot_cube(faces):
    # Crear una figura
    fig = plt.figure()

    # Agregar un objeto Axes3D a la figura
    ax = fig.add_subplot(111, projection='3d')

    # Crear una colección de polígonos 3D a partir de las caras del cubo
    face_collection = Poly3DCollection(faces, linewidths=1, edgecolors='k', alpha=0.5)

    # Agregar la colección de polígonos al objeto Axes3D
    ax.add_collection3d(face_collection)

    # Establecer los límites de los ejes
    ax.set_xlim([0, 2])
    ax.set_ylim([0, 2])
    ax.set_zlim([0, 2])

    # Establecer etiquetas para los ejes
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')

    # Mostrar la gráfica
    plt.show()


def update_cube(num, rotation_speed, translation_speed, cube_faces, ax, face_collection):
    # Actualizar la matriz de rotación y el vector de traslación
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(np.radians(rotation_speed * num)), -np.sin(np.radians(rotation_speed * num))],
        [0, np.sin(np.radians(rotation_speed * num)), np.cos(np.radians(rotation_speed * num))]
    ])
    translation_vector = np.array([0.5 + translation_speed * num, 0.5, 0.5])

    # Crear el cubo actualizado
    new_cube_faces = create_cube(rotation_matrix, translation_vector)
    face_collection.set_verts(new_cube_faces)

def animate_cube(rotation_speed, translation_speed, total_frames):
    # Crear una figura
    fig = plt.figure()

    # Agregar un objeto Axes3D a la figura
    ax = fig.add_subplot(111, projection='3d')

    # Establecer los límites de los ejes
    ax.set_xlim([0, 2])
    ax.set_ylim([0, 2])
    ax.set_zlim([0, 2])

    # Establecer etiquetas para los ejes
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')

    # Crear el cubo inicial
    cube_faces = create_cube(np.identity(3), np.array([0.5, 0.5, 0.5]))

    # Crear la animación
    face_collection = Poly3DCollection(cube_faces, facecolors='cyan', linewidths=1, edgecolors='k', alpha=0.5)
    ax.add_collection3d(face_collection)
    ani = animation.FuncAnimation(fig, update_cube, total_frames, fargs=(rotation_speed, translation_speed, cube_faces, ax, face_collection), interval=100, repeat=False)

    # Mostrar la animación
    plt.show()

# Parámetros de la animación
rotation_speed = 5  # Grados por frame
translation_speed = 0.01  # Unidades por frame
total_frames = 100

# Ejecutar la animación
animate_cube(rotation_speed, translation_speed, total_frames)
