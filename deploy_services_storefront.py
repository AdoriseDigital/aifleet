import os
import sys
import subprocess
import json
import urllib.request
import urllib.error

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def load_cf_env():
    token = os.getenv("CLOUDFLARE_API_TOKEN")
    account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    if not token or not account:
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("CLOUDFLARE_API_TOKEN="):
                        token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("CLOUDFLARE_ACCOUNT_ID="):
                        account = line.split("=", 1)[1].strip().strip('"').strip("'")
    return token or "", account or ""

CF_API_TOKEN, ACCOUNT_ID = load_cf_env()

SERVICES_DIR = r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-services"
FRONTEND_DIR = r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend"

def deploy_project(dir_path, project_name):
    print(f"\n=======================================================")
    print(f"🚀 Deploying {dir_path} -> Cloudflare Pages Project: {project_name}")
    print(f"=======================================================")
    
    env = os.environ.copy()
    env["CLOUDFLARE_API_TOKEN"] = CF_API_TOKEN
    env["CLOUDFLARE_ACCOUNT_ID"] = ACCOUNT_ID
    
    cmd = f'wrangler pages deploy "{dir_path}" --project-name={project_name} --branch=main --commit-dirty=true'
    print(f"[CMD]: {cmd}")
    
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    output_lines = []
    for line in proc.stdout:
        print(line, end="")
        output_lines.append(line)
        
    proc.wait()
    print(f"Result for {project_name}: Exit code {proc.returncode}")
    return proc.returncode == 0

def check_and_bind_domain():
    print(f"\n=======================================================")
    print(f"🌐 Verifying Custom Domain Binding: services.adorisedigital.com")
    print(f"=======================================================")
    
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Check domain on adorise-services
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/adorise-services/domains/services.adorisedigital.com"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            res = data.get("result", {})
            print("Domain Status:", res.get("status"))
            print("Verification Status:", res.get("verification_data", {}).get("status"))
            print("Certificate Authority:", res.get("certificate_authority"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
    except Exception as e:
        print("Error:", e)

def main():
    print("==================================================================")
    print("🌟 ADORISE DIGITAL SERVICES STOREFRONT DEPLOYMENT PIPELINE 🌟")
    print("==================================================================")
    
    # 1. Deploy dedicated adorise-services project
    ok1 = deploy_project(SERVICES_DIR, "adorise-services")
    
    # 2. Deploy updated adorise-frontend project (apex routing & /services/)
    ok2 = deploy_project(FRONTEND_DIR, "adorisedigital")
    
    # 3. Check domain binding
    check_and_bind_domain()
    
    if ok1 and ok2:
        print("\n✅ ALL DEPLOYMENTS SUCCEEDED WITH ZERO ERRORS!")
    else:
        print(f"\n⚠️ Deployment finished with statuses: adorise-services={ok1}, adorisedigital={ok2}")

if __name__ == "__main__":
    main()
