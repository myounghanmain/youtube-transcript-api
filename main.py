from flask import Flask, jsonify
import youtube_transcript_api

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # 모듈을 직접 참조하여 호출 (가장 안전한 방법)
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
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
        }), 200

@app.route('/')
def home():
    return 'YouTube Transcript API is running!'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
