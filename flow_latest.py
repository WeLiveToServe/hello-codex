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
    print("\033[92m" + "="*58)
    print("                W H I S P E R   D I C T A T I O N")
    print("="*58 + "\033[0m\n")

def main_menu():
    print("Welcome to Whisper Dictation.\n")
    print("[1] Start a new transcription session")
    print("[2] Continue an existing transcription session\n")
    print("\033[92m" + "="*58 + "\033[0m")

def run_recording_loop(session_file, new_session=True):
    print("User Selection: [1]\n")
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

    choice = input("User Selection: ")
    print(f"User Selection: [{choice}]")

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
    print_banner()
    main_menu()

    selection = input("User Selection: ")
    print(f"User Selection: [{selection}]\n")

    if selection == "1":
        run_recording_loop(session_file=None, new_session=True)
    elif selection == "2":
        print("Continue session not implemented yet.")
    else:
        print("Invalid selection. Exiting.")

if __name__ == "__main__":
    main()
