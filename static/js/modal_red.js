document.addEventListener('DOMContentLoaded', function () {
    // Select the add student modal
    const addStudentModal = document.getElementById('modal');

    // Clear validation on modal close
    addStudentModal.addEventListener('hidden.bs.modal', function () {
        const formFields = addStudentModal.querySelectorAll('.is-invalid, .is-valid');
        formFields.forEach(field => {
            field.classList.remove('is-invalid', 'is-valid');
        });
    });
});
