import tkinter as tk
import tkinter.messagebox
import customtkinter
from tkinter import font as tkFont
from time import strftime
import threading

import os
import sys
from PIL import Image
import math
import numpy as np
from datetime import datetime, timedelta

import ximu_python_library.xIMUdataClass as xIMU
from scipy import signal
import ahrs
from ahrs.common.orientation import q_prod, q_conj, acc2q, am2q, q2R, q_rot


from tkinter import filedialog

#-------Comunicacion serial--------

##librerias propias
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

import models.AsciiArt as AsciiA
#from controllers import serial_com as my_serial
import controllers.serial_obj as my_serial
from ui.frames.ventana_info_sensor import VentanaInfoSensor
from ui.frames.ventana_info_navigation import VentanaInfoNav





#------inicializar modo del HMI-----------
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



"""
-----------------------------------------------------
|       |                   1                       |
|       |--------------------------------------------
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
        
        self.set_geometry_panel(0.75)
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
            pass

        #----------------Variables de data ------------------------------#

        # Crear una variable para almacenar el estado del botón
        self.serial_button_txtvariable = tk.StringVar()
        self.serial_button_txtvariable.set("Conectar")

        
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
        self.frm1.grid(row=0, column=1, columnspan=3,padx=(10,5), pady=5, sticky="nsew")
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
        self.frm2.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.frm2.grid_rowconfigure(5, weight=1)

        #------------------contenedores del frm menu-------------------------
        self.frm2_TitleLbl = customtkinter.CTkLabel(self.frm2, text=" MENÚ", image=self.logo_image, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frm2_TitleLbl.grid(row=0, column=0, padx=(20,20), pady=(20,10))
                
        self.frm2_HomeBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent", text_color=("gray10", "gray90"),
                                                    hover_color=("gray70", "gray35"), image=self.home_image, anchor="w", command=self.home_button_event)
        self.frm2_HomeBtn.grid(row=1, column=0, sticky="ew")
    


        self.frm2_C1_InfoSenBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="C1: Info sensores", fg_color="transparent",
                                                          text_color=("gray10", "gray90"), hover_color=("gray70", "gray35"), image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frm2_C1_InfoSenBtn.grid(row=2, column=0, sticky="ew")

        self.frm2_C1_InfoNavBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="C1: Info navegación", fg_color="transparent",
                                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray35"), image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frm2_C1_InfoNavBtn.grid(row=3, column=0, sticky="ew")
        

        self.frm2_C2_InfoNavBtn = customtkinter.CTkButton(self.frm2, corner_radius=0, height=40, border_spacing=10, text="C2: Info navegación", fg_color="transparent",
                                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray35"), image=self.add_user_image, anchor="w", command=self.frame_4_button_event)
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

        self.C1_vent_info_sensor = VentanaInfoSensor(self.frm3_main)
        self.configure_C1_vent_info_sensor()

        #self.vent_info_sensor.grid(row=0, column=0, sticky="nsew")

        #---------------------------------------------------------------------------------------------
        #------------------  Creacion del frame Navigation Info---------------------------------------
        #self.C1_info_navigation_frame = customtkinter.CTkFrame(self.frm3_main, corner_radius=0, fg_color="transparent")
        self.C1_info_navigation_frame = VentanaInfoNav(self.frm3_main)
        self.configure_C1_vent_info_nav()


        self.C2_info_navigation_frame = VentanaInfoNav(self.frm3_main)

 
        #---------------------------------------------------------------------------------------------
        #--------------------- 4 creacion de la configuracion de comunicacion-------------------------
        #---------------------------------------------------------------------------------------------
        self.frm4 = customtkinter.CTkFrame(self)
        self.frm4.grid(row=1, column=3, padx=(10, 5), pady=(5, 0), sticky="nsew")
        self.frm4.grid_rowconfigure((5,8), weight=1)

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
        self.frm4_SerialBtn.grid(row=6, column=0, padx=(30, 30), pady=(20, 20), sticky="nsew")

        self.frm4_UpdatePortsBtn = customtkinter.CTkButton(self.frm4, fg_color="transparent", text = "Actualizar puertos",
                                                     border_width=2,text_color=("gray10", "#DCE4EE"), command=self.push_update_ports_button)
        self.frm4_UpdatePortsBtn.grid(row=7, column=0, padx=(30, 30), pady=(0, 20), sticky="nsew")

        
        #---------------------------------------------------------------------------------------------
        #--------------------- 5 creacion del Frame configuracion de lectura, escritura de data-------
        #---------------------------------------------------------------------------------------------

        self.frm5_rs_data = customtkinter.CTkFrame(self)
        self.frm5_rs_data.grid(row=2, column=3, padx=(10, 5), pady=(5, 0), sticky="nsew")
        self.frm5_rs_data.grid_rowconfigure((3,5), weight=1)

        self.read_save_label = customtkinter.CTkLabel(self.frm5_rs_data, text="Lectura y escritura \n de data:", text_color=("#1565C0","#179DFF"),
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.read_save_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.read_button = customtkinter.CTkButton(self.frm5_rs_data, fg_color="transparent", text="Leer data \n de simulacion",
                                                    image=self.csv_image, anchor="w", border_width=2,text_color=("gray10", "#DCE4EE"),
                                                    command=self.push_read_data_btn)
        self.read_button.grid(row=2, column=0, padx=(30, 30), pady=(20, 20), sticky="nsew")

        self.save_button = customtkinter.CTkButton(self.frm5_rs_data, fg_color="transparent", text="Grabar data \n simulacion",
                                                    image=self.play_image, anchor="w",
                                                     border_width=2,text_color=("gray10", "#DCE4EE"), command=self.push_save_data_btn)
        self.save_button.grid(row=4, column=0, padx=(30, 30), pady=(20, 20), sticky="nsew")



        # self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
        #                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        #                                            image=self.home_image, anchor="w", command=self.home_button_event)
        
        ##---------------------- 6 - 7 ------------------------------
        #-6-7-------------crear entrada y botón en la parte inferior---------------
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Message")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(10, 0), pady=(10, 10), sticky="nsew")
        
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text="Enviar",
                                                     text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(30, 30), pady=(10, 10), sticky="nsew")


        ################################Inicializar valores###############################3
        #-------set values----
        self.select_frame_by_name("Home")
        self.frm2_AppearanceModeLbl_OptionMenu.set("Dark")
        self.frm2_ScalingLbl_OptioneMenu.set("100%")
        
        #self.home_textbox.insert("0.0", "\n\n")

        banner1 = AsciiA.welcome_mtrx()
        banner2 = AsciiA.cohete_mtrx()
        self.current_position = 0
        self.update_banner(banner1+ [''] * 2 + banner2, self.home_textbox)

        self.actualizar_hora()

   
    #%&-----------OBJETOS----------------------------------

    def configure_C1_vent_info_sensor(self):
        #------------- Acelerometro-------------
        self.C1_vent_info_sensor.fig_frame_00.set_title(title="Lecturas del acelerómetro")
        self.C1_vent_info_sensor.fig_frame_00.add_line(func="AX", label='ax', linewidth=0.6)
        self.C1_vent_info_sensor.fig_frame_00.add_line(func="AY", label='ay', linewidth=0.6)
        self.C1_vent_info_sensor.fig_frame_00.add_line(func="AZ", label='az', linewidth=0.6)
        #self.vent_info_sensor.fig_frame_00.set_y_limits(-5, 5)
        self.C1_vent_info_sensor.fig_frame_00.customize_legend(show=True, loc='lower left', title='Acel lin')

        #------------- Barometro-------------
        self.C1_vent_info_sensor.fig_frame_10.set_title(title="Presión atmosférica (hPa)")
        self.C1_vent_info_sensor.fig_frame_10.add_line(func="PA", label='Pa', linewidth=0.6)
        #self.vent_info_sensor.fig_frame_11.set_y_limits(950, 1050)
        
        #-------------  Label Temperatura----
        self.C1_vent_info_sensor.frame_02_lbl_00.configure(text="Temperatura (°C)")

        #------------- Label Altura------
        self.C1_vent_info_sensor.frame_12_lbl_00.configure(text="Altura (m)")
 
    def configure_C1_vent_info_nav(self):
        #------------- aceleracion lineal global-------------
        self.C1_info_navigation_frame.fig_frame_00.set_title(title="Aceleracion global")
        self.C1_info_navigation_frame.fig_frame_00.add_line(func="AX", label='ax', linewidth=0.6)
        self.C1_info_navigation_frame.fig_frame_00.add_line(func="AY", label='ay', linewidth=0.6)
        self.C1_info_navigation_frame.fig_frame_00.add_line(func="AZ", label='az', linewidth=0.6)

        #self.vent_info_sensor.fig_frame_00.set_y_limits(-5, 5)
        self.C1_info_navigation_frame.fig_frame_00.customize_legend(show=True, loc='lower left', title='Acel lin')

        #------------- velocidad lineal global-------------
        self.C1_info_navigation_frame.fig_frame_01.set_title(title="Velocidad global")
        self.C1_info_navigation_frame.fig_frame_01.add_line(func="X", label='vx', linewidth=0.6)
        self.C1_info_navigation_frame.fig_frame_01.add_line(func="Y", label='vy', linewidth=0.6)
        self.C1_info_navigation_frame.fig_frame_01.add_line(func="Z", label='vz', linewidth=0.6)

        #self.vent_info_sensor.fig_frame_00.set_y_limits(-5, 5)
        self.C1_info_navigation_frame.fig_frame_01.customize_legend(show=True, loc='lower left', title='Acel lin')

        #------------- posicion lineal global-------------
        self.C1_info_navigation_frame.fig_frame_10.set_title(title="Posicion global")
        self.C1_info_navigation_frame.fig_frame_10.add_line(func="X", label='px', linewidth=0.6)
        self.C1_info_navigation_frame.fig_frame_10.add_line(func="Y", label='py', linewidth=0.6)
        self.C1_info_navigation_frame.fig_frame_10.add_line(func="Z", label='pz', linewidth=0.6)

        #self.vent_info_sensor.fig_frame_00.set_y_limits(-5, 5)
        self.C1_info_navigation_frame.fig_frame_10.customize_legend(show=True, loc='lower left', title='Acel lin')

        #------------- posicion Quaternions-------------
        self.C1_info_navigation_frame.fig_frame_11.set_title("orientacion global")        

        print("Configure naviagation")

    #-----------------------Configuracion puerto serial--------------------------
    
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
                self.iniciar_recepcion_datos()

                #self.after(100, self.check_queue)  # Comprobar la cola cada 100 ms

            except Exception as e:
                print(e)

    def iniciar_recepcion_datos(self):
        self.thread_recepcion = threading.Thread(target=self.recibir_datos)
        self.thread_recepcion.daemon = True  # Hilo en modo daemon para que se cierre cuando se cierre la aplicación
        self.thread_recepcion.start()

    def recibir_datos(self):
        while self.serial_obj.is_connect():
            datos_bytes = self.serial_obj.get_data()
            if datos_bytes:
                datos_decodificados = datos_bytes.decode('utf-8').strip()
                self.procesar_datos(datos_decodificados)

    def procesar_datos(self, datos):
        try:
            l_data = datos.split(",")
            if len(l_data)==13:
                print(l_data)

        except:
            pass

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

                    self.C1_vent_info_sensor.fig_frame_00.add_new_data(0, accel_C1[0])
                    self.C1_vent_info_sensor.fig_frame_00.add_new_data(1, accel_C1[1])
                    self.C1_vent_info_sensor.fig_frame_00.add_new_data(2, accel_C1[2])

                    self.C1_vent_info_sensor.fig_frame_10.add_new_data(0, pres_C1)

                    #-------------  Temperatura----
                    self.C1_vent_info_sensor.frame_02_lbl_10.configure(text = str(temp_C1) + "°C")

                    #------------- Altura------
                    self.C1_vent_info_sensor.frame_12_lbl_10.configure(text=str(alt_C1) + "m")


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
        self.frm2_HomeBtn.configure(fg_color=("gray75", "gray25") if name == "Home" else "transparent")
        self.frm2_C1_InfoSenBtn.configure(fg_color=("gray75", "gray25") if name == "frame2" else "transparent")
        self.frm2_C1_InfoNavBtn.configure(fg_color=("gray75", "gray25") if name == "frame3" else "transparent")
        self.frm2_C2_InfoNavBtn.configure(fg_color=("gray75", "gray25") if name == "frame4" else "transparent")

        # show selected frame
        if name == "Home":
            self.home_textbox.grid(row=0, column=0, sticky="nsew")
        else:
            self.home_textbox.grid_forget()
        if name == "frame2":
            self.C1_vent_info_sensor.grid(row=0, column=0, sticky="nsew")
        else:
            self.C1_vent_info_sensor.grid_forget()
        if name == "frame3":
            self.C1_info_navigation_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.C1_info_navigation_frame.grid_forget()
        
        if name == "frame4":
            self.C2_info_navigation_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.C2_info_navigation_frame.grid_forget()
            

    def home_button_event(self):
        self.select_frame_by_name("Home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame4")

    def push_update_ports_button(self):
        try:
            self.list_ports = self.serial_obj.get_ports()
            self.frm4_ComSelect_OptionMenu.configure(values =self.list_ports  )
            self.frm4_ComSelect_OptionMenu.set(self.list_ports[0])
            self.frm2_AppearanceModeLbl_OptionMenu.set("Dark")
        except:
            pass
    
    #-------- Lectura de data aplotear---------#
    def push_read_data_btn(self):
        current_directory = os.getcwd()
        filepath = filedialog.askopenfilename(initialdir=current_directory)
        self.samplePeriod = 1/256
        self.startTime = 4
        self.stopTime = 47
        if filepath !=None:
            # importando data
            self.xIMUdata = xIMU.xIMUdataClass(filepath, 'SampleRate', 1/self.samplePeriod)
            print("------data leida----")
            self.procesing_data()
    
    def procesing_data(self):
        tm = self.xIMUdata.CalInertialAndMagneticData.Time
        gyrX = self.xIMUdata.CalInertialAndMagneticData.gyroscope[:,0]
        gyrY = self.xIMUdata.CalInertialAndMagneticData.gyroscope[:,1]
        gyrZ = self.xIMUdata.CalInertialAndMagneticData.gyroscope[:,2]
        accX = self.xIMUdata.CalInertialAndMagneticData.accelerometer[:,0]
        accY = self.xIMUdata.CalInertialAndMagneticData.accelerometer[:,1]
        accZ = self.xIMUdata.CalInertialAndMagneticData.accelerometer[:,2]

        #solo se ejecutara entre un rango de tiempo
        indexSel = np.all([tm>=self.startTime,tm<=self.stopTime], axis=0)
        tm   = tm[indexSel]
        gyrX = gyrX[indexSel]
        gyrY = gyrY[indexSel]
        gyrZ = gyrZ[indexSel]
        accX = accX[indexSel]
        accY = accY[indexSel]
        accZ = accZ[indexSel]
        
        self.tm = tm

        # añadimos arr2 a arr1 apilándolos verticalmente
        self.acc_lin = np.hstack((accX.reshape(-1, 1), accY.reshape(-1, 1), accZ.reshape(-1, 1)))
        
        # Compute accelerometer magnitude
        acc_mag = np.sqrt(accX*accX+accY*accY+accZ*accZ)

        # HP filter accelerometer data
        filtCutOff = 0.001
        b, a = signal.butter(1, (2*filtCutOff)/(1/self.samplePeriod), 'highpass')
        acc_magFilt = signal.filtfilt(b, a, acc_mag, padtype = 'odd', padlen=3*(max(len(b),len(a))-1))
        acc_magFilt = np.abs(acc_magFilt)
        # LP filter accelerometer data
        filtCutOff = 5
        b, a = signal.butter(1, (2*filtCutOff)/(1/self.samplePeriod), 'lowpass')
        acc_magFilt = signal.filtfilt(b, a, acc_magFilt, padtype = 'odd', padlen=3*(max(len(b),len(a))-1))


        # Threshold detection
        stationary = acc_magFilt < 0.05
        # Compute orientation
        quat  = np.zeros((tm.size, 4), dtype=np.float64)

        # initial convergence
        initPeriod = 2
        indexSel = tm<=tm[0]+initPeriod
        gyr=np.zeros(3, dtype=np.float64)
        acc = np.array([np.mean(accX[indexSel]), np.mean(accY[indexSel]), np.mean(accZ[indexSel])])
        mahony = ahrs.filters.Mahony(Kp=1, Ki=0,KpInit=1, frequency=1/self.samplePeriod)
        q = np.array([1.0,0.0,0.0,0.0], dtype=np.float64)
        for i in range(0, 2000):
            q = mahony.updateIMU(q, gyr=gyr, acc=acc)
        
        # For all data
        for t in range(0,tm.size):
            if(stationary[t]):
                mahony.Kp = 0.5
            else:
                mahony.Kp = 0
            gyr = np.array([gyrX[t],gyrY[t],gyrZ[t]])*np.pi/180
            acc = np.array([accX[t],accY[t],accZ[t]])
            #print(gyrX[t],gyrY[t])
            quat[t,:]=mahony.updateIMU(q,gyr=gyr,acc=acc)

        self.quat_global = quat[:, [1, 2, 3, 0]]
        print(quat[1])

        # Rotate body accelerations to Earth frame
        acc = []
        for x,y,z,q in zip(accX,accY,accZ,quat):
            acc.append(q_rot(q_conj(q), np.array([x, y, z])))
        acc = np.array(acc)
        acc = acc - np.array([0,0,1])
        self.acc_global = acc 

        acc = acc * 9.81
        #------------------aceleracion global------------------
        
        # acc_offset = np.zeros(3)

        #--------calculo de velocidad----------------------
        vel = np.zeros(acc.shape)
        for t in range(1,vel.shape[0]):
            vel[t,:] = vel[t-1,:] + acc[t,:]*self.samplePeriod
            if stationary[t] == True:
                vel[t,:] = np.zeros(3)

        # Compute integral drift during non-stationary periods
        velDrift = np.zeros(vel.shape)
        stationaryStart = np.where(np.diff(stationary.astype(int)) == -1)[0]+1
        stationaryEnd = np.where(np.diff(stationary.astype(int)) == 1)[0]+1
        for i in range(0,stationaryEnd.shape[0]):
            driftRate = vel[stationaryEnd[i]-1,:] / (stationaryEnd[i] - stationaryStart[i])
            enum = np.arange(0,stationaryEnd[i]-stationaryStart[i])
            drift = np.array([enum*driftRate[0], enum*driftRate[1], enum*driftRate[2]]).T
            velDrift[stationaryStart[i]:stationaryEnd[i],:] = drift

        # Remove integral drift
        vel = vel - velDrift
        #------------velocidad-----------------
        self.vel_global = vel

        ##----------------------calculo ------------------------------------------
        # -------------------------------------------------------------------------
        # Compute translational position
        pos = np.zeros(vel.shape)
        for t in range(1,pos.shape[0]):
            pos[t,:] = pos[t-1,:] + vel[t,:]*self.samplePeriod

        self.pos_global = pos

        ##---------------graficar----------------------
        self.start_plotting()

        #print(vel.shape)
    def count_len_data(self):
        i = 1000
        while i <= len(self.tm):
            yield i
            i += 2
 
    def start_plotting(self):
        self.counter = self.count_len_data()  # Crea el generador
        self.update_plot_csv()  # Inicia la actualización de la trama

    def update_plot_csv(self):
        try:
            cont = next(self.counter)  # Usa el generador existente
        except StopIteration:
            # Todos los valores del generador han sido agotados
            self.after_cancel(self.after_id)
            return
        self.C1_vent_info_sensor.fig_frame_00.add_new_data(0, self.acc_lin[cont,0])
        self.C1_vent_info_sensor.fig_frame_00.add_new_data(1, self.acc_lin[cont,1])
        self.C1_vent_info_sensor.fig_frame_00.add_new_data(2, self.acc_lin[cont,2])

        self.C1_info_navigation_frame.fig_frame_00.add_new_data(0, self.acc_global[cont,0])
        self.C1_info_navigation_frame.fig_frame_00.add_new_data(1, self.acc_global[cont,1])
        self.C1_info_navigation_frame.fig_frame_00.add_new_data(2, self.acc_global[cont,2])

        self.C1_info_navigation_frame.fig_frame_01.add_new_data(0, self.vel_global[cont,0])
        self.C1_info_navigation_frame.fig_frame_01.add_new_data(1, self.vel_global[cont,1])
        self.C1_info_navigation_frame.fig_frame_01.add_new_data(2, self.vel_global[cont,2])

        self.C1_info_navigation_frame.fig_frame_10.add_new_data(0, self.pos_global[cont,0])
        self.C1_info_navigation_frame.fig_frame_10.add_new_data(1, self.pos_global[cont,1])
        self.C1_info_navigation_frame.fig_frame_10.add_new_data(2, self.pos_global[cont,2])

        self.C1_info_navigation_frame.fig_frame_11.rotate_cube('quaternion', self.normalizar_cuaterniones(self.quat_global[cont]))

        self.after_id = self.after(30, self.update_plot_csv)


    @staticmethod
    def normalizar_cuaterniones(orientacion):
        norma = np.linalg.norm(orientacion)
        return orientacion / norma
    
    def push_save_data_btn(self):
        print("push save btn data")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        try:
            self.C1_vent_info_sensor.set_vent_mode(new_appearance_mode)
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
        
        if self.serial_obj.is_connect():  # Si ya estamos conectados, desconectar
            print("Desconectando...")
            self.add_data_textbox("COMUNICACIÓN SERIAL DESCONECTADO","#9C27B0")
            self.serial_button_txtvariable.set("Conectar")
            self.serial_obj.disconnect()
        try:
            #self.thread_recepcion.stop()
            self.thread_recepcion.join()
        except:
            pass
        self.destroy()
        
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
