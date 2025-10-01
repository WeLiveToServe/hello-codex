import os
import queue
import sounddevice as sd
import soundfile as sf
import keyboard
from datetime import datetime
from pydub import AudioSegment

def record_push_to_talk():
    q = queue.Queue()
    samplerate = 44100
    channels = 1

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(indata.copy())

    os.makedirs("sessions", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm-recording")
    wav_outpath = os.path.join("sessions", f"{timestamp}.wav")

    print("Recording... Press BACKSPACE when done.")

    last_state = None  # track last state for printing

    with sf.SoundFile(wav_outpath, mode="w", samplerate=samplerate, channels=channels) as file:
        with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
            while True:
                if keyboard.is_pressed("backspace"):
                    print("⌫ Finished.")
                    break
                elif keyboard.is_pressed("space"):
                    if last_state != "recording":
                        print("🎙️  Recording...")
                        last_state = "recording"
                    file.write(q.get())
                else:
                    if last_state != "paused":
                        print("⏸️  Paused")
                        last_state = "paused"
                    # don’t spam, just wait briefly
                    sd.sleep(200)

    # after finishing recording, convert to mp3
    mp3_outpath = wav_outpath.replace(".wav", ".mp3")
    try:
        AudioSegment.from_wav(wav_outpath).export(mp3_outpath, format="mp3")
        print(f"✓ Compressed recording saved as {mp3_outpath}")
        return mp3_outpath
    except Exception as e:
        print(f"MP3 conversion failed: {e}")
        return wav_outpath
