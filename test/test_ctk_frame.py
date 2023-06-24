
import customtkinter as ctk
import tkinter as tk

class SimpleFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

root = tk.Tk()
app = SimpleFrame(master=root)
app.mainloop()
