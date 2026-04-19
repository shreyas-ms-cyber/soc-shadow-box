function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
}

function getRiskLevel(score) {
    if (score >= 86) return { text: 'CRITICAL RISK', color: '#ff4444' };
    if (score >= 61) return { text: 'HIGH RISK', color: '#ff8844' };
    if (score >= 31) return { text: 'MEDIUM RISK', color: '#ffaa44' };
    return { text: 'LOW RISK', color: '#00ff9d' };
}

function getSeverityBadgeClass(category) {
    const cat = category.toLowerCase();
    if (cat === 'critical') return 'badge-critical';
    if (cat === 'high') return 'badge-high';
    if (cat === 'medium') return 'badge-medium';
    return 'badge-low';
}

function addLogToFeed(message, severity = 'info') {
    const logFeed = document.getElementById('logFeed');
    if (!logFeed) return;
    
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${severity}`;
    logEntry.style.animation = 'slideIn 0.3s ease';
    logEntry.innerHTML = `<span class="log-time">[${new Date().toLocaleTimeString()}]</span> ${message}`;
    logFeed.insertBefore(logEntry, logFeed.firstChild);
    
    setTimeout(() => {
        logEntry.style.background = 'rgba(0, 255, 157, 0.2)';
        setTimeout(() => logEntry.style.background = 'rgba(0, 0, 0, 0.3)', 500);
    }, 100);
    
    while (logFeed.children.length > 100) logFeed.removeChild(logFeed.lastChild);
    logFeed.scrollTop = 0;
}

function showAttackFeedback(message, isError = false) {
    const feedback = document.getElementById('attackFeedback');
    if (!feedback) return;
    feedback.textContent = message;
    feedback.style.background = isError ? 'rgba(255, 68, 68, 0.2)' : 'rgba(0, 255, 157, 0.2)';
    feedback.style.color = isError ? '#ff8888' : '#00ff9d';
    feedback.classList.add('show');
    setTimeout(() => feedback.classList.remove('show'), 3000);
}

function updateDateTime() {
    const elem = document.getElementById('datetime');
    if (elem) {
        elem.textContent = new Date().toLocaleString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit'
        });
    }
}
setInterval(updateDateTime, 1000);

// Suppress blob URL warnings (harmless on localhost)
const originalWarn = console.warn;
console.warn = function(...args) {
    if (args[0] && args[0].includes('blob:') && args[0].includes('insecure')) {
        return; // Ignore blob HTTPS warnings
    }
    originalWarn.apply(console, args);
};
