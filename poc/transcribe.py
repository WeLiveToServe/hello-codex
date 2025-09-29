import os
import sys
from openai import OpenAI
from datetime import datetime
import pathlib

def main():
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <path-to-audio.wav>")
        sys.exit(1)

    audio_path = pathlib.Path(sys.argv[1])
    if not audio_path.exists():
        print(f"Error: file not found -> {audio_path}")
        sys.exit(1)

    # get API key from env
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set in environment.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    try:
        with open(audio_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=f
            )

        text = transcription.text.strip()

        # print to terminal
        print("\n--- Transcript ---\n")
        print(text)
        print("\n------------------\n")

        # determine timestamp prefix from audio filename
        stem = audio_path.stem
        if "-recording" in stem:
            prefix = stem.split("-recording")[0]
        else:
            prefix = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm")

        # always save transcript into sandbox-waves-transcripts
        outdir = os.path.join(os.path.dirname(__file__), "sandbox-waves-transcripts")
        os.makedirs(outdir, exist_ok=True)
        txt_file = os.path.join(outdir, f"{prefix}-transcript.txt")

        with open(txt_file, "w", encoding="utf-8") as out:
            out.write(text + "\n")

        print(f"Transcript saved to {txt_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
