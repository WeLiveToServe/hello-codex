# sessions.py
# Handles session directory, file paths, and log writing.

import os
from datetime import datetime

SESSIONS_DIR = "sessions"

def ensure_dir():
    """Ensure sessions directory exists."""
    os.makedirs(SESSIONS_DIR, exist_ok=True)

def make_session_base(name: str = "") -> str:
    """
    Return a base path (no extension).
    If name is blank, use timestamp format.
    """
    ensure_dir()
    if not name:
        name = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm-session")
    return os.path.join(SESSIONS_DIR, name)

def append_entry(base: str, raw_text: str):
    """
    Append raw_text to .txt and .md logs.
    TXT: just raw text, then '---'
    MD: raw + enhanced sections, enhanced mirrors raw for now.
    """
    txt_path = base + ".txt"
    md_path = base + ".md"

    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(raw_text.strip() + "\n---\n")

    with open(md_path, "a", encoding="utf-8") as f:
        f.write("## Raw Transcript\n")
        f.write(raw_text.strip() + "\n\n")
        f.write("## Enhanced Transcript\n")
        f.write(raw_text.strip() + "\n")
        f.write("---\n")

def list_recent(n: int = 5):
    """Return list of recent session .txt files, newest first."""
    if not os.path.isdir(SESSIONS_DIR):
        return []
    files = [
        f for f in os.listdir(SESSIONS_DIR)
        if f.lower().endswith(".txt")
    ]
    files = sorted(
        files,
        key=lambda f: os.path.getmtime(os.path.join(SESSIONS_DIR, f)),
        reverse=True
    )
    return files[:n]

def preview_last_words(txt_file: str, n: int = 50) -> str:
    """
    Return last n words from a .txt file.
    Returns '(empty file)' if no content.
    """
    path = os.path.join(SESSIONS_DIR, txt_file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            words = f.read().split()
        if not words:
            return "(empty file)"
        return " ".join(words[-n:])
    except Exception:
        return "(preview unavailable)"
