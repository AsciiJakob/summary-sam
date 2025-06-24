import whisper
import copy

model = whisper.load_model("turbo", device="cuda")

def whisper_transcribe(file_path, speaker_name):
    try:
        options = whisper.DecodingOptions()
        result = model.transcribe(file_path, language="en", temperature=0, word_timestamps=False, verbose=False)
        return copy.deepcopy(result)

    finally:
        # Clean up manually
        # os.remove(temp_wav_path)
        print("whisper done")
