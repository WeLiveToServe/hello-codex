import os
import glob
import argparse
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
WAV_DIR = r"C:\Users\Keith\dev\projects\hello-codex\sandbox-waves-transcripts"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def get_latest_wav():
    files = glob.glob(os.path.join(WAV_DIR, "*.wav"))
    if not files:
        raise FileNotFoundError("No .wav files found in sandbox-waves-transcripts/")
    return max(files, key=os.path.getmtime)

def enhance_transcript(raw_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Clean up this voice transcription: fix punctuation, capitalization, and remove filler words like 'um', 'uh', 'like', and 'you know'. Keep the meaning identical. Make it readable but casual."},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"{Colors.RED}Warning: Enhancement failed ({e}). Using raw transcript.{Colors.RESET}")
        return raw_text

def format_for_markdown(text, audio_filename, enhanced=False):
    from datetime import datetime
    md = f"""# Transcript - {os.path.basename(audio_filename)}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Enhanced:** {"Yes" if enhanced else "No"}

---

{text}
"""
    return md

def print_fancy_transcript(text, enhanced=False):
    WIDTH = 60
    GREEN = Colors.GREEN
    RESET = Colors.RESET
    BIGGER = Colors.BOLD
    
    separator = "=" * WIDTH
    title = "✨ ENHANCED TRANSCRIPT ✨" if enhanced else "📝 TRANSCRIPT 📝"
    
    # Match "VOICE MEMO WORKFLOW" formatting
    print(f"\n{separator.center(80)}")
    print(f"{GREEN}{BIGGER}{title.center(80)}{RESET}")
    print(f"{separator.center(80)}\n")
    
    # Wrap transcript body nicely
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > WIDTH:
            print(line)
            line = word
        else:
            line = f"{line} {word}" if line else word
    if line:
        print(line)
    
    print(f"\n{separator.center(80)}\n")

def transcribe(enhance=False):
    audio_path = get_latest_wav()
    print(f"{Colors.BOLD}Using:{Colors.RESET} {os.path.basename(audio_path)}")
    print(f"{Colors.YELLOW}Transcribing...{Colors.RESET}")

    try:
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="en"
            )
    except Exception as e:
        print(f"{Colors.RED}Error during transcription: {e}{Colors.RESET}")
        return

    raw_text = transcript.text.strip()
    final_text = enhance_transcript(raw_text) if enhance else raw_text

    base, _ = os.path.splitext(audio_path)
    md_path, txt_path = base + ".md", base + ".txt"
    
    with open(md_path, "w", encoding="utf-8") as out:
        out.write(format_for_markdown(final_text, audio_path, enhanced=enhance))
    with open(txt_path, "w", encoding="utf-8") as out:
        out.write(final_text)

    print_fancy_transcript(final_text, enhanced=enhance)
    print(f"{Colors.GREEN}✓{Colors.RESET} Markdown saved: hello-codex\\sandbox-waves-transcripts\\{os.path.basename(md_path)}")
    print(f"{Colors.GREEN}✓{Colors.RESET} Plain text saved: hello-codex\\sandbox-waves-transcripts\\{os.path.basename(txt_path)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe the most recent .wav file")
    parser.add_argument("--enhance", action="store_true", help="Post-process transcript with GPT cleanup")
    args = parser.parse_args()
    
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Colors.RED}Error: OPENAI_API_KEY not found in environment{Colors.RESET}")
        print("Set it with: setx OPENAI_API_KEY \"your_key_here\"")
        exit(1)
    
    transcribe(enhance=args.enhance)
