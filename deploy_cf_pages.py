import os
import sys
import subprocess

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
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

def main():
    print("🚀 Deploying Updated Styled Frontend to Cloudflare Pages...")
    load_env()
    env = os.environ.copy()
    if not env.get("CLOUDFLARE_ACCOUNT_ID"):
        env["CLOUDFLARE_ACCOUNT_ID"] = "8313af575700d9629f7f5174e68dfca5"

    cmd = "npx --yes wrangler pages deploy adorise-frontend --project-name=adorisedigital --branch=main --commit-dirty=true"


    
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
    print(f"\n✅ Cloudflare Pages Deployment finished with exit code: {proc.returncode}")

if __name__ == "__main__":
    main()
