# serial_obj.py

import serial
import serial.tools.list_ports
import threading
import queue

class SerialObj:
    def __init__(self):
        self.serial_thread = None
        self.data_queue = queue.Queue()

    @staticmethod
    def get_ports():
        list_ports = serial.tools.list_ports.comports()
        name_ports = [port.device for port in list_ports]
        return name_ports

    def connect(self, port, baudrate):
        self.serial_thread = SerialThread(port, baudrate, self.data_queue)
        self.serial_thread.start()
        
    def is_connect(self):
        return self.serial_thread and self.serial_thread.serial.isOpen()

    def get_data(self):
        if not self.is_connect():
            return None
        else:
            return self.serial_thread.serial.readline()

    def disconnect(self):
        if self.serial_thread is None:
            return
        self.serial_thread.stop()
        self.serial_thread.join()
        self.serial_thread = None


class SerialThread(threading.Thread):
    def __init__(self, serial_port, baud_rate, data_queue):
        super().__init__()
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.data_queue = data_queue
        self.serial = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        self.alive = threading.Event()
        self.alive.set()

    def run(self):
        while self.alive.isSet():
            try: 
                data = self.serial.readline().decode('utf-8').strip()
                if data:
                    self.data_queue.put(data)  # Enviar los datos a la cola
            except:
                pass


    def stop(self):
        self.alive.clear()
        self.serial.close()


if __name__=="__main__":
    ps = SerialObj()
    nombres_puertos = ps.get_ports()
    print("Puertos seriales disponibles:", nombres_puertos)
