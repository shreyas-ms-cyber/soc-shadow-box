const API_BASE = 'http://localhost:8000';

async function callAPI(endpoint, method = 'GET', body = null) {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) options.body = JSON.stringify(body);
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        return { success: response.ok, data };
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: error.message };
    }
}

async function generateAttack(attackType = null) {
    let url = '/api/attack/generate';
    if (attackType && attackType !== 'random') url += `?attack_type=${attackType}`;
    return await callAPI(url, 'POST');
}

async function analyzeLogs(minutes = 5, autoRespond = true) {
    return await callAPI(`/api/detect/analyze?minutes=${minutes}&auto_respond=${autoRespond}`, 'POST');
}

async function getAlerts(status = null, limit = 20) {
    let url = `/api/detect/alerts?limit=${limit}`;
    if (status) url += `&status_filter=${status}`;
    return await callAPI(url);
}

async function getDetectionStats() {
    return await callAPI('/api/detect/stats');
}

async function getLogs(limit = 100, severity = null) {
    // FIXED: Correct endpoint with /api/ prefix
    let url = `/api/logs?limit=${limit}`;
    if (severity) url += `&severity=${severity}`;
    return await callAPI(url);
}

async function respondToAlert(alertId, autoMode = true) {
    return await callAPI(`/api/detect/respond/${alertId}?auto_mode=${autoMode}`, 'POST');
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        return response.ok;
    } catch { 
        return false; 
    }
}
