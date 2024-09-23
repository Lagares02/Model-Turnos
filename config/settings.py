from pathlib import Path

# carpeta rais del proyecto 
BASE_DIR = Path(__file__).resolve().parent.parent

# parameytros principales de manejo 

# distribucion de turnos 
TURNOS = {"apertura": (6, 12), "medio": (13, 17), "cierre": (18, 22)}

# numero de cajeras disponibles a evaluar 
N_CAJERAS = 13  

# numero de cajas disponibles 
CANTIDAD_CAJAS = 10 

# rutas de datasets
DATASET = BASE_DIR / 'data' / 'ventas.csv'