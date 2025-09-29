import os
import sys
import glob
from datetime import datetime
from openai import OpenAI

# ========== TRANSCRIBER ==========

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
WAV_DIR = os.path.join(os.path.dirname(__file__), "sandbox-waves-transcripts")

def get_latest_wav():
    """Return the most recent .wav file from WAV_DIR."""
    files = glob.glob(os.path.join(WAV_DIR, "*.wav"))
    if not files:
        raise FileNotFoundError("No .wav files found in sandbox-waves-transcripts/")
    return max(files, key=os.path.getmtime)

def transcribe(enhance=False):
    """Transcribe the latest wav file, optionally enhance with GPT cleanup."""
    audio_path = get_latest_wav()
    print(f"🎤 Using most recent file: {audio_path}")

    # --- Step 1: Whisper transcription
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    raw_text = transcript.text.strip()

    # --- Step 2: Optional GPT cleanup
    if enhance:
        print("\n✨ Enhancing transcript with GPT cleanup...")
        gpt_resp = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Clean up the following transcript for readability, fix obvious mistakes but keep the meaning:\n\n{raw_text}"
        )
        final_text = gpt_resp.output[0].content[0].text.strip()
    else:
        final_text = raw_text

    # --- Step 3: Save transcript
    base, _ = os.path.splitext(audio_path)
    md_path = base + ".md"
    txt_path = base + ".txt"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Transcript\n\n")
        f.write(final_text)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    # --- Step 4: Print summary
    print("\n--- TRANSCRIPT ---\n")
    print(final_text[:1000])  # show first 1000 chars
    if len(final_text) > 1000:
        print("... [truncated] ...")

    print(f"\nTranscript saved to:\n  {md_path}\n  {txt_path}")

# ========== ENTRY POINT ==========

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--enhance", action="store_true", help="Enhance transcript with GPT cleanup")
    args = parser.parse_args()

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\033[91mWarning: OPENAI_API_KEY not found in environment\033[0m")
        print("Transcription will fail without it. Set it with:")
        print('  setx OPENAI_API_KEY "your_key_here"\n')

    transcribe(enhance=args.enhance)
