document.addEventListener('DOMContentLoaded', function () {
    const serverUrl = 'http://localhost:5000/track'; // Flask server URL
    const pageIdentifier = window.location.pathname; // Unique identifier for the current page
    const referrerPage = document.referrer || 'Direct Access'; // Referring page or "Direct Access"
    const eventType = 'pageview'; // Define the event type (for example, pageview)

    // Generate a UUID for the session if it doesn't already exist
    let sessionId = localStorage.getItem('sessionId');
    if (!sessionId) {
        sessionId = crypto.randomUUID(); // Generate a new UUID
        localStorage.setItem('sessionId', sessionId); // Store it in localStorage
    }

    // Ensure the tracking request is sent only once per session
    if (!sessionStorage.getItem(`tracked-${pageIdentifier}`)) {
        fetch(serverUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                    session_id: sessionId,
                    event_type: eventType,
                    page: pageIdentifier,
                    referrer: referrerPage,
                }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Page hit tracked:', data); // Log success
            sessionStorage.setItem(`tracked-${pageIdentifier}`, true); // Mark as tracked
        })
        .catch(error => console.error('Error tracking page hit:', error)); // Log errors
    }
});
