// Improved export function without blob URL warning
function exportToCSV(data, filename) {
    // Create CSV content
    let csv = "Timestamp,Source IP,Event Type,Severity,Details,Threat Score,Attack ID\n";
    
    data.forEach(log => {
        const row = [
            `"${log.timestamp}"`,
            `"${log.source_ip}"`,
            `"${log.event_type}"`,
            `"${log.severity}"`,
            `"${JSON.stringify(log.details).replace(/"/g, '""')}"`,
            log.threat_score || 0,
            `"${log.attack_id || ''}"`
        ].join(',');
        csv += row + '\n';
    });
    
    // Use data: URI instead of blob to avoid HTTPS warning
    // This method doesn't trigger the insecure connection warning
    const encodedUri = encodeURIComponent(csv);
    const link = document.createElement('a');
    link.setAttribute('href', 'data:application/csv;charset=utf-8,' + encodedUri);
    link.setAttribute('download', filename);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
