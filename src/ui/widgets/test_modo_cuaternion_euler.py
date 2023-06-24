import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

class Cube:
    def __init__(self):
        self.vertices = np.array([
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ])
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for edge in self.edges:
            line = np.vstack((self.vertices[edge[0]], self.vertices[edge[1]]))
            ax.plot(line[:, 0], line[:, 1], line[:, 2], 'k')
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        plt.show()

    def rotate(self, method, *args):
        if method == 'euler':
            self.vertices = R.from_euler(*args).apply(self.vertices)
        elif method == 'quaternion':
            self.vertices = R.from_quat(*args).apply(self.vertices)
        else:
            raise ValueError('Invalid rotation method. Choose either \'euler\' or \'quaternion\'.')
        

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CubeFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.cube = Cube()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.draw_cube()

    def draw_cube(self):
        self.ax.cla()
        for edge in self.cube.edges:
            line = np.vstack((self.cube.vertices[edge[0]], self.cube.vertices[edge[1]]))
            self.ax.plot(line[:, 0], line[:, 1], line[:, 2], 'k')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-2, 2])
        self.canvas.draw()

    def rotate_cube(self, method, *args):
        self.cube.rotate(method, *args)
        self.draw_cube()


def rotate_euler():
    app.rotate_cube('euler', 'xyz', [np.pi/4, np.pi/4, np.pi/4])
    root.after(2000, rotate_quaternion)

def rotate_quaternion():
    app.rotate_cube('quaternion', [np.sqrt(2)/2, 0, 0, np.sqrt(2)/2])

if __name__ =="__main__":
    # Crear la aplicación Tkinter
    root = tk.Tk()
    app = CubeFrame(master=root)
    root.after(2000, rotate_euler)
    root.after(2000, rotate_quaternion)
    app.mainloop()
