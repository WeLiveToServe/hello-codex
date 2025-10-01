# test_sessions.py
# Quick checks for sessions.py functionality

import os
import sessions

def main():
    print("=== Testing sessions.py ===")

    # 1. Make a new session base
    base = sessions.make_session_base("testsession")
    print(f"Session base: {base}")

    # 2. Append dummy transcripts
    sessions.append_entry(base, "This is the first raw transcript.")
    sessions.append_entry(base, "This is the second raw transcript with some extra words.")

    # 3. List recent sessions
    recent = sessions.list_recent()
    print("\nRecent sessions:")
    for f in recent:
        print(" -", f)

    # 4. Preview last words from the test session
    txt_file = os.path.basename(base + ".txt")
    preview = sessions.preview_last_words(txt_file, n=10)
    print(f"\nPreview of last 10 words in {txt_file}:")
    print(preview)

if __name__ == "__main__":
    main()
