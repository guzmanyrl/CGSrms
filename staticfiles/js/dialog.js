(function () {
    const modal = new bootstrap.Modal(document.getElementById("modal"));

    // Reinitialize the modal after HTMX swap
    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id === "dialog") {
            const modalDialog = document.getElementById("modal");
            if (modalDialog) {
                modal.show();
            }
        }
    });

    htmx.on("htmx:beforeSwap", (e) => {
        if (e.detail.target.id === "dialog" && !e.detail.xhr.response) {
            modal.hide();
            e.detail.shouldSwap = false;
        }
    });

    htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = "";
    });
})();
