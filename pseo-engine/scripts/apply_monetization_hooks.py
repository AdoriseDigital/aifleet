import os
import re

file_path = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\pseo-engine\scripts\compile_pseo.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add getRelatedGuides function if not present
related_guides_func = '''
function getRelatedGuides(nicheId, serviceId) {
  const allCombos = [
    { slug: 'b2b-saas/pseo-engine', niche: 'b2b-saas', title: 'B2B SaaS pSEO Engine', tag: 'Programmatic Inbound', description: 'Scale organic demo acquisition and long-tail integration pages.' },
    { slug: 'ecommerce-d2c/ai-agents', niche: 'ecommerce-d2c', title: 'E-Commerce AI Support Agents', tag: 'Autonomous Support', description: '24/7 ticket and order status triage resolving customer inquiries under 60 seconds.' },
    { slug: 'fintech/outbound-infrastructure', niche: 'fintech', title: 'FinTech Outbound Pipeline', tag: 'High-Compliance Outbound', description: 'Institutional email deliverability and cold prospecting systems.' },
    { slug: 'healthtech-biotech/ai-agents', niche: 'healthtech-biotech', title: 'HealthTech Autonomous Triage', tag: 'HIPAA-Ready AI', description: 'Patient routing and practitioner scheduling workflow automation.' },
    { slug: 'proptech-realestate/pseo-engine', niche: 'proptech-realestate', title: 'PropTech Localized Inbound', tag: 'Geo-Targeted Inbound', description: 'Programmatic local neighborhood landing pages for high-value real estate buyer leads.' },
    { slug: 'legaltech-professional/ai-agents', niche: 'legaltech-professional', title: 'LegalTech Document & Intake AI', tag: 'Intake Automation', description: 'Client onboarding, conflict checking, and initial intake qualification.' },
    { slug: 'venture-capital-private-equity/outbound-infrastructure', niche: 'venture-capital-private-equity', title: 'Private Equity Dealflow Sourcing', tag: 'Proprietary Sourcing', description: 'Automated deal sourcing pipelines targeting bootstrapped founders.' },
    { slug: 'edtech/pseo-engine', niche: 'edtech', title: 'EdTech Course Discovery Engine', tag: 'Curriculum SEO', description: 'Programmatic syllabus pages capturing high-intent student enrollments.' },
    { slug: 'cybersecurity/cloud-vps-hardening', niche: 'cybersecurity', title: 'Cybersecurity VPS Hardening', tag: 'Zero-Trust Defense', description: 'Automated reverse proxy, Cloudflare Zero Trust, and SSH firewall hardening.' },
    { slug: 'agency-consultancy/pseo-engine', niche: 'agency-consultancy', title: 'Agency Lead Magnet Inbound', tag: 'Agency pSEO', description: 'Scalable service teardowns and comparison matrices capturing enterprise retainers.' },
    { slug: 'b2b-saas/outbound-infrastructure', niche: 'b2b-saas', title: 'B2B SaaS Cold Outbound Engine', tag: 'Enterprise Outbound', description: 'Multi-inbox cold infrastructure targeting VP and C-level software buyers.' },
    { slug: 'ecommerce-d2c/pseo-engine', niche: 'ecommerce-d2c', title: 'E-Commerce Product pSEO', tag: 'Catalog Indexing', description: 'Dynamic long-tail buyer intent pages driving direct SKU checkouts.' }
  ];

  const currentSlug = `${nicheId}/${serviceId}`;
  const candidates = allCombos.filter(c => c.slug !== currentSlug);
  
  const sameNiche = candidates.filter(c => c.niche === nicheId);
  const diffNiche = candidates.filter(c => c.niche !== nicheId);
  
  const selected = [];
  if (sameNiche.length > 0) {
    selected.push(sameNiche[0]);
  }
  for (const c of diffNiche) {
    if (selected.length < 3 && !selected.includes(c)) {
      selected.push(c);
    }
  }
  while (selected.length < 3 && candidates.length > selected.length) {
    for (const c of candidates) {
      if (selected.length < 3 && !selected.includes(c)) selected.push(c);
    }
  }

  return selected.map(s => ({
    url: `/solutions/${s.slug}/`,
    title: s.title,
    tag: s.tag,
    description: s.description
  }));
}
'''

