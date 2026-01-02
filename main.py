from flask import Flask, jsonify
import os
# 모듈 전체를 가져온 뒤 클래스를 명확히 지정합니다.
import youtube_transcript_api 

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # 모듈명.클래스명.메서드명으로 경로를 아주 상세히 적어줍니다.
        srt = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['ko', 'en']
        )
        
        # 자막 텍스트 합치기
        full_text = " ".join([item['text'] for item in srt])
        
        return jsonify({
            "videoId": video_id,
            "transcript": full_text,
            "success": True
        })
    except Exception as e:
        return jsonify({
            "videoId": video_id,
            "transcript": "",
            "success": False,
            "error": str(e)
        }), 200

@app.route('/')
def home():
    return "YouTube Transcript API is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
