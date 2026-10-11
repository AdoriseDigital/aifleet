import os
import re
import json

FRONTEND_DIR = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\adorise-frontend"
MANIFEST_PATH = r"D:\Obedian Adorise AI Business\Adorise AI Business OS\c_drive_repo\pseo-engine\data\batch_manifest.json"

with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

published_slugs = []
for b in manifest['batches']:
    published_slugs.extend(b['slugs'])

# Check for banned buzzwords
BANNED = ['delve', 'supercharge', 'unleash', 'tapestry', 'seamlessly', 'game-changer', 'revolutionize', 'elevate', 'cutting-edge', 'synergy']

def check_banned(text, context=""):
    for b in BANNED:
        if re.search(r'\b' + re.escape(b) + r'\b', text, re.IGNORECASE):
            raise ValueError(f"Banned word '{b}' found in {context}")

# Define rich, technical prose blocks for the 7 services (each 250+ unique words)
SERVICE_BLOCKS = {
    'pseo-engine': """
      <div class="technical-capability-block p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Programmatic Edge Generation & Indexing Architecture</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Our programmatic search engine compiles dynamic route trees directly into edge-cached static assets utilizing Next.js App Router, Incremental Static Regeneration, and React Server Components.
          By structuring commercial intent taxonomy matrices across target subdirectories, the system captures long-tail software alternatives, competitor comparisons, and transactional buyer queries without manual editorial overhead.
          Every edge page executes with sub-45ms time-to-first-byte (TTFB), zero cumulative layout shift (CLS), pre-rendered HTML payloads, and automated canonical tag management.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          To ensure sustained Google Search Console indexing velocity, the compilation loop chunks XML sitemaps into modular 5,000-URL fragments, synchronizes dynamic lastmod timestamps, and dispatches real-time IndexNow pings across Microsoft Bing and Yandex crawlers.
          Rich structured data schemas are injected into head blocks, generating validated ProfessionalService, Organization, BreadcrumbList, and FAQPage JSON-LD microdata compliant with Google Rich Results criteria.
          Internal linking graphs dynamically interlink related solution hubs, distributing PageRank authority evenly across deep catalog nodes to avoid orphaned routes and crawl budget waste.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-cyan-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Chunked XML Sitemaps</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">IndexNow Fast Ping</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Sub-45ms Edge TTFB</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">JSON-LD Microdata</div>
        </div>
      </div>
    """,

    'ai-agents': """
      <div class="technical-capability-block p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Autonomous Multi-Agent Swarm & Tool-Calling Architecture</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          We engineer deterministic multi-agent runtime swarms coordinated via LangGraph state machines, structured Pydantic schemas, and constrained function-calling loops.
          Rather than relying on brittle zero-shot prompts, our agent architectures decompose complex operational requests into atomic task graphs, validating intermediate payloads against rigorous JSON Schema boundaries to eliminate hallucinations and parameter drift.
          Agents maintain ephemeral session memory buffers paired with vector retrieval pipelines utilizing Pinecone, ChromaDB, and Faiss embeddings to ground decisions in enterprise records.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          For mission-critical operational mutations, our runtime enforces human-in-the-loop approval gates, streaming proposed actions into Slack webhook queues or administrative review dashboards before committing database state changes.
          Containerized background workers running on Celery and Redis message brokers process concurrent customer triage tickets, invoice data extraction, and CRM updates with sub-1.5 second inference latency.
          Comprehensive telemetry records prompt token consumption, model response latency, and tool invocation traces to ensure total governance and auditable compliance.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-cyan-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">LangGraph State Swarms</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">JSON Schema Guardrails</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Human Approval Checkpoints</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Auditable Vector Memory</div>
        </div>
      </div>
    """,

    'web-app-engineering': """
      <div class="technical-capability-block p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Full-Stack Next.js App Router & Edge Engineering</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Our engineering practice builds enterprise web applications on Next.js App Router, React Server Components, TypeScript, and modern edge infrastructure.
          By executing data fetching and business logic server-side, client JavaScript bundle sizes are minimized, achieving 99+ Core Web Vitals, instantaneous hydration, and zero cumulative layout shift across responsive viewports.
          Interface components are constructed using Tailwind CSS, Radix UI primitives, and Framer Motion micro-interactions, ensuring strict adherence to WCAG 2.1 AA accessibility guidelines.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Database layers integrate PostgreSQL, Supabase, or SQLite through type-safe Prisma ORM migrations, utilizing connection pooling via PgBouncer to prevent exhaustion under heavy concurrency.
          Server actions and API route handlers execute inside isolated edge workers, enforcing CSRF protection, secure HTTP-only session cookies, and Zod input validation schemas.
          Continuous integration workflows on GitHub Actions automate unit testing, bundle analysis, and preview deployments with zero-downtime production rollouts.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-cyan-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">React Server Components</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Type-Safe Prisma Models</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">99+ Core Web Vitals</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Edge Serverless Routing</div>
        </div>
      </div>
    """,

    'outbound-infrastructure': """
      <div class="technical-capability-block p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Multi-Domain Outbound Infrastructure & Deliverability Fleet</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          We engineer enterprise outbound sending infrastructure designed to sustain 99%+ primary inbox placement and protect corporate brand reputation.
          Our setups provision isolated secondary domain variants across Google Workspace and Microsoft 365, configuring 2048-bit DKIM keys, strict SPF includes, DMARC reject policies, and custom tracking CNAME records to guarantee flawless DNS alignment.
          Sending fleets undergo an algorithmic 21-day automated warm-up ramp simulating organic peer-to-peer engagement, steadily establishing domain trust with Gmail and Outlook spam algorithms.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Prospect data lists are scrubbed through real-time SMTP handshake validators and MX record verifiers, eliminating catch-all addresses and suppressing bounce rates below 0.5% to avoid spam trap triggers.
          Campaign copy incorporates dynamic spintax variations, personalized firmographic references, and intent signals scraped from social discussions, driving 50% to 65% open rates and 12% to 18% executive reply rates.
          Positive replies trigger immediate webhook dispatchers that sync prospect records into GoHighLevel, HubSpot, or Salesforce with real-time SMS alerts to account executives.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-cyan-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">2048-Bit DKIM Alignment</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">21-Day Automated Warmup</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">0.5% Bounce Suppression</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Real-Time CRM Dispatch</div>
        </div>
      </div>
    """,

    'composio-integrations': """
      <div class="technical-capability-block p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Self-Hosted Composio Tooling & API Orchestration Runtime</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          We architect self-hosted Composio execution environments that establish secure bridges between AI language models and enterprise SaaS platforms.
          Operating within dedicated Docker bridge networks, our Composio runtime eliminates third-party cloud data leakage, isolating OAuth 2.0 PKCE tokens, API credentials, and internal database connection strings inside encrypted AES-256 parameter vaults.
          The platform exposes over 200 turnkey action connectors across GitHub, Slack, Linear, Jira, HubSpot, Salesforce, and Google Workspace with standardized OpenAPI signatures.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          All external tool invocations execute inside temporary sandbox containers configured with strict CPU limits, memory quotas, and execution timeouts to prevent runaway processes or unmonitored API mutations.
          An auditable telemetry dashboard logs complete JSON request payloads, return status codes, and execution timestamps, providing total governance over autonomous operations.
          Automated token refresh daemons monitor credential lifecycles, performing background refresh handshakes to prevent authentication drops during critical workflow sequences.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-cyan-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Self-Hosted Docker Bridge</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">OAuth PKCE Token Vault</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">200+ Turnkey Connectors</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Auditable Mutation Logs</div>
        </div>
      </div>
    """,

    'cloud-vps-hardening': """
      <div class="technical-capability-block p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Cloud VPS Server Hardening & Zero-Trust Docker Architecture</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          We deploy hardened production server environments on Ubuntu 24.04 LTS VPS instances fortified against unauthorized intrusion and network reconnaissance.
          Our hardening protocol disables password authentication, restricts SSH access to ed25519 cryptographic keypairs, optimizes sysctl kernel parameters against SYN flood attacks, and configures Fail2ban jails with automated IP ban policies.
          Inbound public ports are completely closed through Cloudflare Zero Trust Tunnels (cloudflared), establishing outbound encrypted mTLS tunnels that shield origin IP addresses from public port scans and direct DDoS vectors.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Application workloads execute within sandboxed Docker Compose containers running with unprivileged user permissions, read-only root filesystems, and isolated virtual network bridges.
          Encrypted database backups execute automatically on cron schedules, streaming GPG-encrypted snapshots to off-site S3 buckets with verified disaster recovery restore procedures.
          Systemd daemons oversee Prometheus node exporters and Grafana telemetry dashboards, alerting engineering teams to resource spikes, memory leaks, and service restarts in real time.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-cyan-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Zero Open Public Ports</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Cloudflare Zero Trust</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Docker Sandbox Isolation</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Encrypted Offsite Backups</div>
        </div>
      </div>
    """,

    'whop-monetization': """
      <div class="technical-capability-block p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Whop API Monetization & Membership Gating Infrastructure</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          We architect automated digital monetization funnels and membership gating systems utilizing the Whop API v2 and developer platform.
          Our implementations structure multi-tiered subscription catalogs, one-time access passes, and add-on products with granular permission entitlement mappings.
          Checkout flows are optimized for conversion with frictionless one-click payments supporting Apple Pay, Google Pay, and localized regional currencies to maximize global buyer completion rates.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Edge webhook listeners process payment confirmation events in real time, issuing cryptographic software license keys, generating account credentials, and provisioning Discord community roles in under two minutes.
          Automated dunning funnels intercept failed subscription renewals, executing intelligent payment retry handshakes and customer recovery email sequences to protect monthly recurring revenue.
          Customer cancellation webhooks automatically revoke portal access and Discord permissions, ensuring seamless tier governance with zero manual administration.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-cyan-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">One-Click Whop Checkout</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Automated License Dispatch</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Discord Role Gating</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Dunning Churn Recovery</div>
        </div>
      </div>
    """
}

