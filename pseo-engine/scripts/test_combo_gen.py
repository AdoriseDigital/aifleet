import json
import re

# Comprehensive combination generator ensuring >35% pairwise uniqueness across all 70 combinations

NICHES = {
    'b2b-saas': {
        'name': 'B2B SaaS & Enterprise Software',
        'short': 'B2B SaaS',
        'buyer': 'VP of Growth and Chief Technology Officers',
        'acv': '$12,000 - $60,000/yr',
        'metrics_arr': '+340% Pipeline Expansion',
        'stack': 'HubSpot, Salesforce, PostgreSQL, and Stripe',
        'reg': 'SOC2 Type II and GDPR data isolation',
        'context': 'cloud software platforms, recurring ARR growth, seat expansion, and product-led customer onboarding',
        'stress': 'late-night sprint blockers, customer churn notifications, and investor updates',
        'pains': [
            ('Skyrocketing Customer Acquisition Payback Periods', 'Commercial software keyword bidding costs over $60 per click, pushing customer acquisition payback beyond 18 months.', 'Compressed SaaS gross margins and excessive venture capital burn.'),
            ('SDR Outbound Burnout and Corporate Domain Burning', 'Junior sales development reps blast unverified contact lists, triggering spam filters and burning primary corporate email domains.', 'Collapsing enterprise demo pipelines and lost sales velocity.'),
            ('Engineering Sprints Diverted into Marketing Tools', 'Senior developers spend weeks maintaining custom landing pages and third-party webhook integrations instead of shipping core roadmap features.', 'Delayed core software releases and lost market differentiation.')
        ]
    },
    'ecommerce-d2c': {
        'name': 'High-Volume E-Commerce & D2C Brands',
        'short': 'E-Commerce & D2C',
        'buyer': 'Brand Founders and E-Commerce Directors',
        'acv': '$500,000 - $10M GMV',
        'metrics_arr': '-68% Support Ticket Volume',
        'stack': 'Shopify Plus, Gorgias, Klaviyo, and Meta Ads',
        'reg': 'PCI-DSS payment security and consumer privacy rules',
        'context': 'direct-to-consumer storefronts, SKU catalog indexing, promotional drops, and warehouse return logistics',
        'stress': 'supply chain shipping delays, ad account bans, and holiday ticket backlogs',
        'pains': [
            ('Holiday Drop Support Desk Avalanches', 'Promotional drops and holiday traffic surges overwhelm customer care desks with repetitive order tracking and exchange inquiries.', 'Customer dissatisfaction, dispute chargebacks, and lost repeat purchase volume.'),
            ('Paid Social ROAS Volatility and Signal Loss', 'Rising CPMs on Meta and TikTok paired with privacy tracking limitations compress gross margins across fast-moving product catalogs.', 'Erratic cash flow and unsustainable advertising dependency.'),
            ('SKU Catalog SEO Cannibalization and Duplicate Pages', 'Managing product detail pages across thousands of size and color variants produces duplicate content penalized by Google.', 'Erosion of organic category search rankings to major department retailers.')
        ]
    },
    'fintech': {
        'name': 'FinTech & Digital Financial Services',
        'short': 'FinTech',
        'buyer': 'Chief Risk Officers and FinTech Founders',
        'acv': '$25,000 - $150,000/yr',
        'metrics_arr': '99.99% Transaction Integrity',
        'stack': 'Plaid, Stripe, core banking APIs, and ledger databases',
        'reg': 'SEC, FINRA, and PCI-DSS financial regulations',
        'context': 'banking rails, double-entry ledger reconciliation, KYC/AML screening, and institutional payment flows',
        'stress': 'regulatory compliance audits, payment settlement latency, and capital fraud exposure',
        'pains': [
            ('Strict Regulatory Compliance and Audit Burdens', 'Financial platforms face rigid scrutiny from banking partners and regulatory bodies demanding auditable transaction logs and strict encryption.', 'Elongated enterprise onboarding cycles and expensive legal audit penalties.'),
            ('Legacy Core Banking API Latency and Timeouts', 'Interfacing modern client applications with legacy banking networks causes transaction drops and reconciliation discrepancies.', 'Failed customer transactions, manual ledger reconciliations, and lost institutional trust.'),
            ('Escalating Overhead of Manual Risk Underwriting', 'Human compliance teams cannot verify high-frequency account openings in real time, creating onboarding friction for legitimate users.', 'High user drop-off during onboarding and exposure to synthetic identity fraud.')
        ]
    },
    'healthtech-biotech': {
        'name': 'HealthTech & Digital Health Platforms',
        'short': 'HealthTech',
        'buyer': 'Clinical Operations Directors and HealthTech CTOs',
        'acv': '$30,000 - $120,000/yr',
        'metrics_arr': '100% HIPAA Containment',
        'stack': 'Epic, Cerner, FHIR endpoints, and HIPAA cloud vaults',
        'reg': 'HIPAA security rules and Protected Health Information (PHI) standards',
        'context': 'telemedicine portals, electronic medical records, clinical decision support, and patient intake triage',
        'stress': 'patient confidentiality liability, provider scheduling bottlenecks, and EHR API outages',
        'pains': [
            ('HIPAA and Protected Health Information Exposure Risk', 'Managing distributed clinical workloads carries severe statutory penalties if patient health identifiers leak across unencrypted networks.', 'Statutory HIPAA fines, clinical accreditation suspension, and enterprise client loss.'),
            ('EHR and Hospital System Interoperability Silos', 'Transferring diagnostic records and scheduling across fragmented electronic health record systems requires bespoke protocol translation.', 'Clinician scheduling bottlenecks and delayed diagnostic test communication.'),
            ('Patient Intake Drop-Off on Multi-Step Questionnaires', 'Exhausting medical intake questionnaires cause patients to abandon booking consultations, depressing clinic capacity utilization.', 'Lost clinic consultation billings and depressed patient engagement.')
        ]
    },
    'proptech-realestate': {
        'name': 'PropTech & Commercial Real Estate Platforms',
        'short': 'PropTech',
        'buyer': 'Managing Brokers and Real Estate Asset Partners',
        'acv': '$15,000 - $80,000/yr',
        'metrics_arr': '< 45ms Listing TTFB',
        'stack': 'MLS feeds, CoStar, Yardi, and geospatial GIS databases',
        'reg': 'fair housing advertising and RESO data standards',
        'context': 'commercial lease abstraction, regional property syndication, tenant screening, and asset occupancy',
        'stress': 'prolonged leasing vacancies, closing deal delays, and fragmented property data',
        'pains': [
            ('Fragmented Regional MLS and Property Data Ingestion', 'Aggregating property feeds across hundreds of regional boards causes schema errors, outdated asset availability, and missing images.', 'Degraded listing portal accuracy and tenant dissatisfaction.'),
            ('Hyper-Local Search Competition Against National Portals', 'Independent brokerages struggle to rank organically against massive national aggregator sites for local commercial property queries.', 'Inability to attract high-net-worth commercial buyers and leasing tenants.'),
            ('Slow Broker Lead Qualification and Routing Latency', 'Prospective property inquiries languish in email inboxes for hours, allowing competing commercial brokerages to secure tenant tours first.', 'Lost commercial brokerage commissions and extended property vacancy periods.')
        ]
    },
    'legaltech-professional': {
        'name': 'LegalTech & High-Ticket Professional Services',
        'short': 'LegalTech',
        'buyer': 'Managing Partners and General Counsels',
        'acv': '$20,000 - $100,000/yr',
        'metrics_arr': '100% Ethical Privilege',
        'stack': 'Clio, iManage, Thomson Reuters, and secure matter vaults',
        'reg': 'ABA Model Rules and attorney-client privilege mandates',
        'context': 'conflict-of-interest checking, billable hour tracking, matter onboarding, and document discovery',
        'stress': 'grueling 80-hour billable weeks, client conflict disputes, and administrative overhead',
        'pains': [
            ('Astronomical Legal Keyword Advertising Costs', 'Commercial litigation and corporate legal search keywords cost between $90 and $250 per click on paid search networks.', 'Exorbitant client acquisition costs and low return on marketing spend.'),
            ('Strict Bar Association Ethical Outbound Rules', 'State bar rules strictly prohibit deceptive or unsolicited direct marketing, exposing careless practices to ethics investigations.', 'Risk of disciplinary sanction and permanent institutional brand damage.'),
            ('Administrative Drag of Manual Conflict Checking', 'Associates spend hours manually screening parties and related entities for conflicts of interest before formal engagement letters issue.', 'Delayed matter onboarding and non-billable associate hours eroding profits.')
        ]
    },
    'venture-capital-private-equity': {
        'name': 'Venture Capital & Private Equity Firms',
        'short': 'VC & Private Equity',
        'buyer': 'General Partners and Private Equity Operating Principals',
        'acv': '$50M - $1B AUM',
        'metrics_arr': '3.2x Proprietary Dealflow',
        'stack': 'PitchBook, Affinity, Carta, and secure portfolio datarooms',
        'reg': 'SEC accredited investor guidelines and confidential fund reporting',
        'context': 'proprietary deal sourcing, EBITDA expansion, limited partner reporting, and CIM memorandum abstraction',
        'stress': 'dry powder deployment timelines, missed proprietary dealflow, and partner friction',
        'pains': [
            ('Banker-Led Auction Multiple Inflation', 'Bidding exclusively through investment banker auction processes inflates acquisition multiples and compresses investment fund returns.', 'Sub-optimal portfolio IRR and hefty intermediary transaction fees.'),
            ('Fragmented Portfolio KPI Tracking and Spreadsheets', 'Collecting monthly financial metrics across dozens of portfolio companies involves manual email chasing and incompatible spreadsheets.', 'Delayed quarterly limited partner reporting and missed operational interventions.'),
            ('Invisibility to Bootstrapped Market Leaders', 'Top-tier founders building profitable enterprises avoid cold outreach from generic capital providers without clear operational value-add.', 'Missing premier proprietary investment rounds before competitive term sheets emerge.')
        ]
    },
    'edtech': {
        'name': 'EdTech & Online Learning Platforms',
        'short': 'EdTech',
        'buyer': 'Heads of Learning and EdTech Founders',
        'acv': '$10,000 - $50,000/yr',
        'metrics_arr': '+72% Cohort Completion',
        'stack': 'Canvas LMS, Moodle, Stripe, and student databases',
        'reg': 'FERPA student privacy and accessibility guidelines',
        'context': 'digital curricula, asynchronous student engagement, cohort retention, and digital skill credentialing',
        'stress': 'student drop-off after week two, manual grading fatigue, and subscription cancellations',
        'pains': [
            ('Catastrophic Student Drop-Off in Week Two', 'Self-paced learners lose motivation rapidly, driving completion rates below 14% and causing high subscription cancellation rates.', 'Depressed student lifetime value and negative public course reviews.'),
            ('Course Catalog Taxonomy Search Fragmentation', 'Structuring thousands of lectures, prerequisites, and syllabi for organic search indexing requires continuous manual SEO maintenance.', 'Poor organic search discoverability for high-margin specialized certifications.'),
            ('Weak Student Community Monetization Funnels', 'Student discussion communities on chat platforms fail to convert casual participants into recurring paid premium tier subscribers.', 'Lost recurring subscription revenue and unmonetized platform engagement.')
        ]
    },
    'cybersecurity': {
        'name': 'Enterprise Cybersecurity & DevSecOps',
        'short': 'Cybersecurity',
        'buyer': 'CISOs and DevSecOps Directors',
        'acv': '$40,000 - $200,000/yr',
        'metrics_arr': '0 Open Ports Hardened',
        'stack': 'Cloudflare WAF, CrowdStrike, AWS IAM, and SIEM logs',
        'reg': 'NIST Cybersecurity Framework, CIS benchmarks, and SOC2 standards',
        'context': 'zero-trust network perimeter defense, container sandboxing, CVE vulnerability scanning, and threat intelligence',
        'stress': 'zero-day vulnerability notices, enterprise vendor risk reviews, and audit compliance',
        'pains': [
            ('Nine-Month Enterprise Technical Proof of Concept Cycles', 'Enterprise security deals drag through rigorous vendor security questionnaires, compliance audits, and architectural reviews.', 'Elongated enterprise sales velocity tying up principal engineering resources.'),
            ('Conveying Zero-Trust Architecture to Non-Technical Buyers', 'Security firms struggle to articulate complex network protection benefits to procurement committees without jargon.', 'Lost enterprise contracts to competitors with clearer positioning.'),
            ('Public Ingress Vulnerability and Attack Surface Drift', 'Exposing web interfaces without hardened edge tunnels creates vectors for automated port scans, brute-force bots, and DDoS extortion.', 'Security breach risks, service downtime, and regulatory disclosure penalties.')
        ]
    },
    'agency-consultancy': {
        'name': 'Digital Agencies & High-Growth Consultancies',
        'short': 'Agencies & Consultancies',
        'buyer': 'Agency Principals and Managing Partners',
        'acv': '$5,000 - $30,000/mo',
        'metrics_arr': '+180% Retainer Predictability',
        'stack': 'ClickUp, HighLevel, Slack, and client Stripe accounts',
        'reg': 'commercial MSA client service agreements and white-label confidentiality',
        'context': 'predictable inbound retainer acquisition, automated client delivery, scope creep management, and client retention',
        'stress': 'the feast-or-famine client cycle, scope creep negotiations, and client churn anxiety',
        'pains': [
            ('The Feast-or-Famine Client Acquisition Cycle', 'Pausing prospecting during intense client fulfillment sprints causes revenue to drop sharply when contracts conclude.', 'Erratic agency cash flow, hiring delays, and intense quarterly revenue anxiety.'),
            ('Fulfillment Capacity Bottlenecks on Senior Staff', 'Agency leadership spends valuable hours executing manual client fulfillment instead of business development and team coaching.', 'Capped agency billing capacity and severe partner burnout.'),
            ('Retainer Churn from Slow Demonstrable Organic Results', 'Traditional digital marketing retainers take months to produce visible search rankings, leading clients to cancel early.', 'Short average client lifespan and perpetual sales pressure.')
        ]
    }
}

