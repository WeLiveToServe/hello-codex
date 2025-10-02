# Whisper Dictation

Whisper Dictation is a local-first CLI tool for quickly turning short voice notes into structured text.  
It is designed for speed, predictability, and extensibility — no bloat, just record → transcribe → log.

---

## Features
- **Push-to-talk recording**: Hold `SPACE` to capture audio, release to pause, `BACKSPACE` to finish.
- **Local transcription**: Audio compressed to `.mp3`, transcribed with OpenAI Whisper.
- **Session logs**:  
  - `sessions/<name>.txt` → rolling log of raw transcripts with `---` separators.  
  - `sessions/<name>.md` → rich log with raw transcript, optional enhanced text, and agent responses.  
- **Clipboard flows**: Copy last snippet and exit or continue recording seamlessly.
- **Agents integration**:  
  - [6] → Send transcript to *Agent Moneypenny* (direct GPT-4o prompt).  
  - Agents are modular — more can be added (`Agent Maxwell`, etc.).
- **UI polish**:  
  - Banners standardized to 45 characters.  
  - Agent responses displayed in green with typewriter effect.

---

## Quick Start

### Requirements
- Python 3.10+
- PowerShell 7+
- FFmpeg installed and on PATH
- Virtual environment recommended (`.venv`)

### Installation
```powershell
git clone https://github.com/WeLiveToServe/whisper-push-to-transcript.git
cd whisper-push-to-transcript
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-light.txt

### Set your API key in environment:
$env:OPENAI_API_KEY="your_api_key_here"

### Run
python flow.py

## Usage
- **Start or continue session** → enter a name or pick from recent sessions.  
- **Record snippets** → hold `SPACE` to capture, release to pause, press `BACKSPACE` to finish.  
- **Choose a post-record option** → save, re-record, append, copy to clipboard, or call an agent.  
- **Review session logs** in the `sessions/` directory.

---

## Guiding Principles
- **Local-first**: audio is temporary; text is the durable artifact.  
- **Deterministic menus**: flows behave identically every run.  
- **Separation of concerns**:  
  `recorder` ↔ `transcriber` ↔ `flow` ↔ `ui` ↔ `agents` ↔ `sessions`.

---

## Roadmap
- Add **Agent Maxwell** for structured coding prompts.  
- Toggle between instant and cinematic agent replies.  
- Expand unit tests for session handling and menu flows.  
- Optional cross-platform key handling (Windows/macOS/Linux).  
