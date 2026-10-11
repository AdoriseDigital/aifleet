import os
import re
import json

sol_dir = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\adorise-frontend\solutions"

NICHE_NAMES = {
    "b2b-saas": "B2B SaaS & Enterprise Software",
    "ecommerce-d2c": "E-Commerce & High-Volume D2C",
    "fintech": "Financial Technology & Wealth Management",
    "healthtech-biotech": "Digital Health & Clinical Practices",
    "proptech-realestate": "Commercial Real Estate & PropTech",
    "legaltech-professional": "Corporate Law & Accounting Practices",
    "venture-capital-private-equity": "Private Equity & Venture Capital",
    "edtech": "Higher Education & EdTech Platforms",
    "cybersecurity": "Enterprise Cybersecurity & Managed IT",
    "agency-consultancy": "Digital Agencies & High-Growth Consultancies"
}

RELATED_SOLUTIONS = [
    {"slug": "b2b-saas/pseo-engine", "niche": "b2b-saas", "title": "B2B SaaS pSEO Engine", "tag": "Programmatic Inbound", "description": "Scale organic demo acquisition and long-tail integration pages."},
    {"slug": "ecommerce-d2c/ai-agents", "niche": "ecommerce-d2c", "title": "E-Commerce AI Support Agents", "tag": "Autonomous Support", "description": "24/7 ticket and order status triage resolving customer inquiries under 60 seconds."},
    {"slug": "fintech/outbound-infrastructure", "niche": "fintech", "title": "FinTech Outbound Pipeline", "tag": "High-Compliance Outbound", "description": "Institutional email deliverability and cold prospecting systems."},
    {"slug": "healthtech-biotech/ai-agents", "niche": "healthtech-biotech", "title": "HealthTech Autonomous Triage", "tag": "HIPAA-Ready AI", "description": "Patient routing and practitioner scheduling workflow automation."},
    {"slug": "proptech-realestate/pseo-engine", "niche": "proptech-realestate", "title": "PropTech Localized Inbound", "tag": "Geo-Targeted Inbound", "description": "Programmatic local neighborhood landing pages for high-value real estate buyer leads."},
    {"slug": "legaltech-professional/ai-agents", "niche": "legaltech-professional", "title": "LegalTech Document & Intake AI", "tag": "Intake Automation", "description": "Client onboarding, conflict checking, and initial intake qualification."},
    {"slug": "venture-capital-private-equity/outbound-infrastructure", "niche": "venture-capital-private-equity", "title": "Private Equity Dealflow Sourcing", "tag": "Proprietary Sourcing", "description": "Automated deal sourcing pipelines targeting bootstrapped founders."},
    {"slug": "edtech/pseo-engine", "niche": "edtech", "title": "EdTech Course Discovery Engine", "tag": "Curriculum SEO", "description": "Programmatic syllabus pages capturing high-intent student enrollments."},
    {"slug": "cybersecurity/cloud-vps-hardening", "niche": "cybersecurity", "title": "Cybersecurity VPS Hardening", "tag": "Zero-Trust Defense", "description": "Automated reverse proxy, Cloudflare Zero Trust, and SSH firewall hardening."},
    {"slug": "agency-consultancy/pseo-engine", "niche": "agency-consultancy", "title": "Agency Lead Magnet Inbound", "tag": "Agency pSEO", "description": "Scalable service teardowns and comparison matrices capturing enterprise retainers."},
    {"slug": "b2b-saas/outbound-infrastructure", "niche": "b2b-saas", "title": "B2B SaaS Cold Outbound Engine", "tag": "Enterprise Outbound", "description": "Multi-inbox cold infrastructure targeting VP and C-level software buyers."},
    {"slug": "ecommerce-d2c/pseo-engine", "niche": "ecommerce-d2c", "title": "E-Commerce Product pSEO", "tag": "Catalog Indexing", "description": "Dynamic long-tail buyer intent pages driving direct SKU checkouts."}
]

