import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

class RealTimeGraph(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas = self.graph.get_tk_widget()
        self.canvas.pack()

        x_data = np.arange(100)
        y_data = np.zeros(100)

        self.lines = []
        colors = ['blue', 'red', 'green']
        for color in colors:
            line = Line2D(x_data, y_data, color=color, linewidth=0.5)
            self.lines.append(line)
            self.ax.add_line(line)

        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(-1, 1)

        self.graph.draw()
        self.bg = self.graph.copy_from_bbox(self.ax.bbox)

        self.update_data()
    
    def set_mode(self, mode):
        self.color_bg = ["#212121","#333333","#333333"]
        self.color_fg = '#CCD1D1'

        if mode == 'dark':
            # ------configuracion del frame de la grafica ----------------
            self.fig.set_facecolor(self.color_bg[2])   
            self.ax.set_facecolor(self.color_bg[1])
            self.ax.set_ylim(0,100)
            self.ax.set_xlim(0,100)            
            #self.ax.tick_params(axis='y', colors=self.color_fg)
            #self.ax.tick_params(axis='x', colors=self.color_bg[2])
            #self.ax.grid(linestyle='--',which='both')
        


    def set_line_color(self, line_index, color):
        if 0 <= line_index < len(self.lines):
            self.lines[line_index].set_color(color)
            self.graph.draw()
        else:
            print(f"Error: línea {line_index} no existe")

    def update_graph(self, data):
        for i, line in enumerate(self.lines):
            line.set_ydata(data[i])
            self.graph.restore_region(self.bg)
            self.ax.draw_artist(line)

        self.graph.blit(self.ax.bbox)

    def update_data(self):
        data = [np.random.rand(100) * 2 - 1 for _ in range(3)]
        self.update_graph(data)
        self.after(50, self.update_data)

# ... (el código de la clase Application se mantiene igual) ...


# ... (el código de la clase Application se mantiene igual) ...
