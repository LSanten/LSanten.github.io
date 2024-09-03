document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.popover-link');
    const popover = document.querySelector('.popover-content');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            popover.classList.toggle('active');

            // Position the popover near the clicked list item
            const rect = link.getBoundingClientRect();
            popover.style.top = `${rect.bottom + window.scrollY}px`;
            popover.style.left = `${rect.left + window.scrollX}px`;
        });
    });

    // Optional: Close the popover if clicking outside of it
    document.addEventListener('click', function (e) {
        if (!popover.contains(e.target) &&
