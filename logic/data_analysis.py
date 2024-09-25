import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import random
import sys
import os

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import DATASET, TURNOS, N_CAJERAS

# Cargar datos desde el archivo CSV
df = pd.read_csv(DATASET, delimiter=';')

print(df.info())

# Convertir columnas de fecha y hora en un solo campo de tipo datetime
df['datetime'] = pd.to_datetime(df['fecha'] + ' ' + df['Hora'], dayfirst=True, errors='coerce')

# Verificar si hubo errores en la conversión
if df['datetime'].isnull().any():
    print("Advertencia: Algunas fechas no pudieron ser convertidas correctamente.")

# Filtrar filas donde la conversión fue exitosa
df = df[df['datetime'].notna()]

# Asegurarse de que la conversión fue correcta
print(df['datetime'].dtype)

def promedio_ventas_por_hora(df, turnos):
    """
    Calcula y grafica el promedio de ventas por hora.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame que contiene los datos de ventas. Debe incluir una columna 'datetime' y 'vlr_neto'.
    turnos : dict
        Diccionario con los turnos de trabajo. Las claves son los nombres de los turnos y los valores son tuplas (inicio, fin).

    Retorna:
    --------
    pd.Series
        Serie de Pandas con las horas como índice y el promedio de ventas (vlr_neto) por hora.

    Ejemplo:
    --------
    >>> promedio_ventas_por_hora(df, TURNOS)
    hour
    7     15000.00
    8     20000.00
    9     18000.00
    10    22000.00
    dtype: float64
    """
    df['hour'] = df['datetime'].dt.hour
    promedio_ventas_por_hora = df.groupby('hour')['vlr_neto'].mean()

    # Graficar el promedio de ventas por hora
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(promedio_ventas_por_hora.index, promedio_ventas_por_hora.values, color='blue')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
    ax.set_title('Promedio de Ventas por Hora')
    ax.set_xlabel('Hora')
    ax.set_ylabel('Promedio de Ventas')

    # Líneas divisorias para los turnos
    for turno, (inicio, fin) in turnos.items():
        ax.axvline(inicio - 0.5, color='red', linestyle='--', label=f'Inicio {turno.capitalize()}' if inicio == 7 else "")
        ax.axvline(fin + 0.5, color='red', linestyle='--')

    ax.legend()
    plt.tight_layout()
    plt.show()

    return promedio_ventas_por_hora

def promedio_ventas_por_semana(df):
    """
    Calcula el promedio de ventas por semana y mes.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame que contiene los datos de ventas. Debe incluir una columna 'datetime' y 'vlr_neto'.

    Retorna:
    --------
    dict
        Diccionario con el promedio de ventas por semana para cada mes. La clave es el mes/año y el valor es otro diccionario
        con el rango de fechas de la semana como clave y el promedio de ventas como valor.

    Ejemplo:
    --------
    >>> promedio_ventas_por_semana(df)
    {
        '2023-07': {
            '01-Jul - 07-Jul': 15000.00,
            '08-Jul - 14-Jul': 17000.00
        },
        '2023-08': {
            '01-Aug - 07-Aug': 18000.00,
            '08-Aug - 14-Aug': 16000.00
        }
    }
    """
    df['week'] = df['datetime'].dt.isocalendar().week
    df['year_month'] = df['datetime'].dt.to_period('M').astype(str)

    promedio_por_semana_mes = {}
    for mes_año in sorted(df['year_month'].unique(), key=lambda x: pd.to_datetime(x, format='%Y-%m')):
        df_mes = df[df['year_month'] == mes_año]
        semanas_promedio = {}
        
        for semana in df_mes['week'].unique():
            df_semana = df_mes[df_mes['week'] == semana]
            fecha_inicio = df_semana['datetime'].min().strftime('%d-%b')
            fecha_fin = df_semana['datetime'].max().strftime('%d-%b')
            rango_fechas = f'{fecha_inicio} - {fecha_fin}'
            promedio_ventas_semana = df_semana['vlr_neto'].mean()
            semanas_promedio[rango_fechas] = promedio_ventas_semana
        
        promedio_por_semana_mes[mes_año] = semanas_promedio

    return promedio_por_semana_mes


