"""
Adorise Digital - Daily Automated Infrastructure & API Health Monitor
Runs full diagnostic tests across all 6 micro-SaaS workers, live LLM inference,
outreach webhooks, security auth guardrails, and public landing pages.
"""

import sys
import os
import requests
import datetime
import json

LOGS_DIR = r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\logs"
os.makedirs(LOGS_DIR, exist_ok=True)
timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(LOGS_DIR, f"health_check_{datetime.datetime.now().strftime('%Y%m%d')}.log")

def log(msg):
    ts = datetime.datetime.now().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

log("=" * 70)
log("STARTING DAILY ADORISE AUTOMATED INFRASTRUCTURE HEALTH CHECK")
log("=" * 70)

apps = [
    ("DearMee", "https://dearmee.adorisedigital.com"),
    ("Social", "https://social.adorisedigital.com"),
    ("Scout", "https://scout.adorisedigital.com"),
    ("Outreach", "https://outreach.adorisedigital.com"),
    ("ClipCalm", "https://clipcalm.adorisedigital.com"),
    ("InboxCalm", "https://inboxcalm.adorisedigital.com")
]

failures = []

# 1. API Health Checks
log("\n--- [CHECK 1] MICRO-SAAS API HEALTH ENDPOINTS ---")
for name, base_url in apps:
    health_url = f"{base_url}/api/v1/health" if name == "Scout" else f"{base_url}/api/health"
    try:
        r = requests.get(health_url, timeout=10)
        if r.status_code == 200:
            log(f"  [PASS 200] {name:10} Health check OK ({health_url})")
        else:
            log(f"  [FAIL {r.status_code}] {name:10} Health check failed: {r.text[:80]}")
            failures.append(f"{name} health check returned {r.status_code}")
    except Exception as e:
        log(f"  [ERR] {name:10} Health check exception: {e}")
        failures.append(f"{name} health check error: {e}")

# 2. DearMee Live DeepSeek LLM Inference Test
log("\n--- [CHECK 2] DEARMEE LIVE OPENROUTER DEEPSEEK CHAT ENGINE ---")
try:
    payload = {"message": "Daily routine health check: verify reasoning connection.", "persona": "founder_copilot"}
    r = requests.post("https://dearmee.adorisedigital.com/api/chat", json=payload, timeout=15)
    if r.status_code == 200 and r.json().get("reply"):
        log(f"  [PASS 200] DearMee LLM Chat Engine Active: {r.json().get('reply')[:80]}...")
    else:
        log(f"  [FAIL {r.status_code}] DearMee LLM Chat failed: {r.text[:80]}")
        failures.append(f"DearMee LLM chat returned {r.status_code}")
except Exception as e:
    log(f"  [ERR] DearMee LLM Chat exception: {e}")
    failures.append(f"DearMee LLM chat error: {e}")

# 3. Outreach Radar Webhook Check
log("\n--- [CHECK 3] OUTREACH RADAR INBOUND WEBHOOK ---")
try:
    wh_url = "https://outreach.adorisedigital.com/webhook/radar/lead"
    r = requests.post(wh_url, json={"lead_id": f"daily_monitor_{timestamp_str}"}, timeout=10)
    if r.status_code == 200:
        log(f"  [PASS 200] Outreach Radar Webhook received lead successfully")
    else:
        log(f"  [FAIL {r.status_code}] Outreach Radar Webhook failed: {r.text[:80]}")
        failures.append(f"Outreach webhook returned {r.status_code}")
except Exception as e:
    log(f"  [ERR] Outreach webhook exception: {e}")
    failures.append(f"Outreach webhook error: {e}")

