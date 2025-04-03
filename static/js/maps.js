/**
 * Crafted Journeys - Locations Page Map Integration
 * Author: Crafted Journeys Team
 * Version: 1.1
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log("📍 Map script loaded!");

    // ============================
    // 🌍 LOCATIONS PAGE MAP (Database Locations)
    // ============================
    const locationsMap = document.getElementById('locations-map');
    if (locationsMap) {
        const map = L.map('locations-map').setView([20.5937, 78.9629], 5);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        try {
            let locations = [];
            if (locationsMap.dataset.locations) {
                locations = JSON.parse(locationsMap.dataset.locations);
            }

            if (Array.isArray(locations) && locations.length > 0) {
                console.log("✅ Database Locations Loaded:", locations);
                const bounds = L.latLngBounds();

                locations.forEach(location => {
                    if (location.latitude && location.longitude) {
                        const marker = L.marker([location.latitude, location.longitude])
                            .addTo(map)
                            .bindPopup(`
                                <strong>${location.name}</strong><br>
                                ${location.region || ''}<br>
                                <a href="/locations/${location.id}">View Details</a>
                            `);
                        bounds.extend(marker.getLatLng());
                    }
                });

                if (locations.length === 1) {
                    map.setView([locations[0].latitude, locations[0].longitude], 9);
                } else {
                    map.fitBounds(bounds, { padding: [50, 50] });
                }
            } else {
                console.warn("⚠️ No locations found in database.");
            }
        } catch (error) {
            console.error("❌ Error loading locations from database:", error);
        }
    }
});


    
    // Initialize Package Detail Map
    const packageMap = document.getElementById('package-map');
    
    if (packageMap) {
        // Get location data from data attribute
        const latitude = parseFloat(packageMap.dataset.latitude);
        const longitude = parseFloat(packageMap.dataset.longitude);
        const locationName = packageMap.dataset.location;
        
        if (!isNaN(latitude) && !isNaN(longitude)) {
            // Initialize map
            const map = L.map('package-map').setView([latitude, longitude], 12);
            
            // Add OpenStreetMap tile layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            
            // Add marker with popup
            L.marker([latitude, longitude]).addTo(map)
                .bindPopup(`<strong>${locationName}</strong>`)
                .openPopup();
        }
    }
    
    // Initialize Contact Page Map
    const contactMap = document.getElementById('contact-map');
    
    if (contactMap) {
        // Office location (New Delhi)
        const officeLatitude = 28.5456;
        const officeLongitude = 77.1796;
        
        // Initialize map
        const map = L.map('contact-map').setView([officeLatitude, officeLongitude], 15);
        
        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        // Add marker with popup
        L.marker([officeLatitude, officeLongitude]).addTo(map)
            .bindPopup(`
                <strong>Crafted Journeys</strong><br>
                123 Temple Road, Hauz Khas<br>
                New Delhi 110016, India<br><br>
                <a href="https://maps.google.com?q=28.5456,77.1796" target="_blank">Get Directions</a>
            `)
            .openPopup();
    }
    
    // Initialize Custom Itinerary Map
    const itineraryMap = document.getElementById('itinerary-map');
    
    if (itineraryMap) {
        // Check if we have itinerary points data
        if (itineraryMap.dataset.points) {
            try {
                const points = JSON.parse(itineraryMap.dataset.points);
                
                if (points.length > 0) {
                    // Initialize map with first point centered
                    const map = L.map('itinerary-map').setView([points[0].latitude, points[0].longitude], 6);
                    
                    // Add OpenStreetMap tile layer
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(map);
                    
                    // Add markers for each point
                    points.forEach((point, index) => {
                        // Create custom icon with day number
                        const dayIcon = L.divIcon({
                            html: `<div class="day-marker">${index + 1}</div>`,
                            className: 'day-icon',
                            iconSize: [30, 30]
                        });
                        
                        // Add marker with custom icon
                        L.marker([point.latitude, point.longitude], { icon: dayIcon }).addTo(map)
                            .bindPopup(`
                                <strong>Day ${index + 1}: ${point.name}</strong><br>
                                ${point.description || ''}
                            `);
                    });
                    
                    // Create a polyline connecting all points
                    const polyline = L.polyline(
                        points.map(point => [point.latitude, point.longitude]),
                        { color: '#FF9933', weight: 3, opacity: 0.7 }
                    ).addTo(map);
                    
                    // Fit the map to the polyline
                    map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
                }
            } catch (error) {
                console.error('Error parsing itinerary points data:', error);
            }
        }
    }
});
