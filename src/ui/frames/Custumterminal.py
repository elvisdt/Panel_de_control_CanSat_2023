import tkinter as tk

class CustomTerminal(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.tag_configure("red", foreground="red")
        self.tag_configure("green", foreground="green")
        self.tag_configure("blue", foreground="blue")
        self.configure(bg="black")  # Establecer el color de fondo en negro
        self.configure(state="disabled")  # Desactivar la edición

    def insert_colored_text(self, index, text, color_tag):
        self.configure(state="normal")  # Habilitar la edición temporalmente
        self.insert(index, text, color_tag)
        self.configure(state="disabled")  # Desactivar la edición nuevamente

    def change_font(self, font_family, size, weight="normal"):
        self.configure(font=(font_family, size, weight))

def main():
    root = tk.Tk()
    terminal = CustomTerminal(root, wrap="word", height=15, width=50)
    terminal.pack(expand=True, fill="both")

    # Cambiar la fuente
    terminal.change_font("Currier", 10)

    # Insertar un párrafo de 10 líneas
    paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis consequat tellus quis libero sollicitudin pellentesque. Sed ut blandit mauris. Aenean bibendum elit at ullamcorper sollicitudin. Cras tristique enim mi, vitae lacinia arcu commodo id. Nullam a turpis nec tellus venenatis fringilla. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed semper velit eget libero pretium, eu rhoncus risus consectetur. Proin ac egestas odio, at facilisis elit. Pellentesque nec purus id enim bibendum malesuada."
    
    for i, char in enumerate(paragraph):
        color_tag = "red" if i % 3 == 0 else "green" if i % 3 == 1 else "blue"
        terminal.insert_colored_text(f"1.{i}", char, color_tag)

    root.mainloop()

if __name__ == "__main__":
    main()
