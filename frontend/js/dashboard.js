let riskChart = null;
let refreshInterval = null;
let autoResponseEnabled = true;
let isUpdating = false;

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Premium Dashboard initializing...');
    await initPremiumRiskMeter();
    await loadStats();
    await loadAlerts();
    setupEventListeners();
    startAutoRefresh();
    checkAPIHealthStatus();
    updateDateTime();
});

async function initPremiumRiskMeter() {
    const canvas = document.getElementById('riskGauge');
    if (!canvas) return;
    
    // Set canvas size
    canvas.width = 280;
    canvas.height = 280;
    
    const ctx = canvas.getContext('2d');
    
    riskChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 100],
                backgroundColor: ['#00ff9d', 'rgba(18, 22, 59, 0.9)'],
                borderWidth: 0,
                circumference: 360,
                rotation: -90,
                cutout: '75%',
                borderRadius: 20,
                hoverOffset: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            animation: {
                animateRotate: true,
                duration: 1000,
                easing: 'easeOutQuart'
            },
            plugins: { 
                tooltip: { enabled: false }, 
                legend: { display: false }
            }
        }
    });
}

function animateNumber(element, start, end, duration = 800) {
    if (!element) return;
    const startTime = performance.now();
    const updateCounter = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(start + (end - start) * easeOutQuart);
        element.textContent = current;
        if (progress < 1) requestAnimationFrame(updateCounter);
    };
    requestAnimationFrame(updateCounter);
}

function updateRiskMeter(score) {
    const riskScoreElem = document.getElementById('riskScore');
    const currentScore = parseInt(riskScoreElem?.textContent) || 0;
    animateNumber(riskScoreElem, currentScore, score, 1000);
    
    const riskLevelElem = document.getElementById('riskLevel');
    let riskLevel, riskClass;
    
    if (score >= 86) {
        riskLevel = '⚠️ CRITICAL RISK ⚠️';
        riskClass = 'critical';
    } else if (score >= 61) {
        riskLevel = '🔴 HIGH RISK';
        riskClass = 'high';
    } else if (score >= 31) {
        riskLevel = '🟡 MEDIUM RISK';
        riskClass = 'medium';
    } else {
        riskLevel = '🟢 LOW RISK';
        riskClass = 'low';
    }
    
    if (riskLevelElem) {
        riskLevelElem.style.opacity = '0';
        riskLevelElem.style.transform = 'scale(0.9)';
        setTimeout(() => {
            riskLevelElem.textContent = riskLevel;
            riskLevelElem.className = `risk-level ${riskClass}`;
            riskLevelElem.style.transition = 'all 0.4s cubic-bezier(0.34, 1.2, 0.64, 1)';
            riskLevelElem.style.opacity = '1';
            riskLevelElem.style.transform = 'scale(1)';
        }, 150);
    }
    
    let chartColor;
    if (score >= 86) chartColor = '#ff4444';
    else if (score >= 61) chartColor = '#ff8844';
    else if (score >= 31) chartColor = '#ffaa44';
    else chartColor = '#00ff9d';
    
    if (riskChart) {
        const percentage = Math.min(100, Math.max(0, score));
        riskChart.data.datasets[0].data = [percentage, 100 - percentage];
        riskChart.data.datasets[0].backgroundColor[0] = chartColor;
        riskChart.update({ duration: 800, easing: 'easeOutQuart' });
    }
}

