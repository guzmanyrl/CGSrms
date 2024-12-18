// Updated JavaScript for filtering faculty table
function filterTable() {  // Change this to filterTable
    // Get the input element and its value
    let input = document.getElementById("facultysearchInput");
    let filter = input.value.toUpperCase();  // Convert to uppercase to make the search case-insensitive
    let table = document.getElementById("faculty-list");  // Get the tbody element
    let rows = table.getElementsByTagName("tr");  // Get all table rows in the tbody

    // Loop through each row in the table
    for (let i = 0; i < rows.length; i++) {
        let columns = rows[i].getElementsByTagName("td"); // Get all columns (td elements) of the row
        if (columns.length > 0) {  // Ensure the row has columns
            let facultyIdText = columns[0].textContent || columns[0].innerText; // Faculty ID column
            let firstNameText = columns[1].textContent || columns[1].innerText;  // First Name column
            let middleNameText = columns[2].textContent || columns[2].innerText;  // Middle Name column
            let lastNameText = columns[3].textContent || columns[3].innerText;  // Last Name column

            // If any of the columns matches the search filter, display the row; otherwise, hide it
            if (
                facultyIdText.toUpperCase().indexOf(filter) > -1 ||
                firstNameText.toUpperCase().indexOf(filter) > -1 ||
                middleNameText.toUpperCase().indexOf(filter) > -1 ||
                lastNameText.toUpperCase().indexOf(filter) > -1
            ) {
                rows[i].style.display = "";  // Show row
            } else {
                rows[i].style.display = "none";  // Hide row
            }
        }
    }
}