# Define rich, operational deep dives for the 10 niches (each 250+ unique words)
NICHE_BLOCKS = {
    'b2b-saas': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">B2B SaaS Enterprise Systems & Operational Dynamics</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Operating in enterprise software demands balancing rapid annual recurring revenue (ARR) expansion with disciplined customer acquisition cost (CAC) payback velocity.
          Software platforms must navigate multi-tenant isolation, product-led onboarding funnels, and complex seat-based pricing structures while integrating with CRM stacks like HubSpot and Salesforce.
          As competition intensifies across cloud marketplaces, software buyers demand verified SOC2 Type II compliance, single sign-on (SSO) directory synchronization via Okta, and ironclad service level agreements.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Manual customer onboarding and ad-hoc outbound lead generation create friction that inflates net revenue churn and slows expansion revenue.
          By engineering automated inbound discovery channels, self-serve qualification workflows, and hardened data pipelines, SaaS operators reduce payback periods below twelve months.
          Leadership transitions from rented customer acquisition channels to durable software equity, protecting operating margins and maximizing enterprise valuation multiples.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">ARR Payback Velocity</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">SOC2 Type II Isolation</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">HubSpot Webhook Sync</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Churn Rate Suppression</div>
        </div>
      </div>
    """,

    'ecommerce-d2c': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">High-Volume E-Commerce Catalog & Fulfillment Logistics</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Direct-to-consumer and retail commerce platforms operate in a high-velocity environment defined by SKU catalog density, return merchandise authorizations (RMA), and seasonal demand peaks.
          Managing storefront operations across Shopify Plus, Klaviyo lifecycle flows, and third-party logistics (3PL) fulfillment networks requires absolute synchronization to prevent inventory stockouts and customer delivery disputes.
          Promotional shopping events like Black Friday Cyber Monday (BFCM) create massive traffic avalanches that test server capacity, checkout gateways, and customer support desks.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Rising paid advertising costs across Meta Ads and TikTok require e-commerce brands to unlock durable organic product search visibility and automate post-purchase support workflows.
          By deploying structured product schemas, automated ticket triage, and conversational order resolution, retail brands lower cost per acquisition while increasing repeat customer lifetime value.
          Brand operators eliminate fulfillment backlogs and customer chargebacks, achieving predictable gross margins across omni-channel sales environments.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Shopify Plus Ingestion</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">BFCM Peak Concurrency</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">3PL Fulfillment Sync</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">RMA Ticket Automation</div>
        </div>
      </div>
    """,

    'fintech': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">FinTech Institutional Compliance & Transactional Infrastructure</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Financial technology platforms and neobanks operate under intense regulatory scrutiny from the SEC, FINRA, FDIC, and banking partners.
          Core systems must ensure absolute transactional integrity across double-entry ledgers, ACH clearinghouse settlements, Fedwire routing, and automated risk underwriting.
          Every user interaction requires rigorous know-your-customer (KYC) identity verification, anti-money laundering (AML) screening, and immutable audit logging compliant with PCI-DSS 4.0 data security mandates.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Connecting modern client interfaces with legacy core banking providers like Plaid and Unit Finance introduces latency risks and reconciliation discrepancies that manual accounting cannot resolve.
          Our engineered financial systems eliminate settlement lag, automate fraud scoring, and isolate sensitive banking tokens within hardened security perimeters.
          Financial executives protect institutional trust, pass rigorous third-party compliance audits, and scale transaction throughput with zero ledger loss.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">PCI-DSS 4.0 Compliance</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Double-Entry Ledgers</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">KYC/AML Verification</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">ACH Settlement Rails</div>
        </div>
      </div>
    """,

    'healthtech-biotech': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">HealthTech Clinical Workflows & HIPAA Data Governance</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Digital health platforms, clinical trial management systems, and telemedicine providers carry strict statutory responsibilities under HIPAA and HITECH regulations.
          Managing Protected Health Information (PHI) requires end-to-end data encryption, signed Business Associate Agreements (BAAs), and isolated database boundaries to prevent clinical data compromise.
          Clinician workflows require interoperability with entrenched electronic health record (EHR) systems including Epic, Cerner, and Athenahealth utilizing standard HL7 and FHIR API protocols.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Complex medical intake questionnaires, provider scheduling bottlenecks, and prior insurance authorization friction often cause prospective patients to abandon care consultations.
          Our clinical automation architectures streamline patient onboarding, automate practitioner matching, and maintain strict cryptographic audit containment across all diagnostic data.
          Healthcare founders eliminate administrative drag, protect clinical patient confidentiality, and expand practice capacity while satisfying healthcare compliance boards.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">HIPAA Security Vaults</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">HL7 / FHIR Integration</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Clinical Triage Queues</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">EHR Scheduling Bridges</div>
        </div>
      </div>
    """,

    'proptech-realestate': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">PropTech Commercial Real Estate & Geospatial Data Feeds</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Commercial real estate platforms and brokerage portals thrive on real-time asset visibility, localized neighborhood intelligence, and rapid investor deal qualification.
          Ingesting regional Multiple Listing Service (MLS), RESO Web API, and CoStar data feeds requires robust ETL data pipelines to resolve schema conflicts, tax parcel identifiers, and zoning classifications.
          Asset managers evaluate property portfolios based on net operating income (NOI), capitalization rates, rent rolls, and commercial triple-net (NNN) lease terms.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Competing against massive national property aggregators for hyper-local commercial inquiries requires scalable programmatic landing architectures and instant broker lead triage.
          Our PropTech engineering frameworks automate regional property page generation, route qualified tenant leads directly to leasing agents under sixty seconds, and synchronize asset availability in real time.
          Brokerage executives reduce listing vacancy durations, secure high-value commercial leases, and capture high-net-worth investor acquisition interest.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">MLS & RESO Web API</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Geospatial GIS Queries</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Commercial Lease Parser</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Sub-60s Broker Routing</div>
        </div>
      </div>
    """,

    'legaltech-professional': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">LegalTech Ethical Compliance & High-Ticket Matter Management</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Corporate law practices, litigation partnerships, and professional accounting firms operate within rigid ethical frameworks defined by the ABA Model Rules and state bar associations.
          Client communications, litigation work product, and corporate transactions require strict attorney-client privilege protections, isolated document management systems (DMS) like iManage, and audit logs.
          Before opening a new matter, associates must conduct exhaustive conflict-of-interest checks across adverse parties, parent conglomerates, and executive boards.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          High-ticket legal keywords on paid advertising networks cost up to $250 per click, making traditional marketing financially perilous for independent partnerships.
          By implementing programmatic organic authority architectures and automated client onboarding questionnaires, law practices attract high-value retainers without ethical solicitation violations.
          Managing partners eliminate administrative associate drag, streamline matter onboarding, and increase realized billable realization rates across practice groups.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Privilege Vault Security</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Automated Conflict Checks</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">ABA Ethical Compliance</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Matter Intake Funnels</div>
        </div>
      </div>
    """,

    'venture-capital-private-equity': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Private Equity & Venture Capital Portfolio Operations</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Private equity sponsors and venture capital funds compete aggressively to deploy dry powder into high-growth, cash-flowing acquisitions before competitive auctions inflate purchase multiples.
          Managing modern fund operations requires proprietary outbound sourcing, confidential information memorandum (CIM) data extraction, and cap table modeling on platforms like Carta.
          Post-acquisition, operating partners must track monthly financial performance, EBITDA margins, and Rule of 40 benchmarks across dozens of holding companies for limited partner reporting.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Relying exclusively on intermediary banker dealflow compresses fund internal rates of return (IRR) and burdens acquisitions with heavy transaction fees.
          Our private capital engineering systems build automated thematic outbound pipelines that connect general partners directly with bootstrapped founders actively evaluating strategic capitalization.
          Investment teams streamline portfolio reporting, accelerate bolt-on add-acquisition sourcing, and deliver superior cash-on-cash distributions to limited partners.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Proprietary Deal Sourcing</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">EBITDA Margin Analytics</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Limited Partner Telemetry</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">CIM Extraction Pipelines</div>
        </div>
      </div>
    """,

    'edtech': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">EdTech Learning Management Systems & Cohort Engagement</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Online education platforms, university digital curricula, and skill credentialing bootcamps depend heavily on student engagement, syllabus navigation, and cohort retention.
          Integrating learning management systems (LMS) like Canvas and Moodle requires synchronizing video streaming feeds, quiz grading engines, and digital credential issuance via Credly.
          Self-paced and asynchronous education models frequently suffer from catastrophic completion drop-offs after introductory modules, destroying student lifetime value and subscription renewals.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Maintaining thousands of lecture transcripts, prerequisite mappings, and course certification pages for organic search indexing creates continuous technical overhead.
          Our EdTech engineering solutions deploy automated curriculum taxonomy indexing, instant student query resolution bots, and gated cohort discussion portals that convert casual learners into recurring members.
          Education founders protect course completion rates, improve student outcomes, and establish scalable enrollment funnels with zero manual grading drag.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Canvas & Moodle LTI</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Cohort Retention Engine</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Curriculum SEO Matrices</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Digital Credentialing</div>
        </div>
      </div>
    """,

    'cybersecurity': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Cybersecurity Enterprise Threat Defense & Compliance Rigor</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Enterprise security providers, managed detection and response (MDR) firms, and DevSecOps teams operate on the frontlines of threat mitigation against sophisticated attack vectors.
          Security systems must continuously monitor SIEM event logs, orchestrate endpoint detection and response (EDR) telemetry via CrowdStrike, and enforce zero-trust network access (ZTNA).
          Navigating enterprise procurement reviews requires comprehensive SOC2 Type II attestations, NIST CSF alignment, and automated vulnerability scanning against known CVE databases.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Long proof-of-concept evaluation cycles and technical documentation complexity frequently delay enterprise contract closures.
          Our cybersecurity engineering architectures showcase concrete architectural defensibility, isolate public web endpoints behind hardened Cloudflare edge tunnels, and automate technical documentation generation.
          Security executives compress technical evaluation cycles, demonstrate verifiable zero-trust isolation, and earn the confidence of enterprise CISOs and risk committees.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Zero-Trust Network Access</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">SIEM & EDR Log Telemetry</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">NIST & SOC2 Compliance</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">CVE Threat Hardening</div>
        </div>
      </div>
    """,

    'agency-consultancy': """
      <div class="niche-operational-block p-6 rounded-2xl bg-slate-900/70 border border-purple-500/30 mb-8">
        <h3 class="text-xl font-bold text-white mb-3 font-display">Agency High-Ticket Client Retainers & Delivery Scalability</h3>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          High-growth digital agencies, performance marketing firms, and boutique consultancies operate on a business model vulnerable to the feast-or-famine client acquisition cycle.
          Managing recurring client retainers requires automated deliverable reporting, client onboarding portals in GoHighLevel or ClickUp, and strict scope creep governance.
          When fulfillment relies on manual labor by senior directors, agency billing capacity reaches a hard ceiling, compressing gross margins and leading to leadership burnout.
        </p>
        <p class="text-sm text-slate-300 leading-relaxed mb-4">
          Traditional organic search retainers take months to show tangible ranking progress, driving impatient clients to cancel contracts before revenue realizes.
          Our programmatic agency frameworks deploy automated inbound lead generation funnels and turnkey client fulfillment systems that demonstrate rapid commercial ROI.
          Agency owners escape delivery bottlenecks, secure long-term recurring retainer agreements, and scale billing capacity without inflating payroll overhead.
        </p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-purple-300">
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">High-Ticket Retainer Funnels</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Automated Client Portals</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Scope Creep Governance</div>
          <div class="p-2 rounded bg-slate-950/80 border border-slate-800">Turnkey Delivery Pipelines</div>
        </div>
      </div>
    """
}

# Verify banned buzzwords
for k, v in SERVICE_BLOCKS.items():
    check_banned(v, f"SERVICE_BLOCK: {k}")
for k, v in NICHE_BLOCKS.items():
    check_banned(v, f"NICHE_BLOCK: {k}")
print("Banned buzzwords check passed: 0 banned words in all service and niche blocks.")

# Test injecting into the 70 HTML pages in memory
def extract_word_set(text):
    m = re.search(r'<main[\s\S]*?<\/main>', text)
    content = m.group(0) if m else text
    stripped = re.sub(r'<[^>]+>', ' ', content).lower()
    words = re.findall(r'[a-z]{3,}', stripped)
    return set(words)

def jaccard_distance(set_a, set_b):
    inter = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return 1.0 - (len(inter) / len(union))

page_sets = []

for slug in published_slugs:
    parts = slug.strip('/').split('/')
    niche_id = parts[1]
    service_id = parts[2]
    file_path = os.path.join(FRONTEND_DIR, slug.strip('/'), 'index.html')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Construct injected section
    injected_section = f"""
    <!-- Deep Domain & Technical Architecture Specifications -->
    <section class="py-16 border-b border-slate-800/60 bg-slate-950/80">
      <div class="max-w-7xl mx-auto px-6">
        {SERVICE_BLOCKS[service_id]}
        {NICHE_BLOCKS[niche_id]}
      </div>
    </section>
    """

    # If the section was already injected, replace it; otherwise insert before </main>
    if '<!-- Deep Domain & Technical Architecture Specifications -->' in html:
        html = re.sub(r'<!-- Deep Domain & Technical Architecture Specifications -->[\s\S]*?<\/section>', injected_section, html)
    else:
        html = html.replace('</main>', injected_section + '\n  </main>')

    # Check buzzwords in full html
    check_banned(html, f"Full HTML: {slug}")

    wset = extract_word_set(html)
    page_sets.append({
        'slug': slug,
        'set': wset,
        'html': html,
        'path': file_path
    })

min_dist = 1.0
min_pair = ""
violations = []
total_comparisons = 0

for i in range(len(page_sets)):
    for j in range(i + 1, len(page_sets)):
        total_comparisons += 1
        d = jaccard_distance(page_sets[i]['set'], page_sets[j]['set'])
        if d < min_dist:
            min_dist = d
            min_pair = f"{page_sets[i]['slug']} vs {page_sets[j]['slug']}"
        if d <= 0.35:
            violations.append((page_sets[i]['slug'], page_sets[j]['slug'], d))

print(f"Total Comparisons: {total_comparisons}")
print(f"Minimum Uniqueness: {min_dist * 100:.2f}% (Threshold: > 35.0%)")
print(f"Minimum Pair: {min_pair}")
print(f"Violations Count: {len(violations)}")

if len(violations) == 0:
    print("\nSUCCESS! All pairs meet >35% uniqueness threshold. Writing updated HTML files to disk...")
    for p in page_sets:
        with open(p['path'], 'w', encoding='utf-8') as f:
            f.write(p['html'])
    print(f"Successfully wrote {len(page_sets)} updated HTML pages to disk!")
else:
    print(f"First 5 violations: {violations[:5]}")
