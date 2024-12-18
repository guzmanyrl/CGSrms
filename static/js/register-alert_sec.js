document.addEventListener('DOMContentLoaded', function () {
    // Function to hide the alert after 5 seconds
    const alert = document.querySelector('.alert'); // Select the alert element

    if (alert) {
        setTimeout(function () {
            alert.classList.add('hidden'); // Add 'hidden' class to fade out the alert
        }, 5000); // 5000 milliseconds = 5 seconds
    }
});
