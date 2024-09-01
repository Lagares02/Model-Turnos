# sistema de gestion de turnos 
Sistema encarga do de crear cronogrmas de asignacion de turnos de trabajo 

## /logic :
### Asignador de Turnos

La clase `AsignadorTurnos` se encarga de asignar turnos a un grupo de cajeras en base a un cronograma mensual o semanal. La asignación de turnos se realiza considerando diversos factores como la cantidad de días trabajados por cada cajera, los días consecutivos trabajados, y las restricciones para evitar sobrecarga laboral.

### 1. Inicialización

Al crear una instancia de la clase `AsignadorTurnos`, se proporcionan dos parámetros principales:
- **Cajeras**: Una lista de nombres de las cajeras que serán asignadas a los turnos.
- **Tipo de Cronograma**: Define si el cronograma es mensual o semanal.

La clase inicializa varios atributos:
- **`tipo_cronograma`**: Indica si el cronograma es para un mes o una semana.
- **`dias_semana`**: Lista con los días de la semana en español.
- **`cajeras_info`**: Diccionario que almacena información sobre cada cajera, incluyendo días trabajados, horas trabajadas, días de descanso y otros detalles relevantes.
- **`turnos_por_dia`**: Define la cantidad de turnos por tipo de turno (Apertura, Medio, Cierre).
- **`cronograma`**: Lista que almacenará la asignación de turnos por día.
- **`dias_asignados`**: Número de días para los cuales se realizarán asignaciones.

### 2. Orden de Prioridad

Para decidir qué cajera debe ser asignada a un turno específico, se utiliza un criterio de prioridad basado en:
- **Número de días trabajados**: Las cajeras con menos días trabajados tienen mayor prioridad.
- **Número de días consecutivos**: Se intenta evitar asignar turnos consecutivos a las cajeras para prevenir sobrecarga laboral.
![Ejemplo de Gráfico de ordenamiento de empleados por prioridad Prioridad](./logic/orden%20de%20prioridad.png)

### 3. Restricciones y Validaciones

Antes de asignar un turno, se verifican varias restricciones:
- **Días Consecutivos**: Se evita asignar turnos a una cajera en días consecutivos para prevenir el agotamiento.
- **Días Anteriores**: Se comprueba si la cajera trabajó en el día anterior y, si es así, se intenta evitar asignarla nuevamente el día actual.
- **Cantidad de Días Trabajados**: Se asegura que la carga de trabajo esté equilibrada entre las cajeras.

### 4. Asignación de Turnos

Dependiendo del tipo de cronograma (mensual o semanal), se determina la cantidad de días a asignar. Luego, para cada día, se asignan los turnos en función de la prioridad calculada. Se actualizan los registros de las cajeras, incluyendo:
- **Número de días trabajados**.
- **Horas trabajadas**.
- **Fechas y días específicos de trabajo**.

### 5. Generación del Cronograma

Una vez asignados los turnos, se genera un cronograma que incluye:
- **Día del mes o semana**.
- **Asignación de turnos**: Qué cajera está asignada a cada tipo de turno en cada día.

Además, se proporciona un informe detallado sobre el desempeño de cada cajera, incluyendo la cantidad de días trabajados y días consecutivos trabajados.


## Ejemplo de Uso

```python
# Crear una instancia del asignador de turnos
asignador = AsignadorTurnos(cajeras, "mes")

# Asignar los turnos para el período seleccionado
asignador.asignar_turnos(datetime(2024, 2, 1))

# Mostrar el cronograma
asignador.mostrar_cronograma()
