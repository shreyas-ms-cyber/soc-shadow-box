// Complete CSV Export - NO BLOB, NO HTTPS WARNING
function exportToCSV(data, filename) {
    if (!data || data.length === 0) {
        alert('No data to export');
        return false;
    }
    
    // Build CSV string directly
    let csvString = '';
    
    // Add headers
    const headers = ['Timestamp', 'Source IP', 'Event Type', 'Severity', 'Details', 'Threat Score', 'Attack ID'];
    csvString += headers.join(',') + '\n';
    
    // Add data rows
    for (const row of data) {
        const escapedRow = [
            `"${row.timestamp || ''}"`,
            `"${row.source_ip || ''}"`,
            `"${row.event_type || ''}"`,
            `"${row.severity || ''}"`,
            `"${JSON.stringify(row.details || {}).replace(/"/g, '""')}"`,
            row.threat_score || 0,
            `"${row.attack_id || ''}"`
        ].join(',');
        csvString += escapedRow + '\n';
    }
    
    // Create a temporary textarea to copy the CSV content
    // This avoids blob URLs entirely
    const textarea = document.createElement('textarea');
    textarea.value = csvString;
    textarea.style.position = 'fixed';
    textarea.style.top = '-1000px';
    textarea.style.left = '-1000px';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    
    // Show success message
    alert('CSV data copied to clipboard! You can paste it into a text file and save as .csv');
    return true;
}

// Alternative method using hidden iframe (no blob)
function downloadCSVUsingIframe(data, filename) {
    const csvContent = data;
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    iframeDoc.open();
    iframeDoc.write('<html><head><title>CSV Export</title></head><body>');
    iframeDoc.write('<pre>' + csvContent + '</pre>');
    iframeDoc.write('</body></html>');
    iframeDoc.close();
    
    // Trigger save dialog
    iframe.contentWindow.print();
    
    setTimeout(() => {
        document.body.removeChild(iframe);
    }, 1000);
}
