document.getElementById("delete-button").addEventListener("click", function (event) {
    event.preventDefault();

    // Confirm the deletion action
    if (confirm("Are you sure you want to delete the selected files?")) {
        // You may want to perform an AJAX request to delete files
        let form = document.querySelector("form");
        form.submit();  // Submit the form to delete the selected files
    }
});
