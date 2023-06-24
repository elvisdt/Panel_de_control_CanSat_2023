
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

import time
import numpy as np

class Cube:
    def __init__(self):
        self.vertices = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                                  [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1, 1]],
                                  dtype=np.float64)
        
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                      (4, 5), (5, 6), (6, 7), (7, 4),
                      (0, 4), (1, 5), (2, 6), (3, 7)]
        
        self.faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
                      (2, 3, 7, 6), (0, 4, 7, 3), (1, 2, 6, 5)]
        
        self.face_colors = ['red', 'green', 'blue', 'yellow', 'white', 'orange']
       
    def rotate(self, method, *args):
        if method == 'euler':
            self.vertices = R.from_euler(*args).apply(self.vertices)
        elif method == 'quaternion':
            self.vertices = R.from_quat(*args).apply(self.vertices)
            #orden de argumentos del cuaterion (x, y, z, w)
        else:
            raise ValueError('Invalid rotation method. Choose either \'euler\' or \'quaternion\'.')
    
    def scale(self, factor):
        """Escala el cubo por un factor dado respecto al centro del cubo."""
        center = self.vertices.mean(axis=0)
        self.vertices -= center  # trasladar al origen
        self.vertices *= factor  # escalar
        self.vertices += center  # trasladar de vuelta

    def translate(self, vector):
        """Traslada el cubo por un vector dado."""
        self.vertices += vector

    def draw_faces(self, ax):
        """Dibuja las caras del cubo."""
        faces = [[self.vertices[i] for i in face] for face in self.faces]
        face_collection = Poly3DCollection(faces, facecolors=self.face_colors, alpha=.8, linewidths=.5, edgecolors='w')
        ax.add_collection3d(face_collection)

    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        self.draw_faces(ax)
        for edge in self.edges:
            line = np.vstack((self.vertices[edge[0]], self.vertices[edge[1]]))
            ax.plot(line[:, 0], line[:, 1], line[:, 2], 'k')
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        plt.show()


import customtkinter as ctk
import tkinter as tk

#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CubeFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.fig_title = {'title':"titulo de figura",'fontsize':11, 'fontweight':"normal", 'color':"#F39C12"}
        self.create_widgets()
        # modo de apariencia
        self.set_mode(ctk.get_appearance_mode())

    def create_widgets(self):
        self.cube = Cube()
        self.cube.scale(0.7)

        self.fig = plt.figure(dpi=100)
        self.fig.subplots_adjust(left=0.05, bottom=0.05)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        # configuracion
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect("resize_event", self.on_resize)
        self.draw_cube()

    def on_resize(self, event):
        self.fig.tight_layout()

    def draw_cube(self):
        self.ax.cla()
        #self.cube.draw_faces(self.ax)

        #dibujar aristas del cubo
        for edge in self.cube.edges:
            line = np.vstack((self.cube.vertices[edge[0]], self.cube.vertices[edge[1]]))
            self.ax.plot(line[:, 0], line[:, 1], line[:, 2], 'k')
        
        #------------- personalizacion----
        self.ax.set_title(self.fig_title['title'],
                          fontsize=self.fig_title['fontsize'], 
                          fontweight=self.fig_title['fontweight'],
                          color=self.fig_title['color'])
        
        # ajustar llos limites
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-2, 2])

        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])
        self.ax.zaxis.set_ticks([])

        self.ax.xaxis.set_ticks([0])
        self.ax.yaxis.set_ticks([0])
        self.ax.zaxis.set_ticks([0])

        self.ax.xaxis.set_ticklabels(['x'])
        self.ax.yaxis.set_ticklabels(['y'])
        self.ax.zaxis.set_ticklabels(['z'])


        # Dibujar nuevamente la figura en el canvas
        self.canvas.draw()

    


    def rotate_cube(self, method, *args):
        self.rotation_angles = args  # Almacenar los ángulos de rotación
        self.cube.rotate(method, *args)
        self.draw_cube()

    def set_title(self, title, fontsize=11, fontweight="normal", color="#F39C12"):
        self.fig_title['title'] = title
        self.fig_title['fontsize'] = fontsize
        self.fig_title['fontweight'] = fontweight
        self.fig_title['color'] = color

        self.ax.set_title(self.fig_title['title'],
                          fontsize=self.fig_title['fontsize'], 
                          fontweight=self.fig_title['fontweight'],
                          color=self.fig_title['color'])
        self.canvas.draw()

    def set_mode(self, mode:None):
        #print(mode)
        if mode != "Dark":
            self.set_theme(False)
        else:
            self.set_theme(True)

    def set_theme(self, dark_mode=True):
        self.ax.xaxis.set_tick_params(colors='red')
        self.ax.yaxis.set_tick_params(colors='green')
        self.ax.zaxis.set_tick_params(colors='blue')
        
        if dark_mode:
            self.ax.set_facecolor('#303030')
            self.fig.patch.set_facecolor('#202020')
            self.ax.title.set_color("#F39C12")
            self.ax.grid(True, linestyle='--', linewidth=0.5, color='white', alpha=0.3)
            for spine in self.ax.spines.values():
                spine.set_edgecolor('white')
            if self.ax.get_legend() is not None:
                legend=self.ax.get_legend()
                # Cambiar el color del contenedor de la leyenda
                frame = legend.get_frame() # Obtener el objeto de marco de la leyenda
                frame.set_facecolor('#7D7D7D') # Cambiar el color de fondo
                for text in self.ax.get_legend().get_texts():
                    text.set_color('black')
        else:
            self.ax.set_facecolor('#f0f0f0')
            self.fig.patch.set_facecolor('#e0e0e0')
            self.ax.title.set_color('#3D5AFE')
            self.ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.3)
            for spine in self.ax.spines.values():
                spine.set_edgecolor('black')
            if self.ax.get_legend() is not None:
                for text in self.ax.get_legend().get_texts():
                    text.set_color('black')
        self.canvas.draw()



def rotate_euler():
    app.rotate_cube('euler', 'xyz', [np.pi/4, np.pi/4, np.pi/4])
    

def rotate_quaternion():
    app.rotate_cube('quaternion', [np.sqrt(2)/2, 0, 0, np.sqrt(2)/2])



if __name__ =="__main__":
    # Create the Tkinter app
    root = ctk.CTk()
    app = CubeFrame(master=root)
    app.pack()
    #root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.after(2000, rotate_euler)

"""

if __name__ =="__main__":
    # Crear la aplicación Tkinter
    cubo = Cube()
    #cubo.draw_faces()
    cubo.draw()
    
"""


##

class CubeFrame1(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.cube = Cube()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.draw_cube()

    def draw_cube(self):
        self.ax.cla()
        self.cube.draw_faces(self.ax)
        for edge in self.cube.edges:
            line = np.vstack((self.cube.vertices[edge[0]], self.cube.vertices[edge[1]]))
            self.ax.plot(line[:, 0], line[:, 1], line[:, 2], 'k')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-2, 2])
        self.canvas.draw()

