// Suppress blob URL warnings (harmless on localhost)
(function() {
    const originalWarn = console.warn;
    console.warn = function(...args) {
        const message = args[0] || '';
        if (typeof message === 'string' && message.includes('blob:') && message.includes('insecure')) {
            return; // Ignore blob HTTPS warnings
        }
        originalWarn.apply(console, args);
    };
    
    const originalError = console.error;
    console.error = function(...args) {
        const message = args[0] || '';
        if (typeof message === 'string' && message.includes('blob:') && message.includes('insecure')) {
            return; // Ignore blob HTTPS warnings
        }
        originalError.apply(console, args);
    };
})();
