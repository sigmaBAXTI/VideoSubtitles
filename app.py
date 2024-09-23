from flask import Flask, request, render_template, send_file
import assemblyai as aai
from models import transcribe_audio_file, save_subtitles_to_file
import os
import re
from io import BytesIO

app = Flask(__name__)

# HTML sahifasini render qilish
@app.route('/')
def index():
    return render_template('index.html')


# Subtitrlarnini ekstraksiya qilish uchun yo'l
@app.route('/extract-subtitles', methods=['POST'])
def extract_subtitles():
    if 'video' not in request.files:
        return "No file uploaded", 400

    video_file = request.files['video']
    video_path = os.path.join("uploads", video_file.filename)
    video_file.save(video_path)

    # AssemblyAI API kalitingizni qo'shing
    api_key = "c5c24b01481448daa5e56f3f08f2ba9b"
    subtitles = transcribe_audio_file(video_path, api_key)

    # Fayl nomidan raqamlarni ajratib olish
    match = re.search(r'\d+', video_file.filename)
    if match:
        subtitle_name = f"{match.group()}.srt"
    else:
        subtitle_name = "subtitles.srt"

    # SRT faylini yaratish
    srt_file = BytesIO()
    srt_file.write(subtitles.encode('utf-8'))
    srt_file.seek(0)

    return send_file(srt_file, as_attachment=True, download_name=subtitle_name, mimetype="text/srt")


if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
