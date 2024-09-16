document.addEventListener('DOMContentLoaded', function () {
    const inputFecha = document.querySelector('input[name="fecha"]');

    if (inputFecha) {
        const today = new Date().toISOString().split('T')[0]; 
        inputFecha.setAttribute('min', today);  // Fecha mínima: hoy

        // Deshabilitar las fechas ocupadas
        inputFecha.addEventListener('focus', function() {
            const disabledDates = fechasOcupadas.map(fecha => new Date(fecha).toISOString().split('T')[0]);

            inputFecha.addEventListener('input', function() {
                const selectedDate = inputFecha.value;

                // Si la fecha seleccionada está en la lista de fechas ocupadas, mostrar alerta y limpiar el campo
                if (disabledDates.includes(selectedDate)) {
                    alert("La fecha seleccionada está completamente reservada. Por favor, selecciona otra.");
                    inputFecha.value = '';  // Limpiar selección
                }
            });
        });
    }
});
``
