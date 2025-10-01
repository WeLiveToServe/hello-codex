# ui.py
# Presentation-only functions for Whisper Dictation CLI
# Width set to 45 characters, green font for consistency

import sys
import time
from rich.console import Console
from rich.markdown import Markdown

console = Console()

GREEN = "\033[92m"
RESET = "\033[0m"
WIDTH = 45

def banner(title: str = "Whisper Dictation:"):
    """Print the main banner with a title."""
    print(f"{GREEN}{title.center(WIDTH)}{RESET}\n")

def divider():
    """Print a simple green divider line."""
    print(f"{GREEN}{'-' * WIDTH}{RESET}")

def menu_start() -> str:
    """Display the startup menu and return the user's choice."""
    banner()
    print("Welcome to Whisper Dictation.\n")
    print("[1] Start a new transcription session")
    print("[2] Continue an existing transcription session\n")
    divider()
    return input("User Selection: ").strip()

def menu_post_record() -> str:
    """Display the post-record menu and return the user's choice."""
    print("Do you want to keep this or re-record it?")
    print("[1] Re-record")
    print("[2] Keep and close session")
    print("[3] Keep and record another snippet")
    print("[4] Copy last snippet to clipboard and exit")
    print("[5] Copy last snippet to clipboard and record another")
    print("[6] Send transcript to GPT-4o (STUBBED)\n")
    divider()
    return input("User Selection: ").strip()

def show_preview(preview_text: str):
    """Show preview text for continuing a session."""
    print("\nLast ~50 words preview:\n")
    print(preview_text + "\n")
    divider()

def show_transcript(transcript_text: str):
    """Show a transcript block with heading and divider."""
    print(f"{GREEN}{'TRANSCRIPT'.center(WIDTH)}{RESET}\n")
    print(transcript_text + "\n")
    divider()

def snippet_recording_banner():
    """Show the snippet recording banner and instructions."""
    print(f"{GREEN}{'SNIPPET RECORDING'.center(WIDTH)}{RESET}\n")
    print("Hold SPACE bar to record. Press BACKSPACE when done.\n")


def pretty_print_response(text: str, delay: float = 0.01):
    """
    Nicely formats the agent response in green with typewriter effect.
    Uses rich to handle markdown (##, **, etc).
    """
    md = Markdown(text)

    console.print("")  # spacing before response

    # Render line by line, typewriter style
    for line in text.splitlines():
        for char in line:
            console.print(char, style="green", end="")
            sys.stdout.flush()
            time.sleep(delay)
        console.print("")  # newline after each line

    console.print("")  # final spacing
