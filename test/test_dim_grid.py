import tkinter as tk

class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()

        self.contenedor = tk.Frame(self)
        self.contenedor.pack(fill=tk.BOTH, expand=True)

        # Configurar columnas y filas en el contenedor
        self.contenedor.columnconfigure(0, weight=1, minsize=100)
        self.contenedor.rowconfigure(0, weight=1, minsize=100)

        # Crear el frame
        self.frame = tk.Frame(self.contenedor, bg="red")
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Configurar columnas y filas en el frame
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Crear un widget de ejemplo
        boton = tk.Button(self.frame, text="Botón")
        boton.grid(row=0, column=0, sticky="nsew")

if __name__ == '__main__':
    ventana = Ventana()
    ventana.mainloop()