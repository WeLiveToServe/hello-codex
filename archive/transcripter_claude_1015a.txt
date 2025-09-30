import os
import glob
from datetime import datetime
from openai import OpenAI

REPO_ROOT = r"C:\Users\Keith\dev\projects\whisper-push-to-transcript"
SESSION_DIR = os.path.join(REPO_ROOT, "sessions")
os.makedirs(SESSION_DIR, exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def get_latest_audio():
    files = glob.glob(os.path.join(SESSION_DIR, "*.mp3"))
    if not files:
        raise FileNotFoundError("No audio files found in sessions/")
    return max(files, key=os.path.getmtime)


def enhance_transcript(raw_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Clean up this voice transcription: fix punctuation, capitalization, and remove filler words. Keep meaning identical.",
                },
                {"role": "user", "content": raw_text},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"{Colors.RED}Warning: Enhancement failed ({e}). Using raw transcript.{Colors.RESET}")
        return raw_text


def format_for_markdown(text, audio_filename, enhanced=False):
    md = f"""# Transcript Update - {os.path.basename(audio_filename)}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Enhanced:** {"Yes" if enhanced else "No"}

---

{text}
"""
    return md


def transcribe(audio_override=None, enhance=True, append=False, session_base=None):
    if audio_override:
        audio_path = audio_override
    else:
        audio_path = get_latest_audio()

    print(f"{Colors.YELLOW}Transcribing...{Colors.RESET}")

    try:
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="en",
            )
    except Exception as e:
        print(f"{Colors.RED}Error during transcription: {e}{Colors.RESET}")
        return

    raw_text = transcript.text.strip()
    final_text = enhance_transcript(raw_text) if enhance else raw_text

    if append and session_base:
        base_name, _ = os.path.splitext(session_base)
        md_path = base_name + ".md"
        txt_path = base_name + ".txt"

        with open(md_path, "a", encoding="utf-8") as out:
            out.write("\n\n" + format_for_markdown(final_text, audio_path, enhanced=enhance))
        with open(txt_path, "a", encoding="utf-8") as out:
            out.write("\n\n" + final_text)

        print(f"{Colors.GREEN}✓ Transcript appended to session files{Colors.RESET}")

    else:
        base, _ = os.path.splitext(audio_path)
        md_path = base + ".md"
        txt_path = base + ".txt"

        with open(md_path, "w", encoding="utf-8") as out:
            out.write(format_for_markdown(final_text, audio_path, enhanced=enhance))
        with open(txt_path, "w", encoding="utf-8") as out:
            out.write(final_text)

        print(f"{Colors.GREEN}✓ Transcript saved as standalone files{Colors.RESET}")

    print("\n--- Enhanced Transcript ---\n")
    print(final_text)
    print("\n---------------------------\n")
