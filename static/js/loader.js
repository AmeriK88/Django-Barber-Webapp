document.addEventListener('DOMContentLoaded', function() {
    const loader = document.getElementById('loader');

    function showLoader() {
        loader.style.display = 'block';
    }

    function hideLoader() {
        loader.style.display = 'none';
    }

    // Mostrar el loader al enviar un formulario
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            showLoader();
        });
    });

    // Mostrar el loader al hacer clic en un enlace que cargue otra vista
    const links = document.querySelectorAll('a');
    links.forEach(function(link) {
        link.addEventListener('click', function(event) {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#') && !link.hasAttribute('download')) {
                showLoader();
            }
        });
    });

    // Ocultar el loader cuando la página ha terminado de cargar
    window.addEventListener('load', function() {
        hideLoader();
    });
});