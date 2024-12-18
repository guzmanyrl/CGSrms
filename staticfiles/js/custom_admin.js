document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.querySelector(".theme-toggle");
    if (themeToggle) {
        // Customize the theme toggle text
        const currentTheme = themeToggle.getAttribute("data-theme");
        themeToggle.textContent = `Switch to ${currentTheme === "light" ? "dark" : "light"} theme (current: ${currentTheme})`;
    }
});