def get_related_cards_html(niche_id, service_id):
    current = f"{niche_id}/{service_id}"
    candidates = [c for c in RELATED_SOLUTIONS if c["slug"] != current]
    same_niche = [c for c in candidates if c["niche"] == niche_id]
    diff_niche = [c for c in candidates if c["niche"] != niche_id]
    
    selected = []
    if same_niche:
        selected.push(same_niche[0]) if hasattr(selected, 'push') else selected.append(same_niche[0])
    for c in diff_niche:
        if len(selected) < 3 and c not in selected:
            selected.append(c)
    while len(selected) < 3 and len(candidates) > len(selected):
        for c in candidates:
            if len(selected) < 3 and c not in selected:
                selected.append(c)
                
    cards_html = ""
    for rel in selected:
        cards_html += f'''
          <a href="/solutions/{rel["slug"]}/" class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 hover:border-cyan-500/40 hover:bg-slate-900 transition flex flex-col justify-between group">
            <div>
              <div class="text-[11px] font-bold text-cyan-400 uppercase tracking-wider mb-2 font-mono">{rel["tag"]}</div>
              <h4 class="text-base font-bold text-white font-display group-hover:text-cyan-300 transition mb-2">{rel["title"]}</h4>
              <p class="text-xs text-slate-400 leading-relaxed">{rel["description"]}</p>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800/60 text-xs text-cyan-400 font-semibold flex items-center justify-between">
              <span>View System Blueprint</span>
              <span class="group-hover:translate-x-1 transition-transform">&rarr;</span>
            </div>
          </a>'''
    return cards_html