if 'function getRelatedGuides' not in code:
    code = code.replace("function buildHtmlPage(nicheId, serviceId) {", related_guides_func + "\nfunction buildHtmlPage(nicheId, serviceId) {")

# 2. Update Geo Banner (Hook 2)
old_geo_pattern = r'<!-- Geo-Targeted High-Ticket Enterprise Consulting Banner[\s\S]*?<\/aside>'
new_geo_banner = '''<!-- 2. Geo-Targeted B2B Enterprise Consulting Banner (US, Germany, Netherlands) -->
  <aside id="geo-enterprise-banner" aria-label="Enterprise Consulting Notice" class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border-b border-cyan-500/30 px-6 py-2.5 text-center text-xs md:text-sm text-slate-200 flex flex-wrap items-center justify-center gap-2 shadow-md">
    <span class="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono text-[10px] uppercase font-bold tracking-wider">Enterprise Advisory</span>
    <span>Need enterprise-grade AI automation setup or custom agent deployment?</span>
    <a href="https://services.adorisedigital.com" target="_blank" rel="noopener noreferrer" class="font-bold text-cyan-400 hover:text-white underline ml-1 transition">
      Book a 1-on-1 strategy call with Adorise Digital engineers &rarr;
    </a>
  </aside>'''

if re.search(old_geo_pattern, code):
    code = re.sub(old_geo_pattern, new_geo_banner, code)
else:
    print("Warning: old geo banner pattern not matched.")

