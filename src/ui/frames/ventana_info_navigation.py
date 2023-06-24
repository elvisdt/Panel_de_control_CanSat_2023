

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import os 
import sys

import numpy as np
import math

#Agregar ruta actual del archivo
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

#-------------Librerias personalizadas
from real_plot_perso import RealPlotPerso
from cube_plot import CubeFrame

class VentanaInfoNav(ctk.CTkFrame):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        
        #-----------configurar el diseño de una grilla de (6x6)
        self.grid_columnconfigure((0,1), weight=1,minsize=100)    # columnas adaptables
        self.grid_rowconfigure((0,1), weight=1,minsize=100)         # filas adptables

        #customtkinter.set_appearance_mode('Light')
           
        
        self.frame_00 = ctk.CTkFrame(self, border_width=10)
        self.frame_00.grid(row=0, column=0,  padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.fig_frame_00 = RealPlotPerso(master=self.frame_00, max_points=100)

        self.frame_01 = ctk.CTkFrame(self)
        self.frame_01.grid(row=0, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.fig_frame_01 = RealPlotPerso(master=self.frame_01, max_points=100)

        self.frame_10 = ctk.CTkFrame(self)
        self.frame_10.grid(row=1, column=0, padx=(5, 0), pady=(5, 5), sticky="nsew")
        self.fig_frame_10 = RealPlotPerso(master=self.frame_10, max_points=100)

        self.frame_11 = ctk.CTkFrame(self)
        self.frame_11.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.fig_frame_11 = CubeFrame(master=self.frame_11) 

        #self.fig_frame_11 = RealPlotPerso(master=self.frame_11, max_points=100)

                
    
        # Vincular el evento <Configure> a la función mantener_relacion
        self.bind('<Configure>', self.mantener_relacion)

    def mantener_relacion(self, event):
        ancho_ventana = self.winfo_width()
        
        # Establecer el tamaño mínimo de las columnas 0 y 1
        minsize_0_1 = ancho_ventana * 0.4
        self.columnconfigure(0, minsize=minsize_0_1)
        self.columnconfigure(1, minsize=minsize_0_1)



    def set_vent_mode(self,mode):
        self.fig_frame_00.set_fig_appearance_mode(mode)
        self.fig_frame_01.set_fig_appearance_mode(mode)
        self.fig_frame_10.set_fig_appearance_mode(mode)
        self.fig_frame_11.set_mode(mode)


        
        


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Test VentanaSuperior")
    root.geometry("800x600")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    
    ventana_superior = VentanaInfoNav(master=root)
    ventana_superior.grid(row=0, column=0, sticky='nsew')

    ventana_superior.fig_frame_00.set_title("hola")

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
            value = math.cos(t * 0.1*freq2)
            t += 1
            yield value

    def update_plot():
        # Obtén nuevos valores de tus generadores de funciones
        new_cosine_value = next(cosine_gen)
        new_sine_value = next(sine_gen)

        # Agrega los nuevos valores a las líneas de gráfica
        ventana_superior.fig_frame_00.add_new_data(0, new_cosine_value)
        ventana_superior.fig_frame_00.add_new_data(1, new_sine_value)
        print(new_cosine_value )
        # Programa la siguiente actualización en 100 ms
        root.after(100, update_plot)

    sine_gen = sine_function_generator()
    cosine_gen = cosine_function_generator()

    ventana_superior.fig_frame_00.add_line(func=cosine_gen,  label='Coseno', linewidth=0.5)
    ventana_superior.fig_frame_00.add_line(func=sine_gen, linecolor='red', label='Seno', linewidth=0.5)
    
    
    #ventana_superior.plot_frames[0].set_title(title="hola")
    # Configura los pesos de las filas y columnast
    

    root.mainloop()