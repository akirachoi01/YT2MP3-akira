import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert_to_mp3():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path='downloads')
        base, ext = os.path.splitext(out_file)
        mp3_file = base + '.mp3'
        AudioSegment.from_file(out_file).export(mp3_file, format='mp3')
        os.remove(out_file)
        return send_file(mp3_file, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5000)