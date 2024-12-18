function saveChanges(fileId) {
    const hot = new Handsontable(document.getElementById('excel-container'), {
        // Your Handsontable configuration
    });

    const changes = hot.getData(); // Get the edited data

    const formData = new FormData();
    formData.append('file', convertDataToExcel(changes));  // Implement conversion of data to Excel format

    fetch(`/CGS_Records/save_excel_changes/${fileId}/`, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
