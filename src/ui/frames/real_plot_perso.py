

import tkinter as tk
import customtkinter

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import numpy as np
import math

import random

class RealPlotPerso(customtkinter.CTkFrame):
    def __init__(self, master=None, max_points=100):
        super().__init__(master)

        self.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.max_points = max_points
        self.lines = []
        self.colors = ["b", "g", "r", "c", "m", "y", "k"]

        #self.fig = Figure(figsize=(4, 3), dpi=100)
        self.fig = Figure(dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.18, bottom=0.15)

        # configuracion inicial
        self.ax.set_xlim(0, self.max_points - 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_title("Datos en tiempo real")
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel("Valor")



        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        #customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        self.set_fig_appearance_mode(customtkinter.get_appearance_mode())

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Redibujar el gráfico cuando se redimensiona el widget
        self.canvas.mpl_connect("resize_event", self.on_resize)

    def set_fig_appearance_mode(self, mode:None):
        #print(mode)
        if mode != "Dark":
            self.set_theme(False)
        else:
            self.set_theme(True)


    def set_title(self, title, fontsize=11, fontweight="normal", color="#F39C12"):
        self.ax.set_title(title, fontsize=fontsize, fontweight=fontweight, color=color)
        self.canvas.draw()

    def set_x_label(self, x_label, fontsize=12, fontweight="normal", color="black"):
        self.ax.set_xlabel(x_label, fontsize=fontsize, fontweight=fontweight, color=color)
        self.canvas.draw()

    def set_y_label(self, y_label, fontsize=12, fontweight="normal", color="black"):
        self.ax.set_ylabel(y_label, fontsize=fontsize, fontweight=fontweight, color=color)
        self.canvas.draw()

    def set_x_limits(self, x_min, x_max):
        self.ax.set_xlim(x_min, x_max)
        self.canvas.draw()

    def set_y_limits(self, y_min, y_max):
        self.ax.set_ylim(y_min, y_max)
        self.canvas.draw()

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

    def customize_legend(self, show=True, loc='best', **kwargs):
        if show:
            self.ax.legend(loc=loc, **kwargs)
        else:
            self.ax.get_legend().remove()


    def add_line(self, y_data=None, func=None, line_style="-", linecolor=None, marker=None, label=None, linewidth=1.0):

        if y_data is not None:
            if len(y_data) < self.max_points:
                y_data = [None]*(self.max_points - len(y_data)) + y_data
            elif len(y_data) > self.max_points:
                y_data = y_data[-self.max_points:]
        else:
            y_data = [None]*self.max_points

        if linecolor is None:
            linecolor = self.colors[len(self.lines) % len(self.colors)]

        x_data = np.arange(self.max_points)
        line, = self.ax.plot(x_data, y_data, linestyle=line_style, color=linecolor, marker=marker, label=label, linewidth=linewidth)
        self.lines.append({"y_data": y_data, "line": line, "func": func})

    def add_new_data(self, line_index, new_value):
        line_data = self.lines[line_index]
        line_data["y_data"].append(new_value)

        if len(line_data["y_data"]) > self.max_points:
            line_data["y_data"].pop(0)
        line_data["line"].set_ydata(line_data["y_data"])

        # Auto-ajuste de los ejes
        y_mins = [min(y for y in line["y_data"] if y is not None) for line in self.lines if any(y is not None for y in line["y_data"])]
        y_maxs = [max(y for y in line["y_data"] if y is not None) for line in self.lines if any(y is not None for y in line["y_data"])]

        if y_mins and y_maxs: # check if y_mins and y_maxs are not empty
            y_min = min(y_mins)-0.5
            y_max = max(y_maxs)+0.5

            if y_min == y_max:
                y_min -= 1  # decrease the lower limit
                y_max += 1  # increase the upper limit

            self.ax.set_ylim(y_min, y_max)

        # actualiza la etiqueta de la línea con el nuevo valor
        label = line_data["line"].get_label().split(':')[0]  # obtén la etiqueta original sin el valor anterior
        line_data["line"].set_label(f"{label}: {new_value:.2f}")  # establece la nueva etiqueta con el nuevo valor

        # si la leyenda ya existe, debes actualizarla para que muestre la nueva etiqueta
        if self.ax.get_legend() is not None:
            # guarda el título de la leyenda
            legend_title = self.ax.get_legend().get_title().get_text()
            self.ax.legend(title=legend_title, loc='lower left')
            #self.ax.legend(title=legend_title)



        self.canvas.draw_idle()

    def on_resize(self, event):
        self.fig.tight_layout()





if __name__ == "__main__":
    root = customtkinter.CTk()
    #root = tk.Tk()
    root.title("Gráfica en tiempo real en un Frame")
    t = 0
    #----------------------------------------------------------
    def sine_function_generator(freq1=0.2):
        global t
        while True:
            value = math.sin(t * 0.1*freq1)
            t += 1
            yield value

    def cosine_function_generator(freq2=0.1):
        global t
        while True:
            value = math.cos(t * 0.1*freq2)+ random.uniform(0, 1)
            t += 1
            yield value

    def update_plot():
        # Obtén nuevos valores de tus generadores de funciones
        new_cosine_value = next(cosine_gen)
        new_sine_value = next(sine_gen)

        # Agrega los nuevos valores a las líneas de gráfica
        plotter.add_new_data(0, new_cosine_value)
        plotter.add_new_data(1, new_sine_value)

        # Programa la siguiente actualización en 100 ms
        root.after(100, update_plot)


    sine_gen = sine_function_generator()
    cosine_gen = cosine_function_generator()

    plotter = RealPlotPerso(master=root, max_points=100)
    plotter.add_line(func="hola",  label='Coseno', linewidth=0.5)
    plotter.add_line(func="hola", linecolor='red', label='Seno', linewidth=0.5)

    plotter.customize_legend(show=True, title='Funciones')

    plotter.set_title(title="hola",color="#F39C12")
    # Cambiar entre modo oscuro y modo claro
    #dark_mode = True
    #plotter.set_theme(dark_mode)

    # Inicia la actualización de la gráfica
    update_plot()

    root.mainloop()

