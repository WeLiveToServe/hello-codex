import sounddevice as sd
import numpy as np
import sys
import time
import threading
from scipy.io.wavfile import write
from datetime import datetime
import os

# settings
SAMPLE_RATE = 44100
CHANNELS = 2          # stereo input
DEVICE_INDEX = 10     # Stereo Mix device index

# globals
recording = []
is_recording = False
start_time = None

def spinner():
    symbols = "|/-\\"
    i = 0
    while is_recording:
        elapsed = int(time.time() - start_time)
        sys.stdout.write(f"\rRecording... {symbols[i % len(symbols)]}  {elapsed}s ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\rRecording stopped.            \n")
    sys.stdout.flush()

def countdown(msg, seconds):
    for i in range(seconds, 0, -1):
        print(f"{msg} {i}")
        time.sleep(1)

def record_audio():
    global recording, is_recording, start_time
    recording.clear()

    def callback(indata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)
        recording.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE,
                        channels=CHANNELS,
                        callback=callback,
                        device=DEVICE_INDEX):
        start_time = time.time()
        is_recording = True
        spinner_thread = threading.Thread(target=spinner)
        spinner_thread.start()

        input()  # wait for Enter to stop
        is_recording = False
        spinner_thread.join()

def main():
    ans = input("record now? (Y/N): ").strip().lower()
    if ans != "y":
        print("ok maybe later")
        return

    print("starting in 3 seconds, hit enter key to finish recording")
    countdown("Starting in", 3)
    print("Recording... press Enter to stop")
    record_audio()

    print("\ncleaning up:")
    countdown("Cleaning up in", 3)

    ts = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm")
    filename = f"{ts}-recording.wav"

    outdir = os.path.join(os.path.dirname(__file__), "sandbox-waves-transcripts")
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, filename)

    audio = np.concatenate(recording, axis=0)
    write(outfile, SAMPLE_RATE, audio)
    print(f"Saved recording to {outfile}")

if __name__ == "__main__":
    main()
