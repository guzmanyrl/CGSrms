// Pass the file URL dynamically from the template
const fileUrl = '{{ file_url }}';

document.addEventListener('DOMContentLoaded', () => {
    // Check if file input element exists before adding event listener
    const fileInput = document.getElementById('file_input');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }

    // Initialize Handsontable with file data if URL is provided
    if (fileUrl) {
        fetch(fileUrl)
            .then(response => response.arrayBuffer())
            .then(data => {
                const workbook = XLSX.read(data, { type: 'array' });
                const sheet = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], { header: 1 });

                const container = document.getElementById('excel-container');
                const hot = new Handsontable(container, {
                    data: sheet,
                    rowHeaders: true,
                    colHeaders: true,
                    licenseKey: 'non-commercial-and-evaluation'
                });

                window.hotInstance = hot;
            })
            .catch(error => console.error('Error loading file:', error));
    }
});

// Function to handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        const data = e.target.result;
        const workbook = XLSX.read(data, { type: 'binary' });
        const sheet = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], { header: 1 });

        // Initialize Handsontable with uploaded file data
        const container = document.getElementById('excel-container');
        const hot = new Handsontable(container, {
            data: sheet,
            rowHeaders: true,
            colHeaders: true,
            licenseKey: 'non-commercial-and-evaluation'
        });

        window.hotInstance = hot;
    };

    reader.readAsBinaryString(file);
}

// Function to download the edited file
function downloadFile() {
    const sheetData = window.hotInstance.getData();
    const ws = XLSX.utils.aoa_to_sheet(sheetData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

    // Trigger download of the edited file
    XLSX.writeFile(wb, "edited_file.xlsx");
}

// Function to save changes to the server
function saveChanges(fileId) {
    const sheetData = window.hotInstance.getData();
    const ws = XLSX.utils.aoa_to_sheet(sheetData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    const updatedFile = XLSX.write(wb, { bookType: "xlsx", type: "array" });

    const formData = new FormData();
    formData.append("file", new Blob([updatedFile], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }), "updated_file.xlsx");

    fetch(`/save_excel_changes/${fileId}/`, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken()  // CSRF token handling
        }
    }).then(response => {
        if (response.ok) {
            alert("File saved successfully.");
        } else {
            alert("Failed to save the file.");
        }
    });
}

// Function to retrieve CSRF token from the page
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Add download button functionality
const downloadButton = document.getElementById('download-btn');
if (downloadButton) {
    downloadButton.addEventListener('click', () => {
        downloadFile();  // Trigger the file download when the button is clicked
    });
}
