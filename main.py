from flask import Flask, jsonify
import os
# 모듈을 yta라는 별칭으로 가져와 클래스 이름과 확실히 분리합니다.
import youtube_transcript_api as yta

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # yta(모듈) 안의 YouTubeTranscriptApi(클래스)를 명확히 호출합니다.
        transcript_list = yta.YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['ko', 'en']
        )
        
        # 자막 텍스트만 합치기
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