SERVICES = {
    'pseo-engine': {
        'name': 'Programmatic SEO Engine',
        'short': 'pSEO Engine',
        'badge': 'Automated Inbound Engineering',
        'verb': 'compiles dynamic Next.js landing pages',
        'deliv_focus': 'high-intent organic search capture and structured microdata',
        'tech': 'Next.js App Router, Incremental Static Regeneration, Schema.org JSON-LD, and chunked XML sitemaps'
    },
    'ai-agents': {
        'name': 'Autonomous AI Agents',
        'short': 'AI Agents',
        'badge': 'Agentic Workflow Engineering',
        'verb': 'deploys multi-agent decision swarms',
        'deliv_focus': 'automated task decomposition, customer triage, and human-in-the-loop review gates',
        'tech': 'LangGraph multi-agent orchestration, deterministic tool calling, and state machines'
    },
    'web-app-engineering': {
        'name': 'Next.js Web Engineering',
        'short': 'Web Engineering',
        'badge': 'Modern Web Engineering',
        'verb': 'constructs full-stack web applications',
        'deliv_focus': 'sub-50ms edge rendering, type-safe database schemas, and zero layout shift',
        'tech': 'React Server Components, Next.js App Router, TypeScript, Tailwind CSS, and Prisma ORM'
    },
    'outbound-infrastructure': {
        'name': 'Cold Outbound & Lead Engine',
        'short': 'Cold Outbound',
        'badge': 'Outbound Pipeline Engineering',
        'verb': 'engineers dedicated cold sending fleets',
        'deliv_focus': 'isolated secondary domains, automated mailbox warm-up, and intent listening',
        'tech': 'SPF, DKIM, DMARC alignment, real-time SMTP validation, and CRM dispatch webhooks'
    },
    'composio-integrations': {
        'name': 'Composio Agent Integrations',
        'short': 'Composio Integrations',
        'badge': 'Agent Tooling Architecture',
        'verb': 'architects self-hosted Composio execution environments',
        'deliv_focus': 'secure OAuth credential token vaults, sandboxed tool calling, and auditable telemetry',
        'tech': 'self-hosted Composio runtime, OAuth 2.0 PKCE token management, and Docker isolation'
    },
    'cloud-vps-hardening': {
        'name': 'Cloud VPS & Docker Hardening',
        'short': 'VPS Infrastructure',
        'badge': 'Zero-Trust Infrastructure',
        'verb': 'hardens Linux cloud servers and containerized swarms',
        'deliv_focus': 'zero open public ports, Cloudflare Zero Trust tunnels, and automated encrypted backups',
        'tech': 'Ubuntu 24.04 LTS kernel hardening, Cloudflare Tunnels, UFW firewalls, and Fail2ban'
    },
    'whop-monetization': {
        'name': 'Whop Monetization Systems',
        'short': 'Whop Monetization',
        'badge': 'Digital Monetization Systems',
        'verb': 'builds membership gating and digital checkout funnels',
        'deliv_focus': 'tier entitlement logic, automated license provisioning, and Discord role gating',
        'tech': 'Whop API v2, automated license dispatchers, Discord bot sync, and dunning webhooks'
    }
}

print("Loaded definitions successfully.")
