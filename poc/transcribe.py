import sys
from pathlib import Path
from openai import OpenAI

def transcribe_audio(audio_file: str) -> str:
    """
    Transcribe an audio file using OpenAI's API.
    Requires OPENAI_API_KEY in environment.
    """
    client = OpenAI()

    with open(audio_file, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )
    return transcript.text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file.wav>")
        sys.exit(1)

    audio_path = Path(sys.argv[1])
    if not audio_path.exists():
        print(f"File not found: {audio_path}")
        sys.exit(1)

    text = transcribe_audio(str(audio_path))
    print("\n--- TRANSCRIPT ---\n")
    print(text)
