document.getElementById("upload_btn").addEventListener("click", function () {
    const files = document.getElementById("file_input").files;
    const fileCategory = document.getElementById("file_category").value;

    // Validate file category and files
    if (!fileCategory) {
        alert("Please select a file category.");
        return;
    }

    if (files.length === 0) {
        alert("Please select at least one file to upload.");
        return;
    }

    // Prepare the form data to be sent in the POST request
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }
    formData.append('file_category', fileCategory);

    // Get CSRF token from cookie
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send the form data to the server via fetch
    fetch(uploadUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken, // Use CSRF token from the cookie
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json(); // Ensure the server responds with JSON
        })
        .then(data => {
            if (data.success) {
                alert("Files uploaded successfully.");
                location.reload(); // Refresh to show uploaded files
            } else {
                alert(data.error || "An error occurred while uploading files.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while uploading files.");
        });
});
