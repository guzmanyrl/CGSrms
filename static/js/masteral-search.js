// Add this to your JavaScript file (e.g., masteral-toast.js or a new file named masteral-search.js)
function filterMasteralTable() {
    let input = document.getElementById("masteralSearchInput");
    let filter = input.value.toUpperCase();
    let table = document.querySelector("#masteral_student-list");
    let rows = table.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        let studentId = rows[i].getElementsByTagName("td")[0];
        let firstName = rows[i].getElementsByTagName("td")[1];
        let lastName = rows[i].getElementsByTagName("td")[2];

        if (studentId || firstName || lastName) {
            let studentIdText = studentId ? studentId.textContent || studentId.innerText : "";
            let firstNameText = firstName ? firstName.textContent || firstName.innerText : "";
            let lastNameText = lastName ? lastName.textContent || lastName.innerText : "";

            if (
                studentIdText.toUpperCase().indexOf(filter) > -1 ||
                firstNameText.toUpperCase().indexOf(filter) > -1 ||
                lastNameText.toUpperCase().indexOf(filter) > -1
            ) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}
