document.body.addEventListener('htmx:afterRequest', function (event) {
    if (event.detail.xhr.status === 200) {
        const contentType = event.detail.xhr.getResponseHeader("Content-Type");
        if (contentType && contentType.includes("application/json")) {
            try {
                const response = JSON.parse(event.detail.xhr.responseText);
                if (response.redirect) {
                    window.location.href = response.redirect;
                }
            } catch (error) {
                console.error("Failed to parse JSON response:", error);
            }
        } else {
            console.log("Non-JSON response received, ignoring.");
        }
    }
});
