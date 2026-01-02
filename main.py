from flask import Flask, jsonify
import os
# 모듈을 통째로 가져옵니다.
import youtube_transcript_api

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # 모듈 내의 YouTubeTranscriptApi 클래스를 명확하게 지정하여 호출합니다.
        # youtube_transcript_api(모듈) . YouTubeTranscriptApi(클래스) . get_transcript(메서드)
        data = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['ko', 'en']
        )
        
        # 자막 텍스트만 하나로 합치기
        full_text = ' '.join([t['text'] for t in data])
        
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
