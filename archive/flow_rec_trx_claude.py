import os
import sys
import msvcrt
from datetime import datetime

import recorder_claude
import transcripter_claude

SESSION_DIR = os.path.join(
    r"C:\Users\Keith\dev\projects\whisper-push-to-transcript",
    "sessions"
)
os.makedirs(SESSION_DIR, exist_ok=True)


def get_menu_choice():
    print("Welcome to Whisper Dictation.")
    print("[1] Start a new transcription session")
    print("[2] Add on to an existing transcription session")
    print()

    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode("utf-8")
            if char in ["1", "2"]:
                print(f"Selected: {char}")
                return char


def get_post_record_choice():
    print("\nDo you want to keep this or re-record it?")
    print("[1] Re-record")
    print("[2] Keep and close session")
    print("[3] Keep and record a new snippet to add")
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode("utf-8")
            if char in ["1", "2", "3"]:
                print(f"Selected: {char}")
                return char


def pick_recent_session():
    txts = [
        os.path.join(SESSION_DIR, f)
        for f in os.listdir(SESSION_DIR)
        if f.lower().endswith(".txt")
    ]
    if not txts:
        print("No existing session transcripts found.")
        return None

    txts.sort(key=os.path.getmtime, reverse=True)
    top5 = txts[:5]

    print("\nRecent sessions:")
    for i, f in enumerate(top5, 1):
        print(f"[{i}] {os.path.basename(f)}")

    print("Select a number to continue:")
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode("utf-8")
            if char.isdigit():
                idx = int(char)
                if 1 <= idx <= len(top5):
                    print(f"Selected: {idx}")
                    return top5[idx - 1]


def run_recording_loop(session_file):
    while True:
        recorder_claude.fancy_countdown("Starting in")
        recording_path = recorder_claude.record_push_to_talk()
        if not recording_path:
            print("No recording was made. Exiting.")
            return

        # Always transcribe + enhance
        transcripter_claude.transcribe(
            audio_override=recording_path,
            enhance=True,
            append=True,
            session_base=session_file
        )

        choice = get_post_record_choice()
        if choice == "1":
            print("\nDiscarding last attempt. Re-recording...\n")
            continue
        elif choice == "2":
            print("\nTranscript saved. Session closed.\n")
            return
        elif choice == "3":
            print("\nTranscript appended. Record another...\n")
            continue


def main():
    GREEN, RESET, BIGGER = "\033[92m", "\033[0m", "\033[1m"
    title = "💬 VOICE MEMO WORKFLOW 💬"
    separator = "=" * 60

    print(f"{separator.center(80)}")
    print(f"{GREEN}{BIGGER}{title.center(80)}{RESET}")
    print(f"{separator.center(80)}\n")

    choice = get_menu_choice()

    if choice == "1":
        # New session: prompt for name
        name = input("Enter a session name (leave blank to use timestamp): ").strip()
        if not name:
            name = datetime.now().strftime("%Y-%m-%d-%Hh-%Mm-session")
        base_path = os.path.join(SESSION_DIR, name)
        session_file = base_path + ".txt"
        run_recording_loop(session_file=session_file)

    elif choice == "2":
        # Continue existing session
        session_file = pick_recent_session()
        if session_file:
            run_recording_loop(session_file=session_file)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("\033[91mWarning: OPENAI_API_KEY not found in environment\033[0m")
        print("Transcription will fail without it. Set it with:")
        print('  setx OPENAI_API_KEY "your_key_here"\n')

    main()
