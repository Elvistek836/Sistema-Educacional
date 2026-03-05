document.addEventListener('DOMContentLoaded', function() {
    // Function to copy information from Mother to Guardian
    document.querySelectorAll('.copy-from-mother').forEach(button => {
        button.addEventListener('click', function() {
            const madreFields = document.querySelectorAll('[data-padre="Madre"]');
            const apoderadoFields = document.querySelectorAll('[data-apoderado]');

            madreFields.forEach((field, index) => {
                apoderadoFields[index].value = field.value;
            });
        });
    });

    // Function to copy information from Father to Guardian
    document.querySelectorAll('.copy-from-father').forEach(button => {
        button.addEventListener('click', function() {
            const padreFields = document.querySelectorAll('[data-padre="Padre"]');
            const apoderadoFields = document.querySelectorAll('[data-apoderado]');

            padreFields.forEach((field, index) => {
                apoderadoFields[index].value = field.value;
            });
        });
    });
});


