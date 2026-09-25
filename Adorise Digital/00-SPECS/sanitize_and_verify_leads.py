#!/usr/bin/env python3
"""
Deterministic Lead Sanitizer & Routing Engine (Zero-Hallucination Anti-Fake Firewall)
Author: Adorise Digital Engineering Desk

Rules:
1. Pure Python deterministic execution - NO LLM inference or guesses.
2. Filters out fake emails (@reddit.com, webuser@*, example.com, community.*).
3. Routes valid corporate/personal emails to 'verified_email_leads.json' for Brevo/Resend.
4. Routes social handles (Reddit, X/Twitter) to 'social_dm_leads.json' for Composio DMs.
5. Quarantines invalid stubs and logs explicit rejection reasons.
"""

import os
import sys
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


BLACKLISTED_DOMAINS = {
    "reddit.com",
    "community.n8n.io",
    "community.make.com",
    "example.com",
    "test.com",
    "sample.com",
    "tempmail.com",
    "mailinator.com",
    "guerrillamail.com",
    "10minutemail.com",
    "yopmail.com"
}

FABRICATED_PREFIXES = {
    "webuser",
    "placeholder",
    "fake",
    "test",
    "sample",
    "dummy"
}

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def is_valid_syntax(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def sanitize_lead(lead: Dict) -> Tuple[str, Dict, str]:
    """
    Evaluates a lead record and categorizes it into:
    - 'EMAIL_VERIFIED': Valid real email for Brevo/Resend
    - 'SOCIAL_DM': Social platform handle for Composio DM outreach
    - 'QUARANTINED': Blocked fake/invalid lead
    """
    raw_email = (lead.get("email") or "").strip().lower()
    first_name = (lead.get("first_name") or "").strip()
    business = (lead.get("business") or "").strip()
    url = (lead.get("url") or "").strip()
    service = lead.get("matched_service", "ai_automation_suite")

    # Detect Reddit source
    if "reddit.com" in url or "@reddit.com" in raw_email or business.lower() == "reddit":
        # Extract handle
        username = first_name
        if not username or username.lower() == "reddit":
            # Extract from email or url
            if "@reddit.com" in raw_email:
                username = raw_email.split("@")[0]
            elif "/comments/" in url or "/u_" in url:
                parts = url.split("/")
                for i, part in enumerate(parts):
                    if part in ["u", "user"]:
                        username = parts[i+1]
                        break

        social_lead = {
            "platform": "reddit",
            "username": username,
            "profile_url": f"https://www.reddit.com/user/{username}" if username else url,
            "context_url": url,
            "matched_service": service,
            "created_at": datetime.now().isoformat()
        }
        return "SOCIAL_DM", social_lead, "Reddit user routed to Direct Message queue"

    # Validate standard email
    if not raw_email or not is_valid_syntax(raw_email):
        return "QUARANTINED", lead, "Invalid email syntax or empty"

    domain = raw_email.split("@")[-1]
    prefix = raw_email.split("@")[0]

    # Check blacklisted domains
    if domain in BLACKLISTED_DOMAINS or any(b in domain for b in ["community.", "forum.", "reddit."]):
        return "QUARANTINED", lead, f"Blacklisted domain: {domain}"

    # Check fabricated prefixes
    if prefix in FABRICATED_PREFIXES:
        return "QUARANTINED", lead, f"Fabricated generic prefix: {prefix}"

    # Validated business email
    verified_lead = {
        "email": raw_email,
        "first_name": first_name,
        "surname": lead.get("surname", ""),
        "business": business,
        "matched_service": service,
        "source_url": url,
        "verified_at": datetime.now().isoformat()
    }
    return "EMAIL_VERIFIED", verified_lead, "Valid business email"


def process_lead_file(input_path: str, output_dir: str):
    if not os.path.exists(input_path):
        print(f"⚠️ Input lead file not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        try:
            leads = json.load(f)
        except Exception as e:
            print(f"❌ Failed to parse JSON from {input_path}: {e}")
            return

    verified_emails = []
    social_dms = []
    quarantined = []

    for lead in leads:
        category, record, reason = sanitize_lead(lead)
        if category == "EMAIL_VERIFIED":
            verified_emails.append(record)
        elif category == "SOCIAL_DM":
            social_dms.append(record)
        else:
            quarantined.append({"lead": lead, "reason": reason})

    # Write output files
    os.makedirs(output_dir, exist_ok=True)
    
    verified_emails_file = os.path.join(output_dir, "verified_email_leads.json")
    with open(verified_emails_file, "w", encoding="utf-8") as f:
        json.dump(verified_emails, f, indent=2)

    social_dms_file = os.path.join(output_dir, "social_dm_leads.json")
    with open(social_dms_file, "w", encoding="utf-8") as f:
        json.dump(social_dms, f, indent=2)

    quarantined_file = os.path.join(output_dir, "quarantined_leads.json")
    with open(quarantined_file, "w", encoding="utf-8") as f:
        json.dump(quarantined, f, indent=2)

    print("\n" + "=" * 70)
    print("🛡️ DETERMINISTIC LEAD SANITIZER AUDIT REPORT")
    print("=" * 70)
    print(f"Total Raw Leads Processed : {len(leads)}")
    print(f"✅ Verified Business Emails: {len(verified_emails)} (Saved to verified_email_leads.json)")
    print(f"💬 Routed Social DMs       : {len(social_dms)} (Saved to social_dm_leads.json)")
    print(f"🛑 Quarantined / Blocked   : {len(quarantined)} (Saved to quarantined_leads.json)")
    print("=" * 70)
    
    if verified_emails:
        print("\nVerified Emails Ready For Brevo/Resend Dispatch:")
        for ve in verified_emails:
            print(f"  • {ve['email']} ({ve['first_name']} @ {ve['business']})")
    
    if social_dms:
        print("\nSocial DMs Ready For Composio Automation:")
        for sd in social_dms:
            print(f"  • [{sd['platform'].upper()}] u/{sd['username']} -> Context: {sd['context_url']}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "outreach_leads.json")
    output_dir = script_dir
    process_lead_file(input_file, output_dir)
