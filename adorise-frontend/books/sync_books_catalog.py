import os
import sys
import re
import json
import subprocess

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREVIEWS_DIR = os.path.join(BASE_DIR, "previews")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

def find_preview_pdfs():
    previews = {}
    for root, dirs, files in os.walk(PREVIEWS_DIR):
        if 'backup' in root.lower() or 'old' in root.lower():
            continue
        for f in files:
            if f.lower().endswith('.pdf'):
                rel = os.path.relpath(os.path.join(root, f), BASE_DIR).replace('\\', '/')
                previews[f] = '/' + rel
    return previews

def match_book_to_pdf(books, previews):
    mapping = {}
    for b in books:
        bid = b.get('id')
        title_slug = re.sub(r'[^a-zA-Z0-9]+', '_', b.get('title', '')).strip('_').lower()
        
        # Match against preview filenames
        matched_url = None
        for fname, url in previews.items():
            fname_slug = re.sub(r'[^a-zA-Z0-9]+', '_', fname).strip('_').lower()
            if bid.lower() in fname_slug or title_slug in fname_slug:
                matched_url = url
                break
            # Fuzzy match on first 3 significant words
            words = [w for w in title_slug.split('_') if len(w) > 3][:3]
            if words and all(w in fname_slug for w in words):
                matched_url = url
                break
                
        if matched_url:
            mapping[bid] = matched_url
    return mapping

def sync_catalog(do_deploy=False):
    print("==================================================")
    print("ADORISE BOOKS HUB — AUTONOMOUS CATALOG SYNC")
    print("==================================================")

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract books array
    m = re.search(r'const books = (\[.*?\]);\s*const bookPreviewMap', html, re.DOTALL)
    if not m:
        m = re.search(r'const books = (\[.*?\]);', html, re.DOTALL)
    if not m:
        print("ERROR: Could not locate 'const books' in index.html")
        return

    books = json.loads(m.group(1))
    print(f"Loaded {len(books)} catalog books.")

    previews = find_preview_pdfs()
    print(f"Found {len(previews)} preview PDFs in storage.")

    mapping = match_book_to_pdf(books, previews)
    print(f"Successfully matched {len(mapping)} books to preview PDFs:")
    for bid, url in mapping.items():
        print(f"  ✓ {bid}: {url}")

    # Update bookPreviewMap in index.html
    map_json = json.dumps(mapping, indent=12)
    # Format nicely
    map_str = "const bookPreviewMap = " + map_json.strip() + ";"
    
    html = re.sub(r'const bookPreviewMap = \{.*?\};', map_str, html, flags=re.DOTALL)

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("\n✓ Updated index.html with live bookPreviewMap.")

    if do_deploy:
        print("\nDeploying adorise-books to Cloudflare Pages edge network...")
        env = os.environ.copy()
        env['CLOUDFLARE_API_TOKEN'] = os.environ.get('CLOUDFLARE_API_TOKEN', '')
        env['CLOUDFLARE_ACCOUNT_ID'] = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '8313af575700d9629f7f5174e68dfca5')
        cmd = f'npx wrangler pages deploy "{BASE_DIR}" --project-name=adorise-books --commit-dirty=true'
        res = subprocess.run(cmd, shell=True, capture_output=True, env=env)
        print("Deploy Exit Code:", res.returncode)
        if res.returncode == 0:
            print("✨ Successfully deployed live to https://books.adorisedigital.com!")
        else:
            print("Deploy error:", res.stderr.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
    deploy_flag = '--deploy' in sys.argv or '-d' in sys.argv
    sync_catalog(do_deploy=deploy_flag)
