# Build the 58 bespoke combinations with zero boilerplate repetition
import json
import re

BANNED = ['delve', 'supercharge', 'unleash', 'tapestry', 'seamlessly', 'game-changer', 'revolutionize', 'elevate', 'cutting-edge', 'synergy']

def check_clean(text, ctx):
    for w in BANNED:
        if re.search(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE):
            raise ValueError(f"Found banned word '{w}' in {ctx}")

# Load Batch 1 slugs
with open('pseo-engine/data/batch_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

batch1_slugs = set(manifest['batches'][0]['slugs'])
all_slugs = []
for b in manifest['batches']:
    all_slugs.extend(b['slugs'])

missing_slugs = [s for s in all_slugs if s not in batch1_slugs]
print(f"Total slugs: {len(all_slugs)}, Batch 1 slugs: {len(batch1_slugs)}, Missing slugs to craft: {len(missing_slugs)}")
