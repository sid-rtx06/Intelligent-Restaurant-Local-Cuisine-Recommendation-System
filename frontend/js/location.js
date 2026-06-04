// Location utilities

let userLocation = null;

async function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported by your browser'));
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                resolve(userLocation);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

async function requestLocation() {
    try {
        const location = await getCurrentLocation();
        return location;
    } catch (error) {
        console.error('Location error:', error);
        // Default to a sample location if geolocation fails
        // (Hyderabad, India as example)
        userLocation = {
            latitude: 17.3850,
            longitude: 78.4867
        };
        return userLocation;
    }
}

function getUserLocation() {
    return userLocation;
}
