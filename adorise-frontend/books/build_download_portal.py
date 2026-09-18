import os
import json

BASE_DIR = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\adorise-frontend\books"
MANIFEST_PATH = os.path.join(BASE_DIR, "catalog_downloads_manifest.json")

with open(MANIFEST_PATH, encoding='utf-8') as f:
    catalog = json.load(f)

catalog_json_str = json.dumps(catalog, ensure_ascii=False)

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instant Digital Download & Order Confirmation | Adorise Books</title>
    <meta name="description" content="Thank you for your purchase. Instantly download your Master PDF and Kindle EPUB digital blueprints from Adorise Digital.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {{
        darkMode: 'class',
        theme: {{
          extend: {{
            fontFamily: {{
              sans: ['Plus Jakarta Sans', 'sans-serif'],
              display: ['Outfit', 'sans-serif'],
            }}
          }}
        }}
      }}
    </script>
    <style>
      .glass-card {{
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
      }}
      .glass-card:hover {{
        border-color: rgba(6, 182, 212, 0.35);
      }}
      .gradient-glow {{
        background: radial-gradient(circle at 50% -20%, rgba(6, 182, 212, 0.18), transparent 70%);
      }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased selection:bg-cyan-500 selection:text-slate-950 min-h-screen flex flex-col justify-between">

    <!-- Fixed Header Navigation -->
    <header class="h-20 border-b border-slate-800/80 bg-slate-950/95 backdrop-blur-md fixed top-0 left-0 right-0 z-50 px-6 flex items-center justify-between">
        <a href="/" class="flex items-center space-x-3 group">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-600 p-0.5 shadow-lg shadow-cyan-500/20">
                <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                    <span class="font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 text-lg">A</span>
                </div>
            </div>
            <span class="font-extrabold text-lg tracking-tight text-white font-display">ADORISE <span class="text-cyan-400">BOOKS</span></span>
            <span class="px-2 py-0.5 text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full flex items-center space-x-1">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>Fulfillment Portal</span>
            </span>
        </a>
        
        <div class="flex items-center space-x-3 md:space-x-4">
            <a href="/" class="text-xs font-semibold px-4 py-2 rounded-full bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition">
                ← 48 Catalog
            </a>
            <a href="https://services.adorisedigital.com" target="_blank" class="text-xs font-bold px-4 py-2 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20 hover:scale-105 transition">
                AI Services Storefront ⚡
            </a>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="pt-28 pb-20 max-w-6xl mx-auto px-6 w-full gradient-glow">
        
        <!-- Order Confirmation Status Banner -->
        <div class="mb-10 text-center max-w-3xl mx-auto">
            <div class="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold tracking-wide uppercase mb-4">
                <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span id="orderBadgeStatus">Payment Confirmed • Instant Access Granted</span>
            </div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-3 tracking-tight font-display">
                Thank You for Your Order!
            </h1>
            <p class="text-slate-400 text-sm md:text-base leading-relaxed">
                Your payment has been processed securely. Your DRM-free master digital edition is ready for instant download below.
            </p>
        </div>

        <!-- Verified Order Receipt Card -->
        <div class="glass-card rounded-2xl p-5 md:p-6 mb-10 border border-slate-800 shadow-xl">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
                <div>
                    <span class="text-xs font-mono uppercase text-slate-500 tracking-wider">Transaction Receipt</span>
                    <div class="flex items-center space-x-2 mt-1">
                        <span class="text-sm md:text-base font-mono font-bold text-cyan-400" id="receiptTx">TX-VERIFIED-AUTH</span>
                        <button onclick="copyTxId()" class="text-xs text-slate-400 hover:text-cyan-300 transition" title="Copy ID">📋</button>
                    </div>
                </div>
                <div class="flex flex-wrap gap-4 text-xs font-mono">
                    <div class="bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800">
                        <span class="text-slate-500 block text-[10px]">PAYMENT STATUS</span>
                        <span class="text-emerald-400 font-bold" id="receiptStatus">Completed</span>
                    </div>
                    <div class="bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800">
                        <span class="text-slate-500 block text-[10px]">TOTAL AMOUNT</span>
                        <span class="text-white font-bold" id="receiptAmount">$19.99 USD</span>
                    </div>
                    <div class="bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800">
                        <span class="text-slate-500 block text-[10px]">GATEWAY / RAIL</span>
                        <span class="text-cyan-400 font-bold" id="receiptGateway">PayPal Express</span>
                    </div>
                    <div class="bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800">
                        <span class="text-slate-500 block text-[10px]">FULFILLMENT</span>
                        <span class="text-purple-400 font-bold">DRM-Free Direct</span>
                    </div>
                </div>
            </div>
            
            <div class="pt-4 flex flex-col sm:flex-row sm:items-center justify-between text-xs text-slate-400 gap-2">
                <div>
                    Customer Support & Inquiries: <a href="mailto:support@adorisedigital.com" class="text-cyan-400 hover:underline">support@adorisedigital.com</a>
                </div>
                <div class="font-mono text-[11px] text-slate-500" id="receiptTimestamp">
                    Timestamp: 2026-09-19
                </div>
            </div>
        </div>

        <!-- Hero Purchased Book Download Section -->
        <div id="heroBookContainer" class="glass-card rounded-3xl p-6 md:p-10 border border-cyan-500/30 shadow-2xl mb-12 relative overflow-hidden">
            <div class="absolute -top-24 -right-24 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
            
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                <!-- Book Thumbnail & Badge -->
                <div class="lg:col-span-4 flex flex-col items-center text-center">
                    <div class="w-52 md:w-60 h-76 rounded-2xl bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700/80 shadow-2xl p-3 flex flex-col justify-between relative group hover:scale-[1.02] transition duration-300">
                        <div class="flex items-center justify-between text-[10px] font-mono text-cyan-400">
                            <span id="heroBookCatBadge" class="px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/30 uppercase">AI Series</span>
                            <span class="text-slate-500">6"x9" Trade</span>
                        </div>
                        <div class="py-6">
                            <h3 id="heroCoverTitle" class="text-lg md:text-xl font-extrabold text-white leading-snug font-display">The AI Agent Blueprint</h3>
                            <p id="heroCoverAuthor" class="text-xs text-slate-400 mt-2">By Sanjay Shharma</p>
                            <span class="inline-block mt-3 px-2.5 py-1 text-[10px] font-mono font-bold bg-amber-500/10 text-amber-300 border border-amber-500/30 rounded">
                                Complete Unabridged Edition
                            </span>
                        </div>
                        <div class="pt-3 border-t border-slate-800 text-[10px] font-mono text-slate-500 flex justify-between">
                            <span>Adorise Digital LLC</span>
                            <span id="heroCoverPages">164 Pages</span>
                        </div>
                    </div>
                </div>

                <!-- Book Metadata & Download Actions -->
                <div class="lg:col-span-8 flex flex-col justify-center">
                    <div class="flex flex-wrap items-center gap-2 mb-3">
                        <span id="heroCategoryLabel" class="px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                            AI Wealth • Autonomous Agency
                        </span>
                        <span class="px-3 py-1 rounded-full text-xs font-mono bg-slate-900 border border-slate-800 text-emerald-400">
                            ✓ Verified Complete Edition with Backmatter
                        </span>
                    </div>

                    <h2 id="heroBookTitle" class="text-2xl md:text-4xl font-extrabold text-white mb-2 font-display">
                        The AI Agent Blueprint
                    </h2>
                    <p id="heroBookSubtitle" class="text-slate-300 text-sm md:text-base leading-relaxed mb-4">
                        Building, Deploying, and Monetizing Autonomous Software Fleets for Modern Businesses
                    </p>

                    <div class="flex items-center space-x-2 text-xs text-slate-400 mb-6">
                        <span>Author: <strong class="text-white">Sanjay Shharma</strong> (IIM Calcutta Alumni)</span>
                        <span>•</span>
                        <span>Published by <strong class="text-white">Adorise Digital (Wyoming, USA)</strong></span>
                    </div>

                    <!-- Instant Download Action Buttons -->
                    <div class="space-y-3 sm:space-y-0 sm:flex sm:flex-wrap sm:gap-4 mb-6">
                        <!-- Master PDF Button -->
                        <a id="btnDownloadPdf" href="#" download class="flex-1 min-w-[220px] px-6 py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-extrabold text-sm shadow-xl shadow-cyan-500/25 flex items-center justify-center space-x-3 transition transform hover:-translate-y-0.5">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            <div class="text-left">
                                <div class="leading-none">Download Master PDF</div>
                                <span class="text-[10px] font-normal opacity-80" id="btnPdfMeta">Print-Ready • High Res</span>
                            </div>
                        </a>

                        <!-- Kindle EPUB Button -->
                        <a id="btnDownloadEpub" href="#" download class="flex-1 min-w-[220px] px-6 py-4 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-white font-bold text-sm shadow-lg flex items-center justify-center space-x-3 transition transform hover:-translate-y-0.5">
                            <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                            </svg>
                            <div class="text-left">
                                <div class="leading-none">Download Kindle EPUB</div>
                                <span class="text-[10px] font-normal text-slate-400" id="btnEpubMeta">Kindle / Apple Books</span>
                            </div>
                        </a>
                    </div>

                    <!-- Bonus / Direct In-Browser Reader Link -->
                    <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-800/80 pt-4">
                        <div class="flex items-center space-x-2">
                            <span class="text-emerald-400">●</span>
                            <span>Direct Lifetime Access Link: Bookmark this URL anytime.</span>
                        </div>
                        <a id="btnDirectRead" href="#" target="_blank" class="text-cyan-400 hover:text-cyan-300 font-semibold hover:underline">
                            Open In-Browser PDF Reader →
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Easy Reading Instructions (Send-to-Kindle, Apple Books, Android) -->
        <div class="mb-14">
            <h3 class="text-xl md:text-2xl font-bold text-white font-display mb-4 text-center">
                Reading Instructions & Device Setup
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
                <!-- Kindle -->
                <div class="glass-card rounded-2xl p-5 border border-slate-800">
                    <div class="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400 flex items-center justify-center font-bold text-lg mb-3">
                        📖
                    </div>
                    <h4 class="font-bold text-white text-base mb-1">Amazon Kindle</h4>
                    <p class="text-xs text-slate-400 leading-relaxed mb-3">
                        Sync the EPUB directly to your Kindle Paperwhite, Oasis, Scribe, or mobile app.
                    </p>
                    <ol class="text-xs text-slate-300 space-y-1.5 list-decimal list-inside">
                        <li>Visit <a href="https://www.amazon.com/sendtokindle" target="_blank" class="text-cyan-400 hover:underline">amazon.com/sendtokindle</a>.</li>
                        <li>Drag & drop your downloaded <strong>.epub</strong> file.</li>
                        <li>Click Send — your book arrives on your Kindle in under 60 seconds!</li>
                    </ol>
                </div>

                <!-- Apple Books -->
                <div class="glass-card rounded-2xl p-5 border border-slate-800">
                    <div class="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-400 flex items-center justify-center font-bold text-lg mb-3">
                        🍎
                    </div>
                    <h4 class="font-bold text-white text-base mb-1">Apple Books (iOS / Mac)</h4>
                    <p class="text-xs text-slate-400 leading-relaxed mb-3">
                        Native reading with custom typography, page-turn animation, and auto dark mode.
                    </p>
                    <ol class="text-xs text-slate-300 space-y-1.5 list-decimal list-inside">
                        <li>Download the <strong>.epub</strong> file on iPhone, iPad, or Mac.</li>
                        <li>Tap the downloaded file in your Files / Downloads folder.</li>
                        <li>Tap <strong>"Open in Books"</strong> to start reading instantly.</li>
                    </ol>
                </div>

                <!-- Acrobat / PDF -->
                <div class="glass-card rounded-2xl p-5 border border-slate-800">
                    <div class="w-10 h-10 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 flex items-center justify-center font-bold text-lg mb-3">
                        📑
                    </div>
                    <h4 class="font-bold text-white text-base mb-1">Master PDF & Large Screen</h4>
                    <p class="text-xs text-slate-400 leading-relaxed mb-3">
                        Ideal for desktop reading, high-res printing, and interactive checklists.
                    </p>
                    <ol class="text-xs text-slate-300 space-y-1.5 list-decimal list-inside">
                        <li>Download the <strong>Master PDF</strong> above.</li>
                        <li>Open in Chrome, Adobe Acrobat Reader, or Preview.</li>
                        <li>Full luxury 6"x9" layout with complete master catalog included.</li>
                    </ol>
                </div>
            </div>
        </div>

        <!-- 48-Book Master Catalog Title Switcher -->
        <div class="glass-card rounded-2xl p-6 md:p-8 border border-slate-800 mb-14">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                    <h3 class="text-xl font-bold text-white font-display">Switch to Another Purchased Title</h3>
                    <p class="text-xs text-slate-400">Purchased a bundle or multiple books? Select any title from our 48-book catalog to download:</p>
                </div>
                <!-- Search Input -->
                <div class="w-full md:w-72">
                    <input type="text" id="catalogSearchInput" placeholder="Search 48 titles or ID..." oninput="filterCatalog()" class="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500">
                </div>
            </div>

            <!-- Category Pills -->
            <div class="flex flex-wrap gap-2 mb-6 text-xs font-semibold">
                <button onclick="setCategoryFilter('all')" class="cat-pill px-3 py-1.5 rounded-lg bg-cyan-500 text-slate-950 font-bold" data-cat="all">All 48 Titles</button>
                <button onclick="setCategoryFilter('ai')" class="cat-pill px-3 py-1.5 rounded-lg bg-slate-900 text-slate-300 border border-slate-800 hover:text-white" data-cat="ai">AI Wealth Fleet (10)</button>
                <button onclick="setCategoryFilter('care')" class="cat-pill px-3 py-1.5 rounded-lg bg-slate-900 text-slate-300 border border-slate-800 hover:text-white" data-cat="care">Care Collection (14)</button>
                <button onclick="setCategoryFilter('indian')" class="cat-pill px-3 py-1.5 rounded-lg bg-slate-900 text-slate-300 border border-slate-800 hover:text-white" data-cat="indian">Indian Financial Stack (24)</button>
            </div>

            <!-- Catalog Items Grid -->
            <div id="catalogGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                <!-- Injected via JavaScript -->
            </div>
        </div>

        <!-- Ecosystem Cross-Promotion & AI Services Banner -->
        <div class="rounded-3xl p-8 bg-gradient-to-r from-cyan-950/60 via-slate-900 to-purple-950/60 border border-cyan-500/30 text-center relative overflow-hidden">
            <h3 class="text-2xl font-bold text-white font-display mb-2">Deploy Autonomous AI for Your Business</h3>
            <p class="text-sm text-slate-300 max-w-2xl mx-auto mb-6">
                Turn book theory into deployed enterprise software. Hire Adorise Digital to install 24/7 AI Receptionists, autonomous lead scrapers, and programmatic marketing pipelines.
            </p>
            <div class="flex flex-wrap items-center justify-center gap-4">
                <a href="https://services.adorisedigital.com" target="_blank" class="px-6 py-3 rounded-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs tracking-wide uppercase transition shadow-lg shadow-cyan-500/25">
                    Explore Services Storefront ⚡
                </a>
                <a href="https://adorisedigital.com" target="_blank" class="px-6 py-3 rounded-full bg-slate-900 hover:bg-slate-800 border border-slate-700 text-white font-semibold text-xs transition">
                    Main Ecosystem Overview →
                </a>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 py-8 px-6 text-center text-xs text-slate-500">
        <p class="mb-2">© 2026 Adorise Digital LLC • A Division of Trendy DigiStore LLC (Wyoming, USA). All Rights Reserved.</p>
        <p>Support & Author Inquiries: <a href="mailto:support@adorisedigital.com" class="text-slate-400 hover:underline">support@adorisedigital.com</a> • Official Bookstore: <a href="https://books.adorisedigital.com" class="text-slate-400 hover:underline">books.adorisedigital.com</a></p>
    </footer>

    <!-- Toast Notification for Downloads -->
    <div id="downloadToast" class="fixed bottom-6 right-6 hidden bg-slate-900 border border-cyan-500/50 text-white px-5 py-3 rounded-xl shadow-2xl z-50 text-xs font-semibold flex items-center space-x-2 transition">
        <span class="text-cyan-400 text-lg">⚡</span>
        <span id="toastMessage">Download started! Check your downloads folder.</span>
    </div>

    <!-- Embedded Catalog Data & Client Logic -->
    <script>
        const CATALOG = {catalog_json_str};

        let currentBook = null;
        let currentFilter = 'all';

        // Parse Query Parameters
        function getQueryParams() {{
            const p = new URLSearchParams(window.location.search);
            return {{
                book: p.get('book') || p.get('id') || p.get('item_number') || p.get('custom') || p.get('slug'),
                item_name: p.get('item_name'),
                tx: p.get('tx') || p.get('paymentId') || p.get('token') || p.get('txn_id'),
                amt: p.get('amt') || p.get('amount'),
                cc: p.get('cc') || p.get('currency_code') || 'USD',
                st: p.get('st') || p.get('payment_status') || 'Completed',
                payer_email: p.get('payer_email') || p.get('email') || ''
            }};
        }}

        // Match requested book from query string
        function resolveBook(query) {{
            if (!query) return CATALOG[0]; // Default to first book (The AI Agent Blueprint)

            const qLower = query.toLowerCase().trim();
            // 1. Direct ID match
            let found = CATALOG.find(b => b.id.toLowerCase() === qLower);
            if (found) return found;

            // 2. Exact or partial title match
            found = CATALOG.find(b => b.title.toLowerCase().includes(qLower) || qLower.includes(b.title.toLowerCase()));
            if (found) return found;

            // 3. Slug / URL match
            found = CATALOG.find(b => (b.gumroad_url && b.gumroad_url.toLowerCase().includes(qLower)) || (b.pdf_name && b.pdf_name.toLowerCase().includes(qLower)));
            if (found) return found;

            return CATALOG[0];
        }}

        // Render Book in Hero Download Container
        function selectBook(bookId) {{
            const book = CATALOG.find(b => b.id === bookId);
            if (!book) return;
            currentBook = book;

            // Update UI fields
            document.getElementById('heroBookTitle').textContent = book.title;
            document.getElementById('heroBookSubtitle').textContent = book.subtitle;
            document.getElementById('heroCoverTitle').textContent = book.title;
            document.getElementById('heroCategoryLabel').textContent = book.category_label || book.category.toUpperCase();
            document.getElementById('heroBookCatBadge').textContent = book.category.toUpperCase();

            // Set buttons
            const btnPdf = document.getElementById('btnDownloadPdf');
            const btnEpub = document.getElementById('btnDownloadEpub');
            const btnDirectRead = document.getElementById('btnDirectRead');
            const btnPdfMeta = document.getElementById('btnPdfMeta');
            const btnEpubMeta = document.getElementById('btnEpubMeta');

            if (book.pdf_url) {{
                btnPdf.href = book.pdf_url;
                btnPdf.style.display = 'flex';
                btnPdfMeta.textContent = `${{book.pdf_name}} • ${{book.pdf_size_mb || 1.5}} MB`;
                btnPdf.onclick = () => showToast(`Starting download: ${{book.pdf_name}}`);
                btnDirectRead.href = book.pdf_url;
                btnDirectRead.style.display = 'inline-block';
            }} else {{
                btnPdf.style.display = 'none';
                btnDirectRead.style.display = 'none';
            }}

            if (book.epub_url) {{
                btnEpub.href = book.epub_url;
                btnEpub.style.display = 'flex';
                btnEpubMeta.textContent = `${{book.epub_name}} • Kindle / Apple Books`;
                btnEpub.onclick = () => showToast(`Starting download: ${{book.epub_name}}`);
            }} else {{
                btnEpub.style.display = 'none';
            }}

            // Highlight selected in grid
            document.querySelectorAll('.catalog-card').forEach(c => {{
                if (c.dataset.id === book.id) {{
                    c.classList.add('border-cyan-500', 'bg-cyan-500/10');
                }} else {{
                    c.classList.remove('border-cyan-500', 'bg-cyan-500/10');
                }}
            }});
        }}

        // Render the Catalog Grid for title switching
        function renderCatalogGrid() {{
            const grid = document.getElementById('catalogGrid');
            const searchVal = (document.getElementById('catalogSearchInput').value || '').toLowerCase();

            grid.innerHTML = '';
            const filtered = CATALOG.filter(b => {{
                const matchesCat = currentFilter === 'all' || b.category === currentFilter;
                const matchesSearch = !searchVal || b.title.toLowerCase().includes(searchVal) || b.id.toLowerCase().includes(searchVal);
                return matchesCat && matchesSearch;
            }});

            filtered.forEach(b => {{
                const isSelected = currentBook && currentBook.id === b.id;
                const card = document.createElement('div');
                card.className = `catalog-card p-3 rounded-xl border ${{isSelected ? 'border-cyan-500 bg-cyan-500/10' : 'border-slate-800 bg-slate-900/60'}} hover:border-cyan-500/50 cursor-pointer transition flex items-center justify-between gap-3`;
                card.dataset.id = b.id;
                card.onclick = () => {{
                    selectBook(b.id);
                    document.getElementById('heroBookContainer').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }};

                card.innerHTML = `
                    <div class="overflow-hidden">
                        <div class="flex items-center space-x-2">
                            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-cyan-400 font-bold">${{b.id}}</span>
                            <span class="text-[10px] font-mono text-slate-500 uppercase">${{b.category}}</span>
                        </div>
                        <h4 class="text-xs font-bold text-white truncate mt-1">${{b.title}}</h4>
                    </div>
                    <button class="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 font-mono text-slate-300 font-bold transition">
                        Select
                    </button>
                `;
                grid.appendChild(card);
            }});
        }}

        function setCategoryFilter(cat) {{
            currentFilter = cat;
            document.querySelectorAll('.cat-pill').forEach(btn => {{
                if (btn.dataset.cat === cat) {{
                    btn.classList.add('bg-cyan-500', 'text-slate-950', 'font-bold');
                    btn.classList.remove('bg-slate-900', 'text-slate-300');
                }} else {{
                    btn.classList.remove('bg-cyan-500', 'text-slate-950', 'font-bold');
                    btn.classList.add('bg-slate-900', 'text-slate-300');
                }}
            }});
            renderCatalogGrid();
        }}

        function filterCatalog() {{
            renderCatalogGrid();
        }}

        function showToast(msg) {{
            const t = document.getElementById('downloadToast');
            document.getElementById('toastMessage').textContent = msg;
            t.classList.remove('hidden');
            setTimeout(() => t.classList.add('hidden'), 3500);
        }}

        function copyTxId() {{
            const tx = document.getElementById('receiptTx').textContent;
            navigator.clipboard.writeText(tx);
            showToast(`Copied Transaction ID: ${{tx}}`);
        }}

        // =========================================================================
        // GOHIGHLEVEL (GHL) IPN / WEBHOOK FULFILLMENT NOTIFICATION SCAFFOLD
        // =========================================================================
        function triggerGHLWebhook(payload) {{
            // Configure your GHL or n8n Webhook URL here:
            const GHL_WEBHOOK_URL = window.GHL_WEBHOOK_URL || "https://services.leadconnectorhq.com/hooks/adorise-book-purchase-fulfillment";

            console.log("[GHL FULFILLMENT SCAFFOLD] Triggering webhook notification:", payload);

            // Deduplication via LocalStorage
            try {{
                const processed = JSON.parse(localStorage.getItem('adorise_processed_tx') || '[]');
                if (payload.transaction_id && processed.includes(payload.transaction_id)) {{
                    console.log("[GHL FULFILLMENT] Transaction already processed previously:", payload.transaction_id);
                    return;
                }}
                if (payload.transaction_id) {{
                    processed.push(payload.transaction_id);
                    localStorage.setItem('adorise_processed_tx', JSON.stringify(processed));
                }}
            }} catch(e) {{}}

            // If a live webhook URL is configured, perform async dispatch
            if (GHL_WEBHOOK_URL && !GHL_WEBHOOK_URL.includes("adorise-book-purchase-fulfillment")) {{
                fetch(GHL_WEBHOOK_URL, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }}).then(res => console.log("[GHL FULFILLMENT] Webhook response:", res.status))
                  .catch(err => console.warn("[GHL FULFILLMENT] Webhook error:", err));
            }}
        }}

        // Init page on DOM Load
        document.addEventListener('DOMContentLoaded', () => {{
            const params = getQueryParams();
            const resolved = resolveBook(params.book || params.item_name);
            selectBook(resolved.id);

            // Update receipt details from PayPal parameters
            const txId = params.tx || ('ADR-ORD-' + Math.random().toString(36).substring(2, 9).toUpperCase());
            document.getElementById('receiptTx').textContent = txId;
            document.getElementById('receiptAmount').textContent = params.amt ? (`$${{params.amt}} ${{params.cc}}`) : resolved.price_usd;
            document.getElementById('receiptStatus').textContent = params.st;
            document.getElementById('receiptTimestamp').textContent = `Order Verified: ${{new Date().toLocaleString()}}`;

            renderCatalogGrid();

            // Dispatch GHL Webhook Notification
            triggerGHLWebhook({{
                event: 'digital_book_download_accessed',
                transaction_id: txId,
                book_id: resolved.id,
                book_title: resolved.title,
                category: resolved.category,
                amount: params.amt || resolved.price_usd,
                currency: params.cc,
                payer_email: params.payer_email,
                status: params.st,
                timestamp: new Date().toISOString()
            }});
        }});
    </script>
</body>
</html>
"""

# Write to download/index.html
download_dir = os.path.join(BASE_DIR, "download")
os.makedirs(download_dir, exist_ok=True)
with open(os.path.join(download_dir, "index.html"), 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)
print(f"Generated download portal: {os.path.join(download_dir, 'index.html')}")

# Write to thank-you/index.html
thankyou_dir = os.path.join(BASE_DIR, "thank-you")
os.makedirs(thankyou_dir, exist_ok=True)
with open(os.path.join(thankyou_dir, "index.html"), 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)
print(f"Generated thank-you portal: {os.path.join(thankyou_dir, 'index.html')}")
