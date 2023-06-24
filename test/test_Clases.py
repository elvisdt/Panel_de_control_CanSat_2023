import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PersonalizadoMatplotlib(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.figure, self.ax = plt.subplots()
        self.ax.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])  # Ejemplo de gráfico

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Redibujar el gráfico cuando se redimensiona el widget
        self.canvas.mpl_connect("resize_event", self.on_resize)

    def on_resize(self, event):
        self.figure.tight_layout()
    
    def actualizar_grafico(self, x, y):
        self.ax.clear()  # Limpia el gráfico actual
        self.ax.plot(x, y)  # Dibuja el nuevo gráfico
        self.figure.tight_layout()
        self.canvas.draw_idle()  # Actualiza el canvas




class VentanaSuperior(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.frames = []
        for i in range(6):
            frame = PersonalizadoMatplotlib(self)
            frame.grid(row=i//3, column=i%3, sticky='nsew')
            self.frames.append(frame)

        # Establece los pesos de las filas y columnas
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)



class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Graficos Matplotlib en Tkinter")
        self.geometry("800x600")

        self.ventana_superior = VentanaSuperior(self)
        self.ventana_superior.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Ejemplo de cómo modificar las gráficas
        self.modificar_graficas()

        # Vincula el evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_cerrar_ventana)

    def modificar_graficas(self):
        # Aquí puedes personalizar las gráficas como desees
        for i, frame in enumerate(self.ventana_superior.frames):
            x = [0, 1, 2, 3, 4]
            y = [v ** (i+1) for v in x]
            frame.actualizar_grafico(x, y)
    
    def on_cerrar_ventana(self):
        # Cierra todos los objetos de Matplotlib antes de salir
        plt.close("all")
        self.quit()  # Termina el bucle de eventos
        self.destroy()  # Destruye la ventana


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
