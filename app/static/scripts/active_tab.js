document.addEventListener("DOMContentLoaded", function() {
    const currentLocation = window.location.href;

    const links = document.querySelectorAll(".nav-link");
    links.forEach(link => {
        if (link.href === currentLocation) {
            link.classList.add("active");
        }
    });
});