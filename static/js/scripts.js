document.addEventListener("DOMContentLoaded", () => {
    const listaEmpleados = document.getElementById("listaEmpleados");

    // Función para inicializar la lista de empleados al cargar la página
    function cargarEmpleados() {
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
    }

    cargarEmpleados();

    // Función para inicializar la lista de cronogramas al cargar la página
    function cargarCronogramas() {
        fetch('/api/cronogramas')
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data)) {
                    mostrarCronogramas(data);  // Pasa el array completo a la función
                } else {
                    console.error('Formato de datos incorrecto:', data);
                }
            })
            .catch(error => console.error('Error al cargar cronogramas:', error));
    }

    cargarCronogramas();

    // Función para mostrar empleados
    function mostrarEmpleados() {
        listaEmpleados.innerHTML = ""; // Limpiar la lista de empleados actual

        empleados.forEach(emp => {
            const empleadoDiv = document.createElement("div");
            empleadoDiv.className = "empleado-item";

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
                        location.reload();
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

    // Función para mostrar los cronogramas generados
    function mostrarCronogramas(cronogramas) {
        const listaCronogramas = document.getElementById("listaCronogramas");
        listaCronogramas.innerHTML = ""; // Limpia el contenido previo

        cronogramas.forEach(cron => {
            const cronogramaDiv = document.createElement("div");
            cronogramaDiv.className = "cronograma-tarjeta";  // Añadir clase para estilizar la tarjeta

            const tipoCronograma = cron.tipo.charAt(0).toUpperCase() + cron.tipo.slice(1);

            cronogramaDiv.innerHTML = `
            <div class="card">
                <span class="eliminar-cronograma" data-id="${cron.id}" title="Eliminar">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                    </svg>
                </span>
                <div class="card-body">
                    <h5 class="card-title">ID: ${cron.id}</h5>
                    <p class="card-text">Tipo: ${tipoCronograma}</p>
                    <a href="/cronogramas/${cron.tipo}/${cron.id}" class="ver-detalles">Ver Detalles</a>
                </div>
            </div>`;
            
            listaCronogramas.appendChild(cronogramaDiv);
        });

        // Añadir eventos de eliminación a cada ícono de eliminar
        document.querySelectorAll('.eliminar-cronograma').forEach(button => {
            button.addEventListener('click', function () {
                const id = this.getAttribute('data-id');
                eliminarCronograma(id);
            });
        });
    }

    // Función para eliminar un cronograma
    function eliminarCronograma(id) {
        if (confirm(`¿Estás seguro de que deseas eliminar el cronograma con ID: ${id}?`)) {
            fetch(`/api/cronogramas/${id}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                    alert('Cronograma eliminado correctamente.');
                    location.reload();
                    cargarCronogramas(); // Recargar la lista de cronogramas
                } else {
                    alert('Error al eliminar el cronograma.');
                }
            })
            .catch(error => console.error('Error al eliminar el cronograma:', error));
        }
    }

    cargarCronogramas();

    // Función para filtrar los cronogramas generados
    function filtrarCronogramas() {
        const filtroTipo = document.getElementById("filtroTipo").value;
        const fechaInicioFiltro = document.getElementById("fechaInicioFiltro").value;
        const listaCronogramas = document.getElementById("listaCronogramas");
    
        // Obtener los cronogramas del backend
        fetch('/api/cronogramas')
        .then(response => response.json())
        .then(cronogramas => {
            // Filtrar los cronogramas según el tipo y la fecha de inicio
            const filteredCronogramas = cronogramas.filter(cron => {
            const tipoCoincide = filtroTipo === "" || cron.tipo === filtroTipo;
            const fechaCoincide = fechaInicioFiltro === "" || cron.cronogramas.dia_1.fecha >= fechaInicioFiltro;
    
            return tipoCoincide && fechaCoincide;
            });
    
            // Mostrar los cronogramas filtrados
            mostrarCronogramas(filteredCronogramas);
        });
    }

    window.onload = function() {
        // Asignar la función de filtro al botón de filtrado
        document.getElementById('filtrarCronogramas').addEventListener('click', filtrarCronogramas);
    }

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
                    location.reload();
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

        if (fechaInicio) {
            // Llamar a la API para generar el cronograma
            fetch('/api/generar_cronograma', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ tipo_periodo: tipoTurno, fecha: fechaInicio }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);  // Mostrar mensaje de éxito
                    location.reload();
                    mostrarCronogramas(data.cronograma);  // Muestra el cronograma generado
                } else {
                    console.error('Error al generar cronograma:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    cargarCronogramas();

    mostrarEmpleados();
    mostrarCronogramas();
});