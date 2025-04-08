/**
 * Crafted Journeys - Payment Integration JavaScript
 * Author: Crafted Journeys Team
 * Version: 1.0
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Crafted Journeys - Payment JS Loaded');
    
    // Initialize traveler count and price calculation on the checkout page
    const travelersInput = document.getElementById('travelers-input');
    if (travelersInput) {
        // Set initial value to 1
        if (travelersInput.value === '') {
            travelersInput.value = 1;
        }
        
        // Update total when travelers count changes
        travelersInput.addEventListener('input', function() {
            updateTotalPrice();
        });
        
        // Initial calculation
        updateTotalPrice();
    }
    
    // Set min date to today for date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    if (dateInputs.length > 0) {
        const today = new Date().toISOString().split('T')[0];
        dateInputs.forEach(input => {
            input.setAttribute('min', today);
            
            // If no date is set, default to today
            if (input.value === '') {
                input.value = today;
            }
        });
    }
    
    // Form validation
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(event) {
            if (!document.getElementById('terms-checkbox').checked) {
                event.preventDefault();
                showAlert('Please agree to the terms and conditions to proceed.', 'warning');
            }
        });
    }
});

/**
 * Update the total price based on number of travelers
 */
function updateTotalPrice() {
    const travelersInput = document.getElementById('travelers-input');
    const travelerCount = document.getElementById('traveler-count');
    const totalPrice = document.getElementById('total-price');
    const basePriceElement = document.querySelector('.package-price');
    
    if (travelersInput && travelerCount && totalPrice && basePriceElement) {
        // Extract base price from the text (assuming format like "₹25000")
        const basePriceText = basePriceElement.textContent;
        const basePrice = parseInt(basePriceText.replace(/[^0-9]/g, ''));
        
        // Get number of travelers (minimum 1)
        const travelers = Math.max(1, parseInt(travelersInput.value) || 1);
        
        // Update display
        travelerCount.textContent = travelers;
        totalPrice.textContent = '₹' + (basePrice * travelers).toLocaleString('en-IN');
    }
}
