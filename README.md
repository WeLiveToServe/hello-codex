# hello-codex

Voice-to-text workflow using Python + FFmpeg + OpenAI Whisper.

This repo started as a proof-of-concept (poc) and now contains a set of working CLI scripts for recording, converting, and transcribing audio files. All scripts now live in the repo root.

---

## 📂 Project Structure

```
hello-codex/
├── record_ffmpeg.py              # Record audio from system microphone via FFmpeg
├── transcribe.py                  # Transcribe most recent .wav with OpenAI Whisper
├── convert-latest-m4a.py          # Convert most recent .m4a in sandbox-m4a to .wav
├── requirements-light.txt         # Minimal dependencies
├── sandbox-waves-transcripts/     # Stores all .wav recordings and transcripts
├── sandbox-m4a-wav-converter/     # Drop .m4a files here for conversion
└── README.md
```

---

## ⚙️ Setup

1. **Clone repo and enter folder**
   ```powershell
   git clone https://github.com/WeLiveToServe/hello-codex.git
   cd hello-codex
   ```

2. **Create venv and activate**
   ```powershell
   python -m venv .venv ; .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements-light.txt
   ```

4. **Set your OpenAI key**  
   (one-time per session, or add to `$PROFILE`)
   ```powershell
   setx OPENAI_API_KEY "your_api_key_here"
   ```

---

## 🎤 Recording

Record from your system microphone (uses FFmpeg + `Jack Mic` on Windows).  
```powershell
python record_ffmpeg.py
```
- Countdown animation before recording starts  
- Press **space** to stop recording  
- Recording is saved to `sandbox-waves-transcripts/` with timestamped filename  
- Playback starts automatically after recording  

---

## 📝 Transcription

Transcribe the **most recent .wav** in `sandbox-waves-transcripts/`:
```powershell
python transcribe.py
```

- Transcript is printed to console  
- Transcript is also saved as `.txt` next to the .wav  

---

## 🔄 Converting M4A → WAV

If you have an `.m4a` (like from Apple Voice Memos), drop it in:
```
sandbox-m4a-wav-converter/
```

Then run:
```powershell
python convert-latest-m4a.py
```

- Finds the most recent `.m4a`  
- Converts it into `.wav` inside `sandbox-waves-transcripts/`  
- Output filename follows format:  
  ```
  YYYY-MM-DD-HHh-MMm-<originalname>-converted.wav
  ```

---

## ✅ Current Status
- ✅ Working FFmpeg-based recorder (no extra drivers needed)  
- ✅ OpenAI Whisper transcription integrated  
- ✅ Automatic file management (sandbox folders stay uncluttered)  
- ✅ Conversion from `.m4a` → `.wav`  

---

## 🚀 Next Steps
- Add support for more input formats  
- Improve transcript post-processing  
- Optional: merge recording + transcription into single command  
