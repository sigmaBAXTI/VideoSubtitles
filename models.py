import assemblyai as aai

def transcribe_audio_file(file_path, api_key):
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    subtitles = transcript.export_subtitles_srt()
    return subtitles

def save_subtitles_to_file(subtitles, output_path):
    with open(output_path, "w") as file:
        file.write(subtitles)
