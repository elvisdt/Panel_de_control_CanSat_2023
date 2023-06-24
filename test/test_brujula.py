import math
import matplotlib.pyplot as plt

def graficar_brujula(orientacion, distancia_centro):
    # Crear una figura y un eje polar
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    # Convertir la orientación a radianes
    orientacion_rad = math.radians(orientacion)

    # Calcular las coordenadas de la aguja
    x = math.sin(orientacion_rad)
    y = math.cos(orientacion_rad)

    # Graficar la aguja de la brújula
    ax.arrow(0, 0, x, y, alpha=0.5, width=0.02, edgecolor='black', facecolor='red', head_length=0.08)

    # Configurar los límites y etiquetas del eje polar
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Añadir más valores aquí para más aros
    ax.set_xticks([0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi, 5 * math.pi / 4, 3 * math.pi / 2, 7 * math.pi / 4])
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO'])
    ax.set_theta_zero_location("N")

    # Rotar las etiquetas para que coincidan con la orientación correcta
    ax.tick_params(axis='x', pad=1)

    # Mostrar las líneas de los aros en el gráfico
    ax.grid(True)

    # Calcular las coordenadas polares del objeto
    distancia_centro_norm = distancia_centro / ax.get_ylim()[1]  # Normalizar la distancia
    objeto_rad = math.radians(orientacion)
    objeto_r = distancia_centro_norm

    # Agregar el objeto en las coordenadas polares calculadas
    ax.plot(objeto_rad, objeto_r, marker='o', markersize=5, color='blue')

    # Mostrar el gráfico de la brújula
    plt.show()

# Ejemplo de uso
orientacion = 0  # Reemplaza este valor con tu propia orientación
distancia_centro = 0.5  # Reemplaza este valor con tu propia distancia
graficar_brujula(orientacion, distancia_centro)
