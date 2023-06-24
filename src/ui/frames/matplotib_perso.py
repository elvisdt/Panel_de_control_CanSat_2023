import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

class RealTimePlotter(tk.Frame):
    def __init__(self, master=None, max_points=50):
        super().__init__(master)

        self.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.max_points = max_points
        self.lines = []

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.ax.set_xlim(0, self.max_points - 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_title("Datos en tiempo real")
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel("Valor")

        # Personaliza la apariencia de la gráfica
        self.ax.grid(True)
        self.ax.set_facecolor('#f0f0f0')
        self.fig.patch.set_facecolor('#e0e0e0')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.update_data()
    
    
    def set_theme(self, dark_mode=False):
        if dark_mode:
            self.ax.set_facecolor('#303030')
            self.fig.patch.set_facecolor('#202020')
            self.ax.tick_params(colors='white', which='both')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
            self.ax.grid(True, linestyle='--', linewidth=0.5, color='white', alpha=0.3)
            for spine in self.ax.spines.values():
                spine.set_edgecolor('white')
            if self.ax.get_legend() is not None:
                for text in self.ax.get_legend().get_texts():
                    text.set_color('white')
        else:
            self.ax.set_facecolor('#f0f0f0')
            self.fig.patch.set_facecolor('#e0e0e0')
            self.ax.tick_params(colors='black', which='both')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.title.set_color('black')
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


    def add_line(self, y_data=None, func=None, line_style="-", color=None, marker=None, label=None, linewidth=1.0):
        if y_data is not None:
            if len(y_data) < self.max_points:
                y_data = [None]*(self.max_points - len(y_data)) + y_data
            elif len(y_data) > self.max_points:
                y_data = y_data[-self.max_points:]
        else:
            y_data = [None]*self.max_points

        x_data = np.arange(self.max_points)
        line, = self.ax.plot(x_data, y_data, linestyle=line_style, color=color, marker=marker, label=label, linewidth=linewidth)
        self.lines.append({"y_data": y_data, "line": line, "func": func})

    
    

    def update_data(self):
        for line_data in self.lines:
            if line_data["func"] is not None:
                new_value = next(line_data["func"])
                line_data["y_data"].append(new_value)
                if len(line_data["y_data"]) > self.max_points:
                    line_data["y_data"].pop(0)
                line_data["line"].set_ydata(line_data["y_data"])

        self.canvas.draw()
        self.after(100, self.update_data)


#----------------------------------------------------------
def sine_function_generator():
    global t
    while True:
        value = math.sin(t * 0.1)
        t += 1
        yield value

def cosine_function_generator():
    global t
    while True:
        value = math.cos(t * 0.1)
        t += 1
        yield value

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gráfica en tiempo real en un Frame")
    
    t = 0
    sine_gen = sine_function_generator()
    cosine_gen = cosine_function_generator()

    plotter = RealTimePlotter(master=root, max_points=100)
    plotter.add_line(func=cosine_gen, color='red', label='Coseno')
    plotter.add_line(func=sine_gen, color='blue', label='Seno', linewidth=0.2)
    
    plotter.customize_legend(show=True, loc='upper right', title='Funciones')

    # Cambiar entre modo oscuro y modo claro
    dark_mode = False
    plotter.set_theme(dark_mode)

    root.mainloop()

