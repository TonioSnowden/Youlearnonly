// work well
function getVideoTitle() {
    const titleElement = document.querySelector('h1.ytd-video-primary-info-renderer');
    const title = titleElement ? titleElement.textContent.trim() : '';
    return title;
}

// Function to mock prediction 
function mockPredictTitle(title) {
    return "Entertainment";
}

// Function to block the video
function blockVideo() {
    // Create a full-screen blocking overlay
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
            <p style="font-size: 18px;">YouLearnOnly only allows informative content.</p>
        </div>
    `;

    // Add the overlay to the body
    document.body.appendChild(blockOverlay);

    // Pause the video after the overlay is shown
    setTimeout(() => {
        const video = document.querySelector('video');
        if (video) {
            video.pause();
        }
    }, 100);
}

// Function to check video and block if necessary
function checkAndBlockVideo() {
    const title = getVideoTitle();
    if (title) {
        console.log('Video title:', title);
        const prediction = mockPredictTitle(title);
        console.log('Prediction:', prediction);
        if (prediction === "Entertainment") {
            blockVideo();
        }
    }
}

// Watch for navigation to video pages
if (typeof lastUrl === 'undefined') {
    let lastUrl = location.href;
    new MutationObserver(() => {
        if (location.href !== lastUrl) {
            lastUrl = location.href;
            if (location.href.includes('/watch')) {
                setTimeout(checkAndBlockVideo, 1000);
            }
        }
    }).observe(document, {subtree: true, childList: true});

    // Initial check if we're already on a video page
    if (location.href.includes('/watch')) {
        checkAndBlockVideo();
    }
}