def process_file(file_path, niche_id, service_id):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    niche_name = NICHE_NAMES.get(niche_id, niche_id.replace('-', ' ').title())

    # Replace forbidden buzzwords
    # "seamlessly" -> "autonomously"
    html = re.sub(r'\bseamlessly\b', 'autonomously', html, flags=re.IGNORECASE)
    html = re.sub(r'\bdelve\b', 'explore', html, flags=re.IGNORECASE)
    html = re.sub(r'\bsupercharge\b', 'accelerate', html, flags=re.IGNORECASE)
    html = re.sub(r'\bunleash\b', 'deploy', html, flags=re.IGNORECASE)
    html = re.sub(r'\btapestry\b', 'architecture', html, flags=re.IGNORECASE)
    html = re.sub(r'\bgame-changer\b', 'breakthrough', html, flags=re.IGNORECASE)
    html = re.sub(r'\brevolutionize\b', 'transform', html, flags=re.IGNORECASE)
    html = re.sub(r'\belevate\b', 'advance', html, flags=re.IGNORECASE)
    html = re.sub(r'\bcutting-edge\b', 'production-grade', html, flags=re.IGNORECASE)
    html = re.sub(r'\bsynergy\b', 'integration', html, flags=re.IGNORECASE)

    # 1. Hook 2: Geo-Targeted Enterprise Consulting Banner
    geo_banner = '''  <!-- 2. Geo-Targeted B2B Enterprise Consulting Banner (US, Germany, Netherlands) -->
  <aside id="geo-enterprise-banner" aria-label="Enterprise Consulting Notice" class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border-b border-cyan-500/30 px-6 py-2.5 text-center text-xs md:text-sm text-slate-200 flex flex-wrap items-center justify-center gap-2 shadow-md">
    <span class="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono text-[10px] uppercase font-bold tracking-wider">Enterprise Advisory</span>
    <span>Need enterprise-grade AI automation setup or custom agent deployment?</span>
    <a href="https://services.adorisedigital.com" target="_blank" rel="noopener noreferrer" class="font-bold text-cyan-400 hover:text-white underline ml-1 transition">
      Book a 1-on-1 strategy call with Adorise Digital engineers &rarr;
    </a>
  </aside>'''

    if 'id="geo-enterprise-banner"' in html:
        html = re.sub(r'<!-- 2\. Geo-Targeted[\s\S]*?<\/aside>', geo_banner, html)
        html = re.sub(r'<aside id="geo-enterprise-banner"[\s\S]*?<\/aside>', geo_banner, html)
    elif '<aside aria-label="Enterprise Consulting Notice"' in html:
        html = re.sub(r'<aside aria-label="Enterprise Consulting Notice"[\s\S]*?<\/aside>', geo_banner, html)
    elif '</header>' in html:
        html = html.replace('</header>', '</header>\n\n' + geo_banner)

    # 2. Hook 1: High-Contrast Mid-Page Lead Magnet
    lead_magnet_card = f'''    <!-- 1. High-Contrast Inline Resource Hook (Lead Magnet) -->
    <section class="py-14 bg-gradient-to-r from-cyan-950/60 via-slate-900 to-indigo-950/60 border-y border-cyan-400/40 my-10 shadow-[0_0_40px_rgba(6,182,212,0.12)]">
      <div class="max-w-5xl mx-auto px-6">
        <div class="p-8 md:p-10 rounded-3xl bg-slate-950/95 border-2 border-cyan-400/60 shadow-2xl flex flex-col lg:flex-row items-center justify-between gap-8 relative overflow-hidden">
          <div class="absolute -right-20 -top-20 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
          
          <div class="space-y-4 max-w-xl text-left">
            <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-cyan-400/20 text-cyan-300 text-xs font-mono font-bold tracking-wide uppercase border border-cyan-400/30">
              ⚡ Instant Free Download • 48-Book Engineering Library
            </div>
            <h3 class="text-2xl md:text-3xl font-extrabold text-white font-display leading-tight">
              Working on {niche_name} Automation?
            </h3>
            <p class="text-sm md:text-base text-slate-200 leading-relaxed font-medium">
              Download the complete production checklist, prompt templates, and architecture schema from our 48-book library (Instant Free Download).
            </p>
            <div class="flex flex-wrap items-center gap-4 text-xs text-slate-400 font-medium pt-1">
              <span class="flex items-center gap-1.5"><span class="text-cyan-400 font-bold">✓</span> Production Schemas</span>
              <span class="flex items-center gap-1.5"><span class="text-cyan-400 font-bold">✓</span> Verified Prompt Frameworks</span>
              <span class="flex items-center gap-1.5"><span class="text-cyan-400 font-bold">✓</span> Instant Free PDF Access</span>
            </div>
          </div>

          <div class="w-full lg:w-auto shrink-0 w-full max-w-md">
            <form action="https://books.adorisedigital.com" method="GET" target="_blank" class="space-y-3 bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-inner">
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Send Free Blueprint & Schemas To:
              </label>
              <div class="flex flex-col sm:flex-row gap-2">
                <input type="email" name="email" placeholder="founder@yourcompany.com" required class="w-full px-4 py-3 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 transition" />
                <button type="submit" class="px-5 py-3 rounded-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 hover:from-cyan-300 hover:to-blue-400 text-slate-950 text-sm font-display whitespace-nowrap shadow-lg shadow-cyan-500/30 hover:scale-[1.02] transition">
                  Get Free Access &rarr;
                </button>
              </div>
              <p class="text-[11px] text-slate-400 text-center font-mono">
                Instant delivery from our 48-book library backend. Zero credit card required.
              </p>
            </form>
          </div>
        </div>
      </div>
    </section>'''

    if '<!-- 1. High-Contrast Inline Resource Hook (Lead Magnet) -->' in html:
        html = re.sub(r'<!-- 1\. High-Contrast Inline Resource Hook[\s\S]*?<\/section>', lead_magnet_card, html)
    elif '<!-- High-Impact Conversion Lead Magnet' in html:
        html = re.sub(r'<!-- High-Impact Conversion Lead Magnet[\s\S]*?<\/section>', lead_magnet_card, html)
    else:
        # Insert before Human-Centered or Solution section
        human_marker = '<!-- Human-Centered Problem & Solution Architecture'
        if human_marker in html:
            html = html.replace(human_marker, lead_magnet_card + '\n\n    ' + human_marker)
        elif '</section>' in html:
            # Insert after the first major section after header
            first_sec_end = html.find('</section>') + len('</section>')
            html = html[:first_sec_end] + '\n\n' + lead_magnet_card + html[first_sec_end:]

    # 3. Hook 3: Social Proof beside CTAs
    proof_snippet = '''<div class="text-[11px] text-slate-400 font-medium flex items-center justify-center gap-1.5 pt-1 text-center">
              <span class="text-cyan-400">🛡️</span>
              <span>Trusted by founders and operators automating client acquisition across North America and Europe.</span>
            </div>'''
    
    if "Trusted by founders and operators" not in html:
        # Add under Custom Architecture button in Whop card
        custom_arch_anchor = 'Custom Architecture\n            </a>\n          </div>'
        custom_arch_replacement = f'Custom Architecture\n            </a>\n          </div>\n          {proof_snippet}'
        if custom_arch_anchor in html:
            html = html.replace(custom_arch_anchor, custom_arch_replacement)
        
        # Add under Final CTA
        explore_matrix_anchor = 'Explore All Solutions Matrix\n          </a>\n        </div>'
        explore_matrix_replacement = f'Explore All Solutions Matrix\n          </a>\n        </div>\n        <div class="mt-4 text-xs text-slate-400 flex items-center justify-center gap-2"><span class="text-emerald-400">✓</span><span>Trusted by founders and operators automating client acquisition across North America and Europe.</span></div>'
        if explore_matrix_anchor in html:
            html = html.replace(explore_matrix_anchor, explore_matrix_replacement)

    # 4. Hook 3: Dynamic Next Step Micro-Funnel & Related Architecture Blueprints
    related_cards = get_related_cards_html(niche_id, service_id)
    related_section = f'''    <!-- 3. Dynamic "Next Step" Micro-Funnel & Related Architecture Blueprints -->
    <section class="py-16 border-b border-slate-800/60 bg-slate-950/80">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div>
            <div class="text-xs font-bold uppercase tracking-widest text-cyan-400 mb-2">Cross-Industry Architecture</div>
            <h3 class="text-2xl md:text-3xl font-extrabold text-white font-display">
              Related Solutions & Architecture Blueprints
            </h3>
            <p class="text-sm text-slate-400 mt-1">Explore complementary automated pipelines and engineering frameworks across our production matrix.</p>
          </div>
          <a href="https://books.adorisedigital.com" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 text-xs font-bold text-cyan-400 hover:text-cyan-300 transition">
            Browse All 48 Books & Blueprints &rarr;
          </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
{related_cards}

          <!-- Direct Bridge to books.adorisedigital.com -->
          <a href="https://books.adorisedigital.com" target="_blank" rel="noopener noreferrer" class="p-6 rounded-2xl bg-gradient-to-br from-indigo-950/60 via-purple-950/40 to-slate-900 border border-purple-500/30 hover:border-purple-400/60 transition flex flex-col justify-between group">
            <div>
              <div class="text-[11px] font-bold text-purple-400 uppercase tracking-wider mb-2 font-mono">48-BOOK LIBRARY</div>
              <h4 class="text-base font-bold text-white font-display group-hover:text-purple-300 transition mb-2">Autonomous Agency & Systems Catalog</h4>
              <p class="text-xs text-slate-300 leading-relaxed">Full access to 48 masterclass books, prompt frameworks, and code architectures written for modern operators.</p>
            </div>
            <div class="mt-4 pt-3 border-t border-purple-500/30 text-xs text-purple-300 font-semibold flex items-center justify-between">
              <span>Open Books Portal</span>
              <span class="group-hover:translate-x-1 transition-transform">&rarr;</span>
            </div>
          </a>
        </div>
      </div>
    </section>'''

    if '<!-- 3. Dynamic "Next Step" Micro-Funnel' in html:
        html = re.sub(r'<!-- 3\. Dynamic "Next Step" Micro-Funnel[\s\S]*?<\/section>', related_section, html)
    else:
        # Insert before final section or before </main>
        final_sec_marker = '<section class="py-20 relative overflow-hidden text-center">'
        if final_sec_marker in html:
            html = html.replace(final_sec_marker, related_section + '\n\n    ' + final_sec_marker)
        elif '</main>' in html:
            html = html.replace('</main>', related_section + '\n\n  </main>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

count = 0
for root, dirs, files in os.walk(sol_dir):
    if 'index.html' in files:
        rel = os.path.relpath(root, sol_dir).replace('\\', '/')
        if rel != '.':
            parts = rel.split('/')
            if len(parts) >= 2:
                niche_id, service_id = parts[0], parts[1]
                target_file = os.path.join(root, 'index.html')
                process_file(target_file, niche_id, service_id)
                count += 1

print(f"Processed and updated {count} solution pages with all 3 conversion hooks & eliminated buzzwords.")
