import os
from datetime import datetime
from openai import OpenAI

# Create a client
client = OpenAI()

def transcribe_and_enhance(audio_path):
    """
    Transcribes audio with Whisper and enhances with GPT-4o-mini.
    Returns (raw_transcript, enhanced_transcript).
    """
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    raw_text = transcript.text.strip()

    # Enhance with GPT
    # enhanced = client.chat.completions.create(
    #    model="gpt-4o-mini",
     #   messages=[
     #       {"role": "system", "content": "You are a helpful assistant that cleans up spoken transcripts for clarity."},
     #       {"role": "user", "content": raw_text}
     #   ]
    #)
    #enhanced_text = enhanced.choices[0].message.content.strip()
   
    return raw_text, raw_text

def save_transcripts(session_file, raw_text, enhanced_text, audio_file):
    """
    Saves raw and enhanced transcripts into a .md debug log,
    and appends only enhanced text into the rolling .txt session file.
    """
    base_name = os.path.splitext(session_file)[0]
    md_path = base_name + ".md"
    txt_path = base_name + ".txt"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write MD log (debugging)
    with open(md_path, "a", encoding="utf-8") as f:
        f.write(f"# Transcript Update - {os.path.basename(audio_file)}\n\n")
        f.write(f"**Generated:** {timestamp}\n")
        f.write(f"**Enhanced:** Yes\n\n")
        f.write("---\n\n")
        f.write("**Raw Whisper Output**\n\n")
        f.write(raw_text + "\n\n")
        f.write("**Enhanced Transcript**\n\n")
        f.write(enhanced_text + "\n\n")
        f.write("---------------------------\n\n")

    # Write rolling TXT (user log)
    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(enhanced_text + "\n")
        f.write("\n---\n\n")

    return md_path, txt_path
