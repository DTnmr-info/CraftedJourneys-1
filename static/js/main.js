/**
 * Crafted Journeys - Main JavaScript
 * Author: Crafted Journeys Team
 * Version: 1.0
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Sticky Navigation
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Mobile Menu Toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (navbarCollapse.classList.contains('show') && 
                !navbarCollapse.contains(event.target) && 
                !navbarToggler.contains(event.target)) {
                navbarCollapse.classList.remove('show');
            }
        });
    }
    
    // Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 100,
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu after clicking a link
                    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                        navbarCollapse.classList.remove('show');
                    }
                }
            }
        });
    });
    
    // Form Validation
    const forms = document.querySelectorAll('.needs-validation');
    
    if (forms.length > 0) {
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    }
    
    // Package Category Filtering
    const filterForm = document.querySelector('.filter-form');
    
    if (filterForm) {
        const categorySelect = filterForm.querySelector('#category');
        const regionSelect = filterForm.querySelector('#region');
        
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                filterForm.submit();
            });
        }
        
        if (regionSelect) {
            regionSelect.addEventListener('change', function() {
                filterForm.submit();
            });
        }
    }
    
    // Dynamic Copyright Year
    const copyrightYear = document.querySelector('.copyright-year');
    
    if (copyrightYear) {
        copyrightYear.textContent = new Date().getFullYear();
    }
    
    // Package Detail Page Tab Navigation
    const packageDetailTabs = document.querySelectorAll('.package-detail-nav .nav-link');
    
    if (packageDetailTabs.length > 0) {
        packageDetailTabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                packageDetailTabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show corresponding content
                const targetId = this.getAttribute('href');
                const targetContent = document.querySelector(targetId);
                
                if (targetContent) {
                    document.querySelectorAll('.tab-content').forEach(content => {
                        content.style.display = 'none';
                    });
                    
                    targetContent.style.display = 'block';
                }
            });
        });
    }
    
    // Image Gallery Lightbox
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    // Implement a simple lightbox for gallery images if needed
    // This would require additional HTML structure and CSS
    
    // Testimonial Slider
    // If using a carousel/slider, initialize it here
    
    // Accordion Functionality
    const accordionButtons = document.querySelectorAll('.accordion-button');
    
    if (accordionButtons.length > 0) {
        accordionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const isExpanded = this.getAttribute('aria-expanded') === 'true';
                
                // Update aria-expanded attribute
                this.setAttribute('aria-expanded', !isExpanded);
                
                // Toggle the collapse class on the target
                const targetId = this.getAttribute('data-bs-target');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    targetElement.classList.toggle('show');
                }
            });
        });
    }
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Back to Top Button
    const backToTopButton = document.querySelector('.back-to-top');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.classList.add('active');
            } else {
                backToTopButton.classList.remove('active');
            }
        });
        
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Animate on Scroll (simple implementation)
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animateElements.length > 0) {
        // Function to check if element is in viewport
        function isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.bottom >= 0
            );
        }
        
        // Add animation class when element is in viewport
        function checkAnimations() {
            animateElements.forEach(element => {
                if (isInViewport(element) && !element.classList.contains('animated')) {
                    element.classList.add('animated');
                }
            });
        }
        
        // Check animations on scroll
        window.addEventListener('scroll', checkAnimations);
        
        // Check animations on page load
        checkAnimations();
    }
    
    // Newsletter Subscription Form
    const newsletterForm = document.querySelector('.newsletter-form form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email === '') {
                // Show error message
                alert('Please enter your email address');
                return;
            }
            
            // Validate email format
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                // Show error message
                alert('Please enter a valid email address');
                return;
            }
            
            // Form is valid, you would normally submit to server here
            // For demo purposes, just show success message and clear form
            alert('Thank you for subscribing to our newsletter!');
            emailInput.value = '';
        });
    }
});
