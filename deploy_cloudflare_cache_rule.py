"""
Cloudflare Cache Rules Deployment Script
Configures 30-day edge caching (2,592,000s) on Cloudflare Zone for all programmatic SEO routes.

Target Zone: adorisedigital.com (Zone ID: 8c502685e24425039c5ddd0ea93ee0a2)
Rule Name: pSEO Solutions 30-Day Edge Cache Rule
Expression: (http.request.uri.path contains "/solutions")
Action: set_cache_settings (Cache Everything, Edge TTL: 30 days, Stale-While-Revalidate, Cache Deception Armor)
"""

import os
import sys
import json
import urllib.request
import urllib.error

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def load_env():
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip()

load_env()
ZONE_ID = "8c502685e24425039c5ddd0ea93ee0a2"
CF_API_TOKEN = os.getenv("CLOUDFLARE_ZONE_API_TOKEN", os.getenv("CLOUDFLARE_API_TOKEN", ""))

def get_headers():
    return {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

def deploy_cache_rule():
    print("=================================================================")
    print("⚡ CLOUDFLARE CACHE RULE DEPLOYMENT ENGINE")
    print(f"   Target Zone ID: {ZONE_ID} (adorisedigital.com)")
    print("   Rule:           pSEO Solutions 30-Day Edge Cache")
    print("=================================================================\n")

    # Cloudflare Ruleset API for Cache Rules (http_request_cache_settings)
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets/phases/http_request_cache_settings/entrypoint"
    
    payload = {
        "rules": [
            {
                "expression": "(http.request.uri.path contains \"/solutions\")",
                "description": "pSEO Solutions 30-Day Edge Cache Rule",
                "action": "set_cache_settings",
                "action_parameters": {
                    "cache": True,
                    "edge_ttl": {
                        "mode": "override_origin",
                        "default": 2592000
                    },
                    "browser_ttl": {
                        "mode": "respect_origin"
                    },
                    "serve_stale": {
                        "disable_stale_while_updating": False
                    },
                    "cache_deception_armor": True
                },
                "enabled": True
            }
        ]
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=get_headers(), method="PUT")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("✅ Cloudflare Cache Rule successfully deployed via Ruleset API!")
            print(json.dumps(data, indent=2))
            return {"success": True, "result": data.get("result")}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        print(f"⚠️ API Response ({e.code}): {err_body}")
        print("\nNote: Zone-level Cache Rules require a Cloudflare Zone API Token with 'Zone -> Cache Rules:Edit' permission.")
        print("This is part of the Mandatory Founder Review Gate sign-off package.")
        return {"success": False, "code": e.code, "error": err_body}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    deploy_cache_rule()
