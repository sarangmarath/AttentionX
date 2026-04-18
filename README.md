# AttentionX - Automated Content Repurposing Engine

AttentionX is a web app that transforms long-form videos like lectures, podcasts, and workshops into short clips ready for TikTok and Instagram Reels.

## Features
- Upload any long video (MP4, MOV, AVI)
- Auto-detects high-energy moments using audio analysis
- Smart crops to vertical 9:16 format for TikTok/Reels
- Custom clip duration slider (15s to 120s)
- Preview clips directly in the browser
- Download all generated clips

## Tech Stack
- Backend: Python, Flask
- Video Processing: MoviePy
- Audio Analysis: Librosa
- Frontend: HTML, CSS, JavaScript

## How to Run

1. Clone the repo:
git clone https://github.com/sarangmarath/AttentionX.git
cd AttentionX

2. Install dependencies:
pip install flask moviepy librosa

3. Run the app:
python app.py

4. Open browser and go to:
http://localhost:5000

## Demo Video
[Click here to watch the demo](#)

## Built for
AttentionX Hackathon by UnsaidTalks
