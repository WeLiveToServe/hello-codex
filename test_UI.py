# test_UI.py
# Quick test script to exercise ui.py functions
# Prints banners and menus in sequence with dummy text

import ui

def main():
    print(">>> Testing banner()")
    ui.banner()

    print("\n>>> Testing divider()")
    ui.divider()

    print("\n>>> Testing snippet_recording_banner()")
    ui.snippet_recording_banner()

    print("\n>>> Testing show_transcript()")
    ui.show_transcript("This is a sample transcript for testing.")

    print("\n>>> Testing show_preview()")
    ui.show_preview("These are the last ~50 words shown as a preview...")

    print("\n>>> Testing menu_start() [simulated]")
    print("[SIMULATION] Instead of input, showing options:")
    ui.banner()
    print("Welcome to Whisper Dictation.\n")
    print("[1] Start a new transcription session")
    print("[2] Continue an existing transcription session\n")
    ui.divider()

    print("\n>>> Testing menu_post_record() [simulated]")
    print("[SIMULATION] Instead of input, showing options:")
    print("Do you want to keep this or re-record it?")
    print("[1] Re-record")
    print("[2] Keep and close session")
    print("[3] Keep and record another snippet")
    print("[4] Copy last snippet to clipboard and exit")
    print("[5] Copy last snippet to clipboard and record another")
    print("[6] Send transcript to GPT-4o (STUBBED)\n")
    ui.divider()

if __name__ == "__main__":
    main()
