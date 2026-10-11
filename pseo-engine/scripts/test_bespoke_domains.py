import json
import re

# Generator that constructs 58 truly distinct combination entries without boilerplate sentence sharing

NICHE_DOMAINS = {
    'b2b-saas': {
        'name': 'B2B SaaS & Enterprise Software',
        'short': 'B2B SaaS',
        'acv': '$12,000 - $60,000/yr',
        'persona': 'VP of Growth and Chief Technology Officers',
        'lead_obj': 'demo requests and trial activations',
        'tools': 'HubSpot, Salesforce, PostgreSQL, and Stripe',
        'concerns': 'net revenue churn, CAC payback velocity, product-led onboarding, and multi-tenant security'
    },
    'ecommerce-d2c': {
        'name': 'High-Volume E-Commerce & D2C Brands',
        'short': 'E-Commerce & D2C',
        'buyer': 'Brand Founders and E-Commerce Directors',
        'acv': '$500,000 - $10M GMV',
        'lead_obj': 'SKU checkouts and return authorizations',
        'tools': 'Shopify Plus, Gorgias, Klaviyo, and Meta Ads',
        'concerns': 'BFCM peak concurrency, return logistics, ad margin compression, and inventory turnover'
    },
    'fintech': {
        'name': 'FinTech & Digital Financial Services',
        'short': 'FinTech',
        'buyer': 'Chief Risk Officers and FinTech Founders',
        'acv': '$25,000 - $150,000/yr',
        'lead_obj': 'institutional accounts and payment processing volume',
        'tools': 'Plaid, Stripe, core banking APIs, and ledger databases',
        'concerns': 'PCI-DSS compliance, double-entry ledger integrity, KYC/AML screening, and ACH settlement latency'
    },
    'healthtech-biotech': {
        'name': 'HealthTech & Digital Health Platforms',
        'short': 'HealthTech & Biotech',
        'buyer': 'Clinical Operations Directors and HealthTech CTOs',
        'lead_obj': 'patient consultations and clinician onboarding',
        'tools': 'Epic, Cerner, FHIR endpoints, and HIPAA cloud vaults',
        'concerns': 'HIPAA PHI containment, HL7 protocol translation, patient intake friction, and clinical triage'
    },
    'proptech-realestate': {
        'name': 'PropTech & Commercial Real Estate Platforms',
        'short': 'PropTech & Real Estate',
        'buyer': 'Managing Brokers and Real Estate Asset Partners',
        'acv': '$15,000 - $80,000/yr',
        'lead_obj': 'commercial property tours and investor subscriptions',
        'tools': 'MLS feeds, CoStar, Yardi, and geospatial GIS databases',
        'concerns': 'RESO data standards, commercial lease abstraction, tenant screening, and broker routing'
    },
    'legaltech-professional': {
        'name': 'LegalTech & High-Ticket Professional Services',
        'short': 'LegalTech & Advisory',
        'buyer': 'Managing Partners and Firm General Counsels',
        'acv': '$20,000 - $100,000/yr',
        'lead_obj': 'retained legal matters and corporate advisory clients',
        'tools': 'Clio, iManage, Thomson Reuters, and secure matter vaults',
        'concerns': 'attorney-client privilege, conflict checks, ABA ethics compliance, and billable hour tracking'
    },
    'venture-capital-private-equity': {
        'name': 'Venture Capital & Private Equity Firms',
        'short': 'VC & Private Equity',
        'buyer': 'General Partners and Private Equity Operating Principals',
        'acv': '$50M - $1B AUM',
        'lead_obj': 'proprietary investment opportunities and LP subscriptions',
        'tools': 'PitchBook, Affinity, Carta, and secure portfolio datarooms',
        'concerns': 'thematic outbound sourcing, EBITDA multiples, fund IRR, and portfolio company telemetry'
    },
    'edtech': {
        'name': 'EdTech & Online Learning Platforms',
        'short': 'EdTech & Education',
        'buyer': 'Heads of Learning and EdTech Platform Founders',
        'acv': '$10,000 - $50,000/yr',
        'lead_obj': 'student course enrollments and platform subscriptions',
        'tools': 'Canvas LMS, Moodle, Stripe, and student databases',
        'concerns': 'cohort retention drop-off, curriculum taxonomy, automated quiz grading, and credentialing'
    },
    'cybersecurity': {
        'name': 'Enterprise Cybersecurity & DevSecOps',
        'short': 'Cybersecurity',
        'buyer': 'Chief Information Security Officers and DevSecOps Directors',
        'acv': '$40,000 - $200,000/yr',
        'lead_obj': 'enterprise security audits and vendor risk reviews',
        'tools': 'Cloudflare WAF, CrowdStrike, AWS IAM, and SIEM logs',
        'concerns': 'zero-trust perimeter isolation, CVE vulnerability remediation, SOC2 compliance, and port scans'
    },
    'agency-consultancy': {
        'name': 'Digital Agencies & High-Growth Consultancies',
        'short': 'Agencies & Consultancies',
        'buyer': 'Agency Principals and Managing Partners',
        'acv': '$5,000 - $30,000/mo',
        'lead_obj': 'monthly recurring retainers and performance contracts',
        'tools': 'ClickUp, HighLevel, Slack, and client Stripe accounts',
        'concerns': 'feast-or-famine client cycles, fulfillment bottlenecking, scope creep, and retainer churn'
    }
}

print("Loaded Niche Domains.")
