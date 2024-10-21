document.addEventListener('DOMContentLoaded', () => {
    const inputFecha = document.querySelector('input[name="fecha"]');
    const inputHora = document.querySelector('select[name="hora"]');

    if (inputFecha) {
        inputFecha.addEventListener('focus', () => {
            const disabledDates = fechasOcupadas.map(fecha => new Date(fecha).toISOString().split('T')[0]);

            inputFecha.addEventListener('input', () => {
                const selectedDate = inputFecha.value;

                if (disabledDates.includes(selectedDate)) {
                    alert("La fecha seleccionada está completamente reservada. Por favor, selecciona otra.");
                    inputFecha.value = '';
                } else {
                    const horasOcupadas = horasOcupadasPorFecha[selectedDate] || [];

                    Array.from(inputHora.options).forEach(option => {
                        option.disabled = false;
                    });

                    horasOcupadas.forEach(hora => {
                        Array.from(inputHora.options).forEach(option => {
                            if (option.value === hora) {
                                option.disabled = true;
                            }
                        });
                    });
                }
            });
        });
    }
});
