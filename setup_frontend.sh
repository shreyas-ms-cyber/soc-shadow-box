#!/bin/bash

echo "🎨 Setting up SOC Shadow Box Frontend with Animations..."
cd ~/soc-shadow-box/frontend

# Create CSS directory
mkdir -p css

# Create style.css with animations
cat > css/style.css << 'STYLEEOF'
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0a0e27;
    color: #e0e0e0;
    overflow-x: hidden;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.05); }
}

@keyframes glow {
    0% { box-shadow: 0 0 5px rgba(0, 255, 157, 0.2); }
    50% { box-shadow: 0 0 25px rgba(0, 255, 157, 0.6); }
    100% { box-shadow: 0 0 5px rgba(0, 255, 157, 0.2); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.app-container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 260px;
    background: linear-gradient(180deg, #0d122b 0%, #080b1a 100%);
    border-right: 1px solid rgba(0, 255, 157, 0.1);
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    transition: transform 0.3s ease;
    z-index: 100;
}

.logo {
    padding: 24px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgba(0, 255, 157, 0.1);
    animation: fadeIn 0.5s ease;
}

.logo-icon {
    font-size: 32px;
    animation: pulse 2s infinite;
}

.logo-title {
    font-size: 18px;
    font-weight: 700;
    background: linear-gradient(135deg, #00ff9d, #00b8ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.logo-subtitle {
    font-size: 10px;
    color: #5a6e8a;
}

.nav-menu {
    padding: 20px 0;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    color: #8a9bb5;
    text-decoration: none;
    margin: 4px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
    animation: slideIn 0.3s ease;
    animation-fill-mode: backwards;
}

.nav-item:nth-child(1) { animation-delay: 0.1s; }
.nav-item:nth-child(2) { animation-delay: 0.2s; }
.nav-item:nth-child(3) { animation-delay: 0.3s; }
.nav-item:nth-child(4) { animation-delay: 0.4s; }

.nav-item:hover {
    background: rgba(0, 255, 157, 0.1);
    color: #00ff9d;
    transform: translateX(5px);
}

.nav-item.active {
    background: linear-gradient(135deg, rgba(0, 255, 157, 0.15), rgba(0, 184, 255, 0.15));
    color: #00ff9d;
    border-left: 2px solid #00ff9d;
}

/* Main Content */
.main-content {
    flex: 1;
    margin-left: 260px;
    padding: 20px 30px;
    animation: fadeIn 0.5s ease;
}

/* Stats Cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: rgba(18, 22, 59, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 255, 157, 0.1);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease;
    animation-fill-mode: backwards;
    cursor: pointer;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }

.stat-card:hover {
    border-color: #00ff9d;
    transform: translateY(-5px);
    animation: glow 0.5s ease;
}

.stat-icon {
    font-size: 40px;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #00ff9d;
    transition: all 0.3s ease;
}

.stat-value.updated {
    transform: scale(1.1);
    color: #ffaa44;
}

.stat-label {
    font-size: 12px;
    color: #8a9bb5;
    margin-top: 4px;
}

/* Risk Meter */
.risk-meter-card {
    background: rgba(18, 22, 59, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 255, 157, 0.1);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.3s ease;
}

.risk-meter-card h3 {
    color: #00ff9d;
    margin-bottom: 20px;
    font-size: 16px;
}

.risk-gauge {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.gauge-container {
    position: relative;
    width: 200px;
    height: 200px;
}

.gauge-center {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

.risk-score {
    font-size: 48px;
    font-weight: 700;
    animation: fadeIn 0.5s ease;
}

.risk-level {
    font-size: 14px;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 20px;
    background: rgba(0, 255, 157, 0.1);
    transition: all 0.3s ease;
    animation: pulse 2s infinite;
}

/* Attack Buttons */
.attack-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.attack-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.05);
    color: #e0e0e0;
    position: relative;
    overflow: hidden;
}

.attack-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.attack-btn:hover::before {
    left: 100%;
}

.attack-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 255, 157, 0.2);
}

.attack-btn.brute-force:hover { background: #ff4444; animation: shake 0.3s ease; }
.attack-btn.file-activity:hover { background: #ffaa44; }
.attack-btn.ddos:hover { background: #ff44aa; }
.attack-btn.random:hover { background: #44ffaa; color: #0a0e27; }
.attack-btn.campaign:hover { background: #aa44ff; }

/* Log Feed */
.log-feed {
    height: 300px;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}

.log-entry {
    padding: 8px 12px;
    border-left: 3px solid #00ff9d;
    margin-bottom: 8px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
    animation: slideIn 0.3s ease;
    transition: all 0.3s ease;
}

.log-entry:hover {
    transform: translateX(5px);
    background: rgba(0, 255, 157, 0.1);
}

.log-entry.critical { border-left-color: #ff4444; }
.log-entry.high { border-left-color: #ff8844; }
.log-entry.medium { border-left-color: #ffaa44; }

/* Alerts Table */
.alerts-table-container {
    overflow-x: auto;
}

.alerts-table {
    width: 100%;
    border-collapse: collapse;
}

.alerts-table tr {
    transition: all 0.3s ease;
}

.alerts-table tr:hover {
    background: rgba(0, 255, 157, 0.05);
    transform: scale(1.01);
}

.alerts-table th, .alerts-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid rgba(0, 255, 157, 0.1);
}

/* Badges */
.badge-critical { background: #ff4444; padding: 4px 8px; border-radius: 4px; font-size: 11px; animation: pulse 1s infinite; }
.badge-high { background: #ff8844; padding: 4px 8px; border-radius: 4px; font-size: 11px; }
.badge-medium { background: #ffaa44; padding: 4px 8px; border-radius: 4px; font-size: 11px; color: #0a0e27; }
.badge-low { background: #00ff9d; padding: 4px 8px; border-radius: 4px; font-size: 11px; color: #0a0e27; }

/* Buttons */
.resolve-btn {
    padding: 4px 12px;
    background: linear-gradient(135deg, #00ff9d, #00b8ff);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.resolve-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 8px rgba(0, 255, 157, 0.4);
}

/* Toggle Switch */
.mode-toggle {
    display: flex;
    align-items: center;
    gap: 10px;
}

.toggle-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #2a2f4f;
    transition: 0.3s;
    border-radius: 24px;
}

.toggle-slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: 0.3s;
    border-radius: 50%;
}

input:checked + .toggle-slider {
    background: linear-gradient(135deg, #00ff9d, #00b8ff);
}

input:checked + .toggle-slider:before {
    transform: translateX(26px);
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
    }
    .sidebar.mobile-open {
        transform: translateX(0);
    }
    .main-content {
        margin-left: 0;
    }
    .mobile-menu-btn {
        display: block;
    }
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

.mobile-menu-btn {
    display: none;
    background: none;
    border: none;
    color: #00ff9d;
    font-size: 24px;
    cursor: pointer;
}

/* Loading Animation */
.loading {
    text-align: center;
    padding: 40px;
    color: #5a6e8a;
}

.loading::after {
    content: '...';
    animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}

/* Header */
.main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    flex-wrap: wrap;
    gap: 15px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
}

.header-left h1 {
    font-size: 24px;
    font-weight: 600;
    background: linear-gradient(135deg, #ffffff, #8a9bb5);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.datetime {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #5a6e8a;
}

.dashboard-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 30px;
}

.quick-actions-card {
    background: rgba(18, 22, 59, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 255, 157, 0.1);
    border-radius: 16px;
    padding: 20px;
}

.quick-actions-card h3 {
    color: #00ff9d;
    margin-bottom: 20px;
    font-size: 16px;
}

.alerts-section, .logs-section {
    background: rgba(18, 22, 59, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 255, 157, 0.1);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 30px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.section-header h3 {
    color: #00ff9d;
    font-size: 16px;
}

.refresh-btn, .clear-logs-btn {
    padding: 6px 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(0, 255, 157, 0.3);
    border-radius: 6px;
    color: #00ff9d;
    cursor: pointer;
    transition: all 0.3s ease;
}

.refresh-btn:hover, .clear-logs-btn:hover {
    background: rgba(0, 255, 157, 0.1);
    transform: scale(1.05);
}

.attack-feedback {
    margin-top: 15px;
    padding: 10px;
    border-radius: 8px;
    background: rgba(0, 0, 0, 0.3);
    font-size: 12px;
    display: none;
}

.attack-feedback.show {
    display: block;
    animation: fadeIn 0.3s ease;
}

.filter-tabs {
    display: flex;
    gap: 10px;
}

.filter-btn {
    padding: 6px 16px;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 20px;
    cursor: pointer;
    color: #fff;
    transition: all 0.3s ease;
}

.filter-btn:hover {
    transform: translateY(-2px);
    background: rgba(0, 255, 157, 0.3);
}

.filter-btn.active {
    background: #00ff9d;
    color: #0a0e27;
}
STYLEEOF

# Create dark-theme.css
cat > css/dark-theme.css << 'DARKEOF'
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d122b; }
::-webkit-scrollbar-thumb { background: #00ff9d; border-radius: 3px; transition: all 0.3s ease; }
::-webkit-scrollbar-thumb:hover { background: #00b8ff; }

.status-dot.online {
    background: #00ff9d;
    box-shadow: 0 0 8px #00ff9d;
    animation: pulse 2s infinite;
}

.attack-btn .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.4);
    transform: scale(0);
    animation: ripple 0.6s linear;
    pointer-events: none;
}

@keyframes ripple {
    to { transform: scale(4); opacity: 0; }
}
DARKEOF

# Create responsive.css
cat > css/responsive.css << 'RESPEOF'
@media (max-width: 1024px) {
    .dashboard-row { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
    .main-content { padding: 15px; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
    .stat-value { font-size: 22px; }
    .stat-icon { font-size: 28px; }
    .header-left h1 { font-size: 18px; }
}

@media (max-width: 480px) {
    .stats-grid { grid-template-columns: 1fr; }
    .attack-buttons { gap: 8px; }
    .attack-btn { padding: 8px 12px; font-size: 11px; }
}
RESPEOF

# Create utils.js
cat > js/utils.js << 'UTILSEOF'
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
UTILSEOF

# Create api.js
cat > js/api.js << 'APIEOF'
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

async function respondToAlert(alertId, autoMode = true) {
    return await callAPI(`/api/detect/respond/${alertId}?auto_mode=${autoMode}`, 'POST');
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        return response.ok;
    } catch { return false; }
}
APIEOF

# Create dashboard.js
cat > js/dashboard.js << 'DASHBOARDEOF'
let riskChart = null;
let refreshInterval = null;
let autoResponseEnabled = true;

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Dashboard initializing...');
    initRiskMeter();
    await loadStats();
    await loadAlerts();
    setupEventListeners();
    startAutoRefresh();
    checkAPIHealthStatus();
});

function initRiskMeter() {
    const canvas = document.getElementById('riskGauge');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    riskChart = new Chart(ctx, {
        type: 'doughnut',
        data: { datasets: [{ data: [0, 100], backgroundColor: ['#00ff9d', '#2a2f4f'], borderWidth: 0, circumference: 180, rotation: 270, cutout: '70%' }] },
        options: { responsive: true, maintainAspectRatio: true, animation: { animateRotate: true, duration: 1000 }, plugins: { tooltip: { enabled: false }, legend: { display: false } } }
    });
}

function updateRiskMeter(score) {
    const riskScoreElem = document.getElementById('riskScore');
    const riskLevelElem = document.getElementById('riskLevel');
    if (riskScoreElem) riskScoreElem.textContent = score;
    const riskLevel = getRiskLevel(score);
    if (riskLevelElem) {
        riskLevelElem.textContent = riskLevel.text;
        riskLevelElem.style.color = riskLevel.color;
    }
    if (riskChart) {
        riskChart.data.datasets[0].data = [score, 100 - score];
        riskChart.data.datasets[0].backgroundColor[0] = riskLevel.color;
        riskChart.update();
    }
}

async function loadStats() {
    try {
        const result = await getDetectionStats();
        if (result.success && result.data.statistics) {
            document.getElementById('activeAlerts').textContent = result.data.statistics.active_alerts || 0;
            document.getElementById('totalAttacks').textContent = result.data.statistics.total_alerts || 0;
        }
        const alerts = await getAlerts('active', 5);
        if (alerts.success && alerts.data.alerts && alerts.data.alerts.length > 0) {
            const maxScore = Math.max(...alerts.data.alerts.map(a => a.threat_score));
            updateRiskMeter(Math.round(maxScore));
        }
    } catch (error) { console.error('Failed to load stats:', error); }
}

async function loadAlerts() {
    try {
        const result = await getAlerts(null, 10);
        const tbody = document.getElementById('alertsTableBody');
        if (!result.success || !result.data.alerts || result.data.alerts.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="loading">No alerts found</td></tr>';
            return;
        }
        tbody.innerHTML = result.data.alerts.map(alert => `
            <tr>
                <td>${formatTimestamp(alert.timestamp)}</td>
                <td><code>${alert.source_ip}</code></td>
                <td><span class="${getSeverityBadgeClass(alert.category)}">${alert.category}</span></td>
                <td><strong>${Math.round(alert.threat_score)}</strong></td>
                <td>${alert.status}</td>
                <td>${alert.status === 'active' ? `<button class="resolve-btn" data-id="${alert.alert_id}">Resolve</button>` : '✓'}</td>
            </tr>
        `).join('');
        document.querySelectorAll('.resolve-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                await respondToAlert(btn.dataset.id, autoResponseEnabled);
                loadAlerts();
                addLogToFeed(`Alert ${btn.dataset.id} resolved`, 'info');
            });
        });
    } catch (error) { console.error('Failed to load alerts:', error); }
}

async function handleGenerateAttack(attackType) {
    addLogToFeed(`Generating ${attackType} attack...`, 'info');
    const result = await generateAttack(attackType === 'random' ? null : attackType);
    if (result.success) {
        addLogToFeed(`✅ ${attackType} attack generated! ${result.data.logs_created} logs created.`, 'critical');
        showAttackFeedback(`Attack generated! ${result.data.logs_created} logs created.`);
        await analyzeLogs(5, autoResponseEnabled);
        await loadStats();
        await loadAlerts();
    } else {
        addLogToFeed(`❌ Failed: ${result.error}`, 'error');
        showAttackFeedback(`Failed: ${result.error}`, true);
    }
}

async function handleCampaignAttack() {
    addLogToFeed(`Starting attack campaign...`, 'info');
    for (const attack of ['brute_force', 'file_activity', 'ddos']) {
        await generateAttack(attack);
        await new Promise(r => setTimeout(r, 500));
    }
    addLogToFeed(`✅ Campaign completed!`, 'critical');
    showAttackFeedback('Campaign completed! Running analysis...');
    await analyzeLogs(5, autoResponseEnabled);
    await loadStats();
    await loadAlerts();
}

function setupEventListeners() {
    document.querySelectorAll('.attack-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const type = btn.dataset.attack;
            if (type === 'campaign') await handleCampaignAttack();
            else await handleGenerateAttack(type);
        });
    });
    document.getElementById('refreshAlerts')?.addEventListener('click', async () => { await loadAlerts(); await loadStats(); });
    document.getElementById('clearLogs')?.addEventListener('click', () => {
        document.getElementById('logFeed').innerHTML = '<div class="log-entry system">Logs cleared</div>';
    });
    document.getElementById('autoResponseToggle')?.addEventListener('change', (e) => {
        autoResponseEnabled = e.target.checked;
        addLogToFeed(`Auto-response ${autoResponseEnabled ? 'ENABLED' : 'DISABLED'}`, 'info');
    });
    document.getElementById('mobileMenuBtn')?.addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('mobile-open');
    });
}

function startAutoRefresh() {
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(async () => { await loadStats(); await loadAlerts(); }, 10000);
}

async function checkAPIHealthStatus() {
    const elem = document.getElementById('apiStatus');
    if (!elem) return;
    const isHealthy = await checkAPIHealth();
    elem.textContent = isHealthy ? 'API: Connected' : 'API: Disconnected';
    elem.style.color = isHealthy ? '#00ff9d' : '#ff4444';
}
setInterval(checkAPIHealthStatus, 30000);
DASHBOARDEOF

echo "✅ Frontend setup complete!"
echo ""
echo "📁 Files created:"
echo "   - css/style.css"
echo "   - css/dark-theme.css"
echo "   - css/responsive.css"
echo "   - js/utils.js"
echo "   - js/api.js"
echo "   - js/dashboard.js"
echo ""
echo "🚀 To start frontend:"
echo "   cd ~/soc-shadow-box/frontend"
echo "   python3 -m http.server 3000"
echo ""
echo "🌐 Then open: http://localhost:3000/index.html"
