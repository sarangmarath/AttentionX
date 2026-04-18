from flask import Flask, render_template, request, send_file, jsonify
from moviepy import VideoFileClip
import librosa
import numpy as np
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def find_highlights(audio_path, num_clips=3, clip_duration=60):
    y, sr = librosa.load(audio_path, sr=None)
    energy = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(np.arange(len(energy)), sr=sr)
    
    highlights = []
    used = []
    sorted_indices = np.argsort(energy)[::-1]
    
    for idx in sorted_indices:
        t = times[idx]
        overlap = any(abs(t - u) < clip_duration for u in used)
        if not overlap:
            highlights.append(t)
            used.append(t)
        if len(highlights) == num_clips:
            break
    
    return sorted(highlights)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400
    
    file = request.files['video']
    clip_duration = int(request.form.get('duration', 60))
    uid = str(uuid.uuid4())[:8]
    video_path = os.path.join(UPLOAD_FOLDER, f'{uid}.mp4')
    file.save(video_path)
    
    video = VideoFileClip(video_path)

    # Check if video has audio
    if video.audio is None:
        # No audio — just split into equal clips instead
        highlights = [i * clip_duration for i in range(3) if i * clip_duration < video.duration]
    else:
        audio_path = os.path.join(UPLOAD_FOLDER, f'{uid}.wav')
        video.audio.write_audiofile(audio_path)
        highlights = find_highlights(audio_path, clip_duration=clip_duration)
    
    clips = []
    for i, start in enumerate(highlights):
        end = min(start + clip_duration, video.duration)
        start = max(0, start - 5)
        clip = video.subclipped(start, end)
        
        # Crop to vertical 9:16
        w, h = clip.size
        new_w = int(h * 9 / 16)
        x_center = w // 2
        x1 = max(0, x_center - new_w // 2)
        clip = clip.cropped(x1=x1, width=new_w)
        
        out_filename = f'{uid}_clip{i+1}.mp4'
        out_path = os.path.join(OUTPUT_FOLDER, out_filename)
        clip.write_videofile(out_path, logger=None)
        clips.append({
            'download': f'/download/{out_filename}',
            'preview': f'/static/outputs/{out_filename}',
            'label': f'Clip {i+1}'
        })
    
    video.close()
    return jsonify({'clips': clips})

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)