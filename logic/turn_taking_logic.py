import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import locale
import os
import sys

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import N_CAJERAS, CAJEROS

# Establecer el locale a español (deberás tenerlo instalado en tu sistema)
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class AsignadorTurnos:
    def __init__(self, cajeras, tipo_cronograma):
        self.tipo_cronograma = tipo_cronograma
        self.dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        self.cajeras_info = {
            nombre: {
                'dias_repetidos': [],
                'horas_trabajadas': 0,
                'dias_trabajados': 0,
                'dias_descanso': 0,
                'dias_consecutivos': 0,
                'ultimo_dia': -1,
                "fechas_asignadas":[],
                "turnos": []
            }
            for nombre in cajeras
        }
        self.turnos_por_dia = {
            "Apertura": 4,
            "Partido": 6,
            "Cierre": 3
        }
        self.cronograma = []
        self.dias_asignados = 0

    def orden_prioridad(self):
        cajeras_ordenadas = sorted(
            self.cajeras_info.items(), key=lambda x: (x[1]['dias_trabajados'], x[1]['dias_consecutivos'])
        )
        return [cajera[0] for cajera in cajeras_ordenadas]

    def trabajo_dia_consecutivo(self, empleado, dia):
        ultimo_dia = self.cajeras_info[empleado]['ultimo_dia']
        if ultimo_dia == -1:
            return False
        return dia == ultimo_dia + 1

    def puede_trabajar(self, dia, empleado):
        if dia == 0:
            return True
        dia_anterior = dia - 1
        dia_dos_anterior = dia - 2
        dias_trabajados = [self.cajeras_info[empleado]['ultimo_dia'] == dia_anterior,
                           self.cajeras_info[empleado]['ultimo_dia'] == dia_dos_anterior]

        return sum(dias_trabajados) < 2

    def cantidad_dias_del_mes(self, fecha):
        # Devuelve la cantidad de días del mes en cuestión
        siguiente_mes = fecha.replace(day=28) + timedelta(days=4)
        ultimo_dia = siguiente_mes - timedelta(days=siguiente_mes.day)
        return ultimo_dia.day
    
    def asignar_turnos(self, fecha):
        # Días de mayor demanda para los domingos
        dias_mayor_demanda = {1, 2, 3, 4, 6, 15, 16, 17, 27, 28, 29, 30, 31}

        # Definir los días a asignar dependiendo si es mes o semana
        if fecha.day == 1 and self.tipo_cronograma == "mes":
            dias_a_asignar = self.cantidad_dias_del_mes(fecha)
            self.dias_asignados = dias_a_asignar
        else:
            dias_a_asignar = 7

        cronograma_dias = {}

        for dia in range(dias_a_asignar):
            fecha_asignada = fecha + timedelta(days=dia)
            es_domingo = fecha_asignada.weekday() == 6  # domingo es 6 en weekday()

            # Ajustar turnos para domingos según la demanda
            if es_domingo and fecha_asignada.day not in dias_mayor_demanda:
                turnos_dia_config = {"Apertura": 4, "Partido": 4, "Cierre": 2}
            else:
                turnos_dia_config = self.turnos_por_dia  # Usar la configuración por defecto para otros días

            turnos_dia = {turno: [] for turno in turnos_dia_config}
            pers_dia = self.orden_prioridad()

            for turno, cant in turnos_dia_config.items():
                for _ in range(cant):
                    empleado = pers_dia[0]
                    if not self.puede_trabajar(dia, empleado):
                        pers_dia.append(pers_dia.pop(0))
                        empleado = pers_dia[0]

                    turnos_dia[turno].append(empleado)
                    pers_dia.remove(empleado)
                    pers_dia.append(empleado)
                    
                    # Definir horas trabajadas según el turno y día de la semana
                    if turno == "Apertura":
                        horas_trabajadas = 8
                    elif turno == "Cierre":
                        horas_trabajadas = 7 if es_domingo else 8
                    elif turno == "Partido":
                        horas_trabajadas = 7
                    else:
                        horas_trabajadas = 0

                    # Actualizar la información de la cajera
                    self.cajeras_info[empleado]["dias_trabajados"] += 1
                    self.cajeras_info[empleado]["horas_trabajadas"] += horas_trabajadas
                    self.cajeras_info[empleado]["dias_repetidos"].append(dia + 1)
                    dia_fecha = fecha_asignada.strftime('%A')
                    self.cajeras_info[empleado]["fechas_asignadas"].append(f"{fecha_asignada.strftime('%Y-%m-%d')}({dia_fecha})")
                    self.cajeras_info[empleado]["turnos"].append(turno)

                    if self.trabajo_dia_consecutivo(empleado, dia):
                        self.cajeras_info[empleado]["dias_consecutivos"] += 1
                    else:
                        self.cajeras_info[empleado]["dias_consecutivos"] = 1

                    self.cajeras_info[empleado]['ultimo_dia'] = dia
                    
                    cronograma_dia_clave = f"dia_{dia + 1}"
                    cronograma_dias[cronograma_dia_clave] = {
                        "fecha": fecha_asignada.strftime('%Y-%m-%d'),
                        "turnos": turnos_dia
                    }

            self.cronograma.append(turnos_dia)

            for empleado in self.cajeras_info.keys():
                self.cajeras_info[empleado]["dias_descanso"] = dias_a_asignar - self.cajeras_info[empleado]["dias_trabajados"]

        return cronograma_dias, self.cajeras_info

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