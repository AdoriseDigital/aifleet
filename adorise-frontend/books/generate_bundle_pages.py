import re
import urllib.parse
from pathlib import Path

BASE_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books")
PAYPAL_EMAIL = "sanjay.shharma@hotmail.com"

BUNDLES = [
    {
        "slug": "care-vault",
        "title": "Complete 14-Book Care & Healing Vault",
        "badge": "14-BOOK CARE VAULT • 44% DISCOUNT",
        "subtitle": "All 14 Published Emotional & Caregiving Blueprints by Sanjay Shharma with Instant PDF & Kindle EPUB Delivery",
        "price_usd": "$79.00",
        "price_usd_clean": "79.00",
        "original_usd": "$139.86",
        "price_inr": "₹6,999",
        "original_inr": "₹12,586",
        "savings": "SAVE $60.86 (44% OFF)",
        "theme_color": "emerald",
        "books": [
            ("Hum Ladte Nahi Par Baat Hi Nahi Karte", "Navigating Silent Emotional Disconnect in Modern Indian Marriages", "Hinglish Flagship"),
            ("The Quiet Care", "Sustaining Compassion and Emotional Boundaries Through Caregiver Fatigue", "Empathy & Aging"),
            ("Still Married, Just Silent", "Breaking Through Decade-Long Emotional Cold Wars Without Starting a Fire", "Relationship Health"),
            ("When They Forget Your Name", "Navigating Dementia, Cognitive Decline, and the Ambiguous Grief of Slow Loss", "Memory Care"),
            ("The Long Goodbye", "Finding Grounded Strength When Terminal Illness Redefines Every Tomorrow", "Bereavement"),
            ("The Long Hello", "Rekindling Intimacy, Curiosity, and Shared Horizons After Life Calms Down", "Reconnection"),
            ("The Second Chapter", "Rebuilding Identity, Purpose, and Daily Joy After a Massive Life Disruption", "Life Transitions"),
            ("The Second Honeymoon", "Reclaiming Romance, Vulnerability, and Deep Play in the Empty-Nest Era", "Midlife Love"),
            ("The Last Sandwich", "Surviving the Double Pressure of Raising Teens While Nursing Aging Parents", "Family Dynamics"),
            ("The Friends Who Fade", "Making Peace With Drifting Friendships and Building Intentional Adult Tribes", "Social Circles"),
            ("The Survivor", "A Compassionate Protocol for Chronic Medical Battles and Emotional Exhaustion", "Resilience"),
            ("Gray Divorce", "Navigating Separation After 50 With Dignity, Financial Clarity, and Self-Worth", "Midlife Autonomy"),
            ("Remarried at 60", "Blending Adult Families, Protecting Assets, and Opening Your Heart in the Sunset Years", "Late Life Love"),
            ("After the Last Goodbye", "The Practical and Emotional Roadmap for the First 365 Days of Bereavement", "Sudden Loss")
        ],
        "meta_desc": "Get the complete 14-book Care Collection by Sanjay Shharma. Save $60 on all 14 relationship, caregiving, and grief blueprints with instant DRM-free PDF and EPUB downloads."
    },
    {
        "slug": "ai-agent-bundle",
        "title": "5-Book Autonomous AI Agency Wealth Stack",
        "badge": "5-BOOK AGENCY STACK • $20 DISCOUNT",
        "subtitle": "The Architectural Blueprints, Agency Playbooks, Content Agents, Workbooks, and Production System Prompts",
        "price_usd": "$79.99",
        "price_usd_clean": "79.99",
        "original_usd": "$99.95",
        "price_inr": "₹6,999",
        "original_inr": "₹9,495",
        "savings": "SAVE $20.00 (20% OFF)",
        "theme_color": "cyan",
        "books": [
            ("The AI Agent Blueprint", "Building, Deploying, and Monetizing Autonomous Software Fleets for Modern Businesses", "Core Architecture"),
            ("The AI Agency Playbook", "From Zero to Retained Multi-Agent Contracts: Operations, Pricing, and Client Acquisition", "Commercial Strategy"),
            ("The AI Content Agent", "Autonomous Media Engines: Publishing, Distribution, and Multi-Channel Organic Scale", "Autonomous Media"),
            ("The AI Agent Action Workbook", "Tactical Exercises, Discovery Questionnaires, and System Deployment Checklists", "Implementation Manual"),
            ("The AI Agent Cheat Sheets & System Prompts", "Production Prompt Vault, Deterministic Routing Templates, and Tool Schemas", "System Prompts Vault")
        ],
        "meta_desc": "Get the complete 5-book Autonomous AI Agency series by Sanjay Shharma. Architecture blueprints, playbooks, prompts, and code templates with instant DRM-free PDF and EPUB access."
    },
    {
        "slug": "ai-receptionist-bundle",
        "title": "5-Book AI Voice Receptionist Empire Stack",
        "badge": "5-BOOK RECEPTIONIST STACK • $20 DISCOUNT",
        "subtitle": "Complete Inbound & Outbound Voice Blueprints for Trade Services, Home Repairs, Law Firms, and Healthcare",
        "price_usd": "$79.99",
        "price_usd_clean": "79.99",
        "original_usd": "$99.95",
        "price_inr": "₹6,999",
        "original_inr": "₹9,495",
        "savings": "SAVE $20.00 (20% OFF)",
        "theme_color": "purple",
        "books": [
            ("Never Miss Another Call", "The $100K Leak: Why Traditional Front Desks Fail and How AI Plugs the Void", "Foundational Case"),
            ("The AI Receptionist Blueprint", "Telephony Architecture, Ultra-Low Latency Stacks, and Emergency Routing Workflows", "Technical Framework"),
            ("The AI Receptionist Buyer's Guide", "10 Critical Questions to Ask Vendors, Security Audits, and Real Telephony Costs", "Procurement Manual"),
            ("AI Front Desk for HVAC, Plumbing & Home Services", "Capturing Emergency Dispatch Calls 24/7 While Your Technicians Are on Jobs", "Trade Services"),
            ("AI Front Desk for Law Firms, Dentists & Real Estate", "Qualifying High-Net-Worth Consultations and Managing Appointments Without Burnout", "Professional Practices")
        ],
        "meta_desc": "Get the complete 5-book AI Voice Receptionist series by Sanjay Shharma. Plug missed calls, automate 24/7 emergency dispatch, and book appointments instantly."
    }
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Sanjay Shharma (IIM Calcutta Alumni)</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="https://books.adorisedigital.com/{slug}/">

  <!-- Open Graph -->
  <meta property="og:type" content="book">
  <meta property="og:url" content="https://books.adorisedigital.com/{slug}/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">

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
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased selection:bg-cyan-500 selection:text-slate-950 min-h-screen flex flex-col justify-between">

  <!-- Fixed Header Navigation -->
  <header class="h-20 border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md fixed top-0 left-0 right-0 z-50 px-6 flex items-center justify-between">
    <a href="/" class="flex items-center space-x-3 group">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-600 p-0.5 shadow-lg shadow-cyan-500/20">
        <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
          <span class="font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 text-lg">A</span>
        </div>
      </div>
      <span class="font-extrabold text-lg tracking-tight text-white font-display">ADORISE <span class="text-cyan-400">BOOKS</span></span>
    </a>
    
    <div class="flex items-center space-x-3">
      <a href="/" class="text-xs font-semibold px-4 py-2 rounded-full bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition">
        &larr; All 48 Blueprints
      </a>
      <a href="{paypal_url}" target="_blank" rel="noopener noreferrer" class="text-xs font-bold px-4 py-2 rounded-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-lg shadow-cyan-500/20 transition flex items-center gap-1.5">
        <span>⚡ Get Vault ({price_usd})</span>
      </a>
    </div>
  </header>

  <!-- Hero Section -->
  <main class="pt-28 pb-20 max-w-5xl mx-auto px-6">
    <div class="text-center max-w-3xl mx-auto mb-10">
      <span class="px-3.5 py-1 rounded-full text-[10px] font-mono uppercase tracking-widest font-extrabold bg-{theme_color}-500/10 text-{theme_color}-400 border border-{theme_color}-500/30 inline-block mb-3">
        {badge}
      </span>
      <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight font-display">
        {title}
      </h1>
      <p class="text-slate-300 text-base md:text-lg leading-relaxed mb-6">
        {subtitle}
      </p>

      <!-- Price Box -->
      <div class="inline-flex items-center gap-4 bg-slate-900/90 border border-slate-800 p-4 rounded-2xl shadow-xl">
        <div>
          <span class="text-xs text-slate-500 line-through mr-2">{original_usd} / {original_inr}</span>
          <span class="text-2xl font-black text-emerald-400 font-mono">{price_usd} / {price_inr}</span>
        </div>
        <span class="px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-bold text-xs font-mono">
          {savings}
        </span>
      </div>
    </div>

    <!-- Multi-Gateway Buy Bar -->
    <div class="glass-card rounded-3xl p-6 md:p-8 mb-12 shadow-2xl border border-slate-800">
      <h3 class="text-xs font-mono uppercase tracking-wider text-slate-400 font-bold text-center mb-5">
        Select Your Preferred Payment Gateway (Instant Delivery):
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- 1. PayPal Direct -->
        <a href="{paypal_url}" target="_blank" rel="noopener noreferrer" class="py-4 px-5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs uppercase tracking-wider flex flex-col items-center justify-center gap-1 shadow-xl shadow-cyan-500/20 transition transform hover:scale-[1.02]">
          <span class="flex items-center gap-2">
            <span>⚡</span>
            <span>Pay with PayPal ({price_usd})</span>
          </span>
          <span class="text-[10px] font-mono opacity-80">Instant Download Redirect</span>
        </a>

        <!-- 2. Gumroad Global -->
        <a href="https://adorisedigital.gumroad.com" target="_blank" rel="noopener noreferrer" class="py-4 px-5 rounded-2xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs uppercase tracking-wider flex flex-col items-center justify-center gap-1 border border-slate-700 transition transform hover:scale-[1.02]">
          <span class="flex items-center gap-2">
            <span>💳</span>
            <span>Buy on Gumroad ({price_usd})</span>
          </span>
          <span class="text-[10px] font-mono text-slate-400">Cards & Apple Pay</span>
        </a>

        <!-- 3. SuperProfile India UPI -->
        <a href="https://superprofile.bio/adorisedigital" target="_blank" rel="noopener noreferrer" class="py-4 px-5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-bold text-xs uppercase tracking-wider flex flex-col items-center justify-center gap-1 shadow-xl shadow-amber-500/20 transition transform hover:scale-[1.02]">
          <span class="flex items-center gap-2">
            <span>🇮🇳</span>
            <span>Pay via UPI ({price_inr})</span>
          </span>
          <span class="text-[10px] font-mono opacity-80">PhonePe / GPay / RuPay</span>
        </a>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-3 mt-5 text-[11px] font-mono text-slate-400">
        <span>✅ DRM-Free PDF + EPUB</span>
        <span>•</span>
        <span>⚡ 1-Click Fulfillment</span>
        <span>•</span>
        <span>🔒 256-Bit SSL Protection</span>
        <span>•</span>
        <span>♾️ Lifetime Updates</span>
      </div>
    </div>

    <!-- Complete Titles Included in This Bundle -->
    <div class="mb-14">
      <div class="flex items-center justify-between mb-6 pb-3 border-b border-slate-800">
        <h2 class="text-xl md:text-2xl font-bold text-white font-display">
          All Titles Included in This Vault
        </h2>
        <span class="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-3 py-1 rounded-full border border-cyan-500/20">
          Unabridged Digital Editions
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {books_html}
      </div>
    </div>

    <!-- Author Profile -->
    <div class="glass-card rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-center gap-6 mb-12">
      <div class="w-20 h-20 rounded-2xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-3xl font-black text-white flex-shrink-0 shadow-xl shadow-cyan-500/20">
        S
      </div>
      <div>
        <h3 class="text-lg font-bold text-white font-display mb-1">Authored by Sanjay Shharma</h3>
        <p class="text-xs font-mono text-cyan-400 mb-2">Author, Businessman & Coach • IIM Calcutta Alumni • Founder, Adorise Digital LLC</p>
        <p class="text-xs text-slate-300 leading-relaxed">
          With over 30 years of corporate strategy, executive leadership, and deep life experience, Sanjay Shharma writes high-impact playbooks designed for immediate real-world execution. Every title is backed by extensive operational research and published under strict DRM-free standards.
        </p>
      </div>
    </div>

    <!-- Bottom Purchase Bar -->
    <div class="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 text-center">
      <h3 class="text-lg font-bold text-white font-display mb-2">Ready to Download the Complete Vault?</h3>
      <p class="text-xs text-slate-400 mb-5 max-w-md mx-auto">Get instant DRM-free PDF and Kindle EPUB copies for all included titles immediately after checkout.</p>
      <a href="{paypal_url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-xl shadow-cyan-500/25 transition transform hover:scale-105">
        <span>⚡ Unlock Full Vault with PayPal ({price_usd})</span>
      </a>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-950 py-8 text-center text-xs text-slate-500 font-mono">
    <p>&copy; 2026 Adorise Digital LLC. All rights reserved. &bull; <a href="/" class="hover:text-slate-300 underline">Return to Main Bookstore Catalog</a></p>
  </footer>
</body>
</html>
"""

def generate_bundles():
    for b in BUNDLES:
        slug = b["slug"]
        title = b["title"]
        price_usd_clean = b["price_usd_clean"]
        
        # Build PayPal URL
        paypal_params = {
            "cmd": "_xclick",
            "business": PAYPAL_EMAIL,
            "item_name": f"{title} - Digital Bundle (PDF + EPUB)",
            "item_number": slug,
            "amount": price_usd_clean,
            "currency_code": "USD",
            "no_shipping": "1",
            "no_note": "1",
            "return": f"https://books.adorisedigital.com/thank-you/?bundle={slug}&gateway=paypal",
            "cancel_return": f"https://books.adorisedigital.com/{slug}/"
        }
        paypal_url = "https://www.paypal.com/cgi-bin/webscr?" + urllib.parse.urlencode(paypal_params)

        # Build included books HTML
        book_items = []
        for idx, (b_title, b_sub, b_cat) in enumerate(b["books"], 1):
            book_items.append(f"""
        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 transition">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyan-400 font-bold">Book {idx}</span>
            <span class="text-[10px] font-mono text-slate-500">{b_cat}</span>
          </div>
          <h4 class="text-sm font-bold text-white mb-1 font-display">{b_title}</h4>
          <p class="text-xs text-slate-400 leading-relaxed">{b_sub}</p>
        </div>""")
        books_html = "\n".join(book_items)

        html = TEMPLATE.format(
            slug=slug,
            title=title,
            badge=b["badge"],
            subtitle=b["subtitle"],
            price_usd=b["price_usd"],
            original_usd=b["original_usd"],
            price_inr=b["price_inr"],
            original_inr=b["original_inr"],
            savings=b["savings"],
            theme_color=b["theme_color"],
            meta_desc=b["meta_desc"],
            paypal_url=paypal_url,
            books_html=books_html
        )

        out_dir = BASE_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated bundle page: {slug}")

if __name__ == "__main__":
    generate_bundles()
