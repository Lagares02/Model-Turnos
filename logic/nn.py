import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def combinar_imagenes_prioridad():
    # Rutas de las imágenes a combinar
    imagenes = [
        "prioridad_2024-02-01(jueves).png",
        "prioridad_2024-02-02(viernes).png",
        "prioridad_2024-02-03(sÃ¡bado).png",
        "prioridad_2024-02-04(domingo).png"
    ]

    # Verificar que todas las imágenes existan
    for img in imagenes:
        if not os.path.isfile(img):
            raise FileNotFoundError(f"La imagen {img} no se encuentra en el directorio actual.")

    # Leer las imágenes
    imgs = [mpimg.imread(img) for img in imagenes]

    # Configuración de la figura para combinar imágenes
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()

    for ax, img, nombre in zip(axes, imgs, imagenes):
        ax.imshow(img)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig("combinacion_prioridad.png", format='png')
    plt.show()

# Ejecutar la función
#combinar_imagenes_prioridad()


import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import locale
import os

# Establecer el locale a español (deberás tenerlo instalado en tu sistema)
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def generar_informe():
    informe_path = "informe_asignacion_turnos.txt"

    with open(informe_path, 'w', encoding='utf-8') as file:
        # Introducción al informe
        file.write("INFORME DE LÓGICA DE ASIGNACIÓN DE TURNOS\n")
        file.write("="*50 + "\n\n")

        # Explicación de la clase AsignadorTurnos
        file.write("1. Clase AsignadorTurnos\n")
        file.write("La clase AsignadorTurnos se encarga de gestionar la asignación de turnos a las cajeras.\n")
        file.write("A continuación, se explica cada parte de la lógica implementada en esta clase:\n\n")

        # Explicación del método __init__
        file.write("1.1 Método __init__\n")
        file.write("Este método inicializa la clase con la lista de cajeras y el tipo de cronograma (mes o semana).\n")
        file.write("Define las variables para el tipo de cronograma, los días de la semana, la información de las cajeras y los turnos por día.\n\n")

        # Explicación del método orden_prioridad
        file.write("1.2 Método orden_prioridad\n")
        file.write("Ordena a las cajeras en función de los días trabajados y los días consecutivos trabajados.\n")
        file.write("Devuelve una lista de cajeras ordenadas según estos criterios para priorizar su asignación de turnos.\n\n")

        # Explicación del método trabajo_dia_consecutivo
        file.write("1.3 Método trabajo_dia_consecutivo\n")
        file.write("Determina si un empleado ha trabajado en el día anterior al día actual.\n")
        file.write("Esto se utiliza para evitar asignar turnos consecutivos a los mismos empleados.\n\n")

        # Explicación del método puede_trabajar
        file.write("1.4 Método puede_trabajar\n")
        file.write("Verifica si un empleado puede trabajar en el día especificado según sus turnos recientes.\n")
        file.write("Asegura que no se asignen turnos a empleados que hayan trabajado en los dos días anteriores.\n\n")

        # Explicación del método cantidad_dias_del_mes
        file.write("1.5 Método cantidad_dias_del_mes\n")
        file.write("Calcula el número de días en el mes de una fecha dada.\n")
        file.write("Utiliza la fecha actual para determinar el último día del mes.\n\n")

        # Explicación del método asignar_turnos
        file.write("1.6 Método asignar_turnos\n")
        file.write("Asigna turnos a las cajeras para cada día del mes o semana, dependiendo del tipo de cronograma.\n")
        file.write("El método también genera gráficos de prioridad para cada día de asignación.\n\n")

        # Explicación del método mostrar_cronograma
        file.write("1.7 Método mostrar_cronograma\n")
        file.write("Muestra el cronograma generado en la consola, con detalles sobre los turnos asignados y la información de las cajeras.\n\n")

        # Explicación del método graf_prioridad
        file.write("1.8 Método graf_prioridad\n")
        file.write("Genera gráficos de barras que muestran la prioridad de los empleados en función de los días trabajados y consecutivos.\n\n")

        # Añadir imagen combinada
        file.write("2. Imagen de Prioridad Combinada\n")
        file.write("A continuación, se muestra la imagen combinada de las prioridades para las 4 iteraciones generadas:\n")
        
        # Añadir la imagen combinada al informe
        imagen_combinada = "combinacion_prioridad.png"
        if os.path.isfile(imagen_combinada):
            file.write(f"Imagen combinada guardada como {imagen_combinada}\n")
            file.write("![Imagen Combinada](combinacion_prioridad.png)\n")
        else:
            file.write("No se encontró la imagen combinada. Asegúrese de generar la imagen antes de ejecutar este informe.\n")

    print(f"Informe generado y guardado en {informe_path}")

# Ejecutar la función para generar el informe
generar_informe()
