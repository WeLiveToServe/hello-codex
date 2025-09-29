import os
import glob
from datetime import datetime
from pydub import AudioSegment

INPUT_DIR = r"C:\Users\Keith\dev\hello-codex\poc\sandbox-m4a-wav-converter"
OUTPUT_DIR = r"C:\Users\Keith\dev\hello-codex\poc\sandbox-waves-transcripts"

def get_latest_m4a():
    files = glob.glob(os.path.join(INPUT_DIR, "*.m4a"))
    if not files:
        raise FileNotFoundError("No .m4a files found in input directory")
    return max(files, key=os.path.getmtime)

def build_output_name(src_path):
    base = os.path.splitext(os.path.basename(src_path))[0]

    # Detect if filename starts with YYYY-MM-DD-HHh-MMm
    parts = base.split("-", 5)
    has_timestamp = (
        len(parts) >= 5
        and parts[0].isdigit()
        and parts[1].isdigit()
        and "h" in parts[2]
        and "m" in parts[3]
    )

    if has_timestamp:
        prefix = "-".join(parts[:4])
        remainder = "-".join(parts[4:])
        name = f"{prefix}-{remainder}-converted.wav"
    else:
        ts = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm")
        name = f"{ts}-{base}-converted.wav"

    return os.path.join(OUTPUT_DIR, name)

def convert_latest():
    src = get_latest_m4a()
    dst = build_output_name(src)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    audio = AudioSegment.from_file(src, format="m4a")
    audio.export(dst, format="wav")

    print(f"Converted {src} -> {dst}")

if __name__ == "__main__":
    convert_latest()
