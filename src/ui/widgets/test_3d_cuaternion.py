import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R
from matplotlib.animation import FuncAnimation

# Define the eight corners of the cube
cube_definition = [
    [-0.5, -0.5, -0.5],
    [-0.5, -0.5, 0.5],
    [-0.5, 0.5, -0.5],
    [-0.5, 0.5, 0.5],
    [0.5, -0.5, -0.5],
    [0.5, -0.5, 0.5],
    [0.5, 0.5, -0.5],
    [0.5, 0.5, 0.5]
]

fig = plt.figure()

# Initial rotation quaternion
rotation_quaternion = [0, 0, 0, 1]  # [x, y, z, w]

def update(num):
    plt.clf()  # clear the current figure
    ax = fig.add_subplot(111, projection='3d')  # add a new set of 3d axes
    # Here you would update the rotation_quaternion with data from your sensor
    rotation_quaternion = [np.sin(num/10), np.sin(num/10), np.sin(num/10), np.cos(num/10)]
    rotation = R.from_quat(rotation_quaternion)
    cube_definition_array = [
        rotation.apply(point) for point in cube_definition
    ]
    Z = np.array(cube_definition_array)
    verts = [[Z[0],Z[1],Z[5],Z[4]], [Z[7],Z[6],Z[2],Z[3]], [Z[0],Z[1],Z[3],Z[2]], 
             [Z[7],Z[6],Z[4],Z[5]], [Z[7],Z[3],Z[1],Z[5]], [Z[0],Z[2],Z[6],Z[4]]]
    collection = Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25)
    ax.add_collection3d(collection)
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])

ani = FuncAnimation(fig, update, frames=range(100), interval=100)
plt.show()
