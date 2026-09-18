import os
import sys
import zipfile
import http.server
import socketserver
import threading
import urllib.request
import pymupdf

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

BASE_DIR = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\adorise-frontend\books"
AI_PACK = os.path.join(BASE_DIR, "AI_SERIES_GUMROAD_READY_UPLOAD_PACK")

def verify_10_ai_books():
    print("\n=======================================================")
    print("STEP 1: VERIFYING ALL 10 FULL MASTER & INTERIOR PDFS")
    print("=======================================================")

    folders = sorted([d for d in os.listdir(AI_PACK) if os.path.isdir(os.path.join(AI_PACK, d))])
    assert len(folders) == 10, f"Expected 10 folders, found {len(folders)}"

    all_passed = True

    for f in folders:
        fpath = os.path.join(AI_PACK, f)
        files = os.listdir(fpath)
        
        interiors = [x for x in files if 'INTERIOR.pdf' in x]
        leads = [x for x in files if 'Lead' in x]
        masters = [x for x in files if x.endswith('.pdf') and x not in interiors and x not in leads and 'COVER' not in x]

        assert len(masters) == 1, f"Expected 1 master in {f}, found {masters}"
        assert len(interiors) == 1, f"Expected 1 interior in {f}, found {interiors}"

        master_pdf = os.path.join(fpath, masters[0])
        interior_pdf = os.path.join(fpath, interiors[0])

        # Verify Master PDF
        doc_m = pymupdf.open(master_pdf)
        p_cnt_m = len(doc_m)
        t_m3 = doc_m[-3].get_text()
        t_m2 = doc_m[-2].get_text()
        t_m1 = doc_m[-1].get_text()

        m_ok = (
            "ABOUT THE AUTHOR" in t_m3 and
            "48-BOOK MASTER AUTHOR CATALOG" in t_m2 and "PART 1" in t_m2 and
            "48-BOOK MASTER AUTHOR CATALOG" in t_m1 and "PART 2" in t_m1 and
            "books.adorisedigital.com" in t_m1
        )
        doc_m.close()

        # Verify Interior PDF
        doc_i = pymupdf.open(interior_pdf)
        p_cnt_i = len(doc_i)
        t_i3 = doc_i[-3].get_text()
        t_i2 = doc_i[-2].get_text()
        t_i1 = doc_i[-1].get_text()

        i_ok = (
            "ABOUT THE AUTHOR" in t_i3 and
            "48-BOOK MASTER AUTHOR CATALOG" in t_i2 and "PART 1" in t_i2 and
            "48-BOOK MASTER AUTHOR CATALOG" in t_i1 and "PART 2" in t_i1 and
            "books.adorisedigital.com" in t_i1
        )
        doc_i.close()

        status = "PASSED" if (m_ok and i_ok) else "FAILED"
        if not (m_ok and i_ok):
            all_passed = False

        print(f"  [{status}] {f}:")
        print(f"      Master: '{masters[0]}' ({p_cnt_m} pages) - Backmatter Verified: {m_ok}")
        print(f"      Interior: '{interiors[0]}' ({p_cnt_i} pages) - Backmatter Verified: {i_ok}")

    return all_passed

