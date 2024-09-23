import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import locale
import os
import sys

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import N_CAJERAS

# Establecer el locale a español (deberás tenerlo instalado en tu sistema)
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class AsignadorTurnos:
    """
    Clase para asignar turnos a cajeras basado en un cronograma mensual o semanal.

    Attributes:
        tipo_cronograma (str): Tipo de cronograma ('mes' o 'semana').
        dias_semana (list): Lista de días de la semana en español.
        cajeras_info (dict): Información sobre las cajeras.
        turnos_por_dia (dict): Número de turnos por tipo de turno.
        cronograma (list): Lista de turnos asignados por día.
        dias_asignados (int): Número de días asignados en el mes o semana.
    """

    def __init__(self, cajeras, tipo_cronograma):
        """
        Inicializa una instancia de AsignadorTurnos.

        Args:
            cajeras (list): Lista de nombres de cajeras.
            tipo_cronograma (str): Tipo de cronograma ('mes' o 'semana').
        """
        self.tipo_cronograma = tipo_cronograma
        self.dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.cajeras_info = {
            nombre: {
                'dias_repetidos': [],
                'horas_trabajadas': 0,
                'dias_trabajados': 0,
                'dias_descanso': 0,
                'dias_consecutivos': 0,
                'ultimo_dia': -1,
                "fechas_asignadas":[]
            }
            for nombre in cajeras
        }
        self.turnos_por_dia = {
            "Apertura": 4,
            "Medio": 5,
            "Cierre": 1
        }
        self.cronograma = []
        self.dias_asignados = 0

    def orden_prioridad(self):
        """
        Ordena a las cajeras por número de días trabajados y días consecutivos.

        Returns:
            list: Lista de nombres de cajeras ordenadas por prioridad.
        """
        cajeras_ordenadas = sorted(
            self.cajeras_info.items(), key=lambda x: (x[1]['dias_trabajados'], x[1]['dias_consecutivos'])
        )
        return [cajera[0] for cajera in cajeras_ordenadas]

    def trabajo_dia_consecutivo(self, empleado, dia):
        """
        Determina si un empleado ha trabajado en el día anterior al día actual.

        Args:
            empleado (str): Nombre del empleado.
            dia (int): Día actual (índice 0 basado en el primer día).

        Returns:
            bool: True si el empleado trabajó en el día anterior, False en caso contrario.
        """
        ultimo_dia = self.cajeras_info[empleado]['ultimo_dia']
        if ultimo_dia == -1:
            return False
        return dia == ultimo_dia + 1

    def puede_trabajar(self, dia, empleado):
        """
        Verifica si un empleado puede trabajar en el día especificado.

        Args:
            dia (int): Día actual (índice 0 basado en el primer día).
            empleado (str): Nombre del empleado.

        Returns:
            bool: True si el empleado puede trabajar, False en caso contrario.
        """
        if dia == 0:
            return True
        dia_anterior = dia - 1
        dia_dos_anterior = dia - 2
        dias_trabajados = [self.cajeras_info[empleado]['ultimo_dia'] == dia_anterior,
                           self.cajeras_info[empleado]['ultimo_dia'] == dia_dos_anterior]

        return sum(dias_trabajados) < 2

    def cantidad_dias_del_mes(self, fecha):
        """
        Devuelve la cantidad de días del mes en cuestión.

        Args:
            fecha (datetime): Fecha del primer día del mes.

        Returns:
            int: Número de días en el mes.
        """
        # Devuelve la cantidad de días del mes en cuestión
        siguiente_mes = fecha.replace(day=28) + timedelta(days=4)
        ultimo_dia = siguiente_mes - timedelta(days=siguiente_mes.day)
        return ultimo_dia.day
    
    def asignar_turnos(self, fecha):
        """
        Asigna turnos a las cajeras para el período especificado.

        Args:
            fecha (datetime): Fecha del primer día del período.
        """
        # definimos los dias a asignar dependiendo si es mes o semana 
        if fecha.day == 1 and self.tipo_cronograma == "mes":
            dias_a_asignar = self.cantidad_dias_del_mes(fecha)
            self.dias_asignados = dias_a_asignar
        else:
            dias_a_asignar = 7
        
        for dia in range(dias_a_asignar):
            turnos_dia = {turno: [] for turno in self.turnos_por_dia}

            pers_dia = self.orden_prioridad()
           
            for turno, cant in self.turnos_por_dia.items():
                for _ in range(cant):
                    empleado = pers_dia[0]
                    if not self.puede_trabajar(dia, empleado):
                        pers_dia.append(pers_dia.pop(0))
                        empleado = pers_dia[0]

                    turnos_dia[turno].append(empleado)
                    pers_dia.remove(empleado)
                    pers_dia.append(empleado)

                    self.cajeras_info[empleado]["dias_trabajados"] += 1
                    self.cajeras_info[empleado]["horas_trabajadas"] += 8
                    self.cajeras_info[empleado]["dias_repetidos"].append(dia + 1)
                    fecha_asignada = fecha + timedelta(days=dia)
                    dia_fecha = fecha_asignada.strftime('%A')
                    self.cajeras_info[empleado]["fechas_asignadas"].append(f"{fecha_asignada.strftime('%Y-%m-%d')}({dia_fecha})")

                    if self.trabajo_dia_consecutivo(empleado, dia):
                        self.cajeras_info[empleado]["dias_consecutivos"] += 1
                    else:
                        self.cajeras_info[empleado]["dias_consecutivos"] = 1

                    self.cajeras_info[empleado]['ultimo_dia'] = dia

            
            self.cronograma.append(turnos_dia)

    def mostrar_cronograma(self):
        print(f"CRONOGRAMA {self.tipo_cronograma}")
        for i, turno_dia in enumerate(self.cronograma):
            dia_num = i + 1
            dia_semana = self.dias_semana[i % 7]
            print(f"Día {dia_num} ({dia_semana}):")
            for turn, empls in turno_dia.items():
                print(f"   {turn}: {empls}")

        print("\n informe de cajeras")
        for c, info in self.cajeras_info.items():
            print(c)
            for k,v in info.items():
                print(f"   {k}: {v}")

    
    def graf_prioridad(self,list_prioridad, dia_asignado ):
        
        # Extraer nombres de empleados y métricas
        nombres = [empleado for empleado in list_prioridad]
        dias_trabajados = [self.cajeras_info[empleado]['dias_trabajados'] for empleado in list_prioridad]
        dias_consecutivos = [self.cajeras_info[empleado]['dias_consecutivos'] for empleado in list_prioridad]
        
        # Configuración de las posiciones y el ancho de las barras
        x = np.arange(len(nombres))
        ancho_barras = 0.35  # Ancho de las barras

        # Crear la figura y los ejes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Graficar las barras para cada métrica
        barras1 = ax.bar(x - ancho_barras/2, dias_trabajados, ancho_barras, label='Días Trabajados')
        barras2 = ax.bar(x + ancho_barras/2, dias_consecutivos, ancho_barras, label='Días Consecutivos')

        # Añadir etiquetas, título y leyenda
        ax.set_xlabel('Empleados')
        ax.set_ylabel('Número de Días')
        ax.set_title(f'Prioridad de Empleados - Día Asignado {dia_asignado}')
        ax.set_xticks(x)
        ax.set_xticklabels(nombres, rotation=45, ha='right')
        ax.legend()

        # Añadir etiquetas de los valores encima de las barras
        def etiquetar_barras(barras):
            for barra in barras:
                altura = barra.get_height()
                ax.annotate('{}'.format(altura),
                            xy=(barra.get_x() + barra.get_width() / 2, altura),
                            xytext=(0, 3),  # 3 puntos verticales de desplazamiento
                            textcoords="offset points",
                            ha='center', va='bottom')

        etiquetar_barras(barras1)
        etiquetar_barras(barras2)

        # Ajustar el diseño
        plt.tight_layout()

        # Guardar la gráfica como una imagen en un archivo
        plt.savefig(f"prioridad_{dia_asignado}.png", format='png')
        plt.close()
        
        print(f"Gráfico guardado como ")



# test de la clase ----------------------------------------------------------------------

n = N_CAJERAS  # Número de cajeras
cajeras = [f'empleada_{i}' for i in range(1, n + 1)]


# Crear una instancia del asignador de turnos
asignador = AsignadorTurnos(cajeras,"mes")

fecha = datetime(2024, 2, 1)  # Ejemplo de fecha

# Asignar los turnos para el tipo de periodo selecionado 
asignador.asignar_turnos(fecha)

# Mostrar el cronograma
asignador.mostrar_cronograma()

print()

# Crear una instancia del asignador de turnos
asignador = AsignadorTurnos(cajeras,"semana")

fecha = datetime(2024, 9, 2)  # Ejemplo de fecha
# Asignar los turnos para el tipo de periodo selecionado 
asignador.asignar_turnos(fecha)

# Mostrar el cronograma
asignador.mostrar_cronograma()

