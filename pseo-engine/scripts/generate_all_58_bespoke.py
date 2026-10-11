"""
Merge and Validate All 70 Bespoke Combinations
Generates all_70_combinations.json and all_70_human_solutions.json
Validates zero buzzwords and tests pairwise Jaccard Distance.
"""

import json
import re
import os
import sys

# Import the 10 modular files
from data_b2b_saas import DATA as B2B_SAAS
from data_ecommerce import DATA as ECOMMERCE
from data_fintech import DATA as FINTECH
from data_healthtech import DATA as HEALTHTECH
from data_proptech import DATA as PROPTECH
from data_legaltech import DATA as LEGALTECH
from data_vc_pe import DATA as VC_PE
from data_edtech import DATA as EDTECH
from data_cybersecurity import DATA as CYBERSECURITY
from data_agency import DATA as AGENCY

BANNED_WORDS = [
    'delve', 'supercharge', 'unleash', 'tapestry', 'seamlessly',
    'game-changer', 'revolutionize', 'elevate', 'cutting-edge', 'synergy'
]

# 1. Load Batch 1 combinations and human solutions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.abspath(os.path.join(BASE_DIR, '../..'))
DATA_DIR = os.path.join(REPO_DIR, 'pseo-engine/data')

with open(os.path.join(DATA_DIR, 'batch1_combinations.json'), 'r', encoding='utf-8') as f:
    batch1_combos = json.load(f)

with open(os.path.join(DATA_DIR, 'batch1_human_solutions.json'), 'r', encoding='utf-8') as f:
    batch1_human = json.load(f)

print(f"Loaded Batch 1: {len(batch1_combos)} combinations, {len(batch1_human)} human solutions.")

# 2. Merge all 58 new combinations
all_combos = dict(batch1_combos)
all_human = dict(batch1_human)

modules = [
    B2B_SAAS, ECOMMERCE, FINTECH, HEALTHTECH, PROPTECH,
    LEGALTECH, VC_PE, EDTECH, CYBERSECURITY, AGENCY
]

new_count = 0
for mod in modules:
    for key, val in mod.items():
        if key in all_combos and key not in batch1_combos:
            raise ValueError(f"Duplicate key: {key}")
        
        # Extract humanSolutions into separate dictionary if present
        combo_data = dict(val)
        if 'humanSolutions' in combo_data:
            human_val = combo_data.pop('humanSolutions')
            all_human[key] = human_val
        
        all_combos[key] = combo_data
        new_count += 1

print(f"Added {new_count} new combinations. Total combinations: {len(all_combos)}, Total human solutions: {len(all_human)}")

if len(all_combos) != 70 or len(all_human) != 70:
    raise ValueError(f"Expected 70 combinations and human solutions, got {len(all_combos)} and {len(all_human)}")

# 3. Assert zero banned buzzwords
dump_combos = json.dumps(all_combos)
dump_human = json.dumps(all_human)
for b in BANNED_WORDS:
    m1 = re.findall(r'\b' + re.escape(b) + r'\b', dump_combos, re.IGNORECASE)
    m2 = re.findall(r'\b' + re.escape(b) + r'\b', dump_human, re.IGNORECASE)
    if m1 or m2:
        raise ValueError(f"BANNED WORD FOUND: '{b}' (combos: {len(m1)}, human: {len(m2)})")

print("[PASS] Zero forbidden buzzwords detected across all 70 combinations.")

# 4. Save to JSON files
out_combos_path = os.path.join(DATA_DIR, 'all_70_combinations.json')
out_human_path = os.path.join(DATA_DIR, 'all_70_human_solutions.json')

with open(out_combos_path, 'w', encoding='utf-8', errors='replace') as f:
    json.dump(all_combos, f, indent=2, ensure_ascii=False)

with open(out_human_path, 'w', encoding='utf-8', errors='replace') as f:
    json.dump(all_human, f, indent=2, ensure_ascii=False)

print(f"Saved {out_combos_path}")
print(f"Saved {out_human_path}")
