# Script to generate bespoke content for all 58 missing combinations and test Jaccard distance
import json
import re

# Load manifest
with open('pseo-engine/data/batch_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

published_slugs = []
for b in manifest['batches']:
    published_slugs.extend(b['slugs'])

print(f"Total published slugs: {len(published_slugs)}")
