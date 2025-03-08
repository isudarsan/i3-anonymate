import os
from text_anonymizer import TextAnonymizer

# Path to the log file generated during integration tests
LOG_FILE = "../logstest/application-direct-log.txt"
OUTPUT_FILE = "../logstest/pii_detection_result.txt"

def detect_pii():
    """Reads the log file, detects PII, and writes the result to OUTPUT_FILE."""
    text_anonymizer = TextAnonymizer()

    if not os.path.exists(LOG_FILE):
        print(f"Error: Log file {LOG_FILE} not found!")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        logs = file.read()

    # Call AnonyMate (i3-anonymate) to detect PII
    result = text_anonymizer.process(text=logs, detect_language=True, detect=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        if result.get('entities'):
            output.write("Caution: PII detected in logs!\n")
            for entity in result['entities']:
                output.write(f"{entity['type']} found at position {entity['start']}-{entity['end']}\n")
            print("❌ PII detected! Failing build...")
            exit(1)
        else:
            output.write("✅ No PII detected.\n")
            print("✅ No PII detected.")

if __name__ == "__main__":
    detect_pii()
