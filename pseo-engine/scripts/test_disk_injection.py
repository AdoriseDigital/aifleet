import os
import re
import json

# Test script to verify the exact injection of 250 service words and 250 niche words into the HTML files on disk

FRONTEND_DIR = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\adorise-frontend"
MANIFEST_PATH = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\pseo-engine\data\batch_manifest.json"

with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

published_slugs = []
for b in manifest['batches']:
    published_slugs.extend(b['slugs'])

def extract_word_set(text):
    m = re.search(r'<main[\s\S]*?<\/main>', text)
    content = m.group(0) if m else text
    stripped = re.sub(r'<[^>]+>', ' ', content).lower()
    words = re.findall(r'[a-z]{3,}', stripped)
    return set(words)

def jaccard_distance(set_a, set_b):
    inter = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return 1.0 - (len(inter) / len(union))

print(f"Loaded {len(published_slugs)} slugs.")
