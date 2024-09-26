document.addEventListener("DOMContentLoaded", () => {
    const listaEmpleados = document.getElementById("listaEmpleados");
    const listaCronogramas = document.getElementById("listaCronogramas");

    // Obtener la lista de cajeros desde la API y configurar como empleados iniciales
    fetch('/api/cajeros')
        .then(response => response.json())
        .then(data => {
            empleados = data.map((nombre, index) => ({
                id: index + 1, // Generar un ID simple para cada cajero
                nombre: nombre,
                cargo: "Cajero(a)"
            }));
            mostrarEmpleados(); // Llamar a la función para mostrar los empleados
        })
        .catch(error => console.error('Error al cargar cajeros:', error));

    let cronogramas = [
        { id: 1, tipo: "semanal", fechaInicio: "2023-06-01", fechaFin: "2023-06-07" },
        { id: 2, tipo: "mensual", fechaInicio: "2023-06-01", fechaFin: "2023-06-30" }
    ];

    // Función para mostrar empleados
    function mostrarEmpleados() {
        listaEmpleados.innerHTML = ""; // Limpiar la lista de empleados actual

        empleados.forEach(emp => {
            const empleadoDiv = document.createElement("div");
            empleadoDiv.className = "empleado-item"; // Puedes agregar alguna clase CSS para estilo

            // Crear contenido del empleado con el icono de eliminación
            empleadoDiv.innerHTML = `
            ${emp.nombre} - ${emp.cargo}
            <span class="eliminar-empleado" data-id="${emp.id}" title="Eliminar">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                </svg>
            </span>
        `;

            listaEmpleados.appendChild(empleadoDiv); // Añadir cada empleado a la lista
        });

        // Asignar eventos de eliminación a cada botón de eliminar
        document.querySelectorAll(".eliminar-empleado").forEach(button => {
            button.addEventListener("click", (e) => {
                const empleadoId = e.target.closest(".eliminar-empleado").getAttribute("data-id");
                eliminarEmpleado(empleadoId); // Llamar a la función de eliminar empleado
            });
        });
    }

    // Función para eliminar un empleado
    function eliminarEmpleado(empleadoId) {
        // Buscar el empleado a eliminar por su ID
        const empleado = empleados.find(emp => emp.id === parseInt(empleadoId));

        if (empleado) {
            // Mostrar confirmación antes de eliminar
            if (confirm(`¿Está seguro que desea eliminar a ${empleado.nombre}?`)) {
                // Eliminar el empleado del array
                empleados = empleados.filter(emp => emp.id !== parseInt(empleadoId));
                
                // Actualizar la lista de empleados en el servidor
                fetch('/api/eliminar_cajero', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ nombre: empleado.nombre })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Mostrar mensaje de éxito
                        alert(`Empleado ${empleado.nombre} eliminado exitosamente.`);
                        mostrarEmpleados(); // Actualizar la lista en el frontend
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        } else {
            alert("Empleado no encontrado");
        }
    }

    // Función para mostrar los cronogramas (con o sin filtro)
    function mostrarCronogramas(cronogramasFiltrados) {
        listaCronogramas.innerHTML = "";
        cronogramasFiltrados.forEach(cron => {
            const cronogramaDiv = document.createElement("div");
            cronogramaDiv.innerHTML = `
                <div class="cronograma-tarjeta">
                    <h3>${cron.tipo.charAt(0).toUpperCase() + cron.tipo.slice(1)}</h3>
                    <p>Inicio: ${new Date(cron.fechaInicio).toLocaleDateString()}</p>
                    <p>Fin: ${new Date(cron.fechaFin).toLocaleDateString()}</p>
                </div>`;
            listaCronogramas.appendChild(cronogramaDiv);
        });
    }

    // Función para filtrar cronogramas
    function filtrarCronogramas() {
        const filtroFechaInicio = document.getElementById("fechaInicioFiltro").value;
        const filtroFechaFin = document.getElementById("fechaFinFiltro").value;
        const filtroTipo = document.getElementById("filtroTipo").value;

        const cronogramasFiltrados = cronogramas.filter(cron => {
            const fechaInicio = new Date(cron.fechaInicio);
            const fechaFin = new Date(cron.fechaFin);
            
            // Filtrar por tipo
            let tipoValido = true;
            if (filtroTipo) {
                tipoValido = cron.tipo === filtroTipo;
            }

            // Filtrar por fecha de inicio
            let fechaInicioValida = true;
            if (filtroFechaInicio) {
                const fechaFiltroInicio = new Date(filtroFechaInicio);
                fechaInicioValida = fechaInicio >= fechaFiltroInicio;
            }

            // Filtrar por fecha de fin
            let fechaFinValida = true;
            if (filtroFechaFin) {
                const fechaFiltroFin = new Date(filtroFechaFin);
                fechaFinValida = fechaFin <= fechaFiltroFin;
            }

            return tipoValido && fechaInicioValida && fechaFinValida;
        });

        mostrarCronogramas(cronogramasFiltrados);
    }

    // Detectar cambios en los filtros y aplicar la función de filtrado
    document.getElementById("fechaInicioFiltro").addEventListener("change", filtrarCronogramas);
    document.getElementById("fechaFinFiltro").addEventListener("change", filtrarCronogramas);
    document.getElementById("filtroTipo").addEventListener("change", filtrarCronogramas);

    // Lógica para agregar un nuevo empleado
    document.getElementById("agregarEmpleado").addEventListener("click", () => {
        const nombre = document.getElementById("nombreEmpleado").value;
        const cargo = document.getElementById("cargoEmpleado").value;

        // Verificar que el cargo sea "Cajero(a)" y que el nombre no esté vacío
        if (nombre && cargo) {
            fetch('/api/add_cajero', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombre: nombre, cargo: cargo })
            })
            .then(response => response.json())
            .then(data => {
                // Mostrar alerta según la respuesta del servidor
                alert(data.message);

                // Si la respuesta es exitosa, agregar el empleado a la lista local
                if (data.success) {
                    empleados.push({ id: Date.now(), nombre, cargo });
                    mostrarEmpleados();
                }
            })
            .catch(error => console.error('Error al agregar empleado:', error));
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