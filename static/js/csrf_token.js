// Get the CSRF token from the Django cookie
function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^;]*)/);
    return cookieValue ? cookieValue[1] : null;
}

// Add the CSRF token to all HTMX requests
document.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = getCSRFToken();
});