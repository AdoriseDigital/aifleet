import os
import sys
import subprocess

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

CF_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "8313af575700d9629f7f5174e68dfca5")
BASE_DIR = r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books"

env = os.environ.copy()
env["CLOUDFLARE_API_TOKEN"] = CF_API_TOKEN
env["CLOUDFLARE_ACCOUNT_ID"] = ACCOUNT_ID

print(f"Deploying {BASE_DIR} to Cloudflare Pages project 'adorise-books'...")
cmd = f'npx --yes wrangler pages deploy "{BASE_DIR}" --project-name=adorise-books --branch=main --commit-dirty=true'

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

for line in proc.stdout:
    print(line, end="")

proc.wait()
print(f"\nCloudflare Pages Deployment finished with exit code: {proc.returncode}")
