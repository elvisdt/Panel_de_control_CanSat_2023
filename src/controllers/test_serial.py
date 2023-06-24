import tkinter as tk
import threading
from serial_obj import SerialObj
import  time
class InterfazApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Crear la instancia de SerialObj
        self.ps = SerialObj()

        # Etiqueta para mostrar los datos
        self.etiqueta_datos = tk.Label(self, text="")
        self.etiqueta_datos.pack()

        # Conectar con el puerto serial
        puerto = "COM4" # obtener el nombre del puerto seleccionado en la interfaz
        velocidad = 115200 # obtener la velocidad seleccionada en la interfaz
        self.ps.connect(puerto, velocidad)

        # Iniciar la recepción de datos en un hilo separado
        self.iniciar_recepcion_datos()

    
    def recibir_datos(self):
        while True:
            if self.ps.is_connect():
                datos_bytes = self.ps.get_data()
                if datos_bytes:
                    datos_decodificados = datos_bytes.decode('utf-8').strip()
                    self.procesar_datos(datos_decodificados)

    def procesar_datos(self, datos):
        # Dividir la cadena de datos en sus componentes individuales
        componentes = datos.split(", ")
        if len(componentes) >= 13:
            data_c1 = componentes[0].split(":")[1]
            ax = float(componentes[1])
            ay = float(componentes[2])
            az = float(componentes[3])
            vx = float(componentes[4])
            vy = float(componentes[5])
            vz = float(componentes[6])
            px = float(componentes[7])
            py = float(componentes[8])
            pz = float(componentes[9])
            quatReal = float(componentes[10])
            quatI = float(componentes[11])
            quatJ = float(componentes[12])
            quatK = float(componentes[13])

            # Realizar el procesamiento adicional según sea necesario
            # ...

            # Actualizar la etiqueta de la interfaz con los datos procesados
            etiqueta_texto = f"DataC1: {data_c1}\n"
            etiqueta_texto += f"Aceleración lineal: ({ax}, {ay}, {az})\n"
            etiqueta_texto += f"Velocidad: ({vx}, {vy}, {vz})\n"
            etiqueta_texto += f"Posición: ({px}, {py}, {pz})\n"
            etiqueta_texto += f"Orientación: ({quatReal}, {quatI}, {quatJ}, {quatK})"
            self.etiqueta_datos.config(text=etiqueta_texto)

    def iniciar_recepcion_datos(self):
        thread_recepcion = threading.Thread(target=self.recibir_datos)
        thread_recepcion.daemon = True  # Hilo en modo daemon para que se cierre cuando se cierre la aplicación
        thread_recepcion.start()

if __name__ == "__main__":
    app = InterfazApp()
    app.mainloop()