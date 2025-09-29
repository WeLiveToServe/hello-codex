import os
import sys
import time
import threading
import subprocess
from datetime import datetime
import keyboard

WAV_DIR = os.path.join(os.path.dirname(__file__), "sandbox-waves-transcripts")
os.makedirs(WAV_DIR, exist_ok=True)

DEVICE_NAME = "Jack Mic (Realtek High Definition Audio)"  # change if needed

# --------- UI helpers ---------

def animate_line(prefix, target, delay=0.06):
    sys.stdout.write("\r" + " " * (len(prefix) + len(target) + 2))
    sys.stdout.flush()
    sys.stdout.write("\r" + prefix + " ")
    sys.stdout.flush()
    buf = ""
    for ch in target:
        buf += ch
        sys.stdout.write("\r" + prefix + " " + buf)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n\n")
    sys.stdout.flush()

def fancy_countdown(label="Starting in"):
    animate_line(label + ":", "3......2......1......")

def spinner(stop_event):
    RED, RESET = "\x1b[31m", "\x1b[0m"
    symbols = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rRecording... {RED}{symbols[i % len(symbols)]}{RESET}  (press SPACE to stop)")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\rRecording stopped.                             \n\n")
    sys.stdout.flush()

# --------- Core ---------

def record_with_ffmpeg():
    ts = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm")
    outpath = os.path.join(WAV_DIR, f"{ts}-recording.wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "dshow",
        "-i", f"audio={DEVICE_NAME}",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        outpath
    ]
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    stop_event = threading.Event()
    t = threading.Thread(target=spinner, args=(stop_event,), daemon=True)
    t.start()

    keyboard.wait("space")
    stop_event.set()
    try:
        if proc.stdin:
            proc.stdin.write(b"q\n")
            proc.stdin.flush()
    except Exception:
        pass
    proc.wait()
    t.join()

    return outpath

def playback(outpath):
    print("Processing waveform...")
    fancy_countdown("Processing")
    print("Playing back recording (press SPACE to stop)...")

    proc = subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", outpath],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    def stop_playback():
        try:
            proc.terminate()
        except Exception:
            pass

    hk = keyboard.add_hotkey("space", stop_playback)
    proc.wait()
    keyboard.remove_hotkey(hk)
    print("\nPlayback finished.\n")

def main():
    ans = input("record now? (Y/N): ").strip().lower()
    if ans != "y":
        print("ok maybe later")
        return

    print()
    fancy_countdown("Starting in")
    outpath = record_with_ffmpeg()
    playback(outpath)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    relpath = os.path.relpath(outpath, repo_root)
    print(f"Saved recording to {relpath}")

if __name__ == "__main__":
    main()
