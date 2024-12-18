document.addEventListener('DOMContentLoaded', function () {
    const addStudentModal = document.getElementById('modal');

    addStudentModal.addEventListener('hidden.bs.modal', function () {
        const form = addStudentModal.querySelector('form');
        form.reset();
    });
});
