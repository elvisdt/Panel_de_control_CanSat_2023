import ascii_magic
from ascii_magic import AsciiArt, Back


import os
import sys
from tkinter import PhotoImage

current_directory = os.path.dirname(os.path.abspath(__file__))
images_directory = os.path.join(current_directory, "resources", "images")

#image_path = os.path.join(images_directory, "logo_starvek.png")
# Cambia la ruta a la imagen que deseas convertir
image_path = "logo_starvek.png"


my_art = AsciiArt.from_image(image_path)
my_output = my_art.to_ascii(columns=200)
#sys.stdin.write(my_output)
print(my_output)

#print(type(my_output))
#text = "Hola, este es un archivo ASCII de ejemplo."
#filename = "archivo.txt"

#with open(filename, "w") as file:
#    file.write(my_output)
