import os
import json

def ingest_radar_leads():
    radar_file = "radar_scraped_leads.json"
    if os.path.exists(radar_file):
        with open(radar_file, "r") as f:
            try:
                leads = json.load(f)
                if leads:
                    ingest_raw_leads_from_source("social_listening_radar", leads)
                    with open(radar_file, "w") as fw:
                        json.dump([], fw)
                    return
            except Exception as e:
                print(f"[ERROR] Failed to parse radar leads: {e}")
    print("[INGESTION BRIDGE] Radar queue empty. Waiting for social listening scan results...")

if __name__ == "__main__":
    ingest_radar_leads()
    