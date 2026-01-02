from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['ko', 'en']
        )
        text = ' '.join([t['text'] for t in transcript])
        
        return jsonify({
            'videoId': video_id,
            'transcript': text,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'videoId': video_id,
            'transcript': '',
            'success': False,
            'error': str(e)
        }), 404

@app.route('/')
def home():
    return 'YouTube Transcript API is running!'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### **2. requirements.txt**
```
flask
youtube-transcript-api
gunicorn
```

### **3. Procfile** (확장자 없음)
```
web: gunicorn main:app
