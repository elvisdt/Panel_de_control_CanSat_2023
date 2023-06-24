import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection



import tkinter as tk
import customtkinter

class CubeFrame(tk.Frame):
    def __init__(self, master=None, rotation_angles=(0, 0, 0)):
        tk.Frame.__init__(self, master)
        self.pack()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        

        self.vertices = np.array([[-1, -1, -1],
                                  [1, -1, -1 ],
                                  [1, 1, -1],
                                  [-1, 1, -1],
                                  [-1, -1, 1],
                                  [1, -1, 1 ],
                                  [1, 1, 1],
                                  [-1, 1, 1]])
        
        self.vertices =self.vertices * 0.2

        self.ax.set_box_aspect([1, 1, 1])


        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])

        #self.ax.set_xticklabels([])
        #self.ax.set_yticklabels([])
        #self.ax.set_zticklabels([])

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.ax.set_title("Datos en tiempo real")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

                
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.rotate_cube(*rotation_angles)

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

         # Configurar los límites de los ejes
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_zticklabels([])

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')


        # Redraw the canvas
        self.canvas.draw()

    def rotation_matrix(self, angle_x, angle_y, angle_z):
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
        face_colors = ['cyan', 'cyan', 'green', 'red', 'cyan','cyan']

        pc = Poly3DCollection(verts, linewidths=1, edgecolors='r', alpha=.25)
        pc.set_facecolor(face_colors)
        return pc
    
    def update_angles(self, angles):
        self.rotate_cube(*angles)
    

    
    def set_theme(self, dark_mode=True):
        if dark_mode:
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
                frame.set_facecolor('#7D7D7D') # Cambiar el color de fondo
                #frame.set_edgecolor('black') # Cambiar el color del borde
                for text in self.ax.get_legend().get_texts():
                    text.set_color('black')
        else:
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
    root = tk.Tk()
    cube_frame = CubeFrame(root)
    cube_frame.pack()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.after(500, lambda: cube_frame.apply_simulation(10, 2))  # Aplicar simulación después de 1.5 segundos


    root.mainloop()
