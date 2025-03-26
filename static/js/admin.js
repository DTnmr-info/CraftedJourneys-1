/**
 * Crafted Journeys - Admin Dashboard JavaScript
 * Author: Crafted Journeys Team
 * Version: 1.0
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Toggle Sidebar on Mobile
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const adminSidebar = document.querySelector('.admin-sidebar');
    const adminContent = document.querySelector('.admin-content');
    
    if (sidebarToggle && adminSidebar && adminContent) {
        sidebarToggle.addEventListener('click', function() {
            adminSidebar.classList.toggle('collapsed');
            adminContent.classList.toggle('expanded');
        });
    }
    
    // Confirmation for Delete Actions
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // File Input Preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    if (fileInputs.length > 0) {
        fileInputs.forEach(input => {
            input.addEventListener('change', function() {
                const previewContainer = document.querySelector(`#${this.id}-preview`);
                
                if (previewContainer && this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        previewContainer.innerHTML = `<img src="${e.target.result}" class="img-preview">`;
                    };
                    
                    reader.readAsDataURL(this.files[0]);
                }
            });
        });
    }
    
    // Initialize Datepickers
    const datepickers = document.querySelectorAll('.datepicker');
    
    if (datepickers.length > 0) {
        datepickers.forEach(input => {
            // This would normally use a datepicker library like Flatpickr or Bootstrap Datepicker
            // For this example, we'll simulate it with the HTML5 date input
            input.type = 'date';
        });
    }
    
    // Status Change Handlers
    const statusSelects = document.querySelectorAll('.status-select');
    
    if (statusSelects.length > 0) {
        statusSelects.forEach(select => {
            select.addEventListener('change', function() {
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            });
        });
    }
    
    // Bulk Actions
    const bulkActionSelect = document.querySelector('#bulk-action');
    const bulkActionForm = document.querySelector('#bulk-action-form');
    
    if (bulkActionSelect && bulkActionForm) {
        bulkActionSelect.addEventListener('change', function() {
            if (this.value !== '') {
                // Check if any items are selected
                const checkedItems = document.querySelectorAll('input[name="bulk_items[]"]:checked');
                
                if (checkedItems.length === 0) {
                    alert('Please select at least one item to perform bulk action.');
                    this.value = '';
                    return;
                }
                
                // Confirm before proceeding with delete action
                if (this.value === 'delete' && !confirm('Are you sure you want to delete all selected items? This action cannot be undone.')) {
                    this.value = '';
                    return;
                }
                
                // Submit the form
                bulkActionForm.submit();
            }
        });
    }
    
    // Select All Checkboxes
    const selectAllCheckbox = document.querySelector('#select-all');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const itemCheckboxes = document.querySelectorAll('input[name="bulk_items[]"]');
            
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    // Image Upload Modal
    const imageUploadModal = document.querySelector('#uploadImageModal');
    
    if (imageUploadModal) {
        const fileInput = imageUploadModal.querySelector('input[type="file"]');
        const imagePreview = imageUploadModal.querySelector('.image-preview');
        
        if (fileInput && imagePreview) {
            fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        imagePreview.innerHTML = `<img src="${e.target.result}" class="img-fluid">`;
                    };
                    
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
    }
    
    // Filter Tables
    const tableFilters = document.querySelectorAll('.table-filter');
    
    if (tableFilters.length > 0) {
        tableFilters.forEach(filter => {
            filter.addEventListener('change', function() {
                const filterForm = this.closest('form');
                if (filterForm) {
                    filterForm.submit();
                }
            });
        });
    }
    
    // Package Search
    const packageSearch = document.querySelector('#package-search');
    
    if (packageSearch) {
        packageSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const packageItems = document.querySelectorAll('.package-item');
            
            packageItems.forEach(item => {
                const packageName = item.querySelector('.package-name').textContent.toLowerCase();
                
                if (packageName.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Location Search
    const locationSearch = document.querySelector('#location-search');
    
    if (locationSearch) {
        locationSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const locationItems = document.querySelectorAll('.location-item');
            
            locationItems.forEach(item => {
                const locationName = item.querySelector('.location-name').textContent.toLowerCase();
                
                if (locationName.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Time Period Selector
    const timePeriodButtons = document.querySelectorAll('.time-period-btn');
    
    if (timePeriodButtons.length > 0) {
        timePeriodButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all buttons
                timePeriodButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Update chart data based on selected time period
                // This would usually trigger an AJAX call to get new data
                const period = this.dataset.period;
                updateCharts(period);
            });
        });
    }
    
    // Update charts function (placeholder)
    function updateCharts(period) {
        console.log(`Updating charts for period: ${period}`);
        // In a real implementation, this would fetch new data and update the charts
    }
    
    // Form Validation
    const adminForms = document.querySelectorAll('.admin-form');
    
    if (adminForms.length > 0) {
        adminForms.forEach(form => {
            form.addEventListener('submit', function(e) {
                let isValid = true;
                
                // Check required fields
                const requiredFields = form.querySelectorAll('[required]');
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('is-invalid');
                    } else {
                        field.classList.remove('is-invalid');
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    alert('Please fill in all required fields');
                }
            });
        });
    }
});
