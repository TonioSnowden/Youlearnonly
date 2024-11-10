// Function to get video title with retries
async function getVideoTitleWithRetry(maxRetries = 5, delay = 1000) {
    for (let i = 0; i < maxRetries; i++) {
        const titleElement = document.querySelector('h1.ytd-video-primary-info-renderer');
        if (titleElement && titleElement.textContent.trim()) {
            return titleElement.textContent.trim();
        }
        await new Promise(resolve => setTimeout(resolve, delay));
    }
    return null;
}

// Update the predictTitle function with better error handling
async function predictTitle(title) {
    try {
        console.log('Sending prediction request for:', title);
        const response = await fetch('http://localhost:5001/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Prediction response:', data);
        return data.prediction;
    } catch (error) {
        console.error('Error predicting title:', error);
        return 'Error';
    }
}

// Function to block the video
function blockVideo() {
    const blockOverlay = document.createElement('div');
    blockOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.97);
        z-index: 9999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: Arial, sans-serif;
    `;

    blockOverlay.innerHTML = `
        <div style="
            background-color: #ffebee;
            color: #c62828;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            max-width: 600px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h1 style="margin-bottom: 20px;">Access Denied</h1>
            <p style="font-size: 18px; margin-bottom: 15px;">This video has been classified as entertainment content.</p>
            <p style="font-size: 18px; margin-bottom: 25px;">YouLearnOnly only allows informative content.</p>
            <a href="https://www.youtube.com" style="
                display: inline-block;
                background-color: #c62828;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                font-size: 16px;
                transition: background-color 0.2s;
            ">Return to YouTube Home</a>
        </div>
    `;

    document.body.appendChild(blockOverlay);

    setTimeout(() => {
        const video = document.querySelector('video');
        if (video) {
            video.pause();
        }
    }, 100);
}

// Update the checkAndBlockVideo function
async function checkAndBlockVideo() {
    console.log('Checking video...');
    const title = await getVideoTitleWithRetry();
    
    if (title) {
        console.log('Video title detected:', title);
        const prediction = await predictTitle(title);
        console.log('Prediction received:', prediction);
        
        if (prediction === "Entertainment") {
            console.log('Blocking entertainment video');
            blockVideo();
        }
    } else {
        console.warn('Could not detect video title after retries');
    }
}

// Improved navigation watching
let lastUrl = location.href;
const observer = new MutationObserver(async (mutations) => {
    if (location.href !== lastUrl) {
        lastUrl = location.href;
        if (location.href.includes('/watch')) {
            console.log('URL changed to video page, initiating check...');
            // Wait for page to load
            await new Promise(resolve => setTimeout(resolve, 1500));
            await checkAndBlockVideo();
        }
    }
});

// Start observing with improved configuration
observer.observe(document.body, {
    subtree: true,
    childList: true,
    characterData: true
});

// Initial check with delay
if (location.href.includes('/watch')) {
    console.log('Initial video page detected');
    setTimeout(async () => {
        await checkAndBlockVideo();
    }, 1500);
}