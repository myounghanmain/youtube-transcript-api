from flask import Flask, jsonify
import os
from youtube_transcript import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # 새로운 라이브러리 방식으로 호출
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # 텍스트 데이터만 합치기
        full_text = ' '.join([t['text'] for t in transcript_list])
        
        return jsonify({
            'videoId': video_id,
            'transcript': full_text,
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
