import tkinter as tk
import sys

class TerminalApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.terminal = tk.Text(self.master, bg='black', fg='white')
        self.terminal.pack(fill=tk.BOTH, expand=True)
        sys.stdin = self.StdinRedirector(self.terminal)
        sys.stdout = self.StdoutRedirector(self.terminal)

    class StdinRedirector:
        def __init__(self, terminal):
            self.terminal = terminal

        def write(self, text):
            self.terminal.insert(tk.END, text)

    class StdoutRedirector:
        def __init__(self, terminal):
            self.terminal = terminal

        def write(self, text):
            self.terminal.insert(tk.END, text)

    def run(self):
        self.master.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = TerminalApp(root)
    app.run()

    # Imprimir cadena en la terminal
    #sys.stdin.write("Hello, World!\n")
