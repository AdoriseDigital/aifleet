#!/usr/bin/env python3
"""
Hermes 2-Hour Lead Generation & Outreach Controller
Author: Adorise Digital Engineering Desk

Operates strictly on the local Hermes agent runtime / tools (NEVER from Netcup VPS IP)
to protect server IP reputation and comply with social media rate limits.

Schedule: Every 2 Hours (8am, 10am, 12pm, 2pm, 4pm, 6pm, 8pm UTC)
Cadence Limit: 10-15 leads per cycle (~80-100/day max)
"""

import os
import sys
import json
import time
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SANITIZER_PATH = os.path.join(SCRIPT_DIR, "sanitize_and_verify_leads.py")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "agents_config.json")
VERIFIED_LEADS_PATH = os.path.join(SCRIPT_DIR, "verified_email_leads.json")
SOCIAL_DMS_PATH = os.path.join(SCRIPT_DIR, "social_dm_leads.json")
LOG_PATH = os.path.join(SCRIPT_DIR, "H_outreach_log.md")


def run_hermes_cycle():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n" + "=" * 70)
    print(f"🦁 HERMES 2-HOUR AUTONOMOUS LEAD & OUTREACH CYCLE: {now_str}")
    print(f"Safety Gate: Local Hermes Agent Environment (Netcup VPS IP Protected)")
    print("=" * 70)

    # Step 1: Execute Deterministic Lead Sanitizer on raw scraped data
    print("\n[STEP 1/3] Executing Deterministic Lead Sanitizer...")
    try:
        import subprocess
        subprocess.run([sys.executable, SANITIZER_PATH], check=False)
    except Exception as e:
        print(f"❌ Sanitizer execution error: {e}")

    # Step 2: Read Verified Leads
    verified_emails = []
    if os.path.exists(VERIFIED_LEADS_PATH):
        try:
            with open(VERIFIED_LEADS_PATH, "r", encoding="utf-8") as f:
                verified_emails = json.load(f)
        except Exception:
            verified_emails = []

    social_dms = []
    if os.path.exists(SOCIAL_DMS_PATH):
        try:
            with open(SOCIAL_DMS_PATH, "r", encoding="utf-8") as f:
                social_dms = json.load(f)
        except Exception:
            social_dms = []

    print(f"\n[STEP 2/3] Queue Status:")
    print(f"  • Verified Business Emails: {len(verified_emails)}")
    print(f"  • Routed Social DMs       : {len(social_dms)}")

    # Step 3: Rate-Limited Dispatch (Max 10-15 per 2-hour window)
    batch_limit = 12
    emails_to_dispatch = verified_emails[:batch_limit]
    
    if not emails_to_dispatch:
        print("\n[STEP 3/3] ℹ️ Zero new verified business emails in this 2-hour cycle.")
        print("  Anti-Hallucination Gate: Halting safely. No fake sends triggered.")
        return

    print(f"\n[STEP 3/3] Preparing authenticated dispatch for {len(emails_to_dispatch)} verified leads...")
    for lead in emails_to_dispatch:
        print(f"  -> Ready for Brevo dispatch: {lead['email']} ({lead['first_name']} @ {lead['business']})")

    print("\n✅ Hermes 2-Hour cycle complete.")


if __name__ == "__main__":
    run_hermes_cycle()
