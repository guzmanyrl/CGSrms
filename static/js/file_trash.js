document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-file-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const confirmDelete = confirm("Are you sure you want to delete this file?");
            if (confirmDelete) {
                const fileId = this.getAttribute("data-file-id");
                const fileCategory = this.getAttribute("data-file-category");
                const url = this.getAttribute("data-url");

                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                        "HX-Request": "true",
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: `file_id=${fileId}&file_category=${fileCategory}`
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the DOM to reflect the deleted file
                            this.closest("li").remove();
                            alert("File deleted successfully.");
                        } else {
                            alert(data.error || "An error occurred.");
                        }
                    })
                    .catch(error => {
                        console.error("Error:", error);
                        alert("An error occurred. Please try again.");
                    });
            }
        });
    });
});
