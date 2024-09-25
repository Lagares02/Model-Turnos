from pathlib import Path

# carpeta rais del proyecto 
BASE_DIR = Path(__file__).resolve().parent.parent

# parameytros principales de manejo 

"""# distribucion de turnos 
TURNOS = {
    "apertura": (6, 12), # 6 horas
    "medio": (13, 17), # 4 horas
    "cierre": (18, 22) # 4 horas
}"""

"""# distribucion de turnos 
TURNOS = {
    "": (6, 14), # 8 horas
    "Partido_1": (8, 12), # 4 horas
    "Partido_2": (17, 20), # 4 horas
    "cierre": (12, 20) # 8 horas
}"""

"""# distribucion de turnos 
TURNOS = {
    "Apertura": (6, 14), # 8 horas
    "cierre": (12, 20) # 8 horas
}"""

# distribucion de turnos 
TURNOS = {
    "6-7": (6, 7),
    "7-8": (7, 8),
    "8-9": (8, 9),
    "9-10": (9, 10),
    "10-11": (10, 11),
    "11-12": (11, 12),
    "12-13": (12, 13),
    "13-14": (13, 14),
    "14-15": (14, 15),
    "15-16": (15, 16),
    "16-17": (16, 17),
    "17-18": (17, 18),
    "18-19": (18, 19),
    "19-20": (19, 20),
}

# numero de cajeras disponibles a evaluar 
N_CAJERAS = 15  

"""# numero de cajas disponibles 
CANTIDAD_CAJAS = 12 """

# rutas de datasets
DATASET = BASE_DIR / 'data' / 'ventas.csv'