# Comprehensive generator for all 70 combinations with bespoke, non-overlapping content per combination
import json
import re

# We will test Jaccard distance on all 2,415 pairs directly with this script

BANNED = ['delve', 'supercharge', 'unleash', 'tapestry', 'seamlessly', 'game-changer', 'revolutionize', 'elevate', 'cutting-edge', 'synergy']

def check_banned_words(text, context):
    for w in BANNED:
        if re.search(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE):
            raise ValueError(f"Banned word '{w}' in {context}")

print("Verification helper loaded.")