# 3. Update Mid-Page Lead Magnet (Hook 1)
old_lead_magnet_pattern = r'<!-- High-Impact Conversion Lead Magnet[\s\S]*?<\/section>'
new_lead_magnet = '''<!-- 1. High-Contrast Inline Resource Hook (Lead Magnet) -->
    <section class="py-14 bg-gradient-to-r from-cyan-950/60 via-slate-900 to-indigo-950/60 border-y border-cyan-400/40 my-10 shadow-[0_0_40px_rgba(6,182,212,0.12)]">
      <div class="max-w-5xl mx-auto px-6">
        <div class="p-8 md:p-10 rounded-3xl bg-slate-950/95 border-2 border-cyan-400/60 shadow-2xl flex flex-col lg:flex-row items-center justify-between gap-8 relative overflow-hidden">
          <div class="absolute -right-20 -top-20 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
          
          <div class="space-y-4 max-w-xl text-left">
            <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-cyan-400/20 text-cyan-300 text-xs font-mono font-bold tracking-wide uppercase border border-cyan-400/30">
              ⚡ Instant Free Download • 48-Book Engineering Library
            </div>
            <h3 class="text-2xl md:text-3xl font-extrabold text-white font-display leading-tight">
              Working on ${data.niche_name} Automation?
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
              <label for="lead-email" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Send Free Blueprint & Schemas To:
              </label>
              <div class="flex flex-col sm:flex-row gap-2">
                <input id="lead-email" type="email" name="email" placeholder="founder@yourcompany.com" required class="w-full px-4 py-3 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 transition" />
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

if re.search(old_lead_magnet_pattern, code):
    code = re.sub(old_lead_magnet_pattern, new_lead_magnet, code)
else:
    print("Warning: old lead magnet pattern not matched.")

# 4. Update Whop Card with Micro-Proof (Hook 3)
old_whop_cta_block = '''          <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
            <a href="${whopCta.url}" target="_blank" rel="noopener noreferrer" class="px-6 py-3.5 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:scale-105 transition text-center whitespace-nowrap">
              ${whopCta.ctaText}
            </a>
            <a href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult" target="_blank" rel="noopener noreferrer" class="px-6 py-3.5 rounded-xl font-semibold bg-slate-800 border border-slate-700 text-white hover:bg-slate-700 transition text-center whitespace-nowrap">
              Custom Architecture
            </a>
          </div>'''

new_whop_cta_block = '''          <div class="flex flex-col items-center md:items-end gap-2 w-full md:w-auto">
            <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
              <a href="${whopCta.url}" target="_blank" rel="noopener noreferrer" class="px-6 py-3.5 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:scale-105 transition text-center whitespace-nowrap">
                ${whopCta.ctaText}
              </a>
              <a href="https://services.adorisedigital.com" target="_blank" rel="noopener noreferrer" class="px-6 py-3.5 rounded-xl font-semibold bg-slate-800 border border-slate-700 text-white hover:bg-slate-700 transition text-center whitespace-nowrap">
                Custom Architecture
              </a>
            </div>
            <div class="text-[11px] text-slate-400 font-medium flex items-center justify-center gap-1.5 pt-1 text-center">
              <span class="text-cyan-400">🛡️</span>
              <span>Trusted by founders and operators automating client acquisition across North America and Europe.</span>
            </div>
          </div>'''

if old_whop_cta_block in code:
    code = code.replace(old_whop_cta_block, new_whop_cta_block)
else:
    print("Warning: old whop cta block not matched directly.")

# 5. Insert Related Solutions & Architecture Blueprints section + update Final CTA (Hook 3)
related_solutions_section = '''    <!-- 3. Dynamic "Next Step" Micro-Funnel & Related Architecture Blueprints -->
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
          ${getRelatedGuides(nicheId, serviceId).map(rel => `
          <a href="${rel.url}" class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 hover:border-cyan-500/40 hover:bg-slate-900 transition flex flex-col justify-between group">
            <div>
              <div class="text-[11px] font-bold text-cyan-400 uppercase tracking-wider mb-2 font-mono">${rel.tag}</div>
              <h4 class="text-base font-bold text-white font-display group-hover:text-cyan-300 transition mb-2">${rel.title}</h4>
              <p class="text-xs text-slate-400 leading-relaxed">${rel.description}</p>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800/60 text-xs text-cyan-400 font-semibold flex items-center justify-between">
              <span>View System Blueprint</span>
              <span class="group-hover:translate-x-1 transition-transform">&rarr;</span>
            </div>
          </a>
          `).join('')}

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

final_cta_target = '''        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult" target="_blank" rel="noopener noreferrer" class="w-full sm:w-auto px-8 py-4 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-xl shadow-cyan-500/30 hover:scale-105 transition">
            Schedule Engineering Call
          </a>
          <a href="/solutions/" class="w-full sm:w-auto px-8 py-4 rounded-xl font-semibold bg-slate-900 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-800 transition">
            Explore All Solutions Matrix
          </a>
        </div>'''

final_cta_replacement = '''        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a href="https://services.adorisedigital.com" target="_blank" rel="noopener noreferrer" class="w-full sm:w-auto px-8 py-4 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-xl shadow-cyan-500/30 hover:scale-105 transition">
            Schedule Engineering Call
          </a>
          <a href="/solutions/" class="w-full sm:w-auto px-8 py-4 rounded-xl font-semibold bg-slate-900 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-800 transition">
            Explore All Solutions Matrix
          </a>
        </div>
        <div class="mt-4 text-xs text-slate-400 flex items-center justify-center gap-2">
          <span class="text-emerald-400">✓</span>
          <span>Trusted by founders and operators automating client acquisition across North America and Europe.</span>
        </div>'''

if final_cta_target in code:
    code = code.replace(final_cta_target, final_cta_replacement)

# Put related solutions section right before the final section
final_section_tag = '<section class="py-20 relative overflow-hidden text-center">'
if final_section_tag in code and '<!-- 3. Dynamic "Next Step" Micro-Funnel' not in code:
    code = code.replace(final_section_tag, related_solutions_section + "\n\n    " + final_section_tag)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated compile_pseo.js with all 3 conversion hooks successfully.")
