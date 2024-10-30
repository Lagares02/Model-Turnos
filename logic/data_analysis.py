import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import pprint

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import DATASET, TURNOS, N_CAJERAS, DOMINGOS

# Cargar datos desde el archivo CSV
df = pd.read_csv(DATASET, delimiter=';')

# Convertir columnas de fecha y hora en un solo campo de tipo datetime
df['datetime'] = pd.to_datetime(df['fecha'] + ' ' + df['Hora'], dayfirst=True, errors='coerce')

# Verificar si hubo errores en la conversión
if df['datetime'].isnull().any():
    print("Advertencia: Algunas fechas no pudieron ser convertidas correctamente.")

# Filtrar filas donde la conversión fue exitosa
df = df[df['datetime'].notna()]

# Conversión de columnas
df['cantidad_numeric'] = df['cantidad'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
df['unidades_kilo'] = df['cantidad_numeric'] / 1000  # Conversión de cantidad a unidades kilo
df['month'] = df['datetime'].dt.month
df['day_of_month'] = df['datetime'].dt.day
df['hour'] = df['datetime'].dt.hour
print(f"\n{df.head(10)}\n")

print(f"---------------------------------------------------- DESCRIBE ----------------------------------------------------\n{df.describe()}\n------------------------------------------------------------------------------------------------------------------")

# Función para obtener métricas y proporciones
def obtener_metricas_y_proporcion(df, turnos, total_cajeras_disponibles):
    """
    # Calcular el promedio de unidades kilo por día
    promedio_unidades_kilo_dia = (df.groupby('day_of_month')['unidades_kilo'].sum())
    """
    # Agrupamos por mes y día para obtener la suma de unidades kilo de cada día en cada mes
    suma_unidades_kilo_por_dia_y_mes = df.groupby(['month', 'day_of_month'])['unidades_kilo'].sum()

    # Calculo el promedio de las sumas de cada día del mes (como si fuese 1 mes)
    promedio_unidades_kilo_dia = suma_unidades_kilo_por_dia_y_mes.groupby('day_of_month').mean()

    # Calcular el umbral
    umbral = promedio_unidades_kilo_dia.mean()

    # Identificar días de mayor demanda (por encima del umbral)
    dias_mayor_demanda = promedio_unidades_kilo_dia[promedio_unidades_kilo_dia > umbral].index

    # Asignar el tipo de día (mayor demanda o normal)
    df['tipo_dia'] = df['day_of_month'].apply(lambda x: 'mayor_demanda' if x in dias_mayor_demanda else 'normal')

    metrics = {}
    
    df = df.dropna(subset=['Hora'])

    # Cálculo de métricas por tipo de día
    for tipo_dia in ['normal', 'mayor_demanda']:
        df_tipo_dia = df[df['tipo_dia'] == tipo_dia]
        unidades_kilo_por_hora = df_tipo_dia.groupby(['day_of_month', 'hour'])['unidades_kilo'].sum()
        unidades_kilo_por_hora = unidades_kilo_por_hora.groupby('hour').mean()

        """unidades_kilo_por_hora = df.groupby(['day_of_month', 'hour'])['unidades_kilo'].sum()

        unidades_kilo_por_hora = unidades_kilo_por_hora.groupby('hour').mean()"""

        prom_unidades_kilo_por_turnos = {}
        for turno, (inicio, fin) in turnos.items():
            unidades_kilo_turno = unidades_kilo_por_hora.loc[inicio:fin].mean() if not unidades_kilo_por_hora.loc[inicio:fin].empty else 0
            prom_unidades_kilo_por_turnos[turno] = unidades_kilo_turno

        metrics[tipo_dia] = {
            'unidades_kilo_por_hora': unidades_kilo_por_hora.to_dict(),
            'prom_unidades_kilo_por_turnos': prom_unidades_kilo_por_turnos
        }
    
    # Cálculo de cajas por turno y proporciones para ambos tipos de día
    for tipo_dia in ['normal', 'mayor_demanda']:
        prom_unidades_kilo_por_turnos = metrics[tipo_dia]['prom_unidades_kilo_por_turnos']

        total_prom_unidades_kilo = sum(prom_unidades_kilo_por_turnos.values())
        cajas_por_turno = {}
        proporciones = {}

        for turno, promedio in prom_unidades_kilo_por_turnos.items():
            proporcion = promedio / total_prom_unidades_kilo if total_prom_unidades_kilo > 0 else 0
            proporciones[turno] = proporcion
            cajas_asignadas = round(total_cajeras_disponibles * proporcion)
            cajas_por_turno[turno] = cajas_asignadas

        # Añadir las cajas por turno y las proporciones al diccionario de métricas
        metrics[tipo_dia]['cajas_por_turno'] = cajas_por_turno
        metrics[tipo_dia]['proporciones'] = proporciones

    return metrics, promedio_unidades_kilo_dia, umbral

# Ejemplo de uso de la función
metrics, promedio_unidades_kilo_dia, umbral = obtener_metricas_y_proporcion(df, TURNOS, N_CAJERAS)

# Imprimir los resultados
print("\n##### METRICAS: #####")
for tipo_dia, data in metrics.items():
    print("\n------------------------------------------------------------------------------------------------------------------")
    print(f"\n{tipo_dia.capitalize()}:")
    print("Unidades kilo por hora:")
    pprint.pprint(data['unidades_kilo_por_hora'])
    print("Promedio de unidades kilo por turnos:")
    pprint.pprint(data['prom_unidades_kilo_por_turnos'])
    print("Proporciones de unidades kilo por turno:")
    pprint.pprint(data['proporciones'])
    print("Cajas por turno:")
    pprint.pprint(data['cajas_por_turno'])
print("\n------------------------------------------------------------------------------------------------------------------")
print("\nPromedio de unidades kilo por día:")
print(promedio_unidades_kilo_dia)
print(f"\nUmbral: {umbral}")

print("\nGenerando graficas...")

# Graficar resultados
# 1. Unidades kilo por días en promedio (con umbral)

# Crear DataFrame con el promedio de unidades kilo por día
promedio_unidades_kilo = pd.DataFrame({
    'Día': promedio_unidades_kilo_dia.index,
    'Promedio_unidades_kilo': promedio_unidades_kilo_dia.values
})

# Crear el gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x='Día', y='Promedio_unidades_kilo', data=promedio_unidades_kilo, palette='viridis')

# Dibujar la línea del umbral
plt.axhline(y=umbral, color='red', linestyle='--', label=f'Umbral ({umbral:.2f})')

# Añadir título y etiquetas
plt.title('Promedio de Unidades Kilo por Día y el Umbral')
plt.xlabel('Días')
plt.ylabel('Promedio de Unidades Kilo')
plt.legend()

# Mostrar gráfico
plt.tight_layout()
plt.show()

# 2. Unidades kilo promedio en días normales y de mayor demanda

# Extraer los datos para días normales y de mayor demanda
promedio_unidades_kilo_normales = metrics['normal']['unidades_kilo_por_hora']
promedio_unidades_kilo_mayor_demanda = metrics['mayor_demanda']['unidades_kilo_por_hora']

# Crear gráfico comparativo
plt.figure(figsize=(10, 6))

# Dibujar líneas para las franjas horarias
plt.axvline(x=6, color='purple', linestyle='--', label='Apertura')
plt.axvline(x=12, color='blue', linestyle='--', label='Cierre')
plt.axvline(x=8, color='green', linestyle='--', label='Partido 1')
plt.axvline(x=16, color='green', linestyle='--', label='Partido 2')
plt.axvline(x=14, color='purple', linestyle='--')
plt.axvline(x=20, color='blue', linestyle='--')
plt.axvline(x=19, color='green', linestyle='--')

# Graficar datos de días normales
plt.plot(promedio_unidades_kilo_normales.keys(), promedio_unidades_kilo_normales.values(), label='Días Normales', marker='o', color='blue')

# Graficar datos de días de mayor demanda
plt.plot(promedio_unidades_kilo_mayor_demanda.keys(), promedio_unidades_kilo_mayor_demanda.values(), label='Días de Mayor Demanda', marker='o', color='orange')

# Etiquetas y título
plt.xlabel('Horas del Día')
plt.ylabel('Unidades Kilo')
plt.title('Promedio de Unidades Kilo por Hora en Días Normales y Días de Mayor Demanda')
plt.legend()
plt.xticks(np.arange(6, 21, 1))  # Marcar cada hora relevante en el eje x
plt.xlim(5, 21)
plt.tight_layout()
plt.show()

################################################################################
# DOMINGOS
################################################################################

# Cargar el archivo Excel y las hojas 'leve' y 'movida'
xls = pd.ExcelFile(DOMINGOS)

# Leer las hojas
df_leve = pd.read_excel(xls, 'leve')
df_movida = pd.read_excel(xls, 'movida')

# Convertir la columna de 'fecha' a tipo datetime para extraer la hora
df_leve['fecha'] = pd.to_datetime(df_leve['fecha'])
df_movida['fecha'] = pd.to_datetime(df_movida['fecha'])

# Asegurarse de que la columna 'cantidad' sea string antes de aplicar reemplazos
df_leve['cantidad'] = df_leve['cantidad'].astype(str)
df_movida['cantidad'] = df_movida['cantidad'].astype(str)

# Convertir la columna 'cantidad' de texto a float, eliminando los puntos de miles y reemplazando comas con puntos
df_leve['cantidad_numeric'] = df_leve['cantidad'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
df_movida['cantidad_numeric'] = df_movida['cantidad'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

# Crear la nueva columna 'unidades_kilo' dividiendo por 1000
df_leve['unidades_kilo'] = df_leve['cantidad_numeric'] / 1000
df_movida['unidades_kilo'] = df_movida['cantidad_numeric'] / 1000

# Filtrar por el rango de horas de 6 a 19
df_leve_filtered = df_leve[(df_leve['fecha'].dt.hour >= 6) & (df_leve['fecha'].dt.hour <= 19)]
df_movida_filtered = df_movida[(df_movida['fecha'].dt.hour >= 6) & (df_movida['fecha'].dt.hour <= 19)]

# Calcular el promedio de la columna 'unidades_kilo' por hora
df_leve_avg = df_leve_filtered.groupby(df_leve_filtered['fecha'].dt.hour)['unidades_kilo'].sum()
df_movida_avg = df_movida_filtered.groupby(df_movida_filtered['fecha'].dt.hour)['unidades_kilo'].sum()

def obtener_metricas_domingos(df_leve, df_movida, turnos, total_cajeras_disponibles):
    metrics_domingo = {}

    for tipo_domingo, df_domingo in {'normal': df_leve, 'mayor_demanda': df_movida}.items():
        # Agrupación por hora para obtener la suma de unidades kilo
        unidades_kilo_por_hora = df_domingo.groupby(df_domingo['fecha'].dt.hour)['unidades_kilo'].sum()

        # Calcular promedio de unidades kilo por turno
        prom_unidades_kilo_por_turnos = {}
        for turno, (inicio, fin) in turnos.items():
            unidades_kilo_turno = unidades_kilo_por_hora.loc[inicio:fin].mean() if not unidades_kilo_por_hora.loc[inicio:fin].empty else 0
            prom_unidades_kilo_por_turnos[turno] = unidades_kilo_turno

        # Calcular proporciones y cajas por turno
        total_prom_unidades_kilo = sum(prom_unidades_kilo_por_turnos.values())
        cajas_por_turno = {}
        proporciones = {}

        for turno, promedio in prom_unidades_kilo_por_turnos.items():
            proporcion = promedio / total_prom_unidades_kilo if total_prom_unidades_kilo > 0 else 0
            proporciones[turno] = proporcion
            cajas_asignadas = round(total_cajeras_disponibles * proporcion)
            cajas_por_turno[turno] = cajas_asignadas

        # Almacenar métricas de domingo en el diccionario
        metrics_domingo[tipo_domingo] = {
            'unidades_kilo_por_hora': unidades_kilo_por_hora.to_dict(),
            'prom_unidades_kilo_por_turnos': prom_unidades_kilo_por_turnos,
            'cajas_por_turno': cajas_por_turno,
            'proporciones': proporciones
        }

    return metrics_domingo

# Obtener métricas de domingos
metrics_domingo = obtener_metricas_domingos(df_leve, df_movida, TURNOS, N_CAJERAS)

# Imprimir resultados
print("\n##### MÉTRICAS PARA DOMINGOS #####")
for tipo_domingo, data in metrics_domingo.items():
    print(f"\n{tipo_domingo.capitalize()}:")
    #print("Unidades kilo por hora:")
    #pprint.pprint(data['unidades_kilo_por_hora'])
    print("Promedio de unidades kilo por turnos:")
    pprint.pprint(data['prom_unidades_kilo_por_turnos'])
    print("Proporciones de unidades kilo por turno:")
    pprint.pprint(data['proporciones'])
    print("Cajas por turno:")
    pprint.pprint(data['cajas_por_turno'])


# Crear la figura y el gráfico de líneas
plt.figure(figsize=(10, 6))

# Graficar los promedios de unidades kilo para 'leve' y 'movida'
plt.plot(df_leve_avg.index, df_leve_avg.values, label='Domingos normales', marker='o')
plt.plot(df_movida_avg.index, df_movida_avg.values, label='Domingos mayor demanda', marker='o')

# Personalizar el gráfico
plt.title('Promedio de Unidades Kilo con Respecto a la Hora')
plt.xlabel('Horas')
plt.ylabel('Promedio de Unidades Kilo')
plt.xticks(range(6, 20))  # Mostrar las horas de 6 a 19
plt.legend()
plt.show()