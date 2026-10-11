import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VC_PATH = os.path.join(SCRIPT_DIR, 'data_vc_pe.py')
LEGAL_PATH = os.path.join(SCRIPT_DIR, 'data_legaltech.py')

with open(VC_PATH, 'r', encoding='utf-8') as f:
    vc_code = f.read()
import data_vc_pe
vc_data = data_vc_pe.DATA

with open(LEGAL_PATH, 'r', encoding='utf-8') as f:
    legal_code = f.read()
import data_legaltech
legal_data = data_legaltech.DATA

# 1. Differentiate VC/PE Whop Human Solutions & Deep Dives
vc_whop = vc_data['venture-capital-private-equity/whop-monetization']
vc_whop['deep_dive_1'] = 'Running private angel syndicates, co-investment clubs, and emerging manager networks through manual bank wires and informal chat channels creates severe operational bottlenecks. Fund sponsors require automated subscription billing, immediate allocation room gating, and synchronized LP roster access.'
vc_whop['deep_dive_2'] = 'Our team engineers private capital monetization platforms powered by Whop API v2. Whop handles multi-tier membership dues, corporate card charges, and automated credential dispatching. Edge webhook handlers synchronize investor access tiers in real time, granting subscribers instant entry to private deal allocation vaults, gated angel discussion forums, and downloadable sector intelligence memos.'
vc_whop['humanSolutions'] = {
    'businessTitle': 'Capital Allocation Portals Engineered for Modern General Partners',
    'businessStory': 'Leading venture capitalists and angel syndicate leads shouldn\'t waste precious dealmaking hours on tedious dues reconciliation or manual wire follow-ups. We engineer frictionless investor membership portals that automate capital calls, subscription renewals, and co-investment access while maintaining absolute deal confidentiality.',
    'businessPillars': [
        {
            'title': 'One-Touch Accredited LP Onboarding',
            'desc': 'Seamless subscription onboarding with identity validation hooks and instant deal room entry.',
            'product': 'AI Content Automation ($197/mo)'
        },
        {
            'title': 'Automated SPV Carry & Dues Protection',
            'desc': 'Enforces continuous membership validation before distributing allocations or pitch decks.',
            'product': 'AI Automation Suite ($497/mo)'
        },
        {
            'title': 'Smart Corporate Wire & Card Recovery',
            'desc': 'Proactively resolves declined institutional payment cards and tracks corporate dues.',
            'product': 'AI Lead Generation ($297/mo)'
        }
    ],
    'personalTitle': 'Shielding Fund Managers from Operational Fatigue and Diligence Burnout',
    'personalStory': 'Managing partners should concentrate on scouting unicorn founders and negotiating term sheets, not wrestling with administrative billing spreadsheets or answering late-night invoice inquiries from limited partners.',
    'personalPillars': [
        {
            'icon': '🛡️',
            'title': 'Demanding LP Invoicing Demands',
            'desc': 'When institutional investors submit urgent accounting inquiries, InboxCalm drafts clear, professional replies.',
            'product': 'InboxCalm (Automated Email Firewall)',
            'url': 'https://inboxcalm.adorisedigital.com'
        },
        {
            'icon': '🎬',
            'title': 'Portfolio Founder Spotlight Videos',
            'desc': 'Converts technical venture memos into captivating vertical video showcases for LP updates.',
            'product': 'ClipCalm AI (Viral Video Repurposing)',
            'url': 'https://clipcalm.adorisedigital.com'
        },
        {
            'icon': '🕊️',
            'title': 'The Psychological Pressure of Fund Performance',
            'desc': 'Provides a safe, confidential conversational space for fund managers to process market volatility and reset.',
            'product': 'DearMee AI (Empathetic Companion)',
            'url': 'https://dearmee.adorisedigital.com'
        }
    ]
}

# 2. Differentiate VC/PE Cloud VPS Hardening Human Solutions & Deep Dives
vc_vps = vc_data['venture-capital-private-equity/cloud-vps-hardening']
vc_vps['deep_dive_1'] = 'Hosting virtual data rooms, proprietary cap table models, and confidential investment committee evaluations on standard cloud instances leaves investment funds exposed to corporate espionage, credential stuffing, and sudden server downtime during critical transaction closings.'
vc_vps['deep_dive_2'] = 'Our technical team establishes a zero-trust cryptographic defense around your diligence infrastructure. Outbound-only Cloudflare Zero Trust tunnels shut down every public inbound listening port. Internal diligence containers run inside unprivileged Linux namespaces with immutable root filesystems, while automated scripts archive hourly encrypted snapshots to off-site cloud vaults.'
vc_vps['humanSolutions'] = {
    'businessTitle': 'Protecting High-Stakes M&A Diligence Rooms from Espionage',
    'businessStory': 'When private equity sponsors evaluate eight-figure buyouts, confidential financial models and executive background checks become prime targets for malicious hackers. We deploy air-tight cloud server perimeters that hide origin servers completely, ensuring sensitive transaction data remains strictly between deal principals.',
    'businessPillars': [
        {
            'title': 'Dark Server Architecture with Zero Open Ports',
            'desc': 'Cloaks deal room servers completely from internet scanners using outbound-only encrypted tunnels.',
            'product': 'Cloud Infrastructure Hardening'
        },
        {
            'title': 'FIDO2 Hardware Key Enforced Access',
            'desc': 'Mandates cryptographic physical security tokens for all administrative interactions.',
            'product': 'Production Architecture Retainer'
        },
        {
            'title': 'Immutable M&A Data Room Journaling',
            'desc': 'Creates tamper-evident, encrypted archives of all diligence documents with verifiable audit trails.',
            'product': 'AI Automation Suite ($497/mo)'
        }
    ],
    'personalTitle': 'Ending the Anxiety of Diligence Data Leaks During Major Transactions',
    'personalStory': 'Deal principals and investment committee members shoulder intense reputational risks during live mergers and acquisitions. Our hardened infrastructure ensures your sensitive valuation spreadsheets never fall into the wrong hands.',
    'personalPillars': [
        {
            'icon': '🛡️',
            'title': 'Urgent Security Inquiries from Portfolio Boards',
            'desc': 'When corporate board members raise cybersecurity concerns, InboxCalm drafts thorough, authoritative compliance replies.',
            'product': 'InboxCalm (Automated Email Firewall)',
            'url': 'https://inboxcalm.adorisedigital.com'
        },
        {
            'icon': '🎬',
            'title': 'Zero-Trust Diligence Architecture Briefings',
            'desc': 'Translates complex cryptographic protocols into polished executive video summaries for LP advisory committees.',
            'product': 'ClipCalm AI (Viral Video Repurposing)',
            'url': 'https://clipcalm.adorisedigital.com'
        },
        {
            'icon': '🕊️',
            'title': 'The Relentless Pressure of High-Stakes Closings',
            'desc': 'Offers an empathetic, private outlet for partners to decompress from intense negotiation marathons and regain mental clarity.',
            'product': 'DearMee AI (Empathetic Companion)',
            'url': 'https://dearmee.adorisedigital.com'
        }
    ]
}

