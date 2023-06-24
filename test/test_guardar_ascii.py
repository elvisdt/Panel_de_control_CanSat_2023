# Definir contenido de la imagen
contenido = '_-`-|\\//|'

# Definir colores correspondientes
colores = {
    '_': '\033[37m', # Blanco
    '`': '\033[31m', # Rojo
    '-': '\033[33m', # Amarillo
    '|': '\033[32m', # Verde
    '\\': '\033[34m', # Azul
    '/': '\033[35m' # Morado
}

# Abrir archivo en modo escritura
with open('imagen.asc', 'w') as f:
    # Recorrer cada caracter del contenido
    for caracter in contenido:
        # Escribir caracter con su color correspondiente
        f.write(colores[caracter] + caracter)

    # Restablecer color por defecto al final
    f.write('\033[0m')