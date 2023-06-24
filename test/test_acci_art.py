import tkinter as tk
import subprocess

class TerminalApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.start_shell()

    def create_widgets(self):
        self.terminal = tk.Text(self.master, bg='black', fg='white')
        self.terminal.pack(fill=tk.BOTH, expand=True)

    def start_shell(self):
        self.process = subprocess.Popen(
            "cmd.exe", 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            encoding="utf-8",
            bufsize=0
        )

        self.write_output(self.process.stdout.readline())

    def write_output(self, output):
        self.terminal.insert(tk.END, output)
        self.process.stdin.write("\n")
        self.process.stdin.flush()
        output = self.process.stdout.readline()
        if output:
            self.write_output(output)

if __name__ == '__main__':
    root = tk.Tk()
    app = TerminalApp(root)
    app.mainloop()


root.mainloop()