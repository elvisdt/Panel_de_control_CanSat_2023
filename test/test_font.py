import serial.tools.list_ports

def listar_puertos_seriales():
    lista_puertos = serial.tools.list_ports.comports()
    l_ports =[]
    for puerto in lista_puertos:
        l_ports.append(puerto.name)
        print(f"Dispositivo: {puerto.device}, Nombre: {puerto.name}, Descripción: {puerto.description}")

    print(l_ports)
if __name__ == "__main__":
    listar_puertos_seriales()


