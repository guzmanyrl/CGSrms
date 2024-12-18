fetch(`/CGS_Dashboard/get-students/${major}/`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch student data: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        const tbody = document.getElementById('students-table-body');
        tbody.innerHTML = '';
        if (data.students && data.students.length > 0) {
            data.students.forEach(student => {
                const row = `
                    <tr>
                        <td>${student.id}</td>
                        <td>${student.first_name}</td>
                        <td>${student.middle_name}</td>
                        <td>${student.last_name}</td>
                        <td>${student.sex}</td>
                        <td>${student.semester}</td>
                        <td>${student.school_year}</td>
                        <td>${student.programs}</td>
                        <td>${student.majors}</td>
                        <td>${student.student_type}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="10">No students found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error fetching student data:', error);
        alert('Could not load student data. Please try again later.');
    });
