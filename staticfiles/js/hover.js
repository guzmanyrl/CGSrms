// Select all sidebar links
const sidebarLinks = document.querySelectorAll('.sidebar a');

// Function to handle click event
sidebarLinks.forEach(link => {
    link.addEventListener('click', function (event) {
        // Remove active class from all links
        sidebarLinks.forEach(l => l.classList.remove('active'));

        // Add active class to the clicked link
        this.classList.add('active');

        // Optional: Check if link is navigational
        if (this.href) {
            // Prevent focus if navigating to another page
            this.blur(); // Removes focus on the link
        }
    });
});

// Highlight active link on page load
window.addEventListener('load', () => {
    sidebarLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });
});