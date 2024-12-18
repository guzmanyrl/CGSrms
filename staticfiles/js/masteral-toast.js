(function () {
    const toastElement = document.getElementById("masteral-toast");
    const toastBody = document.getElementById("toast-body");
    const toast = new bootstrap.Toast(toastElement);

    htmx.on("showMessage", (e) => {
        toastBody.textContent = e.detail.value;
        toast.show();
    });
})();
