from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # 1. 자막 리스트를 먼저 가져옴
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # 2. 한국어(ko) 또는 영어(en) 자막을 찾음 (자동 생성 포함)
        try:
            transcript = transcript_list.find_transcript(['ko', 'en'])
        except:
            # 3. 못 찾으면 아무 언어나 첫 번째 자막 시도
            transcript = transcript_list.find_manually_created_transcript() or \
                         transcript_list.find_generated_transcript()

        data = transcript.fetch()
        text = ' '.join([t['text'] for t in data])
        
        return jsonify({
            'videoId': video_id,
            'language': transcript.language_code,
            'transcript': text,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'videoId': video_id,
            'transcript': '',
            'success': False,
            'error': str(e)
        }), 200  # n8n에서 에러로 멈추지 않게 200으로 반환

@app.route('/')
def home():
    return 'YouTube Transcript API is running!'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
