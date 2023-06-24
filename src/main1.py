import tkinter as tk
import tkinter.messagebox
import customtkinter
from tkinter import font as tkFont
from time import strftime

import os
import sys
from PIL import Image
import math

from datetime import datetime, timedelta


import ahrs
from ahrs.common.orientation import q_prod, q_conj, acc2q, am2q, q2R, q_rot
import pyquaternion
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



#-------Comunicacion serial--------

##librerias propias
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

import models.AsciiArt as AsciiA
#from controllers import serial_com as my_serial
import controllers.serial_obj as my_serial
from ui.frames.ventana_info_sensor import VentanaInfoSensor
import IMU.imu_data as imu


pos = imu.getPosLin()

print(pos.shape)


#------inicializar modo del HMI-----------
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



"""
-----------------------------------------------------
|                           1                       |
-----------------------------------------------------
|       |                           |               |
|       |                           |       4       |
|       |                           |               |
|       |              3            |---------------|
|   2   |                           |               |
|       |                           |       5       |
|       |                           |               |
|       |--------------------------------------------
|       |              6            |       7       |
-----------------------------------------------------
"""




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #-----------configurar ventana----------------------
        self.title("Panel de control")
        #self.geometry(f"{1100}x{580}")
        
        self.set_geometry_panel(0.7)
        self.minsize(1045, 590)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        #----------------Clases de serial------------------
        self.serial_obj = my_serial.SerialObj()

        ##----------------Variables-----------------------
        
        self.list_baudrate = ["9600", "19200", "38400", "57600", "115200"]
        self.BAUD = int(self.list_baudrate[0])

        try:
            self.list_ports = self.serial_obj.get_ports()
            self.COM  = self.list_ports[0]
        except:
            self.COM  = self.list_ports[0]

        #----------------Variables de data ------------------------------#

        # Crear una variable para almacenar el estado del botón
        self.serial_button_txtvariable = tk.StringVar()
        self.serial_button_txtvariable.set("Conectar")

        #self.Accel = imu.getAccIMU()
        self.generador_acel = self.data_acel()
        self.generador_gyro = self.data_gyro()
        self.generador_mag  = self.data_mag()
                
        #&.............load images for ligth and dark mode..................
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"resources","images")
                
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.logo_starvek = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "light_logo_starvek.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "dark_logo_starvek.png")),size=(100, 100))
        self.logo_starvek_circ = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_cir_starvek.png")), size=(120, 120))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.csv_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "csv.png")), size=(26, 26))
        self.play_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "play.png")), size=(26, 26))
        

        #-----------------crear interfaz grafica-------------------
        #self.create_interfaz()
        


        ################### CREACÍON DE INTERFAZ##########################

        #-----------configurar el diseño de una grilla de (4x4)
        self.grid_columnconfigure((0, 3), weight=0)     # comunnas fijas
        self.grid_columnconfigure((1,2), weight=1)      # columna adaptable
        self.grid_rowconfigure((0,3), weight=0)         # filas fijas
        self.grid_rowconfigure((1,2), weight=1)         # filas adptables
        
        #-----------------------1-----------------------------------
        #-----------crear marco del frame superior con widgets----
        self.frm1 = customtkinter.CTkFrame(self, corner_radius=10)
        self.frm1.grid(row=0, column=0, columnspan=4,padx=5, pady=5, sticky="nsew")
        self.frm1.grid_columnconfigure(1, weight=1)
        self.frm1.grid_columnconfigure(3, weight=0)

        self.frm1_TitleLbl = customtkinter.CTkLabel(self.frm1, text="StarVek Perú", text_color=("#1565C0","#304FFE"),
                                                    font=customtkinter.CTkFont(family='Segoe UI',size=30, weight="bold"))
        self.frm1_TitleLbl.grid(row=0, column=0, columnspan=2 , padx=20, pady=5, sticky="nsew")
        
        self.frm1_ClockLbl = customtkinter.CTkLabel(self.frm1, text="12:12:00", text_color="#D32F2F",
                                                    font=customtkinter.CTkFont(family='Courier New',size=20, weight="bold"))
        self.frm1_ClockLbl.grid(row=0, column=3, padx=20, pady=5, sticky="nsew")
        
        
        #---------------------------------------------------------------------------------------------
        #--------------------- 2 crear marco de navegación  ------------------------------------------
        #---------------------------------------------------------------------------------------------
        self.frm2 = customtkinter.CTkFrame(self, corner_radius=5)
        self.frm2.grid(row=1, column=0, rowspan=3, sticky="nsew")
        self.frm2.grid_rowconfigure(5, weight=1)

        #------------------contenedores del frm menu-------------------------
        self.frm2_TitleLbl = customtkinter.CTkLabel(self.frm2, text=" MENÚ", image=self.logo_image, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frm2_TitleLbl.grid(row=0, column=0, padx=20, pady=10)
                
        self.frm2_HomeBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent", text_color=("gray10", "gray90"),
                                                    hover_color=("gray70", "gray30"), image=self.home_image, anchor="w", command=self.home_button_event)
        self.frm2_HomeBtn.grid(row=1, column=0, sticky="ew")
        
        self.frm2_C1_InfoSenBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="C1: Info sensores", fg_color="transparent",
                                                          text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frm2_C1_InfoSenBtn.grid(row=2, column=0, sticky="ew")

        self.frm2_C1_InfoNavBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="C1: Info navegación", fg_color="transparent",
                                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frm2_C1_InfoNavBtn.grid(row=3, column=0, sticky="ew")
        

        self.frm2_C2_InfoNavBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="C2: Info navegación", fg_color="transparent",
                                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frm2_C2_InfoNavBtn.grid(row=4, column=0, sticky="ew")


        # row 5 adjustable
        self.frm2_figLbl = customtkinter.CTkLabel(self.frm2, text="", image=self.logo_starvek_circ,fg_color='transparent')
        self.frm2_figLbl.grid(row=5, column=0, sticky="nsew")

        self.frm2_AppearanceModeLbl = customtkinter.CTkLabel(self.frm2, text="Appearance Mode:", anchor="w")
        self.frm2_AppearanceModeLbl.grid(row=6, column=0, padx=20, pady=(10, 0))
        
        self.frm2_AppearanceModeLbl_OptionMenu = customtkinter.CTkOptionMenu(self.frm2, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.frm2_AppearanceModeLbl_OptionMenu.grid(row=7, column=0, padx=20, pady=(10, 5))
                
        self.frm2_ScalingLbl = customtkinter.CTkLabel(self.frm2, text="UI Scaling:", anchor="w")
        self.frm2_ScalingLbl.grid(row=8, column=0, padx=20, pady=(10, 0))

        self.frm2_ScalingLbl_OptioneMenu = customtkinter.CTkOptionMenu(self.frm2, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.frm2_ScalingLbl_OptioneMenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        

        #---------------------------------------------------------------------------------------------
        #--------------------- 3 creacion del panel de datos -----------------------------------------
        #---------------------------------------------------------------------------------------------

        self.frm3_main = customtkinter.CTkFrame(self, corner_radius=10)
        self.frm3_main.grid(row=1, column=1, rowspan=2, columnspan=2,  padx=(10, 0), pady=(5, 0), sticky="nsew")
        self.frm3_main.grid_rowconfigure(0, weight=1)
        self.frm3_main.grid_columnconfigure(0, weight=1)

        #---------------------------------------------------------------------------------------------
        #------------------  Creacion del frame Home -------------------------------------------------

        

        self.home_textbox = customtkinter.CTkTextbox(self.frm3_main, font=('Courier',11))
        self.home_textbox.configure(state="normal", text_color=('#0D47A1','#F50057'))

        #---------------------------------------------------------------------------------------------
        #------------------  Creacion del frame Sensor Info ------------------------------------------

        self.vent_info_sensor = VentanaInfoSensor(self.frm3_main)
        
        self.configure_vent_info_sensor()

        #self.vent_info_sensor.grid(row=0, column=0, sticky="nsew")

        #---------------------------------------------------------------------------------------------
        #------------------  Creacion del frame Navigation Info---------------------------------------
        self.info_navigation_frame = customtkinter.CTkFrame(self.frm3_main, corner_radius=0, fg_color="transparent")

 
        #---------------------------------------------------------------------------------------------
        #--------------------- 4 creacion de la configuracion de comunicacion-------------------------
        #---------------------------------------------------------------------------------------------
        self.frm4 = customtkinter.CTkFrame(self)
        self.frm4.grid(row=1, column=3, padx=(10, 5), pady=(5, 0), sticky="nsew")
        self.frm4.grid_rowconfigure(5, weight=1)

        self.frm4_SerialLbl = customtkinter.CTkLabel(self.frm4, text="Comunicación de serial:", text_color=("#1565C0","#179DFF"),
                                                    font=customtkinter.CTkFont(size=14, weight="bold"))
        self.frm4_SerialLbl.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.frm4_ComSelectLbl = customtkinter.CTkLabel(self.frm4, text="Puerto serial: ", anchor="w")
        self.frm4_ComSelectLbl.grid(row=1, column=0, padx=20, pady=(5, 0))
        
        self.frm4_ComSelect_OptionMenu = customtkinter.CTkOptionMenu(self.frm4, values=self.list_ports,
                                                                    command=self.changue_serial_com)
        self.frm4_ComSelect_OptionMenu.grid(row=2, column=0, padx=30, pady=(0, 0))

        self.frm4_BaudSelectLbl  = customtkinter.CTkLabel(self.frm4, text="Baudios:", anchor="w")
        self.frm4_BaudSelectLbl.grid(row=3, column=0, padx=20, pady=(20, 0))
        
        self.frm4_BaudSelectLbl_OptionMenu = customtkinter.CTkOptionMenu(self.frm4, values=self.list_baudrate,
                                                                     command=self.changue_serial_baud)
        self.frm4_BaudSelectLbl_OptionMenu.grid(row=4, column=0, padx=30, pady=(0, 20))
        
        self.frm4_SerialBtn = customtkinter.CTkButton(self.frm4, fg_color="transparent", textvariable=self.serial_button_txtvariable,
                                                     border_width=2,text_color=("gray10", "#DCE4EE"), command=self.push_serial_button)
        self.frm4_SerialBtn.grid(row=6, column=0, padx=(30, 30), pady=(20, 30), sticky="nsew")

        
        #---------------------------------------------------------------------------------------------
        #--------------------- 5 creacion del Frame configuracion de lectura, escritura de data-------
        #---------------------------------------------------------------------------------------------

        self.frm5_rs_data = customtkinter.CTkFrame(self)
        self.frm5_rs_data.grid(row=2, column=3, padx=(10, 5), pady=(5, 0), sticky="nsew")
        self.frm5_rs_data.grid_rowconfigure(3, weight=1)

        self.read_save_label = customtkinter.CTkLabel(self.frm5_rs_data, text="Lectura y escritura \n de data:", text_color=("#1565C0","#179DFF"),
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.read_save_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.read_button = customtkinter.CTkButton(self.frm5_rs_data, fg_color="transparent", text="Leer data \n de simulacion",
                                                    image=self.csv_image, anchor="w", border_width=2,text_color=("gray10", "#DCE4EE"),
                                                    command=self.plot_data_sensor)
        self.read_button.grid(row=2, column=0, padx=(30, 30), pady=(20, 20), sticky="nsew")

        self.save_button = customtkinter.CTkButton(self.frm5_rs_data, fg_color="transparent", text="Grabar data \n simulacion",
                                                    image=self.play_image, anchor="w",
                                                     border_width=2,text_color=("gray10", "#DCE4EE"), command=self.push_serial_button)
        self.save_button.grid(row=4, column=0, padx=(30, 30), pady=(20, 20), sticky="nsew")



        # self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
        #                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        #                                            image=self.home_image, anchor="w", command=self.home_button_event)
        
        ##---------------------- 6 - 7 ------------------------------
        #-6-7-------------crear entrada y botón en la parte inferior---------------
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Message")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text="Enviar",
                                                     text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


        ################################Inicializar valores###############################3
        #-------set values----
        #self.select_frame_by_name("home")
        #self.appearance_mode_optionemenu.set("Dark")
        #self.scaling_optionemenu.set("100%")
        
        #self.home_textbox.insert("0.0", "\n\n")

        self.select_frame_by_name("Home")

        banner1 = AsciiA.welcome_mtrx()
        banner2 = AsciiA.cohete_mtrx()
        self.current_position = 0
        self.update_banner(banner1+ [''] * 2 + banner2, self.home_textbox)

        self.actualizar_hora()

    #-----------------------Emular lectura de sensores-----------------------------
    
    def sine_function_generator(self):
        while True:
            value = math.sin(self.t * 0.1)
            self.t += 1
            yield value

    def cosine_function_generator(self):
        while True:
            value = math.cos(self.t * 0.1)
            self.t += 1
            yield value

    def data_acel(self):
        Accel = imu.getAccIMU()
        #Accelx = Accel[:,0]
        for value in Accel:
            #print("Produciendo valor:", value)
            yield value

    def data_gyro(self):
        Giro= imu.getGyroIMU()
        #Accelx = Accel[:,0]
        for value in Giro:
            #print("Produciendo valor:", value)
            yield value

    def data_mag(self):
        Accel = imu.getMagIMU()
        #Accelx = Accel[:,0]
        for value in Accel:
            #print("Produciendo valor:", value)
            yield value

    def configure_vent_info_sensor(self):
        #------------- Acelerometro-------------
        self.vent_info_sensor.fig_frame_00.set_title(title="Lecturas del acelerómetro")
        self.vent_info_sensor.fig_frame_00.add_line(func="AX", label='ax', linewidth=0.6)
        self.vent_info_sensor.fig_frame_00.add_line(func="AY", label='ay', linewidth=0.6)
        self.vent_info_sensor.fig_frame_00.add_line(func="AZ", label='az', linewidth=0.6)
        self.vent_info_sensor.fig_frame_00.set_y_limits(-5, 5)
        self.vent_info_sensor.fig_frame_00.customize_legend(show=True, loc='upper right', title='Acel lin')



        #------------- Giroscopio-------------
        self.vent_info_sensor.fig_frame_01.set_title(title="Lecturas del giroscopio")
        self.vent_info_sensor.fig_frame_01.add_line(func="GX", label='gx', linewidth=0.6)
        self.vent_info_sensor.fig_frame_01.add_line(func="GY", label='gy', linewidth=0.6)
        self.vent_info_sensor.fig_frame_01.add_line(func="GZ", label='gz', linewidth=0.6)
        self.vent_info_sensor.fig_frame_01.set_y_limits(-5,5)
        self.vent_info_sensor.fig_frame_01.customize_legend(show=True, loc='upper right', title='Giroscopio')

        #------------- Magnetometro----------
        self.vent_info_sensor.fig_frame_10.set_title(title="Lecturas del magnetómetro")
        self.vent_info_sensor.fig_frame_10.add_line(func="MX", label='mx', linewidth=0.6)
        self.vent_info_sensor.fig_frame_10.add_line(func="MY", label='my', linewidth=0.6)
        self.vent_info_sensor.fig_frame_10.add_line(func="MZ", label='mz', linewidth=0.6)

        self.vent_info_sensor.fig_frame_10.set_y_limits(-40, 40)
        self.vent_info_sensor.fig_frame_10.customize_legend(show=True, loc='upper right', title='Magnetómetro')



        #------------- Barometro-------------
        self.vent_info_sensor.fig_frame_11.set_title(title="Presión atmosférica (hPa)")
        self.vent_info_sensor.fig_frame_11.add_line(func="PA", label='Pa', linewidth=0.6)

        self.vent_info_sensor.fig_frame_11.set_y_limits(950, 1050)
        

        #-------------  Label Temperatura----
        self.vent_info_sensor.frame_02_lbl_00.configure(text="Temperatura (°C)")

        #------------- Label Altura------
        self.vent_info_sensor.frame_12_lbl_00.configure(text="Altura (m)")



    def plot_data_sensor(self):
        self.vent_info_sensor.fig_frame_00.add_line(func="AccX", label='AccX', linewidth=0.5)
        self.vent_info_sensor.fig_frame_00.add_line(func="AccY", label='AccY', linewidth=0.5)
        self.vent_info_sensor.fig_frame_00.add_line(func="AccZ", label='AccZ', linewidth=0.5)
        l_min =int( np.min(imu.getAccIMU())) -2
        l_max =int( np.max(imu.getAccIMU())) +2
        self.vent_info_sensor.fig_frame_00.set_y_limits(l_min, l_max)
        self.vent_info_sensor.fig_frame_00.customize_legend(show=True, loc='upper right', title='Acelerometro')

        self.vent_info_sensor.fig_frame_01.add_line(func="GX", label='GX', linewidth=0.5)
        self.vent_info_sensor.fig_frame_01.add_line(func="GY", label='GY', linewidth=0.5)
        self.vent_info_sensor.fig_frame_01.add_line(func="GZ", label='GZ', linewidth=0.5)
        l_min =int( np.min(imu.getGyroIMU())) -2
        l_max =int( np.max(imu.getGyroIMU())) +2
        self.vent_info_sensor.fig_frame_01.set_y_limits(l_min, l_max)
        self.vent_info_sensor.fig_frame_01.customize_legend(show=True, loc='upper right', title='Giroscopio')

        self.vent_info_sensor.fig_frame_10.add_line(func="MX", label='MX', linewidth=0.5)
        self.vent_info_sensor.fig_frame_10.add_line(func="MY", label='MY', linewidth=0.5)
        self.vent_info_sensor.fig_frame_10.add_line(func="MZ", label='MZ', linewidth=0.5)
        l_min =int( np.min(imu.getMagIMU())) -2
        l_max =int( np.max(imu.getMagIMU())) +2
        self.vent_info_sensor.fig_frame_10.set_y_limits(l_min, l_max)
        self.vent_info_sensor.fig_frame_10.customize_legend(show=True, loc='upper right', title='Magnetómetro')

        self.update_plot()
        #self.acc_plot.add_new_data(0, new_cosine_value)

    def update_plot(self):
        try:
            valac = next(self.generador_acel)
            valgy = next(self.generador_gyro)
            valmg = next(self.generador_mag)
        except StopIteration:
            # Todos los valores del generador han sido agotados
            self.after_cancel(self.after_id)
            return
        
        self.vent_info_sensor.fig_frame_00.add_new_data(0,valac[0])
        self.vent_info_sensor.fig_frame_00.add_new_data(1,valac[1])
        self.vent_info_sensor.fig_frame_00.add_new_data(2,valac[2])

        self.vent_info_sensor.fig_frame_01.add_new_data(0,valgy[0])
        self.vent_info_sensor.fig_frame_01.add_new_data(1,valgy[1])
        self.vent_info_sensor.fig_frame_01.add_new_data(2,valgy[2])

        self.vent_info_sensor.fig_frame_10.add_new_data(0,valmg[0])
        self.vent_info_sensor.fig_frame_10.add_new_data(1,valmg[1])
        self.vent_info_sensor.fig_frame_10.add_new_data(2,valmg[2])


        self.after_id = self.after(4, self.update_plot)

    #%&-----------OBJETOS----------------------------------

    def changue_serial_com(self, new_com):
        self.COM = new_com

    def changue_serial_baud(self, new_baud):
        self.BAUD = new_baud

    def push_serial_button(self):
        print("Conectar puerto serial")
        if self.serial_obj.is_connect():  # Si ya estamos conectados, desconectar
            #00C853
            print("Desconectando...")
            self.add_data_textbox("COMUNICACIÓN SERIAL DESCONECTADO","#9C27B0")
            self.serial_button_txtvariable.set("Conectar")
            self.serial_obj.disconnect()
        else :  # Si hay puertos disponibles
            try:
                self.serial_obj.connect(self.COM, self.BAUD)
                print("Conectando a", self.COM,self.BAUD)
                self.add_data_textbox("COMUNICACIÓN SERIAL CONECTADO A " + self.COM,"#9C27B0")

                self.serial_button_txtvariable.set("Desconectar")
                self.after(100, self.check_queue)  # Comprobar la cola cada 100 ms
            except Exception as e:
                print(e)
    

    def check_queue(self):
        while not self.serial_obj.data_queue.empty():
            data = self.serial_obj.data_queue.get()
            print("Datos recibidos: ", data)

            if "SenC1" in data:
                # estructura de data:
                #  SenC1, ax, ay, az, gx, gy, gz, mx, my, mz, temp, pres,  altura
                try:
                    l_data = data.split(",")
                    
                    accel_C1 = [float(l_data[1]), float(l_data[2]),float(l_data[3])]
                    gyro_C1  = [float(l_data[4]), float(l_data[5]),float(l_data[6])]
                    mag_C1   = [float(l_data[7]), float(l_data[8]),float(l_data[9])]
                    temp_C1  = float(l_data[10])
                    pres_C1  = float(l_data[11])
                    alt_C1   = float(l_data[12])

                    self.vent_info_sensor.fig_frame_00.add_new_data(0, accel_C1[0])
                    self.vent_info_sensor.fig_frame_00.add_new_data(1, accel_C1[1])
                    self.vent_info_sensor.fig_frame_00.add_new_data(2, accel_C1[2])

                    self.vent_info_sensor.fig_frame_01.add_new_data(0, gyro_C1[0])
                    self.vent_info_sensor.fig_frame_01.add_new_data(1, gyro_C1[1])
                    self.vent_info_sensor.fig_frame_01.add_new_data(2, gyro_C1[2])

                    self.vent_info_sensor.fig_frame_10.add_new_data(0, mag_C1[0])
                    self.vent_info_sensor.fig_frame_10.add_new_data(1, mag_C1[1])
                    self.vent_info_sensor.fig_frame_10.add_new_data(2, mag_C1[2])

                    self.vent_info_sensor.fig_frame_11.add_new_data(0, pres_C1)

                    #-------------  Temperatura----
                    self.vent_info_sensor.frame_02_lbl_10.configure(text = str(temp_C1) + "°C")

                    #------------- Altura------
                    self.vent_info_sensor.frame_12_lbl_10.configure(text=str(alt_C1) + "m")


                    cadena = f"SenC1-> Acce: {accel_C1} \t Gyro: {gyro_C1} \t Mag: {mag_C1} \t temp: {temp_C1} \t pres: {pres_C1}"
                    self.add_data_textbox(cadena)
                except:
                    pass

            elif "DataC1" in data:

                #  DataC1, ax, ay, az, vx, vy, vz, px, py, pz, q0, q1, q2, q3
                try:
                    l_data = data.split(",")
                    
                    Acc_C1   = [float(l_data[1]), float(l_data[2]),float(l_data[3])]
                    Vel_C1   = [float(l_data[4]), float(l_data[5]),float(l_data[6])]
                    Pos_C1   = [float(l_data[7]), float(l_data[8]),float(l_data[9])]
                    Ori_C1   = [float(l_data[10]), float(l_data[11]), float(l_data[12]), float(l_data[13]) ]
                    

                    #9C27B0 -> morado
                    self.add_data_textbox(data, "#00C853")
                except:
                    pass

            elif "DataC2" in data:
                #9C27B0 -> amarillo
                self.add_data_textbox(data, "#D4AC0D")
                
            else :
                self.add_data_textbox(data, "#F50057")

            #self.textbox.insert("0.0", "Some example text!\n" * 50)
            # Aquí puedes hacer lo que necesites con los datos
        self.after(50, self.check_queue)  # Programar el próximo chequeo

    #---------------OBJETOS DE TEXTBOX ---------------------------------

    def add_data_textbox(self, data, color="#304FFE"):
        tag = "tag" + str(self.home_textbox.index(tk.INSERT).split('.')[0]) # Crear una tag única para cada línea
        self.home_textbox.insert(tk.END, data + "\n", tag)
        self.home_textbox.tag_config(tag, foreground=color) # Configurar la tag
        self.home_textbox.see(tk.END)


    def update_banner(self, banner, textbox):
        max_length = max(len(line) for line in banner)
        self.current_position += 1

        if self.current_position > max_length:
            return

        textbox.delete('1.0', tk.END)

        for line in banner:
            textbox.insert(tk.END, line[:self.current_position].ljust(max_length) + '\n')

        self.after(50, lambda: self.update_banner(banner, textbox))

    def actualizar_hora(self):
        hora_modificada = datetime.now() - timedelta(hours=0)
        # Formatear la hora modificada a una cadena
        
        hora_actual = hora_modificada.strftime("%H:%M:%S")
        self.frm1_ClockLbl.configure(text=hora_actual)
        self.frm1_ClockLbl.after(1000, self.actualizar_hora)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.frm2_HomeBtn.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frm2_C1_InfoSenBtn.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frm2_C1_InfoNavBtn.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "Home":
            self.home_textbox.grid(row=0, column=0, sticky="nsew")
        else:
            self.home_textbox.grid_forget()
        if name == "InfoSensor":
            self.vent_info_sensor.grid(row=0, column=0, sticky="nsew")
        else:
            self.vent_info_sensor.grid_forget()
        if name == "InforNavi":
            self.info_navigation_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.info_navigation_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("Home")

    def frame_2_button_event(self):
        self.select_frame_by_name("InfoSensor")

    def frame_3_button_event(self):
        self.select_frame_by_name("InforNavi")
    



    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        try:
            self.vent_info_sensor.set_vent_mode(new_appearance_mode)
        except:
            pass

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def insert_colorful_text(self, text):
        colors = ['red', 'green', 'blue', 'purple', 'orange', 'brown', 'pink']
        self.home_textbox.insert('end', text )
        
        #for a in text:
        #    self.home_textbox.insert('end', a + '\n')
            #self.home_textbox.configure(tag, font=('Currier',12), text_color = (colors[1],colors[-2]))
        #self.home_textbox.configure(tag, text_color = (colors[1],colors[-2]))

    
    def set_geometry_panel(self,screem_percet=0.7):
         # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular el % del tamaño de la pantalla
        window_width = int(screen_width * screem_percet)
        window_height = int(screen_height * screem_percet)

        # print("Dimension minima")
        # print("x", window_width )
        # print("y", window_height)
        # Calcular la posición de la ventana para que esté centrada en la pantalla
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)

        # Configurar el tamaño y la posición de la ventana
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    def on_close(self):
        # Limpia y cierra el hilo cuando se cierra la aplicación
        #self.serial_thread.stop()
        #self.serial_thread.join()

        if self.serial_obj.is_connect():  # Si ya estamos conectados, desconectar
            print("Desconectando...")
            self.add_data_textbox("COMUNICACIÓN SERIAL DESCONECTADO","#9C27B0")
            self.serial_button_txtvariable.set("Conectar")
            self.serial_obj.disconnect()

        self.destroy()
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
