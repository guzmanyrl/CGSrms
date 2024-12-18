function filterTable() {
    // Get the value from the search input field
    const searchInput = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("#student-list .student-row");

    // Loop through all table rows to show/hide based on the search input
    rows.forEach(row => {
        // Retrieve cells for Student ID, First Name, and Last Name
        const studentId = row.cells[0].innerText.toLowerCase();
        const firstName = row.cells[1].innerText.toLowerCase();
        const lastName = row.cells[2].innerText.toLowerCase();

        // Check if any cell in the row contains the search input
        if (studentId.includes(searchInput) || firstName.includes(searchInput) || lastName.includes(searchInput)) {
            row.style.display = "";  // Show row if there’s a match
        } else {
            row.style.display = "none";  // Hide row if there’s no match
        }
    });
}
