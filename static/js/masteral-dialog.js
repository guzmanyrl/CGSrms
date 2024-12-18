(function () {
    const modal = new bootstrap.Modal(document.getElementById("masteral-modal"));

    // Reinitialize the modal after HTMX swap
    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id === "masteral-dialog") {
            const modalDialog = document.getElementById("masteral-modal");
            if (modalDialog) {
                modal.show();
            }
        }
    });

    htmx.on("htmx:beforeSwap", (e) => {
        if (e.detail.target.id === "masteral-dialog" && !e.detail.xhr.response) {
            modal.hide();
            e.detail.shouldSwap = false;
        }
    });

    htmx.on("hidden.bs.modal", () => {
        document.getElementById("masteral-dialog").innerHTML = "";
    });
})();
