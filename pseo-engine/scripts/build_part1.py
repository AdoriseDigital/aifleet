# -*- coding: utf-8 -*-
"""
Builder for 58 bespoke combinations.
Part 1: pseo-engine, ai-agents, web-app-engineering
"""
import json
import re

BANNED = ['delve', 'supercharge', 'unleash', 'tapestry', 'seamlessly', 'game-changer', 'revolutionize', 'elevate', 'cutting-edge', 'synergy']

def check_clean(text, ctx):
    for w in BANNED:
        if re.search(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE):
            raise ValueError(f"Found banned word '{w}' in {ctx}")

data = {}

# --- PSEO ENGINE (5 missing) ---
data['fintech/pseo-engine'] = {
    'niche_name': 'FinTech & Digital Financial Services',
    'service_name': 'Programmatic SEO Engine',
    'badge': 'Programmatic Search Scaling | FinTech',
    'h1': 'Programmatic SEO Engine for FinTech & Banking Platforms',
    'subheadline': 'Capture institutional CFOs, treasury directors, and compliance officers searching for payment rails, banking-as-a-service alternatives, and AML reconciliation workflows.',
    'metrics': [
        {'val': '< 40ms', 'lbl': 'Edge TTFB', 'sub': 'Sub-second React Server Components load'},
        {'val': '+380%', 'lbl': 'Organic Inbound Growth', 'sub': 'Commercial financial search impressions'},
        {'val': '100%', 'lbl': 'Schema Validated', 'sub': 'ProfessionalService JSON-LD microdata'},
        {'val': '$25k-$150k', 'lbl': 'Target ACV Tier', 'sub': 'High-value institutional financial contracts'}
    ],
    'deep_dive_1': 'Financial technology platforms face astronomical pay-per-click costs on Google Ads where commercial terms like banking-as-a-service and payment gateway alternatives cost upwards of $75 per click. Instead of renting paid traffic, our programmatic architecture deploys hundreds of permanent edge pages targeting long-tail banking integrations, regulatory compliance guides, and core banking comparison matrices.',
    'deep_dive_2': 'Every programmatic route compiles static edge HTML on Next.js App Router with Incremental Static Regeneration, delivering instant page loads and zero layout shift. Inbound demo requests dispatch encrypted webhooks directly into institutional CRM pipelines with complete lead attribution.',
    'pain_points': [
        {'title': 'Prohibitive Financial Search CPC Bidding Wars', 'description': 'Bidding on commercial fintech search terms pushes acquisition costs over sustainable payback thresholds.', 'impact': 'Depressed gross margins and excessive marketing capital burn.'},
        {'title': 'Regulatory Compliance Disclaimers Across Static Pages', 'description': 'Maintaining strict financial disclosures across hundreds of landing pages manually invites regulatory audit non-compliance.', 'impact': 'Exposure to statutory penalties and loss of institutional banking partner accreditation.'},
        {'title': 'Slow Manual Content Production Cycles', 'description': 'Marketing teams spend months authoring individual comparison guides while competitor platforms dominate high-intent organic search real estate.', 'impact': 'Lost organic search authority and stalled inbound pipeline generation.'}
    ],
    'capabilities': [
        {'title': 'FinTech Taxonomy & Banking Rail Keyword Matrix', 'spec': 'Structured database tables mapping 120+ payment gateways, core banking APIs, and financial software comparisons.', 'deliverable': 'Comprehensive JSON taxonomy matrix targeting commercial banking search intent.'},
        {'title': 'Next.js App Router Edge Compilation', 'spec': 'Server-rendered static templates delivering sub-40ms TTFB and 99+ Core Web Vitals across all financial routes.', 'deliverable': 'Production edge repository with automated static export and zero layout shift.'},
        {'title': 'Automated Financial Services Schema.org JSON-LD', 'spec': 'Deeply nested ProfessionalService, Organization, FAQPage, and BreadcrumbList structured data.', 'deliverable': 'Schema markup passing Google Rich Results tests with zero warnings or errors.'},
        {'title': 'Chunked XML Sitemaps with Automated Search Console Pings', 'spec': 'Automated sitemap index and 5,000-URL chunked files with dynamic lastmod timestamps and GSC pings.', 'deliverable': 'Continuous indexation pipeline submitting new pages immediately upon generation.'}
    ],
    'phases': [
        {'title': 'FinTech Taxonomy & Search Intent Extraction', 'desc': 'Map core banking APIs, regulatory terms, and competitor alternatives.', 'tf': 'Days 1 - 3'},
        {'title': 'Next.js Financial Template & Schema Design', 'desc': 'Construct responsive Next.js dynamic routes with Tailwind CSS and JSON-LD microdata.', 'tf:': 'Days 4 - 7'},
        {'title': 'Regulatory Compliance & Uniqueness Assertion', 'desc': 'Execute automated uniqueness checks, buzzword blacklist scans, and schema tests.', 'tf': 'Days 8 - 10'},
        {'title': 'Edge Deployment & Automated Indexation', 'desc': 'Deploy static assets to Cloudflare Pages and trigger GSC and IndexNow sitemap ping routines.', 'tf': 'Days 11 - 14'}
    ],
    'faqs': [
        {'q': 'How does programmatic SEO integrate with existing FinTech domains?', 'a': 'We engineer modular Next.js route handlers that mount under /solutions or /compare without modifying core banking applications.'},
        {'q': 'How do you guarantee regulatory accuracy across hundreds of generated pages?', 'a': 'Every page data record is validated against strict JSON Schemas with deterministic fallback rules and domain assertion gates.'},
        {'q': 'Can demo request forms connect directly with our CRM?', 'a': 'Yes. Inbound demo requests and consultation forms dispatch encrypted webhooks directly into Salesforce or HubSpot.'},
        {'q': 'What payback period can FinTech leadership expect from organic search?', 'a': 'Our programmatic deployments typically achieve sub-45 day customer payback on initial cohorts, outperforming paid search ad channels.'},
        {'q': 'Who owns the generated code, templates, and taxonomy data?', 'a': 'Your organization retains 100% full intellectual property rights to the compiled Next.js components, automation scripts, and database matrices.'}
    ],
    'humanSolutions': {
        'businessTitle': 'Ending the $75/Click CPC Treadmill & Regulatory Lead Decay for FinTech',
        'businessStory': 'FinTech platforms get trapped spending tens of thousands on Google Ads for software integration terms where paid CPC exceeds $75 per click. When ad budgets pause, demo volume evaporates. Meanwhile, competitors dominate organic search for long-tail core banking integration queries.',
        'businessPillars': [
            {'title': 'Programmatic Organic Lead Pipeline', 'desc': 'Deploys hundreds of comparison, integration, and alternative routes on Next.js edge caching, capturing high-intent financial software buyers.', 'product': 'pSEO Engine & AI Lead Generation ($297/mo)'},
            {'title': 'Social Intent Prospect Radar', 'desc': 'Monitors real-time discussions across online forums for software pain points regarding payment gateways, piping pre-qualified buyers directly to sales reps.', 'product': 'Scout Intent Radar & Outreach Pipeline'},
            {'title': 'Daily Thought Leadership Omnipresence', 'desc': 'Establishes founder and brand authority on autopilot with 30 to 60 high-signal posts per month formatted for LinkedIn and X.', 'product': 'AI Content Automation ($197/mo)'}
        ],
        'personalTitle': 'Protecting FinTech Founders from Regulatory Anxiety & Midnight Burnout',
        'personalStory': 'FinTech founders juggle capital adequacy ratios, banking audits, and investor updates while worrying about volatile customer acquisition channels. The sheer cognitive load leads to chronic insomnia and decision fatigue.',
        'personalPillars': [
            {'icon': '🛡️', 'title': 'Inbox Anxiety & Audit Escalations', 'desc': 'Demanding partners and auditors send tense emails. InboxCalm scores toxicity, quarantines trigger phrases, and drafts calm de-escalating replies instantly.', 'product': 'InboxCalm (Automated Email Firewall)', 'url': 'https://inboxcalm.adorisedigital.com'},
            {'icon': '🎬', 'title': 'FinTech Product Demo Video Fatigue', 'desc': 'Cutting technical product updates into vertical shorts for social media is exhausting. ClipCalm AI generates viral 9:16 clips automatically.', 'product': 'ClipCalm AI (Viral Video Repurposing)', 'url': 'https://clipcalm.adorisedigital.com'},
            {'icon': '🕊️', 'title': 'Founder Decision Overload & Solitude', 'desc': 'When banking audit pressure and sprint deadlines feel overwhelming, DearMee provides a private conversational co-pilot for emotional grounding.', 'product': 'DearMee AI (Empathetic Companion)', 'url': 'https://dearmee.adorisedigital.com'}
        ]
    }
}

# Verify clean
for k, v in data.items():
    check_clean(json.dumps(v), k)

print(f"Part 1 ready with {len(data)} combinations.")
with open('pseo-engine/data/curated_part1.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
