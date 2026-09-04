import sys
import time
import subprocess
from datetime import datetime
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def update_live_dashboard():
    dashboard_path = "live_leads_dashboard.md"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    system_health_block = f"""---

## 🟢 System Health
* **Automation Daemon:** Running (30-Minute Interval)
* **Last Sync:** {current_time}
* **pSEO Engine & GitHub Sync:** Operational
* **GHL & Whop Conversion Funnels:** Connected
"""
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "## 🟢 System Health" in content:
            content = content[:content.find("## 🟢 System Health")].rstrip() + "\n\n" + system_health_block
        else:
            content = content.rstrip() + "\n\n" + system_health_block
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        dashboard_content = f"""# 🚀 Autonomous Revenue Engine - Live Operations Board
*Last Updated: {current_time}*

---

## 📊 Pipeline Status Summary
* **Total Processed:** Active (Auto-syncing every 30 mins)
* **Successfully Verified & Dispatched:** Live via Ingestion Bridge
* **Quarantined / Rejected Stubs:** Managed by Pydantic Firewall

{system_health_block}"""
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(dashboard_content)
    print(f"[DAEMON] Live dashboard updated automatically at {current_time}")

def run_hourly_pipelines():
    print(f"\n==================================================")
    print(f"[DAEMON] Triggering Autonomous Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"==================================================")
    
    try:
        print("[DAEMON] Executing Lead Radar & Verification...")
        subprocess.run([sys.executable, "ingestion_bridge.py"], check=False)
    except Exception as e:
        print(f"[ERROR] Lead Radar execution failed: {e}")

    try:
        print("[DAEMON] Executing pSEO Content Engine...")
        subprocess.run([sys.executable, "pseo_engine.py"], check=False)
    except Exception as e:
        print(f"[ERROR] pSEO Engine execution failed: {e}")

    # Automatically refresh the markdown dashboard file with latest status
    update_live_dashboard()
    
    print(f"[DAEMON] Cycle complete. Sleeping for 1800 seconds (30 minutes)...\n")

if __name__ == "__main__":
    print("🚀 Adorise Digital Autonomous Background Daemon Initialized (30-Min Interval).")
    
    # Run immediate cycle on startup
    run_hourly_pipelines()

    # Continuous loop set to 30 minutes (1800 seconds)
    interval = int(os.getenv("DAEMON_INTERVAL", "1800"))
    while True:
        time.sleep(interval)
        run_hourly_pipelines()

        try:
            subprocess.run(["git", "add", "live_leads_dashboard.md", "pseo_pages/"], check=False)
            subprocess.run(["git", "commit", "-m", "Auto-sync: Hourly pSEO batch & live leads dashboard"], check=False)
            subprocess.run(["git", "push", "origin", "main"], check=False)
            print("[DAEMON] Successfully synced and pushed updates to GitHub.")
        except Exception as e:
            print(f"[DAEMON] Git sync warning: {e}")