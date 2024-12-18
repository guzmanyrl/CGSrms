let countdownElement = document.getElementById('countdown');
let countdownTime = parseInt(countdownElement.innerText);
let registrationUrl = document.getElementById('registrationUrl').getAttribute('data-url');

let countdownInterval = setInterval(() => {
    if (countdownTime > 0) {
        countdownTime--;
        countdownElement.innerText = countdownTime;  // Update the displayed countdown
    } else {
        clearInterval(countdownInterval);
        alert("OTP expired. Redirecting to registration.");
        window.location.href = registrationUrl;  // Redirect when expired
    }
}, 1000);  // Change to 1000 ms (1 second) for a proper countdown
