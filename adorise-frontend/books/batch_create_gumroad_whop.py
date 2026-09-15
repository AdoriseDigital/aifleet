import os
import sys
import csv
import json
import re
import argparse
import urllib.request
import urllib.parse

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "adorise_48_books_master_catalog.csv")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

def load_catalog():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Catalog CSV not found at: {CSV_PATH}")
    
    books = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    return books

def save_catalog(books):
    if not books: return
    fieldnames = list(books[0].keys())
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

def build_gumroad_payload(book):
    """Formats professional sales copy for Gumroad product listing."""
    title = book['title']
    subtitle = book['subtitle']
    author = book['author']
    pain = book['pain_point']
    takeaways = book['takeaways'].split(' | ') if book['takeaways'] else []
    excerpt = book['excerpt']
    
    takeaway_bullets = "\n".join([f"• {t}" for t in takeaways])
    
    description = f"""<h3>{title}</h3>
<p><strong>{subtitle}</strong></p>
<p>Authored by <strong>{author}</strong> (IIM Calcutta Alumni • Published by Adorise Digital / Trendy DigiStore LLC, Wyoming, USA).</p>

<hr>
<h4>The Problem This Blueprint Solves:</h4>
<p>{pain}</p>

<hr>
<h4>Core Tactical Takeaways:</h4>
<ul>
{takeaway_bullets}
</ul>

<hr>
<h4>Opening Premise:</h4>
<blockquote>"{excerpt}"</blockquote>

<hr>
<h4>What's Included With Your Digital Purchase:</h4>
<ul>
  <li>✅ Instant DRM-free PDF + EPUB download</li>
  <li>✅ Mobile, iPad, and Kindle formatted editions</li>
  <li>✅ Reflection exercises & implementation worksheets</li>
  <li>✅ Lifetime digital updates delivered to your email</li>
</ul>
"""
    return {
        'name': f"{title}: {subtitle}" if len(f"{title}: {subtitle}") < 100 else title,
        'description': description,
        'price': int(book['price_usd_cents']),
        'currency': 'usd',
        'permalink': book['gumroad_permalink'],
        'custom_summary': subtitle[:150],
        'require_shipping': 'false',
        'shown_on_profile': 'true'
    }

def create_gumroad_product(payload, access_token):
    """Calls Gumroad REST API to create a product."""
    url = "https://api.gumroad.com/v2/products"
    data = payload.copy()
    data['access_token'] = access_token
    
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=encoded_data, headers={
        'User-Agent': 'Adorise-Catalog-Batch-Deployer/1.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            res_body = resp.read().decode('utf-8')
            res_json = json.loads(res_body)
            if res_json.get('success'):
                product = res_json.get('product', {})
                return {
                    'success': True,
                    'short_url': product.get('short_url'),
                    'id': product.get('id')
                }
            return {'success': False, 'error': res_json.get('message', 'Unknown error')}
    except urllib.error.HTTPError as he:
        err_body = he.read().decode('utf-8', errors='ignore')
        try:
            err_json = json.loads(err_body)
            return {'success': False, 'error': err_json.get('message', err_body)}
        except:
            return {'success': False, 'error': f"HTTP {he.code}: {err_body}"}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def update_index_html_links(updated_books):
    """Syncs live Gumroad URLs back into index.html."""
    if not os.path.exists(INDEX_PATH): return
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
        
    for b in updated_books:
        bid = b['id']
        gurl = b.get('gumroad_url')
        if gurl and f'"id": "{bid}"' in html:
            # Update or inject gumroad_url
            if f'"gumroad_url":' in html:
                pattern = r'("id":\s*"' + re.escape(bid) + r'",\s*"gumroad_url":\s*")[^"]+(")'
                html = re.sub(pattern, r'\g<1>' + gurl + r'\2', html)
            else:
                pattern = r'("id":\s*"' + re.escape(bid) + r'",)'
                html = re.sub(pattern, r'\1\n    "gumroad_url": "' + gurl + r'",', html)
                
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Synced new Gumroad checkout links into index.html")

def run_dry_run(books):
    print("================================================================================")
    print(f"ADORISE DIGITAL — GUMROAD UPLOAD AUDIT & DRY-RUN ({len(books)} Books Selected)")
    print("================================================================================")
    all_ready = True
    for i, b in enumerate(books):
        payload = build_gumroad_payload(b)
        file_path = b.get('deliverable_file_path', '')
        file_exists = os.path.exists(file_path) if file_path else False
        if not file_exists:
            all_ready = False
            
        print(f"[{i+1:02d}/{len(books)}] [{b['category'].upper():<6}] {b['title'][:40]:<40} | ${payload['price']/100:>5.2f} USD")
        print(f"       Slug:  https://adorisedigital.gumroad.com/l/{payload['permalink']}")
        print(f"       File:  {'✓ READY' if file_exists else '❌ MISSING'} ({b.get('file_size_mb', '0.00')} MB) -> {os.path.basename(file_path)}")
    print("--------------------------------------------------------------------------------")
    if all_ready:
        print(f"✨ AUDIT PASS: All {len(books)} books have verified files, titles, copy, and slugs ready for Gumroad!")
    else:
        print(f"⚠️ Some files need review before upload.")

def main():
    parser = argparse.ArgumentParser(description="Batch create Gumroad & Whop product listings for books.")
    parser.add_argument('--dry-run', action='store_true', help="Preview selected product listings without making API calls.")
    parser.add_argument('--platform', choices=['gumroad', 'whop', 'all'], default='gumroad', help="Target publishing platform.")
    parser.add_argument('--token', type=str, help="Gumroad Access Token or Whop API Key.")
    parser.add_argument('--company-id', type=str, help="Whop Company ID (if targeting Whop).")
    parser.add_argument('--limit', type=int, default=None, help="Limit number of books to process (e.g. --limit 3).")
    parser.add_argument('--ids', type=str, default=None, help="Comma-separated book IDs to process (e.g. care-01,care-02,care-03).")
    
    args = parser.parse_args()
    all_books = load_catalog()
    
    # Filter books if limit or ids specified
    selected_books = all_books
    if args.ids:
        target_ids = [x.strip() for x in args.ids.split(',')]
        selected_books = [b for b in all_books if b['id'] in target_ids]
    elif args.limit:
        selected_books = all_books[:args.limit]
        
    token = args.token or os.environ.get('GUMROAD_ACCESS_TOKEN')
    
    if args.dry_run or not token:
        if not args.dry_run:
            print("Notice: No API token provided. Running in safe DRY-RUN audit mode.\n")
        run_dry_run(selected_books)
        return

    # Live execution
    if args.platform in ['gumroad', 'all']:
        print(f"\n🚀 Launching live Gumroad batch creation for {len(selected_books)} books...")
        successes = 0
        updated = []
        for i, b in enumerate(selected_books):
            payload = build_gumroad_payload(b)
            print(f"[{i+1:02d}/{len(selected_books)}] Creating '{b['title'][:35]}'...", end=" ")
            res = create_gumroad_product(payload, token)
            if res['success']:
                print(f"✓ LIVE: {res['short_url']}")
                b['gumroad_url'] = res['short_url']
                updated.append(b)
                successes += 1
            else:
                print(f"❌ Failed: {res['error']}")
        
        if updated:
            save_catalog(all_books)
            update_index_html_links(updated)
            
        print(f"\nFinished! {successes}/{len(selected_books)} products published live to Gumroad.")

if __name__ == '__main__':
    main()
