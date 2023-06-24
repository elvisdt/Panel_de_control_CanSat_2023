import tkinter as tk

class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.text_box = tk.Text(self.master)
        self.text_box.pack()

    def agregar_dato(self, dato, color, fuente):
        tag = "tag" + str(self.text_box.index(tk.INSERT).split('.')[0]) # Crear una tag única para cada línea
        self.text_box.insert(tk.END, dato + "\n")
        self.text_box.tag_add(tag, "end-2l", "end-1l") # Aplicar la tag a la última línea
        self.text_box.tag_config(tag, foreground=color, font=fuente) # Configurar la tag
        self.text_box.see(tk.END)

root = tk.Tk()
app = Aplicacion(root)

# Agregamos algunos datos de prueba con diferentes colores y fuentes
app.agregar_dato("Hola", "red", ("Helvetica", 12))
app.agregar_dato("¿Cómo estás?", "blue", ("Courier", 14))
app.agregar_dato("¡Hasta luego!", "green", ("Times", 16))

root.mainloop()
