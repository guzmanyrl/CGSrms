// Function to show the loading icon
function showLoadingIcon() {
    document.getElementById("loadingIcon").style.display = "block";
}

// HTMX event listener to hide the loading icon after receiving a response
document.body.addEventListener('htmx:afterRequest', function () {
    document.getElementById("loadingIcon").style.display = "none";
});