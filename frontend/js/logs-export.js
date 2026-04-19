// Fixed export function - no blob URL warning
function exportLogsToCSV(logs) {
    if (!logs || logs.length === 0) {
        console.log('No logs to export');
        return;
    }
    
    // Create CSV headers
    const headers = ['Timestamp', 'Source IP', 'Event Type', 'Severity', 'Details', 'Threat Score', 'Attack ID'];
    
    // Create CSV rows
    const rows = logs.map(log => [
        log.timestamp,
        log.source_ip,
        log.event_type,
        log.severity,
        JSON.stringify(log.details).replace(/,/g, ';').replace(/"/g, "'"),
        log.threat_score || 0,
        log.attack_id || ''
    ]);
    
    // Combine headers and rows
    const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n');
    
    // Use data URI instead of blob - NO HTTPS WARNING
    const dataUri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvContent);
    
    // Create download link
    const link = document.createElement('a');
    link.setAttribute('href', dataUri);
    link.setAttribute('download', `logs_export_${new Date().toISOString().slice(0,19)}.csv`);
    link.style.position = 'absolute';
    link.style.left = '-9999px';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Show success message
    const exportBtn = document.getElementById('exportLogs');
    const originalText = exportBtn.textContent;
    exportBtn.textContent = '✅ Exported!';
    setTimeout(() => {
        exportBtn.textContent = originalText;
    }, 2000);
}
