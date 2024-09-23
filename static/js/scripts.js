document.addEventListener("DOMContentLoaded", () => {
    const listaEmpleados = document.getElementById("listaEmpleados");
    const listaCronogramas = document.getElementById("listaCronogramas");
    
    let empleados = [
        { id: 1, nombre: "Juan Pérez", cargo: "Gerente" },
        { id: 2, nombre: "María López", cargo: "Supervisor" },
        { id: 3, nombre: "Carlos Rodríguez", cargo: "Operario" }
    ];

    let cronogramas = [
        { id: 1, tipo: "semanal", fechaInicio: "2023-06-01", fechaFin: "2023-06-07" },
        { id: 2, tipo: "mensual", fechaInicio: "2023-06-01", fechaFin: "2023-06-30" }
    ];

    // Función para mostrar empleados
    function mostrarEmpleados() {
        listaEmpleados.innerHTML = "";
        empleados.forEach(emp => {
            const empleadoDiv = document.createElement("div");
            empleadoDiv.innerHTML = `${emp.nombre} - ${emp.cargo}`;
            listaEmpleados.appendChild(empleadoDiv);
        });
    }

    // Función para mostrar cronogramas
    function mostrarCronogramas() {
        listaCronogramas.innerHTML = "";
        cronogramas.forEach(cron => {
            const cronogramaDiv = document.createElement("div");
            cronogramaDiv.innerHTML = `${cron.tipo.charAt(0).toUpperCase() + cron.tipo.slice(1)}: ${cron.fechaInicio} - ${cron.fechaFin}`;
            listaCronogramas.appendChild(cronogramaDiv);
        });
    }

    // Lógica para agregar un nuevo empleado
    document.getElementById("agregarEmpleado").addEventListener("click", () => {
        const nombre = document.getElementById("nombreEmpleado").value;
        const cargo = document.getElementById("cargoEmpleado").value;
        
        if (nombre && cargo) {
            empleados.push({ id: Date.now(), nombre, cargo });
            mostrarEmpleados();
        }
    });

    // Lógica para generar un nuevo cronograma
    document.getElementById("generarCronograma").addEventListener("click", () => {
        const tipoTurno = document.getElementById("tipoTurnoSelect").value;
        const fechaInicio = document.getElementById("fechaInicio").value;
        const fechaFin = document.getElementById("fechaFin").value;

        if (fechaInicio && fechaFin) {
            cronogramas.push({ id: Date.now(), tipo: tipoTurno, fechaInicio, fechaFin });
            mostrarCronogramas();
        }
    });

    mostrarEmpleados();
    mostrarCronogramas();
});