# 3. Differentiate LegalTech Cloud VPS Hardening Human Solutions & Deep Dives
legal_vps = legal_data['legaltech-professional/cloud-vps-hardening']
legal_vps['deep_dive_1'] = 'Storing sensitive attorney work product, privileged client disclosures, and discovery databases on standard cloud virtual machines with open ports leaves law practices vulnerable to devastating cyber-extortion, regulatory reprimands, and ethical wall breaches.'
legal_vps['deep_dive_2'] = 'We engineer a zero-trust cryptographic barrier defending your law practice servers. By routing all external requests through Cloudflare Zero Trust tunnels, every public listening port is permanently closed. Matter OCR daemons run in isolated unprivileged containers, while automated cron jobs encrypt case databases hourly using GPG public keys.'
legal_vps['humanSolutions'] = {
    'businessTitle': 'Fortifying Law Firm Digital Vaults Against Hostile Intruders',
    'businessStory': 'Managing partners and litigation chairs cannot risk client confidences leaking to digital adversaries or ransomware syndicates. Our zero-trust server hardening wraps your practice management systems, case transcripts, and billing ledgers in a private cryptographic shell that closes all public entryways.',
    'businessPillars': [
        {
            'title': 'Impenetrable Zero-Exposure Perimeter',
            'desc': 'Drops all external internet probes by terminating connections at private Cloudflare edge enclaves.',
            'product': 'Cloud Infrastructure Hardening'
        },
        {
            'title': 'Tamper-Proof Case Evidence Storage',
            'desc': 'Isolates deposition audio, scanned exhibits, and litigation hold files on encrypted volumes.',
            'product': 'Production Architecture Retainer'
        },
        {
            'title': 'Disaster-Resilient Matter Restoration',
            'desc': 'Streams continuous cryptographic database journals to cold storage for instant point-in-time recovery.',
            'product': 'AI Automation Suite ($497/mo)'
        }
    ],
    'personalTitle': 'Protecting Legal Partners from 3:00 AM Cybersecurity Panic',
    'personalStory': 'The weight of personal liability and state bar discipline keeps legal partners awake at night worrying about digital espionage. Our hardened server enclave gives you unwavering confidence in your firm\'s confidentiality.',
    'personalPillars': [
        {
            'icon': '🛡️',
            'title': 'Demanding General Counsel Security Inquiries',
            'desc': 'When corporate clients demand proof of cybersecurity safeguards, InboxCalm drafts clear, authoritative compliance memos.',
            'product': 'InboxCalm (Automated Email Firewall)',
            'url': 'https://inboxcalm.adorisedigital.com'
        },
        {
            'icon': '🎬',
            'title': 'Ethical Wall Security Video Briefings',
            'desc': 'Turns complex technical security architecture into polished vertical video summaries for firm executive committees.',
            'product': 'ClipCalm AI (Viral Video Repurposing)',
            'url': 'https://clipcalm.adorisedigital.com'
        },
        {
            'icon': '🕊️',
            'title': 'The Mental Exhaustion of Trial Deadlines',
            'desc': 'Provides a safe, confidential space for trial lawyers to decompress from intense courtroom battles and reset.',
            'product': 'DearMee AI (Empathetic Companion)',
            'url': 'https://dearmee.adorisedigital.com'
        }
    ]
}

# Write back both files cleanly
with open(VC_PATH, 'w', encoding='utf-8') as f:
    f.write('"""\nVenture Capital & Private Equity Firms - Bespoke Data\n"""\nimport json\n\nDATA = ')
    json.dump(vc_data, f, indent=4)
    f.write('\n')

with open(LEGAL_PATH, 'w', encoding='utf-8') as f:
    f.write('"""\nLegalTech & High-Ticket Professional Services - Bespoke Data\n"""\nimport json\n\nDATA = ')
    json.dump(legal_data, f, indent=4)
    f.write('\n')

print("Successfully updated VC/PE and LegalTech bespoke sections!")
