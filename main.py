from flask import Flask, jsonify
import os
# 모듈을 yta라는 별칭으로 가져와서 클래스 이름과 확실히 분리합니다.
import youtube_transcript_api as yta

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # yta(모듈) 안의 YouTubeTranscriptApi(클래스)를 명확하게 호출합니다.
        # 이 방식은 파이썬에서 가장 명시적이고 오류가 없는 호출법입니다.
        transcript_list = yta.YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['ko', 'en']
        )
        
        # 자막 텍스트만 하나로 합치기
        full_text = ' '.join([t['text'] for t in transcript_list])
        
        return jsonify({
            'videoId': video_id,
            'transcript': full_text,
            'success': True
        })
    except Exception as e:
        # 에러가 나더라도 어떤 에러인지 정확히 보여줍니다.
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
    # Render 환경에 맞는 포트 설정
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