async function loadStats() {
    if (isUpdating) return;
    isUpdating = true;
    
    try {
        const result = await getDetectionStats();
        if (result.success && result.data.statistics) {
            const activeAlerts = result.data.statistics.active_alerts || 0;
            const totalAttacks = result.data.statistics.total_alerts || 0;
            const blockedIPs = result.data.statistics.blocked_ips || 0;
            const aiDetections = result.data.statistics.ai_detections || 0;
            
            animateNumber(document.getElementById('activeAlerts'), 
                parseInt(document.getElementById('activeAlerts').textContent) || 0, 
                activeAlerts, 500);
            animateNumber(document.getElementById('totalAttacks'), 
                parseInt(document.getElementById('totalAttacks').textContent) || 0, 
                totalAttacks, 500);
            animateNumber(document.getElementById('blockedIPs'), 
                parseInt(document.getElementById('blockedIPs').textContent) || 0, 
                blockedIPs, 500);
            animateNumber(document.getElementById('aiDetections'), 
                parseInt(document.getElementById('aiDetections').textContent) || 0, 
                aiDetections, 500);
        }
        
        const alerts = await getAlerts('active', 5);
        if (alerts.success && alerts.data.alerts && alerts.data.alerts.length > 0) {
            const maxScore = Math.max(...alerts.data.alerts.map(a => a.threat_score));
            updateRiskMeter(Math.round(maxScore));
        } else {
            updateRiskMeter(0);
        }
    } catch (error) {
        console.error('Failed to load stats:', error);
    } finally {
        setTimeout(() => { isUpdating = false; }, 500);
    }
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
            <tr style="animation: fadeIn 0.3s ease">
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
                loadStats();
                addLogToFeed(`Alert resolved`, 'info');
            });
        });
    } catch (error) {
        console.error('Failed to load alerts:', error);
    }
}

async function handleGenerateAttack(attackType) {
    addLogToFeed(`Generating ${attackType} attack...`, 'info');
    const result = await generateAttack(attackType === 'random' ? null : attackType);
    
    if (result.success) {
        addLogToFeed(`✅ ${attackType} attack generated!`, 'critical');
        showAttackFeedback(`Attack generated!`);
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
    showAttackFeedback('Campaign completed!');
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
    
    document.getElementById('refreshAlerts')?.addEventListener('click', async () => {
        await loadAlerts();
        await loadStats();
        addLogToFeed('Manual refresh triggered', 'info');
    });
    
    document.getElementById('clearLogs')?.addEventListener('click', () => {
        document.getElementById('logFeed').innerHTML = '<div class="log-entry system">Logs cleared</div>';
    });
    
    document.getElementById('autoResponseToggle')?.addEventListener('change', (e) => {
        autoResponseEnabled = e.target.checked;
        addLogToFeed(`Auto-response ${autoResponseEnabled ? 'ENABLED' : 'DISABLED'}`, 'info');
    });
    
    document.getElementById('mobileMenuBtn')?.addEventListener('click', () => {
        document.getElementById('sidebar')?.classList.toggle('mobile-open');
    });
}

function startAutoRefresh() {
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(async () => {
        await loadStats();
        await loadAlerts();
    }, 15000);
}

async function checkAPIHealthStatus() {
    const apiStatusElem = document.getElementById('apiStatus');
    const statusDot = document.getElementById('statusDot');
    const systemStatus = document.getElementById('systemStatus');
    
    if (!apiStatusElem) return;
    
    const isHealthy = await checkAPIHealth();
    
    if (isHealthy) {
        apiStatusElem.textContent = 'API: Connected';
        apiStatusElem.className = 'api-status connected';
        if (statusDot) statusDot.className = 'status-dot online';
        if (systemStatus) systemStatus.textContent = 'System Online';
    } else {
        apiStatusElem.textContent = 'API: Disconnected';
        apiStatusElem.className = 'api-status disconnected';
        if (statusDot) statusDot.className = 'status-dot offline';
        if (systemStatus) systemStatus.textContent = 'System Offline';
    }
}

function updateDateTime() {
    const elem = document.getElementById('datetime');
    if (elem) {
        const now = new Date();
        elem.textContent = now.toLocaleString('en-US', {
            month: 'short', day: 'numeric', year: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit'
        });
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    .stat-value {
        transition: all 0.3s cubic-bezier(0.34, 1.2, 0.64, 1);
        display: inline-block;
        min-width: 60px;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// Initial calls
updateDateTime();
setInterval(updateDateTime, 1000);
setInterval(checkAPIHealthStatus, 10000);

// Force initial load
setTimeout(() => {
    loadStats();
}, 500);
