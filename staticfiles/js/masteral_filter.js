// JavaScript to submit filter form when any dropdown changes
function submitFilterForm() {
    document.getElementById("filterForm").submit();
}

// Handle search filtering for the table
function filterMasteralTable() {
    var input = document.getElementById("masteralSearchInput");
    var filter = input.value.toUpperCase();
    var table = document.querySelector(".table");
    var tr = table.getElementsByTagName("tr");

    for (var i = 1; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td");
        var showRow = false;
        for (var j = 0; j < td.length; j++) {
            if (td[j] && td[j].textContent.toUpperCase().indexOf(filter) > -1) {
                showRow = true;
                break;
            }
        }
        tr[i].style.display = showRow ? "" : "none";
    }
}