document.addEventListener('DOMContentLoaded', function () {
    const loader = document.getElementById('loader');
    const form = document.querySelector('form');
    const submitButton = form?.querySelector("button[type='submit']");

    function showLoader() {
        if (loader) loader.style.display = 'block';
    }

    function hideLoader() {
        if (loader) loader.style.display = 'none';
    }
});

// Ckeditor5
const editors = document.querySelectorAll('textarea')

editors.forEach(editor => {
    editor.removeAttribute('required')
    ClassicEditor
        .create(editor)
        .catch(error => {
            console.error(error);
        })
});

// Tooltip
document.addEventListener("DOMContentLoaded", function () {
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
