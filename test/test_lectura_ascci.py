# Definir listas vacías para almacenar caracteres y colores
caracteres = []
colores = []

# Abrir archivo en modo lectura
with open('logo.asc', 'r') as f:
    # Leer contenido del archivo
    contenido = f.read()

# Recorrer cada caracter del contenido
for caracter in contenido:
    # Determinar color correspondiente al caracter
    if caracter == '_':
        color = '\033[37m' # Blanco
    elif caracter == '`':
        color = '\033[31m' # Rojo
    elif caracter == '-':
        color = '\033[33m' # Amarillo
    elif caracter == '|':
        color = '\033[32m' # Verde
    elif caracter == '\\':
        color = '\033[34m' # Azul
    elif caracter == '/':
        color = '\033[35m' # Morado
    else:
        color = '\033[0m' # Sin color

    # Agregar caracter y color a las listas correspondientes
    caracteres.append(caracter)
    colores.append(color)
    
# Imprimir listas de caracteres y colores
print('Caracteres:', caracteres)
print('Colores:', colores)
