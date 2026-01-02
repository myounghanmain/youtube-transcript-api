from flask import Flask, jsonify
import os
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # [로컬 성공 로직] 1. 인스턴스 생성
        yt = YouTubeTranscriptApi()
        
        # [로컬 성공 로직] 2. fetch 메서드 사용 (한국어/영어 순)
        transcript_data = yt.fetch(video_id, languages=['ko', 'en'])
        
        # 3. 텍스트 추출 및 합치기
        full_text = ""
        for item in transcript_data:
            # 객체 속성(.text) 또는 딕셔너리(['text']) 모두 대응
            if hasattr(item, 'text'):
                full_text += item.text + " "
            elif isinstance(item, dict):
                full_text += item['text'] + " "
            else:
                full_text += str(item) + " "
        
        return jsonify({
            'videoId': video_id,
            'transcript': full_text.strip(),
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
