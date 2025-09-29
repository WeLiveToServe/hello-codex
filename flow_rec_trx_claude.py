import os
import sys

# Import the recording and transcription modules
import recorder_claude
import transcripter_claude

def main():
    print("="*60)
    print("VOICE MEMO WORKFLOW")
    print("="*60)
    print()
    
    ans = input("Start recording session? (Y/N): ").strip().lower()
    if ans != "y":
        print("Maybe later!")
        return
    
    print()
    recorder_claude.fancy_countdown("Starting in")
    
    # Step 1: Record (with pause/resume)
    recording_path = recorder_claude.record_push_to_talk()
    
    if not recording_path:
        print("No recording was made. Exiting.")
        return
    
    # Playback
    recorder_claude.playback(recording_path)
    
    # Step 2: Ask about transcription
    print()
    transcribe_ans = input("Transcribe now? (Y/N): ").strip().lower()
    
    if transcribe_ans == "y":
        # Ask about enhancement
        enhance_ans = input("Enhance with GPT cleanup? (Y/N): ").strip().lower()
        enhance = (enhance_ans == "y")
        
        print()
        transcripter_claude.transcribe(enhance=enhance)
    else:
        print(f"\nRecording saved at: {recording_path}")
        print("You can transcribe it later by running: python transcripter_claude.py")

if __name__ == "__main__":
    # Check for API key if transcription might be needed
    if not os.getenv("OPENAI_API_KEY"):
        print("\033[91mWarning: OPENAI_API_KEY not found in environment\033[0m")
        print("Transcription will fail without it. Set it with:")
        print('  setx OPENAI_API_KEY "your_key_here"\n')
    
    main()