def obtener_metricas_y_proporcion(df, turnos, total_cajeras_disponibles):
    """
    Calcula las métricas de promedio de facturas por hora y por turnos, tanto para días normales como de mayor demanda,
    y luego asigna cajas disponibles en función de la proporción de facturas por turno.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame que contiene los datos de facturación. Debe incluir una columna 'datetime' y 'documento'.
    turnos : dict
        Diccionario con los turnos de trabajo. Las claves son los nombres de los turnos y los valores son tuplas (inicio, fin).
    total_cajeras_disponiblles : int
        El número total de cajas disponibles para asignar entre los turnos.

    Retorna:
    --------
    dict
        Diccionario con las métricas de promedio de facturas por hora y por turnos, separadas por días normales y días de mayor demanda.
    dict
        Diccionario con los turnos como claves y el número de cajas asignadas a cada turno como valores.
    dict
        Diccionario con los turnos como claves y la proporción de facturas de cada turno como valores.
    """
    
    # Días del mes considerados como de mayor demanda (independiente del mes o año)
    #dias_mayor_demanda = {1, 2, 3, 14, 15, 16, 17, 18, 27, 28, 29}
    dias_mayor_demanda = {1, 2, 3, 4, 5, 6, 15, 16, 17, 18, 19, 20, 27, 28, 29}
    
    # Agregar columnas adicionales para el análisis
    df['date'] = df['datetime'].dt.date
    df['day_of_month'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['tipo_dia'] = df['day_of_month'].apply(lambda x: 'mayor_demanda' if x in dias_mayor_demanda else 'normal')

    metrics = {}
    
    # Cálculo de métricas por tipo de día
    for tipo_dia in ['normal', 'mayor_demanda']:
        df_tipo_dia = df[df['tipo_dia'] == tipo_dia]
        facturas_por_hora = df_tipo_dia.groupby('hour')['documento'].count()

        prom_facturas_por_turnos = {}
        for turno, (inicio, fin) in turnos.items():
            facturas_turno = facturas_por_hora.loc[inicio:fin].mean() if not facturas_por_hora.loc[inicio:fin].empty else 0
            prom_facturas_por_turnos[turno] = facturas_turno

        metrics[tipo_dia] = {
            'facturas_por_hora': facturas_por_hora.to_dict(),
            'prom_facturas_por_turnos': prom_facturas_por_turnos
        }
    
    # Cálculo de cajas por turno y proporciones para ambos tipos de día
    for tipo_dia in ['normal', 'mayor_demanda']:
        prom_facturas_por_turnos = metrics[tipo_dia]['prom_facturas_por_turnos']

        total_prom_facturas = sum(prom_facturas_por_turnos.values())
        cajas_por_turno = {}
        proporciones = {}

        for turno, promedio in prom_facturas_por_turnos.items():
            proporcion = promedio / total_prom_facturas if total_prom_facturas > 0 else 0
            proporciones[turno] = proporcion
            cajas_asignadas = round(total_cajeras_disponibles * proporcion)
            cajas_por_turno[turno] = cajas_asignadas

        # Añadir las cajas por turno y las proporciones al diccionario de métricas
        metrics[tipo_dia]['cajas_por_turno'] = cajas_por_turno
        metrics[tipo_dia]['proporciones'] = proporciones

    return metrics

# Ejemplo de uso de la función
metrics = obtener_metricas_y_proporcion(df, TURNOS, N_CAJERAS)

# Imprimir los resultados
print("Métricas por tipo de día:")
for tipo_dia, datos in metrics.items():
    print(f"{tipo_dia.capitalize()}:")
    print("Facturas por hora:")
    print(datos['facturas_por_hora'])
    print("Promedio de facturas por turnos:")
    print(datos['prom_facturas_por_turnos'])
    print("Cajas por turno:")
    print(datos['cajas_por_turno'])
    print("Proporciones de facturas por turno:")
    print(datos['proporciones'])
    print()