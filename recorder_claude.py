import os
import sys
import time
import threading
import subprocess
from datetime import datetime
import keyboard

# Directories
WAV_DIR = r"C:\Users\Keith\dev\projects\hello-codex\sandbox-waves-transcripts"
os.makedirs(WAV_DIR, exist_ok=True)

DEVICE_NAME = "Jack Mic (Realtek High Definition Audio)"  # adjust if needed
REPO_ROOT = r"C:\Users\Keith\dev\projects\hello-codex"

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

def spinner(stop_event, recording_event, paused_event):
    RED, GREEN, YELLOW, RESET = "\x1b[31m", "\x1b[32m", "\x1b[33m", "\x1b[0m"
    symbols = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        if recording_event.is_set():
            sys.stdout.write(f"\r{RED}🔴 RECORDING...{RESET} {symbols[i % len(symbols)]}  (release SPACE to pause, BACKSPACE to finish)    ")
        elif paused_event.is_set():
            sys.stdout.write(f"\r{YELLOW}⏸️  PAUSED{RESET} (hold SPACE to continue, BACKSPACE to finish)    ")
        else:
            sys.stdout.write(f"\r{GREEN}⏸️  Ready{RESET} (hold SPACE to start recording)    ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

# --------- Core ---------

def record_push_to_talk():
    ts = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm")
    outpath = os.path.join(WAV_DIR, f"{ts}-recording.wav")
    temp_files = []

    proc = None
    recording_event = threading.Event()
    paused_event = threading.Event()
    stop_event = threading.Event()
    has_recorded = threading.Event()
    segment_count = [0]

    # Start spinner
    spinner_thread = threading.Thread(
        target=spinner,
        args=(stop_event, recording_event, paused_event),
        daemon=True
    )
    spinner_thread.start()

    def start_recording():
        nonlocal proc
        if not recording_event.is_set():
            recording_event.set()
            paused_event.clear()
            has_recorded.set()

            segment_count[0] += 1
            temp_path = os.path.join(WAV_DIR, f".temp_segment_{segment_count[0]}.wav")
            temp_files.append(temp_path)

            cmd = [
                "ffmpeg", "-y",
                "-f", "dshow",
                "-i", f"audio={DEVICE_NAME}",
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                temp_path
            ]

            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    def pause_recording():
        nonlocal proc
        if recording_event.is_set() and proc:
            recording_event.clear()
            paused_event.set()
            try:
                if proc.stdin:
                    proc.stdin.write(b"q\n")
                    proc.stdin.flush()
            except Exception:
                pass
            proc.wait()
            proc = None

    # Keyboard bindings
    keyboard.on_press_key("space", lambda _: start_recording())
    keyboard.on_release_key("space", lambda _: pause_recording())

    print("\nHold SPACE to record, release to pause")
    print("Press BACKSPACE when finished\n")

    # Wait for BACKSPACE to exit
    keyboard.wait("backspace")

    # Cleanup
    stop_event.set()
    if recording_event.is_set():
        pause_recording()

    keyboard.unhook_all()
    spinner_thread.join()

    if has_recorded.is_set() and temp_files:
        print(f"\n✓ Combining {len(temp_files)} segment(s)...\n")

        if len(temp_files) == 1:
            os.rename(temp_files[0], outpath)
        else:
            concat_list = os.path.join(WAV_DIR, ".concat_list.txt")
            with open(concat_list, "w") as f:
                for temp_file in temp_files:
                    f.write(f"file '{os.path.basename(temp_file)}'\n")

            concat_cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_list,
                "-c", "copy",
                outpath
            ]

            subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=WAV_DIR)

            for temp_file in temp_files:
                try: os.remove(temp_file)
                except: pass
            try: os.remove(concat_list)
            except: pass

        return outpath
    else:
        print("\n✗ No recording was made.\n")
        return None

def playback(outpath):
    print("\nProcessing waveform...")
    fancy_countdown("Processing")
    print("Playing back recording (press SPACE to stop)...")

    proc = subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", outpath],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    def stop_playback():
        try: proc.terminate()
        except Exception: pass

    hk = keyboard.add_hotkey("space", stop_playback)
    proc.wait()
    keyboard.remove_hotkey(hk)
    print("\nPlayback finished.\n")

def main():
    outpath = record_push_to_talk()
    if outpath:
        playback(outpath)
        short_path = outpath.replace(REPO_ROOT + "\\", "")
        print(f"Saved recording to {short_path}")
        return outpath
    return None

if __name__ == "__main__":
    main()
