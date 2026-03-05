// custom_admin.js
(function($) {
    $(document).ready(function() {
        // Aplica Select2 a todos los elementos <select> con clase 'custom-select'
        $('.form-select form-select-lg text-dark').select2({
            placeholder: 'Buscar...',
            allowClear: true,
        });
    });
})(django.jQuery);