def verify_10_zip_bundles():
    print("\n=======================================================")
    print("STEP 2: VERIFYING ALL 10 COMPLETE ZIP BUNDLES")
    print("=======================================================")

    folders = sorted([d for d in os.listdir(AI_PACK) if os.path.isdir(os.path.join(AI_PACK, d))])
    all_passed = True

    for f in folders:
        fpath = os.path.join(AI_PACK, f)
        zips = [x for x in os.listdir(fpath) if x.endswith('.zip')]
        assert len(zips) == 1, f"Expected 1 zip in {f}, found {zips}"
        
        zip_path = os.path.join(fpath, zips[0])
        zip_size_mb = round(os.path.getsize(zip_path) / (1024*1024), 2)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            namelist = zf.namelist()
            interiors = [x for x in namelist if 'INTERIOR.pdf' in x]
            leads = [x for x in namelist if 'Lead' in x]
            masters = [x for x in namelist if x.endswith('.pdf') and x not in interiors and x not in leads and 'COVER' not in x]

            assert len(masters) == 1, f"Expected 1 master in zip {zips[0]}"
            assert len(interiors) == 1, f"Expected 1 interior in zip {zips[0]}"

            # Test internal master
            data_m = zf.read(masters[0])
            doc_m = pymupdf.open(stream=data_m, filetype='pdf')
            m_ok = "48-BOOK MASTER AUTHOR CATALOG" in doc_m[-1].get_text() and "PART 2" in doc_m[-1].get_text()
            p_m = len(doc_m)
            doc_m.close()

            # Test internal interior
            data_i = zf.read(interiors[0])
            doc_i = pymupdf.open(stream=data_i, filetype='pdf')
            i_ok = "48-BOOK MASTER AUTHOR CATALOG" in doc_i[-1].get_text() and "PART 2" in doc_i[-1].get_text()
            p_i = len(doc_i)
            doc_i.close()

            status = "PASSED" if (m_ok and i_ok) else "FAILED"
            if not (m_ok and i_ok):
                all_passed = False

            print(f"  [{status}] {zips[0]} ({zip_size_mb} MB, {len(namelist)} files):")
            print(f"      Internal Master '{masters[0]}' ({p_m}p) Backmatter: {m_ok}")
            print(f"      Internal Interior '{interiors[0]}' ({p_i}p) Backmatter: {i_ok}")

    return all_passed

def verify_download_portal_and_routing():
    print("\n=======================================================")
    print("STEP 3: TESTING DOWNLOAD PORTAL UI & FILE ASSET ROUTING")
    print("=======================================================")

    dl_html = os.path.join(BASE_DIR, "download", "index.html")
    ty_html = os.path.join(BASE_DIR, "thank-you", "index.html")

    assert os.path.exists(dl_html), "download/index.html does not exist!"
    assert os.path.exists(ty_html), "thank-you/index.html does not exist!"

    with open(dl_html, encoding='utf-8') as f:
        content = f.read()

    assert "Download Master PDF" in content, "Missing 'Download Master PDF' button"
    assert "Download Kindle EPUB" in content, "Missing 'Download Kindle EPUB' button"
    assert "amazon.com/sendtokindle" in content, "Missing Send-to-Kindle instructions"
    assert "Apple Books" in content, "Missing Apple Books instructions"
    assert "GHL FULFILLMENT" in content, "Missing GHL webhook scaffold"
    assert "receiptTx" in content, "Missing PayPal receipt elements"
    print("  ✓ download/index.html UI components and GHL scaffold verified.")
    print("  ✓ thank-you/index.html route verified.")

    # Start ephemeral local HTTP server to verify live HTTP 200 routing
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=BASE_DIR, **kwargs)
        def log_message(self, format, *args):
            pass

    port = 8877
    httpd = socketserver.TCPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    routes_to_test = [
        f"http://127.0.0.1:{port}/download/",
        f"http://127.0.0.1:{port}/download/?book=ai-01&tx=TEST-TX-12345&amt=19.99&cc=USD&st=Completed",
        f"http://127.0.0.1:{port}/thank-you/",
        f"http://127.0.0.1:{port}/downloads/ai-01/The_AI_Agent_Blueprint.pdf",
        f"http://127.0.0.1:{port}/downloads/ai-01/The_AI_Agent_Blueprint.epub",
        f"http://127.0.0.1:{port}/downloads/care-01/Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf",
        f"http://127.0.0.1:{port}/downloads/care-01/Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.epub",
        f"http://127.0.0.1:{port}/downloads/in-cibil-99/CIBIL_7_Error_Audit-7.pdf"
    ]

    print("\nTesting local HTTP asset routing:")
    routing_passed = True
    for url in routes_to_test:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                cl = resp.headers.get('Content-Length', 'N/A')
                print(f"  ✓ HTTP {status} [{cl} bytes]: {url}")
        except Exception as e:
            print(f"  ✗ FAILED: {url} -> {e}")
            routing_passed = False

    httpd.shutdown()
    return routing_passed

def main():
    v1 = verify_10_ai_books()
    v2 = verify_10_zip_bundles()
    v3 = verify_download_portal_and_routing()

    print("\n=======================================================")
    if v1 and v2 and v3:
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY (100% PASS) ✨")
    else:
        print("VERIFICATION ISSUES ENCOUNTERED")
    print("=======================================================\n")
    if not (v1 and v2 and v3):
        sys.exit(1)

if __name__ == '__main__':
    main()
