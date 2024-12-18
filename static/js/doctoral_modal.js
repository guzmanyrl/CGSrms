// Listen for modal close event and reset form
var modalElement = document.getElementById('doctoralFormModal');
modalElement.addEventListener('hidden.bs.modal', function () {
    // Reset the form fields when the modal is hidden
    var modalForm = modalElement.querySelector('form');
    if (modalForm) {
        modalForm.reset(); // Reset form fields
    }

    // Clear the backdrop and other states
    modalElement.classList.remove('show'); // Ensure the modal is completely closed
    document.body.classList.remove('modal-open'); // Ensure the backdrop is removed
    document.querySelector('.modal-backdrop').remove(); // Remove the backdrop element
});

