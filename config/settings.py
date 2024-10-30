from pathlib import Path
import json

# Carpeta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta al archivo JSON de cajeros
CAJEROS_FILE = BASE_DIR / 'config' / 'cajeros.json'
# Ruta al archivo JSON de cronogramas
CRONOGRAMAS_FILE = BASE_DIR / 'config' / 'cronogramas.json'

# Cargar cajeros desde el archivo JSON
def cargar_cajeros():
    with open(CAJEROS_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get("cajeros", [])

# Guardar cajeros en el archivo JSON
def guardar_cajeros(cajeros):
    with open(CAJEROS_FILE, 'w', encoding='utf-8') as file:
        json.dump({"cajeros": cajeros}, file, ensure_ascii=False, indent=4)

# Cargar cronogramas desde el archivo JSON
def cargar_cronogramas():
    with open(CRONOGRAMAS_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get("cronogramas", [])

# Guardar cronogramas en el archivo JSON
def guardar_cronogramas(cronogramas):
    with open(CRONOGRAMAS_FILE, 'w', encoding='utf-8') as file:
        json.dump({"cronogramas": cronogramas}, file, ensure_ascii=False, indent=4)

# Cargar lista de cajeros al iniciar
CAJEROS = cargar_cajeros()
# Cargar lista de cronogramas al iniciar
CRONOGRAMAS = cargar_cronogramas()

# distribucion de turnos 
TURNOS = {
    "apertura": (6, 14), # 8 horas
    "Partido_1": (8, 12), # 4 horas
    "Partido_2": (16, 19), # 3 horas
    "cierre": (12, 20) # 8 horas
}

"""TURNOS = {
    "inicioApertura (de 6 a 8)": (6, 8), # 2 horas
    "Apertura (de 8 a 13)": (8, 13), # 4 horas
    "Partido (de 13 a 14)": (13, 14), # 5 horas
    "Partido (de 14 a 16)": (14, 16), # 3 horas
    "cierre (de 16 a 19)": (16, 19), # 7 horas
    "Cierre (de 19 a 20)": (19, 20) # 2 horas
}"""


# numero de cajeras disponibles a evaluar 
N_CAJERAS = 17  

# rutas de datasets
DATASET = BASE_DIR / 'data' / 'ventas.csv'
DOMINGOS = BASE_DIR / 'data' / 'domingos.xlsx'