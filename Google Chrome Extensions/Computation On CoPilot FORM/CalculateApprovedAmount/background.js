chrome.runtime.onInstalled.addListener((details) => {
    console.log('Extension installed or updated:', details);

    if (details.reason === 'install') {
        console.log('Extension installed for the first time.');
    } else if (details.reason === 'update') {
        console.log('Extension updated to a new version.');
    }
});

chrome.runtime.onStartup.addListener(() => {
    console.log('Chrome has started.');
});