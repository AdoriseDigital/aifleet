import json
import re

# Comprehensive database builder for all 70 combinations with zero repetitive boilerplate sentences

BANNED = ['delve', 'supercharge', 'unleash', 'tapestry', 'seamlessly', 'game-changer', 'revolutionize', 'elevate', 'cutting-edge', 'synergy']

def check_banned_words(text, context):
    for w in BANNED:
        if re.search(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE):
            raise ValueError(f"Banned word '{w}' in {context}")

# 10 Niches with deep operational vocabularies
NICHES = {
    'b2b-saas': {
        'name': 'B2B SaaS & Enterprise Software',
        'short': 'B2B SaaS',
        'buyer': 'VP of Growth and Chief Technology Officers',
        'acv': '$12k-$60k',
        'stack': 'HubSpot, Salesforce, and Stripe',
        'reg': 'SOC2 Type II data isolation',
        'domain_focus': 'demo requests, ARR expansion, churn mitigation, and multi-tenant security'
    },
    'ecommerce-d2c': {
        'name': 'High-Volume E-Commerce & D2C Brands',
        'short': 'E-Commerce & D2C',
        'buyer': 'Brand Founders and E-Commerce Directors',
        'acv': '$500k-$10M GMV',
        'stack': 'Shopify Plus, Gorgias, and Klaviyo',
        'reg': 'PCI-DSS payment and consumer privacy guidelines',
        'domain_focus': 'order tracking, return logistics, BFCM spikes, and inventory turnover'
    },
    'fintech': {
        'name': 'FinTech & Digital Financial Services',
        'short': 'FinTech',
        'buyer': 'Chief Risk Officers and FinTech Founders',
        'acv': '$25k-$150k',
        'stack': 'Plaid, Stripe, and core banking APIs',
        'reg': 'SEC, FINRA, and PCI-DSS compliance mandates',
        'domain_focus': 'double-entry ledgers, ACH clearing, KYC/AML screening, and risk underwriting'
    },
    'healthtech-biotech': {
        'name': 'HealthTech & Digital Health Platforms',
        'short': 'HealthTech',
        'buyer': 'Clinical Operations Directors and HealthTech CTOs',
        'acv': '$30k-$120k',
        'stack': 'Epic, Cerner, and FHIR endpoints',
        'reg': 'HIPAA security rules and PHI confidentiality',
        'domain_focus': 'patient intake, telehealth queues, electronic health records, and clinical triage'
    },
    'proptech-realestate': {
        'name': 'PropTech & Commercial Real Estate Platforms',
        'short': 'PropTech',
        'buyer': 'Managing Brokers and Real Estate Asset Partners',
        'acv': '$15k-$80k',
        'stack': 'MLS feeds, CoStar, and Yardi',
        'reg': 'RESO data standards and fair housing guidelines',
        'domain_focus': 'commercial lease abstraction, tenant screening, property listings, and broker routing'
    },
    'legaltech-professional': {
        'name': 'LegalTech & High-Ticket Professional Services',
        'short': 'LegalTech',
        'buyer': 'Managing Partners and General Counsels',
        'acv': '$20k-$100k',
        'stack': 'Clio, iManage, and Thomson Reuters',
        'reg': 'ABA Model Rules and attorney-client privilege',
        'domain_focus': 'conflict checks, matter onboarding, billable hour tracking, and document discovery'
    },
    'venture-capital-private-equity': {
        'name': 'Venture Capital & Private Equity Firms',
        'short': 'VC & Private Equity',
        'buyer': 'General Partners and Private Equity Operating Principals',
        'acv': '$50M-$1B AUM',
        'stack': 'PitchBook, Affinity, and Carta',
        'reg': 'SEC accredited investor guidelines',
        'domain_focus': 'thematic deal sourcing, EBITDA multiples, fund IRR, and portfolio company telemetry'
    },
    'edtech': {
        'name': 'EdTech & Online Learning Platforms',
        'short': 'EdTech',
        'buyer': 'Heads of Learning and EdTech Founders',
        'acv': '$10k-$50k',
        'stack': 'Canvas LMS, Moodle, and Stripe',
        'reg': 'FERPA student privacy standards',
        'domain_focus': 'cohort retention drop-off, curriculum taxonomy, automated grading, and credentialing'
    },
    'cybersecurity': {
        'name': 'Enterprise Cybersecurity & DevSecOps',
        'short': 'Cybersecurity',
        'buyer': 'CISOs and DevSecOps Directors',
        'acv': '$40k-$200k',
        'stack': 'Cloudflare WAF, CrowdStrike, and AWS IAM',
        'reg': 'NIST Cybersecurity Framework and CIS benchmarks',
        'domain_focus': 'zero-trust perimeter defense, container sandboxing, CVE vulnerability scans, and SIEM logs'
    },
    'agency-consultancy': {
        'name': 'Digital Agencies & High-Growth Consultancies',
        'short': 'Agencies & Consultancies',
        'buyer': 'Agency Principals and Managing Partners',
        'acv': '$5k-$30k/mo',
        'stack': 'ClickUp, HighLevel, and client Stripe accounts',
        'reg': 'commercial MSA client service agreements',
        'domain_focus': 'feast-or-famine client cycles, fulfillment bottlenecks, scope creep, and retainer churn'
    }
}

# Service details
SERVICES = {
    'pseo-engine': {
        'name': 'Programmatic SEO Engine',
        'short': 'pSEO Engine',
        'badge': 'Automated Inbound Engineering',
        'tech': 'Next.js App Router, Incremental Static Regeneration, Schema.org JSON-LD, and chunked XML sitemaps'
    },
    'ai-agents': {
        'name': 'Autonomous AI Agents',
        'short': 'AI Agents',
        'badge': 'Agentic Workflow Engineering',
        'tech': 'LangGraph multi-agent orchestration, deterministic tool calling, and human-in-the-loop review gates'
    },
    'web-app-engineering': {
        'name': 'Next.js Web Engineering',
        'short': 'Web Engineering',
        'badge': 'Modern Web Engineering',
        'tech': 'React Server Components, Next.js App Router, TypeScript, Tailwind CSS, and edge Prisma ORM'
    },
    'outbound-infrastructure': {
        'name': 'Cold Outbound & Lead Engine',
        'short': 'Cold Outbound',
        'badge': 'Outbound Pipeline Engineering',
        'tech': 'isolated secondary domains, automated mailbox warm-up, DNS security alignment, and intent scraping'
    },
    'composio-integrations': {
        'name': 'Composio Agent Integrations',
        'short': 'Composio Integrations',
        'badge': 'Agent Tooling Architecture',
        'tech': 'self-hosted Composio runtime, OAuth 2.0 PKCE token vaults, Docker sandboxing, and webhook dispatchers'
    },
    'cloud-vps-hardening': {
        'name': 'Cloud VPS & Docker Hardening',
        'short': 'VPS Infrastructure',
        'badge': 'Zero-Trust Infrastructure',
        'tech': 'Ubuntu 24.04 LTS OS hardening, Cloudflare Zero Trust tunnels, Docker sandboxing, and UFW firewall rules'
    },
    'whop-monetization': {
        'name': 'Whop Monetization Systems',
        'short': 'Whop Monetization',
        'badge': 'Digital Monetization Systems',
        'tech': 'Whop API v2, automated license key generation, Discord role synchronization, and dunning webhooks'
    }
}

print("Base dictionaries defined.")
