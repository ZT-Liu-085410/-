import whisper

def transcribe(wav_path):
    model = whisper.load_model("base")
    result = model.transcribe(wav_path, language='zh')
    return result['text']
