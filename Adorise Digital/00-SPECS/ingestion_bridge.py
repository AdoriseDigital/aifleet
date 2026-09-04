import os
import json
from revenue_engine import ProductionRevenueSystem

def ingest_raw_leads_from_source(source_name: str, raw_records: list):
    """
    Unified intake bridge for all external tools, scrapers, and multi-model inputs.
    """
    print(f"\n================================================================================")
    print(f"[INGESTION BRIDGE] Receiving batch from source: {source_name.upper()} ({len(raw_records)} records)")
    print(f"================================================================================")
    
    system = ProductionRevenueSystem()
    
    passed_count = 0
    rejected_count = 0
    
    for record in raw_records:
        success = system.process_lead(record)
        if success:
            passed_count += 1
        else:
            rejected_count += 1
            
    print(f"\n[SUMMARY] Batch processed from {source_name}:")
    print(f"  -> Successfully Verified & Dispatched: {passed_count}")
    print(f"  -> Quarantined/Rejected Stubs: {rejected_count}")
    print(f"================================================================================")

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
    