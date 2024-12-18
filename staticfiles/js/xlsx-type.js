document.querySelectorAll('#edit-file-btn').forEach(button => {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        const fileUrl = this.dataset.fileUrl;

        fetch(fileUrl)
            .then(res => res.arrayBuffer())
            .then(data => {
                const workbook = XLSX.read(data, { type: 'array' });
                const worksheet = workbook.Sheets[workbook.SheetNames[0]];
                const htmlString = XLSX.utils.sheet_to_html(worksheet);
                document.body.innerHTML = htmlString;

                // Add a save button
                const saveBtn = document.createElement('button');
                saveBtn.innerText = "Save Changes";
                saveBtn.addEventListener('click', () => {
                    const newWorkbook = XLSX.utils.table_to_book(document.querySelector('table'));
                    const newFile = XLSX.write(newWorkbook, { type: 'array', bookType: 'xlsx' });
                    saveFile(newFile);
                });
                document.body.appendChild(saveBtn);
            });
    });
});

function saveFile(data) {
    const formData = new FormData();
    formData.append('file', new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }));
    fetch(`/save_excel_changes/${file_id}/`, {
        method: 'POST',
        body: formData
    }).then(res => res.json()).then(data => alert(data.message));
}
