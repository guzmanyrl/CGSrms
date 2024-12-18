function showLoadingIcon() {
    document.getElementById("loadingIcon1").style.display = "block";
}

// HTMX event listener to hide the loading icon after receiving a response
document.body.addEventListener('htmx:afterRequest', function () {
    document.getElementById("loadingIcon1").style.display = "none";
});
