// Fix for logs API endpoint
async function loadLogs() {
    try {
        // Use correct API endpoint with /api/ prefix
        const response = await fetch('http://localhost:8000/api/logs?limit=100');
        const data = await response.json();
        
        if (data.success && data.logs) {
            console.log('Logs loaded:', data.logs.length);
            // Display logs here
        } else {
            console.error('Failed to load logs');
        }
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}
