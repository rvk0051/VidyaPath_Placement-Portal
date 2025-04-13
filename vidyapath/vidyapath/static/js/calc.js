document.addEventListener('DOMContentLoaded', () => {
    // Function to handle navbar color change on scroll
    function changeNavbarColor() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) { // Change 50 to control when navbar color changes
            navbar.classList.add('scrolled'); // Adds 'scrolled' class (blue background)
        } else {
            navbar.classList.remove('scrolled'); // Removes 'scrolled' class (transparent background)
        }
    }

    // Attach the scroll event listener for navbar color change
    window.onscroll = changeNavbarColor;

    // Handle fade-in and fade-out effect for images
    const images = document.querySelectorAll('.fade-on-scroll img');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add the "visible" class with a delay for each image when it comes into view
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 300); // Delay by 300ms for each image
            } else {
                // Remove the "visible" class when the image scrolls out of view
                entry.target.classList.remove('visible');
            }
        });
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 0.1 // Trigger when at least 10% of the image is visible
    });

    // Observe each image for the fade-in/fade-out effect
    images.forEach(image => observer.observe(image));
});

