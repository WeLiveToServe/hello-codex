import os
import sys
import msvcrt

import recorder_claude
import transcripter_claude

def get_yn_input(prompt):
    print(prompt, end='', flush=True)
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8').lower()
            if char in ['y', 'n']:
                print(char.upper())
                return char == 'y'

def main():
    GREEN, RESET, BIGGER = '\033[92m', '\033[0m', '\033[1m'
    title = "💬 VOICE MEMO WORKFLOW 💬"
    separator = "="*60

    print(f"{separator.center(80)}")
    print(f"{GREEN}{BIGGER}{title.center(80)}{RESET}")
    print(f"{separator.center(80)}\n")

    if not get_yn_input("Start recording session? (Y/N): "):
        print("Maybe later!")
        return

    print()
    recorder_claude.fancy_countdown("Starting in")

    # Record
    recording_path = recorder_claude.record_push_to_talk()
    if not recording_path:
        print("No recording was made. Exiting.")
        return

    # Playback
    recorder_claude.playback(recording_path)

    # Transcribe?
    print()
    if get_yn_input("Transcribe now? (Y/N): "):
        enhance = get_yn_input("Enhance with GPT cleanup? (Y/N): ")
        print()
        transcripter_claude.transcribe(enhance=enhance)
    else:
        print(f"\nRecording saved at: {recording_path}")
        print("You can transcribe it later with: python transcripter_claude.py")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("\033[91mWarning: OPENAI_API_KEY not found in environment\033[0m")
        print("Transcription will fail without it. Set it with:")
        print('  setx OPENAI_API_KEY "your_key_here"\n')

    main()
