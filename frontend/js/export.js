// Server-side export - NO BLOB URL, NO HTTPS WARNING
function downloadLogsCSV(severity = null) {
    let url = `${API_BASE}/api/export/logs/csv?limit=5000`;
    if (severity && severity !== 'all') {
        url += `&severity=${severity}`;
    }
    
    // Use direct download with window.location - NO BLOB
    window.location.href = url;
    
    // Show notification
    showToast('📥 Downloading logs...');
}

function downloadAlertsCSV(status = null) {
    let url = `${API_BASE}/api/export/alerts/csv`;
    if (status && status !== 'all') {
        url += `?status=${status}`;
    }
    
    // Use direct download with window.location - NO BLOB
    window.location.href = url;
    
    showToast('📥 Downloading alerts...');
}

function showToast(message, isError = false) {
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: ${isError ? '#ff4444' : '#00ff9d'};
        color: ${isError ? 'white' : '#0a0e27'};
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
