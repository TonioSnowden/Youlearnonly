# YouLearnOnly - AI-Powered YouTube Content Filter

Chrome extension that filter all the video entertainement you can only load interesting videos.

## Overview
YouLearnOnly is a Chrome extension that uses AI to automatically filter YouTube content, allowing only informative videos while blocking entertainment content. The extension helps users stay focused on educational and informative content by analyzing video titles in real-time.

## Features
- Real-time analysis of YouTube video titles
- Automatic blocking of entertainment content
- Clean and intuitive user interface
- Backend powered by BERT model
- Containerized backend service for easy deployment

## Technical Stack
- **Frontend**: Chrome Extension (JavaScript)
- **Backend**: Flask API with Docker
- **ML Model**: BERT (bert-tiny) fine-tuned for content classification
- **Training**: Performed on Google Colab GPUs
- **Containerization**: Docker

## Model Performance
The model was trained on a custom dataset of YouTube video titles, achieving impressive results:
- Training Loss: 0.0078
- Training Accuracy: 99.87%

## Installation

### 1. Backend Setup

```bash

# Clone the repository
git clone https://github.com/yourusername/youlearnonly.git

# Navigate to the project directory
cd youlearnonly

# Start the Docker container
docker-compose up -d
```


### 2. Chrome Extension Installation
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome_extension` folder from the project directory

## Project Structure

```
youlearnonly/
├── backend/
│   ├── app.py           # Flask API
│   ├── Dockerfile       # Backend container configuration
│   └── requirements.txt
├── chrome_extension/
│   ├── manifest.json
│   ├── content.js
│   ├── background.js
│   ├── popup.html
│   └── popup.js
├── model/              # Trained BERT model files
└── docker-compose.yml
```



## How It Works
1. The extension monitors YouTube video pages
2. When a video is loaded, it extracts the title
3. The title is sent to the backend API for classification
4. If classified as entertainment, the video is blocked with an overlay
5. Users can see the classification status in the extension popup

## Development
The model was trained on a custom dataset of YouTube video titles from various channels, categorized as either informative or entertainment content. Training was performed using Google Colab's GPU resources for optimal performance.

### Training Process
- Dataset: Custom-built from YouTube channels
- Architecture: BERT-tiny
- Training Environment: Google Colab GPUs
- Optimization: AdamW optimizer
- Early Stopping: Implemented for optimal model selection

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License

## Acknowledgments
- Google Colab for providing GPU resources
- Hugging Face for the BERT implementation
- All contributors and testers
