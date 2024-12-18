document.querySelector('.filter').addEventListener('click', function (event) {
    const schoolYear = document.querySelector('.formselect').value;
    const program = document.querySelector('.formselect2').value;
    const studentType = document.querySelector('.formselect1').value;
    const semester = document.querySelector('.formselect3').value;

    if (!schoolYear || !program || !studentType || !semester) {
        alert("Please select all filters before applying.");
        event.preventDefault();
    }
});
