import os
import sys
import shutil
import zipfile
import pymupdf

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

BASE_DIRS = [
    r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\adorise-frontend\books\AI_SERIES_GUMROAD_READY_UPLOAD_PACK",
    r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\adorise-core-private\books\AI_SERIES_GUMROAD_READY_UPLOAD_PACK"
]

def update_pdf_with_backmatter(target_pdf_path, lead_magnet_path):
    doc = pymupdf.open(target_pdf_path)
    # Check if already has backmatter
    if len(doc) > 0 and "48-BOOK MASTER AUTHOR CATALOG" in doc[-1].get_text():
        p_count = len(doc)
        print(f"    [SKIP] Already contains 48-Book Master Catalog: {os.path.basename(target_pdf_path)} ({p_count} pages)")
        doc.close()
        return p_count, False

    lead = pymupdf.open(lead_magnet_path)
    p_cnt = len(lead)
    if p_cnt < 3:
        doc.close()
        lead.close()
        raise ValueError(f"Lead magnet {lead_magnet_path} has fewer than 3 pages!")

    initial_len = len(doc)
    doc.insert_pdf(lead, from_page=p_cnt - 3, to_page=p_cnt - 1)
    new_len = len(doc)

    tmp_path = target_pdf_path + ".tmp.pdf"
    doc.save(tmp_path, garbage=3, deflate=True)
    doc.close()
    lead.close()

    os.replace(tmp_path, target_pdf_path)
    print(f"    [OK] Appended 3 backmatter pages: {os.path.basename(target_pdf_path)} ({initial_len} -> {new_len} pages)")
    return new_len, True

def repack_zip_bundle(folder_path, zip_filename):
    zip_path = os.path.join(folder_path, zip_filename)
    tmp_zip_path = zip_path + ".tmp.zip"

    all_files = sorted(os.listdir(folder_path))
    files_to_pack = [f for f in all_files if f != zip_filename and not f.endswith(".tmp.zip") and not f.endswith(".tmp.pdf")]

    with zipfile.ZipFile(tmp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for f in files_to_pack:
            fp = os.path.join(folder_path, f)
            if os.path.isfile(fp):
                zf.write(fp, arcname=f)

    os.replace(tmp_zip_path, zip_path)
    print(f"    [OK] Re-packed {zip_filename} with {len(files_to_pack)} files ({os.path.getsize(zip_path):,} bytes)")

def process_pack(base_dir):
    print(f"\n=======================================================")
    print(f"PROCESSING AI SERIES PACK: {base_dir}")
    print(f"=======================================================")

    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        return

    summary = []
    folders = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        print(f"\nProcessing Book Folder: {folder}")

        # Find files
        all_files = os.listdir(folder_path)
        leads = [f for f in all_files if 'Lead_Magnet' in f or 'Lead' in f]
        interiors = [f for f in all_files if 'INTERIOR.pdf' in f]
        zips = [f for f in all_files if f.endswith('.zip')]
        
        # Master PDF is .pdf that is NOT interior, NOT lead, NOT cover
        masters = [f for f in all_files if f.endswith('.pdf') and f not in interiors and f not in leads and 'COVER' not in f]

        if not leads:
            raise FileNotFoundError(f"Lead magnet not found in {folder_path}")
        if not interiors:
            raise FileNotFoundError(f"Interior PDF not found in {folder_path}")
        if not masters:
            raise FileNotFoundError(f"Master PDF not found in {folder_path}")
        if not zips:
            raise FileNotFoundError(f"ZIP bundle not found in {folder_path}")

        lead_path = os.path.join(folder_path, leads[0])
        master_path = os.path.join(folder_path, masters[0])
        interior_path = os.path.join(folder_path, interiors[0])
        zip_name = zips[0]

        # 1. Update Master PDF
        m_pages, m_mod = update_pdf_with_backmatter(master_path, lead_path)

        # 2. Update Interior PDF
        i_pages, i_mod = update_pdf_with_backmatter(interior_path, lead_path)

        # 3. Repack ZIP bundle
        repack_zip_bundle(folder_path, zip_name)

        summary.append({
            "folder": folder,
            "master": masters[0],
            "master_pages": m_pages,
            "interior": interiors[0],
            "interior_pages": i_pages,
            "zip": zip_name,
            "zip_size_mb": round(os.path.getsize(os.path.join(folder_path, zip_name)) / (1024*1024), 2)
        })

    return summary

def main():
    results = {}
    for b in BASE_DIRS:
        res = process_pack(b)
        results[b] = res

    print("\n\n=======================================================")
    print("BATCH UPDATE COMPLETE - VERIFICATION SUMMARY")
    print("=======================================================")
    for b, items in results.items():
        print(f"\nLocation: {b}")
        if not items:
            continue
        for item in items:
            print(f"  ✓ {item['folder']}: Master '{item['master']}' ({item['master_pages']}p), Interior '{item['interior']}' ({item['interior_pages']}p), Zip '{item['zip']}' ({item['zip_size_mb']} MB)")

if __name__ == "__main__":
    main()
