const sidebar = document.querySelector(".sidebar");
const sidebarToggle = document.querySelector("#sidebar-toggle"); // Ensure this matches the HTML ID

sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});
