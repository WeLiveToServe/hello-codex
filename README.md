# Whisper Push to Transcript

Whisper Push to Transcript is a Python project for capturing audio notes, transcribing them with OpenAI
Whisper, and producing clean text outputs. It is intended as a simple foundation for voice-driven coding,
documentation, and automation workflows.

---

## Project Story

Whisper Push to Transcript started as an idea to take notes in audio format without needing a dedicated
app or manually transferring files between recorders and other tools. The solution was built around a
command-line interface.

The repository began with three core files:
- a Python script for **recording**
- a Python script for **transcription**
- a Python script that **combines recording and transcription into one flow**

Initial scaffolding and coding work was done with ChatGPT+. Later, after Claude released Sonnet 4.5,
development was migrated into that environment, which helped clean and improve the structure. Although
casual, the project has already proven useful.

Typical usage flow:
- Run `flow_rec_TRX_Claude.py`
- Press **Yes** to begin
- Hold **spacebar** to record; release to pause; press again to resume
- Press **backspace** to finish recording
- Choose whether to transcribe using OpenAI Whisper
- Optionally run post-processing for cleaner output

This project represents my first end-to-end app and GitHub repository.

---

## Features
- Record audio locally from microphone
- Push audio files to OpenAI Whisper for transcription
- Clean and normalize transcripts for readability
- Pause/resume audio capture with keyboard controls
- Simple CLI-driven workflow

---

## Repository Layout
```
whisper-push-to-transcript/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   └── whisper_transcript/
│       ├── __init__.py
│       ├── transcriber.py       # handles Whisper API calls and returns raw text
│       ├── postprocess.py       # cleanup functions: normalize text, punctuation
│       ├── utils.py             # helpers: paths, save, logging
│       └── cli.py               # CLI entry point
├── poc/
│   └── record.py                # proof-of-concept microphone recorder
├── flow_rec_TRX_Claude.py       # integrated record+transcribe flow with keyboard control
└── tests/
    ├── test_transcriber.py
    ├── test_postprocess.py
    └── test_utils.py
```

---

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/WeLiveToServe/whisper-push-to-transcript.git
   cd whisper-push-to-transcript
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate # Linux/Mac
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set your OpenAI API key:
   ```
   $env:OPENAI_API_KEY="your_key_here"     # PowerShell
   export OPENAI_API_KEY="your_key_here"   # Linux/Mac
   ```

---

## Usage

**Run the combined flow**
```
python flow_rec_TRX_Claude.py
```
- Hold **spacebar** to record
- Release **spacebar** to pause
- Press **spacebar** again to resume
- Press **backspace** to stop and choose to transcribe
- Transcript saved and optionally post-processed

**Transcribe an existing file**
```
python -m whisper_transcript.cli --file samples/test.wav --output transcript.txt
```

**Proof-of-concept recorder**
```
python poc/record.py
```

---

## Roadmap
- Add real-time transcription (streaming microphone input)
- Prefect flow integration for automated pipelines
- Advanced post-processing (summaries, code block extraction, task lists)
- Support for local Whisper models (e.g., whisper.cpp)

---

## License
MIT License
