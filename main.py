from flask import Flask, jsonify
import os
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # [성공한 로직 적용] 1. 인스턴스 생성
        yt = YouTubeTranscriptApi()
        
        # 2. 자막 가져오기 (방법 1: fetch 사용)
        # 한국어('ko')를 우선으로 하되, 없으면 영어('en')를 가져오도록 설정
        try:
            transcript_data = yt.fetch(video_id, languages=['ko', 'en'])
        except Exception:
            # 방법 1 실패 시 방법 2 (list -> find -> fetch) 시도
            transcript_list = yt.list(video_id)
            transcript = transcript_list.find_transcript(['ko', 'en'])
            transcript_data = transcript.fetch()

        # 3. 텍스트만 추출하여 합치기
        full_text = ""
        for item in transcript_data:
            # 사용자님 코드처럼 객체 속성과 딕셔너리 방식 모두 대응
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
        # 에러 발생 시 상세 내용을 반환
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
