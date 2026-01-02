from flask import Flask, jsonify
import os
from youtube_transcript_api import YouTubeTranscriptApi as yta

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # .join으로 수정되었습니다.
        transcript = yta.get_transcript(video_id, languages=['ko', 'en'])
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
        }), 200

@app.route('/')
def home():
    return 'YouTube Transcript API is running!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
