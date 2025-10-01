import os
import datetime
import keyboard
import pyperclip
import recorder_latest
import transcripter_latest

LOG_FILE = "debug_log.txt"

def log_debug(message: str, mode: str = "a"):
    """Write debug messages to debug_log.txt in repo root."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode, encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# Force a marker as soon as flow_latest.py starts
log_debug(">>> flow_latest.py started", mode="w")

def print_banner():
    print("blah")
    title = "W H I S P E R   D I C T A T I O N"
    width = 50
    print(title.center(width, "="))
    # print("                W H I S P E R   D I C T A T I O N")
    print("="*width + "\033[0m\n")

def main_menu():
    print("\033[94mWelcome to Whisper Dictation.\033[0\n")
    print("[1] Start a new transcription session")
    print("[2] Continue an existing transcription session\n")
    print("\033[92m" + "="*58 + "\033[0m")

def run_recording_loop(session_file, new_session=True):
    session_name = input("Enter a session name (leave blank to use timestamp): ")

    if not session_name.strip():
        session_name = datetime.datetime.now().strftime("%Y-%m-%d-%Hh-%Mm")

    print("\033[92m" + "="*20 + " SNIPPET RECORDING " + "="*20 + "\033[0m\n")
    print("\033[94mHold SPACE bar to record. Press BACKSPACE when done.\033[0m\n")

    recording_path = recorder_latest.record_push_to_talk()

    print("⌫ Finished.\n")

    # Call transcription
    try:
        transcript_raw, transcript_enhanced = transcripter_latest.transcribe_and_enhance(recording_path)
        print("\033[92m" + "="*22 + " TRANSCRIPT " + "="*22 + "\033[0m\n")
        print(transcript_enhanced + "\n")
        print("\033[92m" + "="*58 + "\033[0m\n")
    # Save transcripts
        txt_path = session_file + ".txt"
        md_path = session_file + ".md"

        with open(txt_path, "a", encoding="utf-8") as f:
            f.write(transcript_raw.strip() + "\n---\n")

        with open(md_path, "a", encoding="utf-8") as f:
            f.write("## Raw Transcript\n")
            f.write(transcript_raw.strip() + "\n\n")
            f.write("## Enhanced Transcript\n")
            f.write(transcript_enhanced.strip() + "\n")
            f.write("---\n")       
    except Exception as e:
        log_debug(f"Error during transcription: {e}")
        print("✗ Error transcribing audio. See debug_log.txt for details.")
        return

    # Menu after recording
    print("Do you want to keep this or re-record it?")
    print("[1] Re-record")
    print("[2] Keep and close session")
    print("[3] Keep and record another snippet")
    print("[4] Copy last snippet to clipboard and exit")
    print("[5] Copy last snippet to clipboard and record another")
    print("[6] Send transcript to GPT-4o (STUBBED)\n")
    print("\033[92m" + "="*58 + "\033[0m")

    choice = input("User Selection: ").strip()
    print(f"User Selection: [{choice}]\n")
 

    if choice == "4":
        pyperclip.copy(transcript_enhanced)
        print("✓ Copied last snippet to clipboard. Exiting.")
    elif choice == "5":
        pyperclip.copy(transcript_enhanced)
        print("✓ Copied last snippet to clipboard. You can record another.\n")
        run_recording_loop(session_file, new_session=False)
    elif choice == "1":
        print("Re-recording...")
        run_recording_loop(session_file, new_session=True)
    elif choice == "2":
        print("Session closed.")
    elif choice == "3":
        run_recording_loop(session_file, new_session=False)
    elif choice == "6":
        print("Stubbed GPT-4o send option.")
    else:
        print("Invalid choice, please try again.")

def main():
    # Banner + start menu
    print("\033[92m" + "="*58 + "\033[0m")
    print("                W H I S P E R   D I C T A T I O N")
    print("\033[92m" + "="*58 + "\033[0m\n")
    print("Welcome to Whisper Dictation.\n")
    print("blah blah blah")
    print("[1] Start a new transcription session")
    print("[2] Continue an existing transcription session\n")
    print("\033[92m" + "="*58 + "\033[0m")

    selection = input("User Selection: ").strip()
    print(f"User Selection: [{selection}]\n")

    if selection == "1":
        name = input("Enter a session name (leave blank to use timestamp): ").strip()
        if not name:
            name = datetime.datetime.now().strftime("%Y-%m-%d-%Hh-%Mm-session")
        os.makedirs("sessions", exist_ok=True)
        session_base = os.path.join("sessions", name)  # no extension
        run_recording_loop(session_file=session_base, new_session=True)

    elif selection == "2":
        sessions_dir = "sessions"
        if not os.path.isdir(sessions_dir):
            print("No existing sessions found.")
            return

        files = [f for f in os.listdir(sessions_dir) if f.lower().endswith(".txt")]
        if not files:
            print("No existing sessions found.")
            return

        files = sorted(
            files,
            key=lambda f: os.path.getmtime(os.path.join(sessions_dir, f)),
            reverse=True
        )
        recent = files[:5]

        print("\nRecent Sessions:")
        for i, fname in enumerate(recent, 1):
            print(f"[{i}] {fname}")
        print("\033[92m" + "="*58 + "\033[0m")

        sel = input("User Selection: ").strip()
        print(f"User Selection: [{sel}]\n")

        try:
            idx = int(sel) - 1
            assert 0 <= idx < len(recent)
        except Exception:
            print("Invalid selection.")
            return

        chosen_txt = os.path.join(sessions_dir, recent[idx])

        # Preview last ~50 words from .txt
        try:
            with open(chosen_txt, "r", encoding="utf-8") as f:
                words = f.read().split()
            preview = " ".join(words[-50:]) if words else "(empty file)"
            print("\nLast ~50 words preview:\n" + preview + "\n")
        except Exception:
            print("\n(Preview unavailable)\n")

        # Strip extension to pass a base path to the recorder/transcriber flow
        base_no_ext = os.path.splitext(recent[idx])[0]
        session_base = os.path.join(sessions_dir, base_no_ext)  # no extension
        run_recording_loop(session_file=session_base, new_session=False)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
