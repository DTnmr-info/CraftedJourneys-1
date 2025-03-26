/**
 * Crafted Journeys - Charts and Analytics JavaScript
 * Author: Crafted Journeys Team
 * Version: 1.0
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Inquiry Status Chart
    const inquiryStatusChart = document.getElementById('inquiryStatusChart');
    
    if (inquiryStatusChart) {
        // Get data from data attributes
        const pendingCount = parseInt(inquiryStatusChart.dataset.pending) || 0;
        const contactedCount = parseInt(inquiryStatusChart.dataset.contacted) || 0;
        const resolvedCount = parseInt(inquiryStatusChart.dataset.resolved) || 0;
        
        const ctx = inquiryStatusChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Contacted', 'Resolved'],
                datasets: [{
                    data: [pendingCount, contactedCount, resolvedCount],
                    backgroundColor: ['#ffc107', '#17a2b8', '#28a745'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw}`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Initialize Packages by Category Chart
    const packagesCategoryChart = document.getElementById('packagesCategoryChart');
    
    if (packagesCategoryChart) {
        // Parse the JSON data from the data attribute
        let categoryData = {};
        
        try {
            categoryData = JSON.parse(packagesCategoryChart.dataset.categories || '{}');
        } catch (error) {
            console.error('Error parsing category data:', error);
            categoryData = {};
        }
        
        // Prepare data for the chart
        const categories = Object.keys(categoryData);
        const counts = Object.values(categoryData);
        
        const ctx = packagesCategoryChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Number of Packages',
                    data: counts,
                    backgroundColor: [
                        '#ff9933', // Orange (Adventure)
                        '#192b7a', // Blue (Cultural)
                        '#ffc107', // Yellow (Heritage)
                        '#9c27b0', // Purple (Spiritual)
                        '#4caf50'  // Green (Wellness)
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Initialize Monthly Bookings Chart
    const monthlyBookingsChart = document.getElementById('monthlyBookingsChart');
    
    if (monthlyBookingsChart) {
        // This would normally get real data from the server
        // Simulating with sample data
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const bookingsData = [12, 19, 15, 20, 22, 25, 28, 30, 24, 18, 15, 21];
        
        const ctx = monthlyBookingsChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Bookings',
                    data: bookingsData,
                    borderColor: '#192b7a',
                    backgroundColor: 'rgba(25, 43, 122, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: '#ff9933',
                    pointBorderColor: '#ff9933',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Initialize Inquiry Sources Chart
    const inquirySourcesChart = document.getElementById('inquirySourcesChart');
    
    if (inquirySourcesChart) {
        // Parse the JSON data from the data attribute
        let sourcesData = {};
        
        try {
            sourcesData = JSON.parse(inquirySourcesChart.dataset.sources || '{}');
        } catch (error) {
            console.error('Error parsing sources data:', error);
            sourcesData = {};
        }
        
        // Prepare data for the chart
        const sources = Object.keys(sourcesData);
        const counts = Object.values(sourcesData);
        
        const ctx = inquirySourcesChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: sources,
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        '#ff9933', // Orange
                        '#192b7a', // Blue
                        '#ffc107', // Yellow
                        '#17a2b8'  // Cyan
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw} (${Math.round(context.raw / context.dataset.data.reduce((a, b) => a + b, 0) * 100)}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Initialize Revenue by Region Chart
    const revenueRegionChart = document.getElementById('revenueRegionChart');
    
    if (revenueRegionChart) {
        // This would normally get real data from the server
        // Simulating with sample data
        const regions = ['North India', 'South India', 'East India', 'West India', 'Central India', 'Northeast India'];
        const revenueData = [35, 25, 10, 15, 10, 5];
        
        const ctx = revenueRegionChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: regions,
                datasets: [{
                    label: 'Revenue Percentage',
                    data: revenueData,
                    backgroundColor: 'rgba(255, 153, 51, 0.2)',
                    borderColor: '#ff9933',
                    pointBackgroundColor: '#ff9933',
                    pointBorderColor: '#ffffff',
                    pointHoverBackgroundColor: '#ffffff',
                    pointHoverBorderColor: '#ff9933'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 40
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Initialize Customer Satisfaction Chart
    const satisfactionChart = document.getElementById('satisfactionChart');
    
    if (satisfactionChart) {
        // This would normally get real data from the server
        // Simulating with sample data
        const ratings = ['5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Star'];
        const satisfactionData = [60, 25, 10, 3, 2];
        
        const ctx = satisfactionChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: ratings,
                datasets: [{
                    label: 'Percentage of Reviews',
                    data: satisfactionData,
                    backgroundColor: [
                        '#28a745', // 5 Stars - Green
                        '#8bc34a', // 4 Stars - Light Green
                        '#ffc107', // 3 Stars - Yellow
                        '#ff9800', // 2 Stars - Orange
                        '#dc3545'  // 1 Star - Red
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.raw}% of reviews`;
                            }
                        }
                    }
                }
            }
        });
    }
});
