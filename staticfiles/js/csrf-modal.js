document.addEventListener("htmx:configRequest", (event) => {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    event.detail.headers["X-CSRFToken"] = csrfToken;
});