# 4. Security Auth Guardrail: Exploit Regression (whop_ & lic_ prefix must be 401)
log("\n--- [CHECK 4] SECURITY GUARDRAIL: EXPLOIT PREFIX BLOCKING ---")
bypass_payload = {"email": "audit_probe@example.com", "password": "whop_daily_probe_test"}
for name, base_url in apps:
    login_url = f"{base_url}/api/auth/login"
    try:
        r = requests.post(login_url, json=bypass_payload, timeout=10)
        if r.status_code == 401:
            log(f"  [PASS 401] {name:10} properly blocked bypass probe")
        else:
            log(f"  [FAIL {r.status_code}] {name:10} exploit probe vulnerability detected!")
            failures.append(f"{name} accepted or misrouted exploit probe: {r.status_code}")
    except Exception as e:
        log(f"  [ERR] {name:10} login check exception: {e}")
        failures.append(f"{name} login probe error: {e}")

# 5. Security Auth Guardrail: Self-Registration Lockdown (/api/auth/signup must be 403)
log("\n--- [CHECK 5] SECURITY GUARDRAIL: SELF-REGISTRATION LOCKDOWN ---")
signup_payload = {"email": "random_probe@example.com", "password": "random_password_123"}
for name, base_url in apps:
    signup_url = f"{base_url}/api/auth/signup"
    try:
        r = requests.post(signup_url, json=signup_payload, timeout=10)
        if r.status_code == 403:
            log(f"  [PASS 403] {name:10} signup properly disabled (403)")
        else:
            log(f"  [FAIL {r.status_code}] {name:10} signup allowed or misrouted!")
            failures.append(f"{name} signup returned {r.status_code}")
    except Exception as e:
        log(f"  [ERR] {name:10} signup check exception: {e}")
        failures.append(f"{name} signup probe error: {e}")

# 6. Legitimate Pro Login Test (Must return 200 OK + JWT)
log("\n--- [CHECK 6] LEGITIMATE PRO AUTHENTICATION (pro@adorisedigital.com) ---")
valid_payload = {"email": "pro@adorisedigital.com", "password": "pro_growth_2026"}
for name, base_url in apps:
    login_url = f"{base_url}/api/auth/login"
    try:
        r = requests.post(login_url, json=valid_payload, timeout=10)
        if r.status_code == 200 and r.json().get("token"):
            log(f"  [PASS 200] {name:10} verified authorized Pro login successfully")
        else:
            log(f"  [FAIL {r.status_code}] {name:10} valid Pro login failed: {r.text[:80]}")
            failures.append(f"{name} valid Pro login returned {r.status_code}")
    except Exception as e:
        log(f"  [ERR] {name:10} valid login exception: {e}")
        failures.append(f"{name} valid login error: {e}")

# 7. Landing & Resource Pages
log("\n--- [CHECK 7] PUBLIC STOREFRONTS & KNOWLEDGE HUB ---")
pages = [
    ("Main Landing", "https://adorisedigital.com/"),
    ("Resources Hub", "https://adorisedigital.com/resources/"),
    ("Solutions Matrix", "https://adorisedigital.com/solutions/"),
    ("Services Storefront", "https://adorisedigital.com/services/")
]
for pname, purl in pages:
    try:
        r = requests.get(purl, timeout=10)
        if r.status_code == 200:
            log(f"  [PASS 200] {pname:18} accessible ({len(r.text)} bytes)")
        else:
            log(f"  [FAIL {r.status_code}] {pname:18} returned status {r.status_code}")
            failures.append(f"{pname} returned {r.status_code}")
    except Exception as e:
        log(f"  [ERR] {pname:18} request error: {e}")
        failures.append(f"{pname} error: {e}")

log("\n" + "=" * 70)
if not failures:
    log("ALL 25/25 DAILY SYSTEM CHECKS PASSED WITH ZERO FAILURES! [STATUS: HEALTHY]")
    log("=" * 70)
    sys.exit(0)
else:
    log(f"DAILY HEALTH CHECK DETECTED {len(failures)} FAILURE(S):")
    for f in failures:
        log(f"  ❌ {f}")
    log("=" * 70)
    sys.exit(1)
