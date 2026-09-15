import os
import sys
import re
from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\manuscripts\hum_ladte_nahi")
PART1 = BASE_DIR / "book_manuscript_part1.md"
PART2 = BASE_DIR / "book_manuscript_part2.md"
PART3 = BASE_DIR / "book_manuscript_part3.md"
PART4 = BASE_DIR / "book_manuscript_part4.md"
COMPLETE_MD = BASE_DIR / "book_manuscript_complete.md"

ABOUT_AUTHOR = """
---

# ABOUT THE AUTHOR

## Sanjay Shharma
**M.Sc., MBA, APSCM (IIM Calcutta Alumni)**  
*Author of The Care Collection • Marital Communication Strategist*

Sanjay Shharma is an executive mentor, behavioral strategist, and author of *The Care Collection*. Having spent over three decades studying executive performance, human behavior, and corporate stress, he noticed a recurring tragedy in urban Indian homes: highly successful, intelligent, hard-working professionals were excelling at work while their marriages were silently starving in quiet living rooms.

His work combines deep cultural empathy, psychological neuroscience, and practical executive frameworks into compassionate, actionable blueprints for modern Indian couples. He lives and works between India and international consulting engagements.

### Connect & Official Resources:
- **Official Bookstore & Previews:** [books.adorisedigital.com](https://books.adorisedigital.com)
- **Global Digital Distribution:** [adorisedigital.gumroad.com](https://adorisedigital.gumroad.com)
- **Reader Correspondence:** `support@adorisedigital.com`
- **Publisher:** Adorise Digital — A Division of Trendy DigiStore LLC, 30 N Gould St, Ste R, Sheridan, WY 82801, USA
"""

def merge_manuscripts():
    p1 = PART1.read_text(encoding="utf-8")
    p2 = PART2.read_text(encoding="utf-8")
    p3 = PART3.read_text(encoding="utf-8")
    p4 = PART4.read_text(encoding="utf-8")
    
    full_text = f"{p1.strip()}\n\n---\n\n{p2.strip()}\n\n---\n\n{p3.strip()}\n\n---\n\n{p4.strip()}\n\n{ABOUT_AUTHOR.strip()}\n"
    COMPLETE_MD.write_text(full_text, encoding="utf-8")
    print(f"Successfully merged into {COMPLETE_MD} ({len(full_text)} characters, {len(full_text.splitlines())} lines).")
    return full_text

if __name__ == "__main__":
    merge_manuscripts()
