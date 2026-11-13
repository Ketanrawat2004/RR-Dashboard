import os
import json

transcript_path = r"C:\Users\hp\.gemini\antigravity\brain\86e75d6e-a557-49fb-a93b-7211dec7e1a0\.system_generated\logs\transcript_full.jsonl"
compact_path = r"C:\Users\hp\.gemini\antigravity\brain\86e75d6e-a557-49fb-a93b-7211dec7e1a0\.system_generated\logs\transcript.jsonl"

for path in [compact_path, transcript_path]:
    if os.path.exists(path):
        print(f"Checking {path}...")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f):
                if any(x in line for x in ["Russell", "Maxwell", "Bumrah"]) and any(y in line for y in ["192", "378", "120"]):
                    try:
                        data = json.loads(line)
                        print(f"Step {data.get('step_index')}, source {data.get('source')}, type {data.get('type')}")
                        content = str(data.get("content", ""))
                        if "192" in content:
                            for l in content.split("\n"):
                                if "192" in l and any(k in l for k in ["Russell", "pressure", "Balls", "Deliveries"]):
                                    print("   ", l.strip()[:100])
                    except Exception as e:
                        pass
