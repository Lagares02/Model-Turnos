# Sistema de Gestión de Turnos

## Descripción

`MODEL-TURNOS` es un sistema para la gestión y generación de cronogramas de turnos de trabajo. Permite a los administradores crear y organizar turnos de empleados (por ejemplo, cajeros) y visualizar cronogramas semanales y mensuales.

## Estructura del proyecto

- `config/` -> Contiene la configuración general del sistema.
- `data/` -> Archivo donde se encuentra el csv para el analisis de los datos
- `logic/` -> Lógica del negocio para la asignación de turnos
- `static/` -> Archivos estáticos, como lo son el CSS y JS
- `templates/` -> Plantillas HTML utilizadas para la visualización de cronogramas y el home.
- `main.py` -> Script principal para iniciar la aplicación.

> [!TIP]
> Mantener una estructura modular del proyecto facilita el mantenimiento y la escalabilidad del mismo.

## Requisitos previos

- Python 3.8+
- Librerías necesarias: `Flask`


## Intalación

Pasos para configurar el proyecto localmente:

- Clona este repo:

```
git clone https://github.com/Lagares02/Model-Turnos.git
cd MODEL-TURNOS
```

## Uso

- Ejecutamos el archivo principal, con tan solo:

```
py main.py
```

> [!WARNING]
> Asegúrate de que el puerto `5000` esté libre para evitar conflictos con otras aplicaciones.

- Abre tu navegador y navega a `http://127.0.0.1:5000` para ver la app