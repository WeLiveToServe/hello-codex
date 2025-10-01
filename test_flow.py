# test_flow.py
# Mocked test harness for flow.py orchestration.

import builtins
import os
import flow

# --- Mocks ---

# Fake recorder just returns a dummy mp3 path
def fake_record_push_to_talk():
    print("[MOCK] recorder called")
    return "sessions/fake_recording.mp3"

# Fake transcriber returns fixed text
def fake_transcribe_and_enhance(path):
    print(f"[MOCK] transcriber called with {path}")
    return ("raw transcript here", "enhanced transcript here")

# Monkeypatch modules
flow.recorder_latest.record_push_to_talk = fake_record_push_to_talk
flow.transcripter_latest.transcribe_and_enhance = fake_transcribe_and_enhance

# --- Fake input() responses ---
# Sequence of inputs the test will feed:
# 1 = new session, "testflow" as name, then choose option 2 (keep and close)
inputs = iter([
    "1",          # menu_start() → New session
    "testflow",   # session name
    "2"           # menu_post_record() → Keep and close session
])

def fake_input(prompt=""):
    try:
        val = next(inputs)
        print(f"{prompt}{val}")
        return val
    except StopIteration:
        return "2"  # default fallback

# Monkeypatch input
builtins.input = fake_input

# --- Run test ---
def main():
    print("=== Running flow.py test with mocks ===")
    flow.main()

    txt_path = os.path.join("sessions", "testflow.txt")
    md_path = os.path.join("sessions", "testflow.md")

    # --- Second run: continue most recent session ---
    print("\n=== Running continue-session test ===")

    # reset fake inputs for continue flow
    cont_inputs = iter([
        "2",  # menu_start() → Continue session
        "1",  # pick first recent file
        "2"   # post-record menu → Keep and close
    ])

    def cont_fake_input(prompt=""):
        try:
            val = next(cont_inputs)
            print(f"{prompt}{val}")
            return val
        except StopIteration:
            return "2"

    builtins.input = cont_fake_input

    flow.main()

    print("\n--- Session File Check ---")
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            print("TXT Content:\n", f.read())
    else:
        print("No TXT file found.")

    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            print("MD Content:\n", f.read())
    else:
        print("No MD file found.")

if __name__ == "__main__":
    main()
