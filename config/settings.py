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
    "apertura": (6, 12), # 8 horas
    "Partido_1": (8, 12), # 4 horas
    "Partido_2": (16, 20), # 4 horas
    "cierre": (12, 18) # 8 horas
}

# numero de cajeras disponibles a evaluar 
N_CAJERAS = 16  

# rutas de datasets
DATASET = BASE_DIR / 'data' / 'ventas.csv'