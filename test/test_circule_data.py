import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class Objeto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.point, = plt.plot(self.x, self.y, 'bo')

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy
        self.point.set_data(self.x, self.y)

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de plano")

        # Crear los objetos
        self.objeto1 = Objeto(1, 1)
        self.objeto2 = Objeto(-1, -1)

        # Crear el gráfico
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)

        # Crear el canvas y empaquetarlo
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Configurar la animación
        self.animacion()

    def animacion(self):
        self.objeto1.mover(0.1, 0.1)  # mover el objeto1
        self.objeto2.mover(-0.1, -0.1)  # mover el objeto2
        self.canvas.draw()
        self.root.after(100, self.animacion)  # repetir cada 100 ms

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()


