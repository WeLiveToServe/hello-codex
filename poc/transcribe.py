import os
import glob
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
WAV_DIR = os.path.join(os.path.dirname(__file__), "sandbox-waves-transcripts")

def get_latest_wav():
    files = glob.glob(os.path.join(WAV_DIR, "*.wav"))
    if not files:
        raise FileNotFoundError("No .wav files found in sandbox-waves-transcripts/")
    return max(files, key=os.path.getmtime)

def transcribe():
    # 1. Find most recent wav
    audio_path = get_latest_wav()
    print(f"Using most recent file: {audio_path}")

    # 2. Transcribe
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    text = transcript.text.strip()

    # 3. Save transcript as .txt next to wav
    base, _ = os.path.splitext(audio_path)
    txt_path = base + ".txt"
    with open(txt_path, "w", encoding="utf-8") as out:
        out.write(text)

    # 4. Print results
    print("\n--- TRANSCRIPT ---")
    print(text)
    print(f"\nTranscript saved to: {txt_path}")

if __name__ == "__main__":
    transcribe()
