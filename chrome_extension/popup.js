document.addEventListener('DOMContentLoaded', () => {
    const statusDiv = document.getElementById('status');
    
    // Get current tab
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
      const currentUrl = tabs[0].url;
      if (currentUrl.includes('youtube.com/watch')) {
        // For demo purposes, showing random status
        const isAllowed = Math.random() >= 0.5;
        statusDiv.className = `status ${isAllowed ? 'allowed' : 'blocked'}`;
        statusDiv.textContent = isAllowed ? 
          'Current video: Informative content ✓' : 
          'Current video: Entertainment content ✗';
      } else {
        statusDiv.textContent = 'Navigate to a YouTube video';
      }
    });
  });