
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


import tkinter as tk
import customtkinter


import time

import numpy as np

class CubeFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, rotation_angles=(0, 0, 0)):
        super().__init__(master)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.ag_x = 0
        self.ag_y = 0
        self.ag_z = 0

        #------------------------------#
        self.fig_title = {'title':"titulo de figura",'fontsize':11, 'fontweight':"normal", 'color':"black"}
        self.color_lg = "black"

        self.fig = Figure(dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.subplots_adjust(left=0.18, bottom=0.15)
        
        self.vertices = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                                  [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1, 1]])
        
        self.vertices = self.vertices * 0.4

        self.ax.set_box_aspect([1, 1, 1])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self) 
        self.canvas.draw()

        #customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        self.set_fig_appearance_mode(customtkinter.get_appearance_mode())

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Redibujar el gráfico cuando se redimensiona el widget
        self.canvas.mpl_connect("resize_event", self.on_resize)

        # graficar el cubo
        self.rotate_cube(*rotation_angles)

    def set_fig_appearance_mode(self, mode:None):
        #print(mode)
        if mode != "Dark":
            self.set_theme(False)
            print("light")
        else:
            print("Dark")
            self.set_theme(True)

    def fig_configure(self):
        # Configurar los límites de los ejes
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_zticklabels([])

        #self.ax.set_xlabel('X')
        #self.ax.set_ylabel('Y')
        #self.ax.set_zlabel('Z')

        self.ax.set_title(self.fig_title['title'],
                          fontsize=self.fig_title['fontsize'], 
                          fontweight=self.fig_title['fontweight'],
                          color=self.fig_title['color'])
        
        
        # Agregar texto dentro del cuadro informativo
        data = f"ax: {self.ag_x}°\n ay: {self.ag_y}°\n az: {self.ag_z}°"
        self.ax.text(0.5, 0.5, 0.5, "Ángulos \n" + data, color=self.color_lg, ha='center', va='center', rotation='vertical')


        

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

    def set_theme(self, dark_mode=True):
        if dark_mode:
            self.color_lg = "#1F51D8"
            self.ax.set_facecolor('#303030')
            self.fig.patch.set_facecolor('#202020')
            self.ax.tick_params(colors='white', which='both')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color("#F39C12")
            self.ax.grid(True, linestyle='--', linewidth=0.5, color='white', alpha=0.3)
            for spine in self.ax.spines.values():
                spine.set_edgecolor('white')
            if self.ax.get_legend() is not None:
                legend=self.ax.get_legend()
                # Cambiar el color del contenedor de la leyenda
                frame = legend.get_frame() # Obtener el objeto de marco de la leyenda
                frame.set_facecolor('0x1F1F1F') # Cambiar el color de fondo
                #frame.set_edgecolor('black') # Cambiar el color del borde
                for text in self.ax.get_legend().get_texts():
                    text.set_color('black')
        else:
            self.color_lg = "black"
            self.ax.set_facecolor('#f0f0f0')
            self.fig.patch.set_facecolor('#e0e0e0')
            self.ax.tick_params(colors='black', which='both')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.title.set_color('#3D5AFE')
            self.ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.3)
            for spine in self.ax.spines.values():
                spine.set_edgecolor('black')
            if self.ax.get_legend() is not None:
                for text in self.ax.get_legend().get_texts():
                    text.set_color('black')
        self.canvas.draw()


    def rotate_cube(self, angle_x, angle_y, angle_z):
        # Clear the current plot
        self.ax.cla()

        # Rotate vertices
        rotation_matrix = self.rotation_matrix(angle_x, angle_y, angle_z)
        rotated_vertices = np.dot(self.vertices, rotation_matrix)

        # Plot rotated cube
        z = [rotated_vertices]
        self.ax.add_collection3d(self.plot_cube(z))
        self.ax.set_box_aspect([1,1,1])

        self.fig_configure()

        # Redraw the canvas
        self.canvas.draw()

    def rotation_matrix(self, angle_x, angle_y, angle_z):
        self.ag_x = angle_x
        self.ag_y = angle_y
        self.ag_z = angle_z

        # Generate rotation matrix
        angle_x = np.radians(angle_x)
        angle_y = np.radians(angle_y)
        angle_z = np.radians(angle_z)

        rotation_matrix_x = np.array([[1, 0, 0],
                                      [0, np.cos(angle_x), -np.sin(angle_x)],
                                      [0, np.sin(angle_x), np.cos(angle_x)]])

        rotation_matrix_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                                      [0, 1, 0],
                                      [-np.sin(angle_y), 0, np.cos(angle_y)]])

        rotation_matrix_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                                      [np.sin(angle_z), np.cos(angle_z), 0],
                                      [0, 0, 1]])

        return np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, rotation_matrix_x))

    def plot_cube(self, z):
        self.ax.scatter3D(z[0][:, 0], z[0][:, 1], z[0][:, 2])

        verts = [[z[0][0],z[0][1],z[0][5],z[0][4]],
                [z[0][7],z[0][6],z[0][2],z[0][3]],
                [z[0][0],z[0][1],z[0][2],z[0][3]],
                [z[0][7],z[0][6],z[0][5],z[0][4]],
                [z[0][7],z[0][3],z[0][0],z[0][4]],
                [z[0][1],z[0][2],z[0][6],z[0][5]]]
        

        #return Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25)
        face_colors = ['yellow', 'blue', 'green', 'red', 'orange','cyan']
        # ['front', 'back', 'down', 'top', 'left','right']

        pc = Poly3DCollection(verts, linewidths=0.5, edgecolors='r', alpha=.3)
        pc.set_facecolor(face_colors)
        return pc
    
    @staticmethod
    def normalizar_cuaterniones(orientacion):
        norma = np.linalg.norm(orientacion)
        return orientacion / norma

    def update_angles(self, angles):
        self.rotate_cube(*angles)
    
    def on_resize(self, event):
        self.fig.tight_layout()

    def apply_simulation(self, duration, angle_step):
        angles = [0, 0, 0]
        num_steps = int(duration / angle_step)

        def update():
            nonlocal angles
            angles = [angle + angle_step for angle in angles]
            self.update_angles(angles)
            self.canvas.draw()
            if angles[0] < 360:
                self.after(10, update)  # Volver a llamar a update después de 10 ms

        update()


def on_close():
    root.destroy()

if __name__ == "__main__":
    root = customtkinter.CTk()
    cube_frame = CubeFrame(root)
    cube_frame.pack()
    cube_frame.set_title(title="hola nuevo titulo",color="#F39C12")

    root.protocol("WM_DELETE_WINDOW", on_close)
    #time.sleep(3)

    #root.after(2000, lambda: cube_frame.apply_simulation(10, 2))  # Aplicar simulación después de 1.5 segundos


    root.mainloop()
