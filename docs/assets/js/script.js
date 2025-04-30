// File: assets/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    handleSmoothScroll();
    addSpeakButtons();
    handleBackToTopButton();
    handleStickyNavigation();
    handleMobileMenu();
});

// 1. Smooth Scrolling for anchor links
function handleSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Ensure it's a valid internal link and not just "#"
            if (href.length > 1 && href.startsWith('#')) {
                const targetElement = document.querySelector(href);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start' // Aligns the top of the target with the top of the viewport
                    });
                    // Optional: Close mobile menu if open after clicking a link
                    const navMenu = document.querySelector('.nav-menu');
                    if (navMenu && navMenu.classList.contains('active')) {
                        navMenu.classList.remove('active');
                        document.querySelector('.menu-toggle').setAttribute('aria-expanded', 'false');
                    }
                }
            }
        });
    });
}

// 2. Text-to-Speech functionality
function speak(text) {
    if ('speechSynthesis' in window) {
        // Cancel any previous speech
        window.speechSynthesis.cancel();

        const msg = new SpeechSynthesisUtterance();
        msg.text = text.trim(); // Text to be spoken
        msg.lang = 'en-US'; // Language: English (US)
        msg.rate = 0.9; // Speed (1 is default, <1 is slower)
        msg.pitch = 1; // Pitch (0 to 2, 1 is default)

        // Attempt to find a suitable voice (optional, improves quality sometimes)
        const voices = window.speechSynthesis.getVoices();
        // Example: Prefer a specific voice if available
        // msg.voice = voices.find(voice => voice.name === 'Google US English') || voices.find(voice => voice.lang === 'en-US');

        window.speechSynthesis.speak(msg);
    } else {
        alert('מצטערים, הדפדפן שלך אינו תומך בהקראת טקסט.');
    }
}

// Pre-load voices if necessary (browser dependent)
if ('speechSynthesis' in window && window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
}

// 3. Add Speak Buttons to tables
function addSpeakButtons() {
    const tables = document.querySelectorAll('table');

    tables.forEach(table => {
        // Get header text to find the "English Term" column index robustly
        const headers = Array.from(table.querySelectorAll('th'));
        // Find index based on common Hebrew header text variations
        const englishTermHeaderIndex = headers.findIndex(th =>
            th.textContent.includes('מונח באנגלית') || th.textContent.includes('English Term')
        );

        // Fallback to second column if header not found
        const termColumnIndex = englishTermHeaderIndex !== -1 ? englishTermHeaderIndex : 1;


        const rows = table.querySelectorAll('tbody tr'); // Target only body rows

        rows.forEach(row => {
            const cells = row.querySelectorAll('td');

            if (cells.length > termColumnIndex) {
                const termCell = cells[termColumnIndex];
                // Clone the cell content to avoid including button text in speak()
                const termText = termCell.cloneNode(true).textContent.trim();

                // Only add button if term exists and no button already exists
                if (termText && !termCell.querySelector('.speak-button')) {
                    const button = document.createElement('button');
                    button.classList.add('speak-button');
                    button.setAttribute('aria-label', `הקרא את המונח ${termText}`);
                    button.title = `הקרא את המונח ${termText}`;
                    button.innerHTML = '<i class="fas fa-volume-up" aria-hidden="true"></i>'; // Speaker icon
                    button.onclick = (e) => {
                        e.stopPropagation(); // Prevent potential row click events
                        speak(termText);
                    };

                    // Append button - consider placing it before the text
                     termCell.appendChild(button);
                    // Or prepend: termCell.insertBefore(button, termCell.firstChild);
                }
            }
        });
    });
}


// 4. Back to Top Button visibility
function handleBackToTopButton() {
    const backToTopButton = document.getElementById('back-to-top');
    if (!backToTopButton) return; // Exit if button doesn't exist

    const scrollThreshold = 300; // Pixels to scroll before showing button

    window.addEventListener('scroll', () => {
        if (window.scrollY > scrollThreshold) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 5. Sticky Navigation and Header Shrink
function handleStickyNavigation() {
    const header = document.getElementById('site-header');
    const nav = document.getElementById('site-nav'); // Assuming nav is separate now

    if (!header || !nav) return; // Exit if elements don't exist

    const scrollThreshold = 50; // How far to scroll before shrinking

    window.addEventListener('scroll', () => {
        if (window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
            // nav.classList.add('scrolled'); // Add if nav also needs a 'scrolled' style
        } else {
            header.classList.remove('scrolled');
            // nav.classList.remove('scrolled');
        }
    });
}

// 6. Mobile Menu Toggle
function handleMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (!menuToggle || !navMenu) return; // Exit if elements don't exist

    menuToggle.addEventListener('click', () => {
        const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
        navMenu.classList.toggle('active');
        menuToggle.setAttribute('aria-expanded', !isExpanded);
        // Optional: Toggle icon class
        const icon = menuToggle.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times'); // Assuming you use 'X' icon when open
        }
    });

     // Close menu if clicking outside of it
     document.addEventListener('click', (event) => {
        const isClickInsideNav = navMenu.contains(event.target);
        const isClickOnToggle = menuToggle.contains(event.target);

        if (!isClickInsideNav && !isClickOnToggle && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', 'false');
            const icon = menuToggle.querySelector('i');
             if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });
}