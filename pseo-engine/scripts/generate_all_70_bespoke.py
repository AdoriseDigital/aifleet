import json
import re

# Comprehensive generator for all 70 combinations with bespoke entries

BANNED = ['delve', 'supercharge', 'unleash', 'tapestry', 'seamlessly', 'game-changer', 'revolutionize', 'elevate', 'cutting-edge', 'synergy']

def check_banned(text, context):
    for b in BANNED:
        if re.search(r'\b' + re.escape(b) + r'\b', text, re.IGNORECASE):
            raise ValueError(f"Banned word '{b}' found in {context}")

# We will write the full generator that outputs a complete JSON file:
# pseo-engine/data/all_70_bespoke_combinations.json
print("Generator script template ready.")
