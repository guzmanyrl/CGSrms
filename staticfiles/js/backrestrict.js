// Redirect to login if history navigation is detected
window.addEventListener("pageshow", function (event) {
    if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
        window.location.href = "{% url 'accounts:home_login' %}";
    }
});