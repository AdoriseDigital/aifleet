import os
import shutil
import zipfile
import json
from pathlib import Path

# Paths
SRC_MANUSCRIPT_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\manuscripts\hum_ladte_nahi")
SRC_PREVIEW_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\previews\Care Collection Lead magnets")
DEST_CARE_DIR = Path(r"C:\Users\HOME_PC\Downloads\Mini Books\The Care Collection")

# Source files
PDF_FULL = SRC_MANUSCRIPT_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf"
EPUB_FULL = SRC_MANUSCRIPT_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.epub"
TRACKER_PDF = SRC_MANUSCRIPT_DIR / "Hum_Ladte_Nahi_30_Day_Reconnection_Tracker.pdf"
PREVIEW_PDF = SRC_MANUSCRIPT_DIR / "Hum_Ladte_Nahi_3_Chapter_Preview.pdf"
COVER_REAL = SRC_PREVIEW_DIR / "Hum_Ladte_Nahi_Real_Cover.jpg"
SQUARE_REAL = SRC_PREVIEW_DIR / "Hum_Ladte_Nahi_Real_Square_Thumbnail.jpg"

def run_packaging():
    print("=== PACKAGING HUM LADTE NAHI PRODUCTION ASSETS ===")
    
    # 1. Copy to Care Collection directory
    shutil.copy2(PDF_FULL, DEST_CARE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf")
    shutil.copy2(EPUB_FULL, DEST_CARE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.epub")
    shutil.copy2(TRACKER_PDF, DEST_CARE_DIR / "Hum_Ladte_Nahi_30_Day_Reconnection_Tracker.pdf")
    shutil.copy2(COVER_REAL, DEST_CARE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_Cover_Front.jpg")
    shutil.copy2(COVER_REAL, DEST_CARE_DIR / "Hum_Ladte_Nahi_Real_Cover.jpg")
    shutil.copy2(SQUARE_REAL, DEST_CARE_DIR / "Hum_Ladte_Nahi_Square_Thumbnail.jpg")
    
    # 2. Update README.md
    readme_content = """# Hum Ladte Nahi, Par Baat Nahi Karte
### A 4-Phase Framework for the Silent Indian Marriage
**By Sanjay Shharma (M.Sc., MBA, APSCM - IIM Calcutta Alumni)**
*Published by Adorise Digital — A Division of Trendy DigiStore LLC, Wyoming, USA*

---

## Welcome & Deliverables Overview

Thank you for purchasing the complete edition of **Hum Ladte Nahi, Par Baat Nahi Karte**. 
This digital asset package contains everything you need across all reading and printing devices:

### Files Included in this Package:
1. `Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf`:
   - Master 249-page publication-grade PDF (6x9 in trade format).
   - Contains all 14 Chapters, 6 Action Toolkits, 12 Couple Stories, 8 Case Studies, Helplines, and 2-Page Master Catalog.
   - Ideal for reading on iPad, tablets, laptops, and desktop screens.
2. `Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.epub`:
   - Standard reflowable EPUB format with full table of contents and cover.
   - Compatible with Amazon Kindle, Apple Books, Google Play Books, Kobo, and Android e-readers.
3. `Hum_Ladte_Nahi_30_Day_Reconnection_Tracker.pdf`:
   - High-resolution single-page companion worksheet.
   - Formatted for Letter / A4 printing to pin on your refrigerator or nightstand.
4. `Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_Cover_Front.jpg`:
   - Ultra high-definition front cover artwork (1800 x 2700 px).
5. `Hum_Ladte_Nahi_Square_Thumbnail.jpg`:
   - High-resolution 1:1 square artwork (1080 x 1080 px).

---

## How to Load on Kindle / Apple Books:
- **Kindle App / Paperwhite:** Email the `.epub` file to your Send-to-Kindle email address or drag and drop via [amazon.com/sendtokindle](https://www.amazon.com/sendtokindle).
- **iPhone / iPad:** Tap the `.epub` file and choose "Open in Apple Books".
- **Android:** Open with Google Play Books, ReadEra, or Moon+ Reader.

---

## Support & Connect
- Official Bookstore: https://books.adorisedigital.com
- Author Inquiries: `support@adorisedigital.com`
- Publisher: Adorise Digital (Trendy DigiStore LLC, Wyoming, USA)
"""
    (DEST_CARE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_README.md").write_text(readme_content, encoding="utf-8")
    
    # 3. Update manifest.json
    manifest = {
        "title": "Hum Ladte Nahi, Par Baat Nahi Karte",
        "subtitle": "A 4-Phase Framework for the Silent Indian Marriage",
        "author": "Sanjay Shharma",
        "credentials": "M.Sc., MBA, APSCM (IIM Calcutta Alumni)",
        "publisher": "Adorise Digital",
        "collection": "The Care Collection",
        "edition": "Complete Bestseller Master Edition (249 Pages • 14 Chapters • 6 Toolkits • 12 Stories • 8 Cases)",
        "pages": 249,
        "language": "Hinglish (Hindi-English)",
        "formats": ["PDF", "EPUB", "Printable Tracker PDF", "JPG Artwork"],
        "price_usd": 9.99,
        "price_inr": 899,
        "gumroad_slug": "hum-ladte-nahi",
        "updated_at": "2026-09-16T00:15:00Z"
    }
    (DEST_CARE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # 4. Create updated zip bundle
    zip_path = DEST_CARE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_bundle.zip"
    files_to_zip = [
        "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf",
        "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.epub",
        "Hum_Ladte_Nahi_30_Day_Reconnection_Tracker.pdf",
        "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_Cover_Front.jpg",
        "Hum_Ladte_Nahi_Square_Thumbnail.jpg",
        "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_KDP_FULL_COVER.pdf",
        "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_README.md",
        "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte_manifest.json"
    ]
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fname in files_to_zip:
            fpath = DEST_CARE_DIR / fname
            if fpath.exists():
                zf.write(fpath, arcname=fname)
                print(f"Added to bundle: {fname} ({fpath.stat().st_size} bytes)")
            else:
                print(f"Warning: {fname} not found in {DEST_CARE_DIR}")
                
    print(f"Updated bundle generated at {zip_path} ({zip_path.stat().st_size} bytes).")

    # 5. Update Preview lead magnet folder
    shutil.copy2(PREVIEW_PDF, SRC_PREVIEW_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf")
    shutil.copy2(PREVIEW_PDF, SRC_PREVIEW_DIR / "Hum_Ladte_Nahi_3_Chapter_Preview.pdf")
    print(f"Updated preview lead magnet at {SRC_PREVIEW_DIR / 'Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf'}")

if __name__ == "__main__":
    run_packaging()
