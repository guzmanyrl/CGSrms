function updatePerPage() {
    const perPage = document.getElementById('itemsPerPage').value;
    htmx.ajax('GET', `?page=1&per_page=${perPage}`, { target: '#student-list' });
}