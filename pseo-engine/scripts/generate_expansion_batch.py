import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

SOLUTIONS_DIR = r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\solutions"
SOLUTIONS_DATA_FILE = r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\solutions_data.json"
SITEMAP_FILE = r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\sitemaps\sitemap-1.xml"

# Definition of the 10 new pages across the 2 requested industries
PAGES_CONFIG = [
    # --- LOGISTICS & SUPPLY CHAIN ---
    {
        "type": "hub",
        "industry": "Logistics & Supply Chain Automation",
        "industry_slug": "logistics-supply-chain",
        "rel_path": "logistics-supply-chain/index.html",
        "url": "/solutions/logistics-supply-chain/",
        "title": "Logistics & Supply Chain AI & Automation Solutions | Adorise Digital",
        "description": "Deploy custom autonomous AI dispatch agents, programmatic freight SEO systems, and TMS/WMS integrations for Logistics & Supply Chain operators.",
        "h1": "Autonomous Systems Engineered for Logistics & Supply Chain Operators",
        "subheadline": "Enterprise digital architectures built to eliminate manual dispatch bottlenecks, track exceptions in real time, and scale freight brokerage margins.",
        "capabilities_list": [
            ("Autonomous AI Agents", "ai-agents", "Automated carrier rate negotiation, bill of lading OCR extraction, and real-time shipment exception tracking."),
            ("Cold Outbound & Freight Pipeline", "outbound-infrastructure", "Multi-channel intent scraping targeting high-volume shippers, manufacturers, and enterprise logistics directors."),
            ("Programmatic SEO Engine", "pseo-engine", "Automated search scaling targeting freight lane rates, 3PL warehousing locations, and intermodal transport keywords."),
            ("Composio TMS/WMS Integrations", "composio-integrations", "Connect autonomous logistics agents directly into McLeod, MercuryGate, Samsara, and SAP Transportation Management.")
        ]
    },
    {
        "type": "detail",
        "industry": "Logistics & Supply Chain",
        "industry_slug": "logistics-supply-chain",
        "capability": "Ai Agents",
        "capability_slug": "ai-agents",
        "rel_path": "logistics-supply-chain/ai-agents/index.html",
        "url": "/solutions/logistics-supply-chain/ai-agents/",
        "title": "Autonomous AI Agents for Logistics & Supply Chain | Adorise Digital",
        "description": "Deploy autonomous AI agents that handle carrier dispatch, load exception tracking, and automated bill of lading processing 24/7.",
        "h1": "Autonomous AI Dispatch & Exception Agents for Logistics",
        "subheadline": "Eliminate 80% of dispatch coordination phone calls and manual check-ins. Autonomous AI agent squads that parse rate confirmations, verify carrier insurance, and resolve shipment exceptions 24/7.",
        "metrics": [
            ("< 480ms", "Dispatch Response", "Instant carrier rate and quote confirmation"),
            ("-72%", "Manual Check-in Calls", "Automated ELD & telemetry tracking updates"),
            ("100%", "BOL Parsing Accuracy", "Deterministic LLM OCR document extraction"),
            ("$45k/mo", "Broker Margin Saved", "Average operational headcount cost reduction")
        ],
        "pain_points": [
            ("Overwhelming Manual Dispatch & Rate Confirmation Delays", "Brokers spend 4+ hours daily answering carrier inquiries, negotiating spot rates, and validating certificates of insurance.", "Lost loads to faster digital freight brokers and margin compression."),
            ("Unmonitored Transit Exceptions Triggering Customer Churn", "Shipment delays or detention fee disputes go undetected until enterprise shippers complain.", "Contractual penalty chargebacks and churned enterprise shipper accounts."),
            ("Fragmented Communication Across Telematics & WMS", "Data trapped across Samsara, McLeod, and carrier portal silos requiring constant human copy-pasting.", "High dispatch overhead and human error in load tender acknowledgments.")
        ],
        "capabilities": [
            ("Autonomous Freight Spot Rate Negotiator", "LLM-driven negotiation engine integrated with DAT and Truckstop rate benchmarks to lock loads within margin thresholds.", "Autonomous spot freight negotiation workflow with broker approval gates."),
            ("Real-Time Exception Detection & Telemetry Sentinel", "WebRTC & GPS webhook monitoring that detects dwell time deviations and alerts dispatchers before detention penalties accrue.", "Automated driver detention alert and exception routing engine."),
            ("Deterministic Bill of Lading & POD Parser", "Vision-LLM OCR pipeline that extracts commodity weights, consignee stamps, and signatures directly into accounting.", "Instant POD verification microservice with zero manual document data entry.")
        ],
        "whop": {
            "badge": "Logistics Autonomous Tier",
            "title": "Autonomous Logistics AI Dispatch Engine",
            "price": "$797 / month",
            "intentCluster": "Logistics AI Agents & Freight Dispatch Automation",
            "ctaText": "Deploy Logistics Agent Squad",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    },
    {
        "type": "detail",
        "industry": "Logistics & Supply Chain",
        "industry_slug": "logistics-supply-chain",
        "capability": "Outbound Infrastructure",
        "capability_slug": "outbound-infrastructure",
        "rel_path": "logistics-supply-chain/outbound-infrastructure/index.html",
        "url": "/solutions/logistics-supply-chain/outbound-infrastructure/",
        "title": "Cold Outbound & Freight Pipeline for Logistics | Adorise Digital",
        "description": "High-deliverability cold outbound pipeline filling 3PL and freight brokerage sales calendars with enterprise shippers and supply chain directors.",
        "h1": "Enterprise Shipper Outbound & Freight Pipeline Engine",
        "subheadline": "Target high-volume commercial shippers, manufacturers, and import/export directors. Multi-inbox rotation and AI-personalized outreach that books qualified RFP freight meetings on autopilot.",
        "metrics": [
            ("1,500+", "Shipper Touches/Mo", "Multi-inbox rotating outbound sequence"),
            ("68.4%", "Average Open Rate", "Dedicated domain warmup & secondary domain isolation"),
            ("18-25", "Monthly Shipper RFPs", "Direct conversations with verified logistics buyers"),
            ("0% Bounce", "Guaranteed Deliverability", "Real-time SMTP handshake and MX verification")
        ],
        "pain_points": [
            ("Reliance on Cold Calling Saturated Carrier & Shipper Lists", "Freight brokers burning out cold-calling gatekeepers on outdated lists with 95% rejection rates.", "High sales team turnover and high customer acquisition costs."),
            ("Primary Email Domain Blacklisting", "Sending cold freight proposals from corporate root domains, triggering spam filters and landing in junk folders.", "Lost corporate credibility and ruined email domain reputation."),
            ("Inconsistent Pipeline Leading to Brokerage Revenue Droughts", "Feast-or-famine cycles where brokers stop prospecting during heavy dispatch periods.", "Volatile quarterly revenue and missed growth milestones.")
        ],
        "capabilities": [
            ("Multi-Domain High-Deliverability Sending Grid", "Isolated secondary domains configured with custom SPF, DKIM, DMARC, and automated 21-day algorithmic warmup.", "Bulletproof email infrastructure ensuring 99%+ inbox placement."),
            ("B2B Shipper Intent & Freight Volume Scraper", "Scrapes import/export bills of lading, corporate registry expansions, and warehouse leasing records for buyer intent.", "Targeted list of commercial shippers with active freight budget."),
            ("Dynamic Lane & Capacity Personalization", "AI sequence compiler tailoring every outreach email with specific freight lanes, equipment types (Dry Van, Reefer, Flatbed), and real-time capacity.", "Hyper-relevant cold outreach converting shippers at 3x industry baseline.")
        ],
        "whop": {
            "badge": "Freight Pipeline Tier",
            "title": "Autonomous Freight Outbound Engine",
            "price": "$497 / month",
            "intentCluster": "Logistics Outbound & Freight Broker Lead Generation",
            "ctaText": "Deploy Freight Outbound Engine",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    },
    {
        "type": "detail",
        "industry": "Logistics & Supply Chain",
        "industry_slug": "logistics-supply-chain",
        "capability": "Pseo Engine",
        "capability_slug": "pseo-engine",
        "rel_path": "logistics-supply-chain/pseo-engine/index.html",
        "url": "/solutions/logistics-supply-chain/pseo-engine/",
        "title": "Programmatic SEO Engine for Logistics & 3PL Warehousing | Adorise Digital",
        "description": "Capture commercial intent search volume for hundreds of freight shipping lanes, cold storage locations, and 3PL warehousing corridors.",
        "h1": "Programmatic SEO Engine for Freight & 3PL Logistics",
        "subheadline": "Dominate search rankings across 500+ freight shipping corridors, specialized Reefer lanes, and regional warehousing hubs. Programmatic edge landing pages generating organic shipper quote inquiries.",
        "metrics": [
            ("500+", "Indexed Shipping Lanes", "Programmatic city-to-city freight routes"),
            ("< 42ms", "Edge TTFB", "Cloudflare edge SSR with zero layout shift"),
            ("+410%", "Organic Quote Requests", "Direct freight rate requests from commercial shippers"),
            ("100%", "Schema.org Logistics", "Service & Organization rich results compliance")
        ],
        "pain_points": [
            ("Prohibitive Paid Search Cost on Freight Keywords", "Google Ads click costs for '3PL warehousing Dallas' or 'freight broker Chicago' exceed $45 per click.", "Eroded profit margins and unsustainable digital ad spend."),
            ("Static Websites Missing Local & Lane-Specific Searches", "Logistics websites with only 5 static pages missing thousands of localized shipping lane queries.", "Invisibility to shippers searching specific transport routes."),
            ("Shallow Generic Content Penalized by Search Algorithms", "Generic blog posts about 'supply chain trends' generating zero qualified shipper leads.", "Wasted marketing budget with no measurable inbound ROI.")
        ],
        "capabilities": [
            ("City-Pair Freight Lane Combinatorial Matrix", "Automated matrix mapping origin-destination freight corridors across 100 major North American industrial hubs.", "Comprehensive structured taxonomy database of commercial shipping lanes."),
            ("Dynamic Rate Calculator & Quote Lead Capture", "Client-side interactive freight quote calculator capturing freight weight, equipment type, and shipper contact.", "High-converting lane-specific lead capture mechanism."),
            ("Automated Logistics Schema & Breadcrumb Markup", "Deeply nested Schema.org microdata asserting service availability, operating hours, and warehouse capacity.", "Search result snippets displaying verified service capabilities.")
        ],
        "whop": {
            "badge": "Logistics pSEO Tier",
            "title": "Freight Programmatic SEO Engine",
            "price": "$497 / month",
            "intentCluster": "Logistics Programmatic SEO & Freight Inbound",
            "ctaText": "Deploy Freight pSEO Engine",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    },
    {
        "type": "detail",
        "industry": "Logistics & Supply Chain",
        "industry_slug": "logistics-supply-chain",
        "capability": "Composio Integrations",
        "capability_slug": "composio-integrations",
        "rel_path": "logistics-supply-chain/composio-integrations/index.html",
        "url": "/solutions/logistics-supply-chain/composio-integrations/",
        "title": "Composio TMS & WMS Integrations for Logistics | Adorise Digital",
        "description": "Connect autonomous AI agents directly to McLeod, MercuryGate, Samsara, and SAP ERP with hardened Composio API tool calling.",
        "h1": "Composio TMS, WMS & Carrier API Integrations",
        "subheadline": "Give your autonomous logistics agents direct read/write access to TMS databases, ELD telematics, and EDI messaging systems with battle-tested OAuth callbacks and secure sandboxes.",
        "metrics": [
            ("250+", "Native Tool APIs", "Pre-built connectors for ERP, TMS, and CRM"),
            ("< 350ms", "Webhook Latency", "Sub-second execution across cloud transport APIs"),
            ("SOC2", "Compliant Execution", "Encrypted token storage and audit logging"),
            ("0", "Manual Data Re-Entry", "End-to-end sync between dispatch and accounting")
        ],
        "pain_points": [
            ("Brittle Custom API Scripts Constantly Breaking", "In-house Python scripts break every time carrier APIs or TMS webhooks update schema.", "Dispatch delays and critical shipment data dropped silently."),
            ("Manual Data Entry Between WMS and Customer Portals", "Operators re-keying inventory counts and tracking numbers across disparate software systems.", "Fatigue-induced errors and costly misrouted shipments."),
            ("Inability of AI Agents to Take Real Operational Action", "AI chat tools that only answer questions but cannot update shipment status or generate BOL PDFs.", "Zero labor savings from superficial chatbot implementations.")
        ],
        "capabilities": [
            ("Hardened Composio Execution Environment", "Containerized runtime executing authenticated API actions with rate-limit handling and automatic retries.", "Resilient API integration layer for enterprise logistics stacks."),
            ("Bi-Directional EDI & Webhook Normalizer", "Translates legacy EDI 204, 214, and 210 formats into modern JSON payloads for LLM processing.", "Universal data bridge connecting legacy freight systems with modern AI."),
            ("Role-Based Action Permission Gateways", "Strict authorization gates requiring supervisor approval for freight adjustments exceeding specified dollar amounts.", "Enterprise governance ensuring AI agents operate within defined risk parameters.")
        ],
        "whop": {
            "badge": "Integrations Tier",
            "title": "Logistics Composio Integration Architecture",
            "price": "$497 / month",
            "intentCluster": "Logistics API Integrations & TMS Automation",
            "ctaText": "Deploy Logistics Integrations",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    },

    # --- MANUFACTURING & INDUSTRIAL OPERATIONS ---
    {
        "type": "hub",
        "industry": "Manufacturing & Industrial Operations",
        "industry_slug": "manufacturing-industrial",
        "rel_path": "manufacturing-industrial/index.html",
        "url": "/solutions/manufacturing-industrial/",
        "title": "Manufacturing & Industrial AI & Automation Solutions | Adorise Digital",
        "description": "Deploy custom autonomous AI agents, contract manufacturing outbound pipelines, and IoT ERP integrations for Manufacturing & Industrial plants.",
        "h1": "Autonomous Systems Engineered for Manufacturing & Industrial Leaders",
        "subheadline": "Enterprise digital architectures built to prevent unplanned downtime, streamline OEM quotation workflows, and scale high-value contract manufacturing pipelines.",
        "capabilities_list": [
            ("Autonomous AI Agents", "ai-agents", "Predictive maintenance anomaly detection, automated CAD/drawing RFQ extraction, and plant floor shift log processing."),
            ("B2B Contract Manufacturing Pipeline", "outbound-infrastructure", "Multi-channel intent scraping targeting procurement officers, VP of Supply Chain, and industrial OEM buyers."),
            ("Programmatic SEO Engine", "pseo-engine", "Automated search scaling targeting precision CNC machining, custom stamping, and industrial equipment specification searches."),
            ("Composio Industrial IoT & ERP", "composio-integrations", "Connect autonomous industrial agents directly into SAP, NetSuite, Rockwell, and Siemens PLC telemetry streams.")
        ]
    },
    {
        "type": "detail",
        "industry": "Manufacturing & Industrial",
        "industry_slug": "manufacturing-industrial",
        "capability": "Ai Agents",
        "capability_slug": "ai-agents",
        "rel_path": "manufacturing-industrial/ai-agents/index.html",
        "url": "/solutions/manufacturing-industrial/ai-agents/",
        "title": "Autonomous AI Agents for Manufacturing & Industrial Operations | Adorise Digital",
        "description": "Deploy autonomous AI agents that analyze plant floor IoT telemetry, parse engineering drawings for RFQs, and optimize machine uptime 24/7.",
        "h1": "Autonomous Plant Floor & Predictive Maintenance AI Agents",
        "subheadline": "Eliminate unplanned downtime and manual RFQ engineering reviews. Autonomous AI agent squads that monitor PLC vibration data, extract CAD specs for estimation, and audit supplier quality in real time.",
        "metrics": [
            ("-42%", "Unplanned Downtime", "Early vibration & acoustic anomaly detection"),
            ("< 12m", "RFQ Estimation Time", "Reduced from 4 days of engineering manual review"),
            ("99.4%", "Quality Audit Accuracy", "Automated vision inspection & defect classification"),
            ("$120k+", "Annual Spares Savings", "Just-in-time predictive component replacement")
        ],
        "pain_points": [
            ("Costly Unplanned Machine Breakdowns & Emergency Repairs", "Critical CNC spindles and extrusion motors failing unexpectedly, halting assembly lines at thousands of dollars per hour.", "Severe production schedule slippage and expedited freight penalties."),
            ("Engineering Capacity Bottlenecked on Manual RFQ Quotations", "Senior manufacturing engineers spend 30% of their week calculating material costs and tolerances from customer 2D PDFs.", "Slow quote turnaround resulting in lost contracts to offshore competitors."),
            ("Tribal Knowledge Trapped in Aging Operator Heads", "Veteran maintenance technicians retiring without standardized digital SOPs or diagnostic documentation.", "Lengthened machine repair cycles and inconsistent shift handovers.")
        ],
        "capabilities": [
            ("Autonomous Telemetry Sentinel & Anomaly Engine", "Continuous ingestion of SCADA and PLC sensor feeds flagging thermal and bearing degradation patterns before mechanical seizure.", "Real-time predictive maintenance alerting engine with automated work order creation."),
            ("CAD/PDF Drawing Estimator & Tolerance Parser", "Vision-LLM engine that ingests engineering blueprints, calculates cycle times, bill of materials, and surface treatments.", "Automated manufacturing quote generation pipeline with engineer sign-off."),
            ("Autonomous Shift Handover & Diagnostic Copilot", "Natural language knowledge retrieval agent indexed against machine manuals, historic repair logs, and OEM schematics.", "Floor technician tablet assistant for instant field troubleshooting.")
        ],
        "whop": {
            "badge": "Industrial AI Tier",
            "title": "Autonomous Manufacturing AI Operations Suite",
            "price": "$997 / month",
            "intentCluster": "Manufacturing AI Agents & Predictive Maintenance",
            "ctaText": "Deploy Industrial AI Suite",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    },
    {
        "type": "detail",
        "industry": "Manufacturing & Industrial",
        "industry_slug": "manufacturing-industrial",
        "capability": "Outbound Infrastructure",
        "capability_slug": "outbound-infrastructure",
        "rel_path": "manufacturing-industrial/outbound-infrastructure/index.html",
        "url": "/solutions/manufacturing-industrial/outbound-infrastructure/",
        "title": "B2B Contract Manufacturing Outbound Pipeline | Adorise Digital",
        "description": "Fill machine capacity with high-margin contract manufacturing orders. Automated outbound engine targeting VP of Procurement and OEM engineering buyers.",
        "h1": "B2B Contract Manufacturing & OEM Outbound Pipeline",
        "subheadline": "End reliance on word-of-mouth and trade shows. Multi-inbox cold outbound infrastructure targeting procurement directors, VP of Supply Chain, and industrial OEMs needing manufacturing capacity.",
        "metrics": [
            ("1,500+", "Targeted Procurement Touches", "Monthly sequence to verified OEM buyers"),
            ("12-18", "Commercial RFQs/Mo", "Direct RFQ inquiries with CAD specifications"),
            ("64.2%", "Open Rate", "Dedicated domain warmup & technical credibility positioning"),
            ("$250k+", "Average Deal Size", "Targeted at recurring commercial OEM production runs")
        ],
        "pain_points": [
            ("Expensive Trade Shows with Low Attributable ROI", "Spending $30k+ on annual manufacturing expos yielding business cards that never convert into production runs.", "High customer acquisition costs with zero predictability."),
            ("Idle Spindle & Machine Capacity Eating Margins", "Multi-million dollar CNC machines and injection molding lines sitting idle between project cycles.", "Fixed overhead carrying costs depressing company EBITDA."),
            ("Gatekeeper Friction Reaching Corporate Procurement Heads", "Sales reps unable to get past front desks to reach the VP of Global Sourcing.", "Inability to present factory capabilities to tier-1 enterprise buyers.")
        ],
        "capabilities": [
            ("OEM Intent & Production Relocation Scraper", "Tracks corporate reshoring announcements, capital expenditure filings, and tariff impact news to identify companies seeking domestic manufacturing.", "Verified list of procurement decision-makers with active RFQ requirements."),
            ("Technical Capability-Focused Personalization", "Sequences tailored to specific engineering capabilities (5-axis machining, ISO 9001/AS9100 certifications, cleanroom assembly) rather than generic pitches.", "High-authority technical messaging resonating with senior engineering heads."),
            ("Multi-Inbox Deliverability & Warmup Cluster", "10 secondary domains configured with custom DNS records and gradual volume scaling ensuring primary inbox delivery.", "Protected corporate domain reputation with guaranteed enterprise delivery.")
        ],
        "whop": {
            "badge": "Contract Manufacturing Tier",
            "title": "Industrial OEM Outbound Pipeline",
            "price": "$797 / month",
            "intentCluster": "Contract Manufacturing Outbound & OEM Sourcing",
            "ctaText": "Deploy Manufacturing Outbound",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    },
    {
        "type": "detail",
        "industry": "Manufacturing & Industrial",
        "industry_slug": "manufacturing-industrial",
        "capability": "Pseo Engine",
        "capability_slug": "pseo-engine",
        "rel_path": "manufacturing-industrial/pseo-engine/index.html",
        "url": "/solutions/manufacturing-industrial/pseo-engine/",
        "title": "Programmatic SEO Engine for Industrial Equipment & CNC Parts | Adorise Digital",
        "description": "Capture industrial engineers and buyers searching for specific material grades, CNC tolerances, and custom manufactured components.",
        "h1": "Programmatic SEO Engine for Industrial Equipment & OEM Parts",
        "subheadline": "Dominate search rankings across 600+ industrial material specifications, custom CNC machining capabilities, and replacement part numbers. Edge landing pages converting technical searchers into qualified RFQs.",
        "metrics": [
            ("600+", "Indexed Part & Material Pages", "Covering metals, polymers, and tolerance standards"),
            ("< 38ms", "Edge TTFB", "Sub-second technical specification page loading"),
            ("+380%", "Engineering Drawing Uploads", "Direct CAD file submissions from organic search"),
            ("100%", "Schema Product & Service", "Full compliance with technical specification rich results")
        ],
        "pain_points": [
            ("Competitors Winning High-Margin Long-Tail Part Inquiries", "Buyers searching for specific alloy specifications (e.g., 'Inconel 718 5-axis machining') landing on competitor websites.", "Lost high-margin specialized production orders."),
            ("Traditional Agency Inability to Write Technical Industrial Copy", "Marketing agencies producing superficial fluff that technical design engineers immediately dismiss as amateur.", "Wasted marketing spend and damaged engineering credibility."),
            ("Static Websites Failing to Cover Broad Machine Capability Catalogs", "A single 'Capabilities' page unable to rank for hundreds of distinct machining processes and materials.", "Invisible to procurement teams searching specific manufacturing capabilities.")
        ],
        "capabilities": [
            ("Material x Process x Tolerance Combinatorial Matrix", "Automated taxonomy combining 40+ engineering metals/polymers with 15 manufacturing processes (milling, turning, EDM, sheet metal).", "Exhaustive technical search universe targeting commercial intent."),
            ("Interactive Tolerance & Finishes Specification Matrix", "Engineered component specification tables detailing DIN/ISO tolerances, Ra surface finishes, and certification standards.", "High-credibility landing experience for quality assurance managers."),
            ("Direct Secure CAD/STEP File Upload Module", "Client-side encrypted CAD file upload integrated directly into your engineering quote queue.", "Frictionless conversion path turning search visitors into active RFPs.")
        ],
        "whop": {
            "badge": "Industrial pSEO Tier",
            "title": "Manufacturing Programmatic SEO Engine",
            "price": "$497 / month",
            "intentCluster": "Manufacturing Programmatic SEO & Industrial Inbound",
            "ctaText": "Deploy Industrial pSEO Engine",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    },
    {
        "type": "detail",
        "industry": "Manufacturing & Industrial",
        "industry_slug": "manufacturing-industrial",
        "capability": "Composio Integrations",
        "capability_slug": "composio-integrations",
        "rel_path": "manufacturing-industrial/composio-integrations/index.html",
        "url": "/solutions/manufacturing-industrial/composio-integrations/",
        "title": "Composio Industrial IoT & SAP ERP Automation | Adorise Digital",
        "description": "Connect autonomous AI agents directly to SAP, NetSuite, Rockwell Automation, and Siemens PLC streams with secure Composio tool execution.",
        "h1": "Composio Industrial IoT, MES & SAP ERP Automation",
        "subheadline": "Enable autonomous AI agents to interact directly with shop floor MES systems, inventory ERPs, and industrial IoT gateways without exposing plant control networks to security risks.",
        "metrics": [
            ("250+", "Industrial Tool Connectors", "SAP, NetSuite, Ignition, and Siemens MindSphere"),
            ("Air-Gapped", "Security Architecture", "Zero direct inbound connections to OT plant networks"),
            ("100%", "Traceability Audit Log", "Immutable event logging for ISO compliance"),
            ("< 400ms", "Event Trigger Latency", "Near real-time dispatch of automated maintenance work orders")
        ],
        "pain_points": [
            ("IT/OT Security Divide Blocking Automation", "IT security teams rejecting cloud AI tools due to fear of exposing plant PLC controllers to public internet threats.", "Stalled digital transformation and continued manual clipboard logging."),
            ("Inventory Discrepancies Between Shop Floor and ERP", "Raw material usage not updated in SAP until end-of-shift batch entries, creating stockout panics.", "Unexpected production halts due to missing raw materials."),
            ("Disjointed Maintenance Ticketing and Procurement", "Maintenance technicians diagnosing a failed part but having to manually log into ERP to order replacement spares.", "Extended machine downtime waiting for spare parts delivery.")
        ],
        "capabilities": [
            ("Unidirectional OT-to-Cloud Event Gateway", "Secure edge proxy streaming telemetry data outbound to AI models without opening any inbound ports on the plant network.", "Zero-trust industrial IoT security posture compliant with IEC 62443."),
            ("Automated ERP Spare Parts Requisition Bot", "When an anomaly agent detects bearing wear, Composio triggers an automated PO in SAP/NetSuite for replacement parts.", "Autonomous just-in-time spare parts replenishment."),
            ("Compliance Audit & Shift Handover Ledger", "Automated compilation of machine OEE, environmental telemetry, and operator maintenance actions into certified PDF audit records.", "Effortless compliance with ISO 9001 and IATF 16949 audit requirements.")
        ],
        "whop": {
            "badge": "Industrial Integrations Tier",
            "title": "Manufacturing Composio Integration Engine",
            "price": "$497 / month",
            "intentCluster": "Industrial ERP Integrations & MES Automation",
            "ctaText": "Deploy Industrial Integrations",
            "url": "https://whop.com/adorise-digital-usa/"
        }
    }
]

def generate_hub_html(p):
    cards_html = ""
    for name, slug, desc in p["capabilities_list"]:
        cards_html += f"""
      <div class="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-cyan-500/40 transition flex flex-col justify-between">
        <div>
          <div class="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">Capability</div>
          <h2 class="text-xl font-bold text-white font-display mb-3">{name}</h2>
          <p class="text-sm text-slate-400 leading-relaxed mb-6">{desc}</p>
        </div>
        <div>
          <a href="/solutions/{p['industry_slug']}/{slug}/" class="w-full inline-block text-center py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-cyan-600 hover:text-white text-cyan-400 text-xs font-bold transition">
            Explore {name} →
          </a>
        </div>
      </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['title']}</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="https://adorisedigital.com{p['url']}">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    h1, h2, h3, h4, .font-display {{ font-family: 'Outfit', sans-serif; }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Adorise Digital — {p['industry']}",
    "description": "{p['description']}",
    "url": "https://adorisedigital.com{p['url']}",
    "parentOrganization": {{
      "@type": "Organization",
      "name": "Adorise Digital",
      "url": "https://adorisedigital.com"
    }}
  }}
  </script>
</head>
<body class="bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500 selection:text-slate-950">
  <header class="sticky top-0 z-50 backdrop-blur-md bg-slate-950/80 border-b border-slate-800/60">
    <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
      <a href="/" class="flex items-center space-x-3">
        <span class="font-extrabold text-xl tracking-tight text-white font-display">ADORISE <span class="text-cyan-400 font-light">DIGITAL</span></span>
      </a>
      <div class="flex items-center space-x-4">
        <a href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult" target="_blank" rel="noopener noreferrer" class="px-5 py-2.5 rounded-full text-sm font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:scale-[1.02] transition">
          Book Architecture Call
        </a>
      </div>
    </div>
  </header>

  <div class="max-w-7xl mx-auto px-6 py-16">
    <nav aria-label="Breadcrumb" class="text-xs text-slate-400 mb-8">
      <ol class="flex items-center space-x-2">
        <li><a href="/" class="hover:text-cyan-400 transition">Home</a></li>
        <li><span class="text-slate-600">/</span></li>
        <li><a href="/solutions/" class="hover:text-cyan-400 transition">Solutions</a></li>
        <li><span class="text-slate-600">/</span></li>
        <li class="text-cyan-400 font-medium">{p['industry']}</li>
      </ol>
    </nav>

    <div class="max-w-4xl mb-16">
      <div class="inline-block px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 text-xs font-semibold mb-4 border border-cyan-500/20">
        Industry Solutions Hub
      </div>
      <h1 class="text-4xl md:text-5xl font-extrabold text-white font-display mb-6">
        {p['h1']}
      </h1>
      <p class="text-slate-300 text-lg leading-relaxed mb-6">
        {p['subheadline']}
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      {cards_html}
    </div>
  </div>

  <footer class="border-t border-slate-800/80 py-12 text-center text-xs text-slate-500">
    <p>© 2026 Adorise Digital LLC • All rights reserved.</p>
  </footer>

  <script defer src="/concierge.js?v=20260927_luna"></script>
</body>
</html>
"""

def generate_detail_html(p):
    metrics_html = "".join([f"""
        <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div class="text-3xl font-extrabold text-cyan-400 font-display mb-1">{val}</div>
          <div class="text-xs font-bold text-white uppercase tracking-wider mb-1">{lbl}</div>
          <div class="text-xs text-slate-400">{sub}</div>
        </div>
    """ for val, lbl, sub in p["metrics"]])

    pains_html = "".join([f"""
        <div class="p-6 rounded-2xl bg-slate-900/40 border border-red-500/20 hover:border-red-500/40 transition">
          <div class="text-red-400 text-xl font-bold mb-2">⚠️ {t}</div>
          <p class="text-sm text-slate-300 mb-3 leading-relaxed">{d}</p>
          <div class="p-3 rounded-lg bg-slate-950/60 border border-red-500/10 text-xs text-red-300/80">
            <strong>Operational Impact:</strong> {imp}
          </div>
        </div>
    """ for t, d, imp in p["pain_points"]])

    caps_html = "".join([f"""
        <div class="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 hover:border-cyan-500/40 transition">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center font-bold text-xs">
              {idx + 1}
            </div>
            <h3 class="text-lg font-bold text-white font-display">{t}</h3>
          </div>
          <p class="text-sm text-slate-300 leading-relaxed mb-3">{spec}</p>
          <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/60 text-xs text-cyan-300/90 font-mono">
            Deliverable: {deliv}
          </div>
        </div>
    """ for idx, (t, spec, deliv) in enumerate(p["capabilities"])])

    whop = p["whop"]

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['title']}</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="https://adorisedigital.com{p['url']}">
  <meta name="robots" content="index, follow">

  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    h1, h2, h3, h4, .font-display {{ font-family: 'Outfit', sans-serif; }}
  </style>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Adorise Digital — {p['title']}",
    "description": "{p['description']}",
    "url": "https://adorisedigital.com{p['url']}",
    "parentOrganization": {{
      "@type": "Organization",
      "name": "Adorise Digital",
      "url": "https://adorisedigital.com"
    }},
    "areaServed": "Global",
    "priceRange": "$$$$"
  }}
  </script>
</head>
<body class="bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500 selection:text-slate-950">
  <header class="sticky top-0 z-50 backdrop-blur-md bg-slate-950/80 border-b border-slate-800/60">
    <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
      <a href="/" class="flex items-center space-x-3">
        <span class="font-extrabold text-xl tracking-tight text-white font-display">ADORISE <span class="text-cyan-400 font-light">DIGITAL</span></span>
      </a>
      <div class="flex items-center space-x-4">
        <a href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult" target="_blank" rel="noopener noreferrer" class="px-5 py-2.5 rounded-full text-sm font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:scale-[1.02] transition">
          Book Architecture Call
        </a>
      </div>
    </div>
  </header>

  <main>
    <section class="py-16 md:py-24 border-b border-slate-800/60">
      <div class="max-w-7xl mx-auto px-6">
        <nav aria-label="Breadcrumb" class="text-xs text-slate-400 mb-8">
          <ol class="flex items-center space-x-2">
            <li><a href="/" class="hover:text-cyan-400 transition">Home</a></li>
            <li><span class="text-slate-600">/</span></li>
            <li><a href="/solutions/" class="hover:text-cyan-400 transition">Solutions</a></li>
            <li><span class="text-slate-600">/</span></li>
            <li><a href="/solutions/{p['industry_slug']}/" class="hover:text-cyan-400 transition">{p['industry']}</a></li>
            <li><span class="text-slate-600">/</span></li>
            <li class="text-cyan-400 font-medium">{p['capability']}</li>
          </ol>
        </nav>

        <div class="max-w-4xl">
          <div class="inline-block px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 text-xs font-semibold mb-4 border border-cyan-500/20">
            {p['industry']} • {p['capability']} Architecture
          </div>
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-white font-display tracking-tight leading-tight mb-6">
            {p['h1']}
          </h1>
          <p class="text-slate-300 text-lg md:text-xl leading-relaxed mb-8">
            {p['subheadline']}
          </p>

          <div class="flex flex-wrap gap-4 mb-12">
            <a href="{whop['url']}" target="_blank" rel="noopener noreferrer" class="px-7 py-4 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:scale-105 transition">
              {whop['ctaText']} &rarr;
            </a>
            <a href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult" target="_blank" rel="noopener noreferrer" class="px-7 py-4 rounded-xl font-semibold bg-slate-900 border border-slate-700 text-white hover:bg-slate-800 transition">
              Book Architecture Call
            </a>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8 border-t border-slate-800/60">
          {metrics_html}
        </div>
      </div>
    </section>

    <section class="py-20 border-b border-slate-800/60">
      <div class="max-w-7xl mx-auto px-6">
        <div class="max-w-3xl mb-12">
          <div class="text-xs font-bold uppercase tracking-widest text-red-400 mb-2">Critical Bottlenecks</div>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white font-display mb-4">
            Operational Vulnerabilities in {p['industry']}
          </h2>
          <p class="text-slate-300 text-base leading-relaxed">
            Manual processes and legacy software architectures cause systemic margin erosion. Here is what our deployment addresses:
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          {pains_html}
        </div>
      </div>
    </section>

    <section class="py-20 border-b border-slate-800/60">
      <div class="max-w-7xl mx-auto px-6">
        <div class="max-w-3xl mb-12">
          <div class="text-xs font-bold uppercase tracking-widest text-cyan-400 mb-2">Engineered Deliverables</div>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white font-display mb-4">
            Production System Architecture
          </h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          {caps_html}
        </div>
      </div>
    </section>

    <section class="py-16 bg-gradient-to-r from-cyan-950/40 via-slate-900 to-indigo-950/40 border-b border-slate-800/80">
      <div class="max-w-7xl mx-auto px-6">
        <div class="p-8 md:p-10 rounded-3xl bg-slate-900/90 border border-cyan-500/30 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-8">
          <div class="max-w-2xl">
            <div class="inline-block px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-bold uppercase tracking-wider mb-3">
              {whop['badge']}
            </div>
            <h3 class="text-2xl md:text-3xl font-extrabold text-white font-display mb-2">
              Deploy {whop['title']}
            </h3>
            <p class="text-sm text-slate-300 leading-relaxed mb-4">
              Target Intent: <span class="text-white font-medium">{whop['intentCluster']}</span>. Instant self-service provisioning with code <code class="text-cyan-400 font-mono">FOUNDERFREE</code> for $0 setup fee.
            </p>
            <div class="flex items-center space-x-3 text-sm text-slate-400">
              <span class="text-cyan-400 font-bold text-xl">{whop['price']}</span>
              <span>•</span>
              <span>Instant Activation</span>
              <span>•</span>
              <span>Cancel Anytime</span>
            </div>
          </div>
          <a href="{whop['url']}" target="_blank" rel="noopener noreferrer" class="px-8 py-4 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:scale-105 transition text-center whitespace-nowrap">
            {whop['ctaText']} &rarr;
          </a>
        </div>
      </div>
    </section>
  </main>

  <footer class="border-t border-slate-800/80 py-12 text-center text-xs text-slate-500">
    <p>© 2026 Adorise Digital LLC • All rights reserved.</p>
  </footer>

  <script defer src="/concierge.js?v=20260927_luna"></script>
</body>
</html>
"""

def main():
    print("=" * 60)
    print("🚀 ADORISE DIGITAL — pSEO BATCH GENERATOR (81 -> 91)")
    print("=" * 60)

    # 1. Generate HTML Files
    new_slugs = []
    for p in PAGES_CONFIG:
        target_path = os.path.join(SOLUTIONS_DIR, p["rel_path"])
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        if p["type"] == "hub":
            html = generate_hub_html(p)
        else:
            html = generate_detail_html(p)
            
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(html)
            
        new_slugs.append(p["url"])
        print(f"  [CREATED] {p['url']} -> {target_path}")

    # 2. Update solutions_data.json
    with open(SOLUTIONS_DATA_FILE, "r", encoding="utf-8") as f:
        solutions_data = json.load(f)
        
    existing_urls = set(item.get("url") for item in solutions_data)
    added_to_json = 0
    for p in PAGES_CONFIG:
        if p["url"] not in existing_urls:
            solutions_data.append({
                "title": p["title"].split("|")[0].strip(),
                "url": p["url"],
                "description": p["description"],
                "industry": p["industry"],
                "industry_slug": p["industry_slug"],
                "capability": p.get("capability", "Overview"),
                "capability_slug": p.get("capability_slug", "")
            })
            added_to_json += 1

    with open(SOLUTIONS_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(solutions_data, f, indent=2)
    print(f"  [UPDATED] solutions_data.json with {added_to_json} new entries (Total: {len(solutions_data)})")

    # 3. Update sitemaps/sitemap-1.xml
    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        sitemap_content = f.read()

    new_urls_xml = ""
    today_iso = datetime.utcnow().strftime("%Y-%m-%d")
    for u in new_slugs:
        full_url = f"https://adorisedigital.com{u}"
        if full_url not in sitemap_content:
            new_urls_xml += f"""  <url>
    <loc>{full_url}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

    if new_urls_xml:
        sitemap_content = sitemap_content.replace("</urlset>", new_urls_xml + "</urlset>")
        with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
            f.write(sitemap_content)
        print("  [UPDATED] sitemaps/sitemap-1.xml with new URLs")

    print("\n✅ All 10 expansion pages successfully compiled and registered!")

if __name__ == "__main__":
    main()
