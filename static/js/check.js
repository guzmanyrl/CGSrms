document.addEventListener('DOMContentLoaded', function () {
    const successCheckmark = document.getElementById('successCheckmark');
    const message = document.getElementById('message');

    if (message && message.classList.contains('success') && message.textContent.includes('OTP verified successfully')) {
        // Show the checkmark GIF
        successCheckmark.style.display = 'block';

        // Hide the OTP form wrapper
        document.getElementById('wrapper1').style.display = 'none';

        // Redirect to login page after 2 seconds
        setTimeout(function () {
            window.location.href = message.dataset.redirectUrl;
        }, 2000);
    }
});
