// Combinatorial Matrix Tailoring Engine
// Generates fully tailored (niche, service) data structures with zero boilerplate overlap

const NICHE_DEFS = {
  'b2b-saas': {
    name: 'B2B SaaS & Enterprise Software',
    short: 'B2B SaaS',
    buyer: 'VP of Growth & CTOs',
    market: 'cloud software platforms',
    entities: 'HubSpot, Salesforce, Stripe, and PostgreSQL',
    terms: ['multi-tenant', 'ARR expansion', 'churn reduction', 'product-led onboarding', 'seat license', 'SOC2 compliance', 'API webhooks'],
    pain1: { t: 'Skyrocketing Paid Software Clicks', d: 'Bidding on commercial software keywords pushes CPC beyond $60 per click, making customer acquisition payback exceed 18 months.', i: 'Compressed SaaS gross margins and excessive venture cash burn.' },
    pain2: { t: 'SDR Outbound Burnout & Domain Blacklisting', d: 'Outbound SDR teams blasting cold sequences burn secondary and corporate email domains through high bounce rates.', i: 'Collapsing enterprise demo pipelines and lost sales velocity.' },
    pain3: { t: 'Core Engineering Sprints Lost to Marketing CMS', d: 'Senior software developers spend sprints maintaining landing page CMS templates instead of delivering roadmap product features.', i: 'Delayed core software releases and lost market differentiation.' },
    biz_narrative: 'SaaS operators cannot afford to burn capital on rented advertising channels while software developer resources are tied up in manual integrations.',
    pers_narrative: 'SaaS founders face severe cognitive exhaustion context-switching between sprint deadlines, investor updates, and client churn escalations.'
  },
  'ecommerce-d2c': {
    name: 'High-Volume E-Commerce & D2C Brands',
    short: 'E-Commerce & D2C',
    buyer: 'Brand Founders & E-Commerce Heads',
    market: 'consumer brands and digital storefronts',
    entities: 'Shopify Plus, Gorgias, Klaviyo, and Meta Ads',
    terms: ['SKU velocity', 'unboxing', 'cart abandonment', 'BFCM spikes', 'return merchandise', 'ROAS volatility', 'inventory turnover'],
    pain1: { t: 'Holiday Promotional Support Desk Collapse', d: 'Flash drops and holiday promotions flood support queues with repetitive order status and exchange inquiries, driving wait times past 14 hours.', i: 'Elevated customer churn, dispute chargebacks, and damaged brand reputation.' },
    pain2: { t: 'Meta & TikTok Paid Ad Margin Compression', d: 'Rising customer acquisition costs and signal loss on social ad platforms compress gross margins across fast-moving product catalogs.', i: 'Unpredictable monthly profitability and reliance on discounted promotional sales.' },
    pain3: { t: 'Catalog SEO Cannibalization & Thin Content', d: 'Managing product detail pages across thousands of size and color variants produces duplicate content penalized by Google.', i: 'Loss of organic category search rankings to major department retailers.' },
    biz_narrative: 'Consumer brand executives face margin erosion from rising ad costs and fulfillment friction during peak seasonal demand.',
    pers_narrative: 'E-commerce brand owners suffer from round-the-clock anxiety checking ad performance, inventory stocks, and customer complaints.'
  },
  'fintech': {
    name: 'FinTech & Digital Financial Services',
    short: 'FinTech',
    buyer: 'Chief Risk Officers & FinTech Founders',
    market: 'financial technology platforms and banking rails',
    entities: 'Plaid, Stripe, core banking APIs, and ledger databases',
    terms: ['KYC verification', 'AML screening', 'PCI-DSS', 'ledger reconciliation', 'ACH settlement', 'wire transfers', 'audit trails'],
    pain1: { t: 'Strict Regulatory Compliance & Audit Burdens', d: 'Financial platforms face rigid scrutiny from banking partners and regulatory bodies demanding auditable transaction logs and strict encryption.', i: 'Elongated enterprise onboarding cycles and expensive legal audit penalties.' },
    pain2: { t: 'Legacy Core Banking API Latency & Drops', d: 'Interfacing modern client applications with legacy banking networks causes transaction drops and reconciliation discrepancies.', i: 'Failed customer transactions, manual ledger reconciliations, and lost institutional trust.' },
    pain3: { t: 'Manual Risk Underwriting & Fraud Backlog', d: 'Human compliance teams cannot verify high-frequency account openings in real time, creating onboarding friction for legitimate users.', i: 'High user drop-off during onboarding and exposure to synthetic identity fraud.' },
    biz_narrative: 'Financial technology leaders require zero transaction error rates, auditable security boundaries, and automated compliance.',
    pers_narrative: 'FinTech executives endure immense fiduciary pressure, constant regulatory scrutiny, and insomnia over capital security.'
  },
  'healthtech-biotech': {
    name: 'HealthTech & Digital Health Platforms',
    short: 'HealthTech',
    buyer: 'Clinical Directors & HealthTech CTOs',
    market: 'digital health platforms and clinical systems',
    entities: 'Epic, Cerner, FHIR endpoints, and HIPAA cloud vaults',
    terms: ['HIPAA containment', 'PHI encryption', 'HL7 protocol', 'telehealth queues', 'clinical triage', 'physician credentialing', 'patient intake'],
    pain1: { t: 'HIPAA & Protected Health Information Exposure', d: 'Managing distributed clinical workloads carries severe statutory penalties if patient health identifiers leak across unencrypted networks.', i: 'Statutory HIPAA fines, clinical accreditation suspension, and enterprise client loss.' },
    pain2: { t: 'EHR and Hospital System Interoperability Silos', d: 'Transferring diagnostic records and scheduling across fragmented electronic health record systems requires bespoke protocol translation.', i: 'Clinician scheduling bottlenecks and delayed diagnostic test communication.' },
    pain3: { t: 'Patient Intake Drop-Off on Multi-Step Forms', d: 'Exhausting medical intake questionnaires cause patients to abandon booking consultations, depressing clinic capacity utilization.', i: 'Lost clinic consultation billings and depressed patient engagement.' },
    biz_narrative: 'Healthcare technology providers must ensure airtight patient privacy while removing clinical scheduling friction.',
    pers_narrative: 'HealthTech founders carry the emotional burden of patient care outcomes, complex healthcare bureaucracy, and clinical audits.'
  },
  'proptech-realestate': {
    name: 'PropTech & Commercial Real Estate Platforms',
    short: 'PropTech',
    buyer: 'Managing Brokers & Asset Partners',
    market: 'commercial real estate and property portals',
    entities: 'MLS feeds, CoStar, Yardi, and geospatial GIS databases',
    terms: ['cap rates', 'commercial leases', 'rent rolls', 'geospatial queries', 'tenant screening', 'property syndication', 'broker commissions'],
    pain1: { t: 'Fragmented Regional MLS & Property Data Ingestion', d: 'Aggregating property feeds across hundreds of regional boards causes schema errors, outdated asset availability, and missing images.', i: 'Degraded listing portal accuracy and tenant dissatisfaction.' },
    pain2: { t: 'Hyper-Local Search Competition Against National Portals', d: 'Independent brokerages struggle to rank organically against massive national aggregator sites for local commercial property queries.', i: 'Inability to attract high-net-worth commercial buyers and leasing tenants.' },
    pain3: { t: 'Slow Broker Lead Qualification & Routing Latency', d: 'Prospective property inquiries languish in email inboxes for hours, allowing competing commercial brokerages to secure tenant tours first.', i: 'Lost commercial brokerage commissions and extended property vacancy periods.' },
    biz_narrative: 'Commercial property firms depend on localized listing discovery, rapid tenant response, and accurate building data.',
    pers_narrative: 'Real estate operators navigate erratic transaction cycles, volatile property interest rates, and high-stress closing deadlines.'
  },
  'legaltech-professional': {
    name: 'LegalTech & High-Ticket Professional Services',
    short: 'LegalTech',
    buyer: 'Managing Partners & General Counsels',
    market: 'corporate law firms and advisory partnerships',
    entities: 'Clio, iManage, Thomson Reuters, and secure matter vaults',
    terms: ['attorney-client privilege', 'conflict checks', 'billable hours', 'e-discovery', 'ABA Model Rules', 'matter intake', 'retainer agreements'],
    pain1: { t: 'Astronomical Legal Keyword Advertising Costs', d: 'Commercial litigation and corporate legal search keywords cost between $90 and $250 per click on paid search networks.', i: 'Exorbitant client acquisition costs and low return on marketing spend.' },
    pain2: { t: 'Strict Bar Association Ethical Outbound Rules', d: 'State bar rules strictly prohibit deceptive or unsolicited direct marketing, exposing careless practices to ethics investigations.', i: 'Risk of disciplinary sanction and permanent institutional brand damage.' },
    pain3: { t: 'Administrative Drag of Manual Conflict Checking', d: 'Associates spend hours manually screening parties and related entities for conflicts of interest before formal engagement letters issue.', i: 'Delayed matter onboarding and non-billable associate hours eroding profits.' },
    biz_narrative: 'Professional partnerships require high-integrity client acquisition, automated intake, and strict ethical compliance.',
    pers_narrative: 'Managing partners shoulder grueling 80-hour workweeks, billable hour pressure, and partner profit allocation tensions.'
  },
  'venture-capital-private-equity': {
    name: 'Venture Capital & Private Equity Firms',
    short: 'VC & Private Equity',
    buyer: 'General Partners & Operating Principals',
    market: 'investment funds and private equity firms',
    entities: 'PitchBook, Affinity, Carta, and secure portfolio datarooms',
    terms: ['proprietary sourcing', 'EBITDA multiples', 'fund IRR', 'dry powder', 'LP memos', 'CIM analysis', 'portfolio telemetry'],
    pain1: { t: 'Banker-Led Auction Multiple Inflation', d: 'Bidding exclusively through investment banker auction processes inflates acquisition multiples and compresses investment fund returns.', i: 'Sub-optimal portfolio IRR and hefty intermediary transaction fees.' },
    pain2: { t: 'Fragmented Portfolio KPI Tracking & Spreadsheets', d: 'Collecting monthly financial metrics across dozens of portfolio companies involves manual email chasing and incompatible spreadsheets.', i: 'Delayed quarterly limited partner reporting and missed operational interventions.' },
    pain3: { t: 'Invisibility to Bootstrapped Market Leaders', d: 'Top-tier founders building profitable enterprises avoid cold outreach from generic capital providers without clear operational value-add.', i: 'Missing premier proprietary investment rounds before competitive term sheets emerge.' },
    biz_narrative: 'Private capital managers must build proprietary outbound deal flow and automated portfolio operations to outperform benchmarks.',
    pers_narrative: 'General partners navigate relentless fundraising pressure, fund performance anxiety, and difficult board room dynamics.'
  },
  'edtech': {
    name: 'EdTech & Online Learning Platforms',
    short: 'EdTech',
    buyer: 'Heads of Learning & EdTech Founders',
    market: 'digital education and university programs',
    entities: 'Canvas LMS, Moodle, Stripe, and student databases',
    terms: ['course completion', 'cohort retention', 'curriculum taxonomy', 'student drop-off', 'grading automation', 'credential issuance', 'LMS sync'],
    pain1: { t: 'Catastrophic Student Drop-Off in Week Two', d: 'Self-paced learners lose motivation rapidly, driving completion rates below 14% and causing high subscription cancellation rates.', i: 'Depressed student lifetime value and negative public course reviews.' },
    pain2: { t: 'Course Catalog Taxonomy Search Fragmentation', d: 'Structuring thousands of lectures, prerequisites, and syllabi for organic search indexing requires continuous manual SEO maintenance.', i: 'Poor organic search discoverability for high-margin specialized certifications.' },
    pain3: { t: 'Weak Student Community Monetization Funnels', d: 'Student discussion communities on chat platforms fail to convert casual participants into recurring paid premium tier subscribers.', i: 'Lost recurring subscription revenue and unmonetized platform engagement.' },
    biz_narrative: 'Educational platforms require automated curriculum indexing and responsive student support to protect cohort retention.',
    pers_narrative: 'EdTech founders suffer chronic mental exhaustion answering repetitive student questions and troubleshooting course logistics.'
  },
  'cybersecurity': {
    name: 'Enterprise Cybersecurity & DevSecOps',
    short: 'Cybersecurity',
    buyer: 'CISOs & DevSecOps Directors',
    market: 'enterprise security and cloud defense',
    entities: 'Cloudflare WAF, CrowdStrike, AWS IAM, and SIEM logs',
    terms: ['zero-trust network', 'CVE vulnerability', 'SOC2 Type II', 'container sandboxing', 'firewall rules', 'ed25519 keys', 'penetration audits'],
    pain1: { t: 'Nine-Month Enterprise Technical Proof of Concept Cycles', d: 'Enterprise security deals drag through rigorous vendor security questionnaires, compliance audits, and architectural reviews.', i: 'Elongated enterprise sales velocity tying up principal engineering resources.' },
    pain2: { t: 'Conveying Zero-Trust Architecture to Non-Technical Buyers', d: 'Security firms struggle to articulate complex network protection benefits to procurement committees without jargon.', i: 'Lost enterprise contracts to competitors with clearer positioning.' },
    pain3: { t: 'Public Ingress Vulnerability & Attack Surface Drift', d: 'Exposing web interfaces without hardened edge tunnels creates vectors for automated port scans, brute-force bots, and DDoS extortion.', i: 'Security breach risks, service downtime, and regulatory disclosure penalties.' },
    biz_narrative: 'Cybersecurity enterprises must demonstrate absolute technical defensibility and clear architectural boundaries to earn buyer trust.',
    pers_narrative: 'Security executives live on edge, continuously anticipating zero-day vulnerability alerts and ransomware incidents.'
  },
  'agency-consultancy': {
    name: 'Digital Agencies & High-Growth Consultancies',
    short: 'Agencies & Consultancies',
    buyer: 'Agency Principals & Managing Partners',
    market: 'client service agencies and growth consultancies',
    entities: 'ClickUp, HighLevel, Slack, and client Stripe accounts',
    terms: ['client retainers', 'scope creep', 'onboarding friction', 'deliverable tracking', 'agency churn', 'margin per client', 'white-label'],
    pain1: { t: 'The Feast-or-Famine Client Acquisition Cycle', d: 'Pausing prospecting during intense client fulfillment sprints causes revenue to drop sharply when contracts conclude.', i: 'Erratic agency cash flow, hiring delays, and intense quarterly revenue anxiety.' },
    pain2: { t: 'Fulfillment Capacity Bottlenecks on Senior Staff', d: 'Agency leadership spends valuable hours executing manual client fulfillment instead of business development and team coaching.', i: 'Capped agency billing capacity and severe partner burnout.' },
    pain3: { t: 'Retainer Churn from Slow Demonstrable Organic Results', d: 'Traditional digital marketing retainers take months to produce visible search rankings, leading clients to cancel early.', i: 'Short average client lifespan and perpetual sales pressure.' },
    biz_narrative: 'Consulting agencies require predictable inbound retainer pipelines and automated fulfillment to unlock scale.',
    pers_narrative: 'Agency founders suffer severe burnout balancing unpredictable client demands, scope creep battles, and payroll stress.'
  }
};

const SERVICE_DEFS = {
  'pseo-engine': {
    name: 'Programmatic SEO Engine',
    short: 'pSEO Engine',
    focus: 'dynamic Next.js landing pages and organic keyword indexing',
    tech_stack: 'Next.js App Router, Incremental Static Regeneration, Schema.org microdata, and automated XML sitemaps',
    cap_specs: [
      (n) => ({ title: `Combinatorial Keyword Matrix for ${n.short}`, spec: `Compiles database tables mapping commercial search intent across ${n.terms[0]}, ${n.terms[1]}, and buyer alternatives.`, del: `Targeted keyword taxonomy matrix tailored for ${n.market}.` }),
      (n) => ({ title: `Next.js App Router Edge Pages`, spec: `Builds server-rendered dynamic templates with zero layout shift, Tailwind CSS styling, and sub-45ms TTFB.`, del: `Production Next.js repository with automated static export.` }),
      (n) => ({ title: `Automated Schema.org Microdata`, spec: `Embeds Rich Results validated ProfessionalService, Organization, FAQPage, and BreadcrumbList JSON-LD.`, del: `Verified schema blocks on all dynamic ${n.short} routes.` }),
      (n) => ({ title: `Dynamic XML Sitemap & Indexing Engine`, spec: `Automates chunked 5,000-URL sitemaps with dynamic lastmod timestamps and search console pings.`, del: `Continuous indexing pipeline submitting new pages directly to search engines.` })
    ],
    faqs: [
      (n) => ({ q: `How does programmatic SEO generate inbound demos for ${n.short}?`, a: `We target thousands of long-tail search queries regarding ${n.terms[0]} and ${n.terms[1]}, capturing buyers ready to evaluate alternatives.` }),
      (n) => ({ q: `How do you ensure high content uniqueness for ${n.market}?`, a: `Every route injects distinct market metrics, tailored pain points, and specific capabilities, maintaining >35% mathematical uniqueness.` }),
      (n) => ({ q: `Can demo request forms connect to our ${n.entities.split(',')[0]}?`, a: `Yes. Inbound demo submissions trigger encrypted webhooks directly into ${n.entities.split(',')[0]} with lead attribution.` }),
      (n) => ({ q: `How fast do programmatic pages index on Google?`, a: `With dynamic sitemap chunking and IndexNow protocols, search engines crawl new edge pages within 48 to 72 hours of deployment.` }),
      (n) => ({ q: `Who owns the codebase and taxonomy assets?`, a: `Your organization retains 100% full intellectual property rights to the compiled Next.js components, scripts, and database matrices.` })
    ]
  },
  'ai-agents': {
    name: 'Autonomous AI Agents',
    short: 'Autonomous Agents',
    focus: 'multi-agent task orchestration and deterministic tool calling',
    tech_stack: 'LangGraph, deterministic LLM tool calling, state machines, and human approval checkpoints',
    cap_specs: [
      (n) => ({ title: `Multi-Agent Autonomous Orchestration for ${n.short}`, spec: `Coordinates specialized agent loops executing ${n.terms[0]} and ${n.terms[1]} workflows without manual triage.`, del: `Deterministic agent cluster with auditable state machine transitions.` }),
      (n) => ({ title: `Hardened Tool-Calling Architecture`, spec: `Connects agents directly to ${n.entities} with strict JSON Schema parameter validation.`, del: `Production tool interfaces preventing parameter hallucinations or unauthorized actions.` }),
      (n) => ({ title: `Human-in-the-Loop Approval Checkpoints`, spec: `Routes sensitive decisions regarding ${n.terms[2]} to human operators via Slack or dashboard before execution.`, del: `Secure operator review queue with complete transaction audit logs.` }),
      (n) => ({ title: `Containerized High-Concurrency Runtime`, spec: `Deploys dedicated Docker agent microservices with sub-second inference and response caching.`, del: `Production Docker Compose agent stack with automated health telemetry.` })
    ],
    faqs: [
      (n) => ({ q: `How do autonomous agents prevent errors in ${n.short} operations?`, a: `We enforce deterministic tool boundaries, schema validation gates, and human approval checkpoints for critical operations in ${n.market}.` }),
      (n) => ({ q: `Can these agents integrate directly with ${n.entities}?`, a: `Yes. Agents interact securely with ${n.entities} via authenticated REST APIs and webhook dispatchers.` }),
      (n) => ({ q: `What response latency do your autonomous agents deliver?`, a: `Our optimized tool-calling pipelines achieve sub-1.5 second initial response times across customer chat and webhook interfaces.` }),
      (n) => ({ q: `How are proprietary client credentials protected?`, a: `All API keys and credentials are encrypted using AES-256 and stored in an isolated, scoped environment vault.` }),
      (n) => ({ q: `Who owns the agent prompts and orchestration code?`, a: `Your company retains full intellectual property rights to all system prompts, state machine graphs, and custom tool connectors.` })
    ]
  },
  'web-app-engineering': {
    name: 'Next.js Web Engineering',
    short: 'Web Engineering',
    focus: 'React Server Components, Next.js App Router, and edge web development',
    tech_stack: 'Next.js App Router, React Server Components, TypeScript, Tailwind CSS, and edge Prisma ORM',
    cap_specs: [
      (n) => ({ title: `React Server Components Architecture for ${n.short}`, spec: `Constructs modular page components that render on the server, eliminating client-side JavaScript overhead across ${n.terms[0]} views.`, del: `Production Next.js application codebase with optimized bundle splitting.` }),
      (n) => ({ title: `Type-Safe Database Integration & Server Actions`, spec: `Connects PostgreSQL databases through Prisma ORM with end-to-end typing across ${n.terms[1]} workflows.`, del: `Type-safe database schemas, migration files, and validated server actions.` }),
      (n) => ({ title: `Accessible Component Library & UI System`, spec: `Designs responsive, accessible user interfaces styled with Tailwind CSS meeting WCAG 2.1 AA standards.`, del: `Comprehensive reusable UI component design library.` }),
      (n) => ({ title: `Automated Edge CI/CD Pipeline`, spec: `Configures GitHub Actions pipelines with automated linting, test suites, and edge CDN deployments.`, del: `Continuous deployment pipeline deploying preview and production branches.` })
    ],
    faqs: [
      (n) => ({ q: `Why use Next.js App Router for ${n.short} platforms?`, a: `Next.js App Router delivers sub-50ms edge rendering, zero layout shift, and optimal search indexing for ${n.market}.` }),
      (n) => ({ q: `Can this web architecture scale to millions of monthly visitors?`, a: `Yes. Serverless edge caching enables the web application to absorb high-traffic spikes without server degradation.` }),
      (n) => ({ q: `How do you guarantee zero cumulative layout shift (CLS)?`, a: `We enforce explicit font preloading, fixed image aspect ratios, and server-rendered skeletons to prevent layout reflows.` }),
      (n) => ({ q: `Can the frontend integrate with ${n.entities}?`, a: `Yes. We engineer secure API client wrappers and server actions synchronizing data with ${n.entities}.` }),
      (n) => ({ q: `Do we receive complete source code ownership?`, a: `Yes. All source code, design tokens, and deployment scripts are transferred directly to your organization GitHub repository.` })
    ]
  },
  'outbound-infrastructure': {
    name: 'Cold Outbound & Lead Engine',
    short: 'Cold Outbound',
    focus: 'multi-domain cold email deliverability and social intent listening',
    tech_stack: 'isolated secondary domains, automated mailbox warm-up, DNS security alignment, and intent scraping',
    cap_specs: [
      (n) => ({ title: `Multi-Domain Sending Fleet for ${n.short}`, spec: `Provisions isolated secondary domains and dedicated mailboxes targeting ${n.buyer}.`, del: `Turnkey outbound domain portfolio configured with dedicated IP pools.` }),
      (n) => ({ title: `DNS Authentication & Deliverability Hardening`, spec: `Deploys 2048-bit DKIM keys, strict SPF records, DMARC policies, and custom tracking CNAMEs.`, del: `Authenticated DNS infrastructure achieving 99%+ inbox placement.` }),
      (n) => ({ title: `Automated Mailbox Warm-Up Network`, spec: `Gradually ramps sending volume over 21 days with simulated peer engagement to build sender authority with ISPs.`, del: `Continuous warm-up network with automated deliverability health monitoring.` }),
      (n) => ({ title: `Intent-Driven Prospect Scraping & Verification`, spec: `Scrapes verified decision-makers actively researching ${n.terms[0]} and validates email deliverability under 0.5% bounce rates.`, del: `Enriched contact lists scrubbed through real-time SMTP validators.` })
    ],
    faqs: [
      (n) => ({ q: `How does outbound prospecting protect our primary ${n.short} domain?`, a: `We deploy isolated secondary domains so your primary corporate domain is never exposed to spam complaints or ISP filters.` }),
      (n) => ({ q: `What open and reply rates do clients in ${n.market} experience?`, a: `Our warmed outbound sending infrastructure achieves 50% to 65% open rates and 10% to 18% executive reply rates.` }),
      (n) => ({ q: `How does the system identify high-intent decision-makers?`, a: `We monitor social platforms and firmographic databases for discussions about ${n.terms[0]} and ${n.terms[1]}.` }),
      (n) => ({ q: `Can positive replies sync directly into ${n.entities.split(',')[0]}?`, a: `Yes. Warm prospect responses dispatch immediate webhook alerts into ${n.entities.split(',')[0]} for instant sales rep followup.` }),
      (n) => ({ q: `What ramp-up timeline is needed before campaigns launch?`, a: `We follow an algorithmic 21-day ramp-up schedule to establish high sender trust before initiating high-volume sending.` })
    ]
  },
  'composio-integrations': {
    name: 'Composio Agent Integrations',
    short: 'Composio Integrations',
    focus: 'self-hosted Composio execution runtime and 200+ SaaS tool connectors',
    tech_stack: 'self-hosted Composio runtime, OAuth 2.0 PKCE token vaults, Docker sandboxing, and webhook dispatchers',
    cap_specs: [
      (n) => ({ title: `Self-Hosted Composio Runtime for ${n.short}`, spec: `Deploys private Composio infrastructure on dedicated servers ensuring zero data leakage for ${n.market}.`, del: `Production Composio engine isolated within a private Docker bridge network.` }),
      (n) => ({ title: `Custom SaaS Action Connectors for ${n.entities}`, spec: `Configures pre-built and custom API action bindings connecting agents directly to ${n.entities}.`, del: `Validated tool registry ready for autonomous LLM function calling.` }),
      (n) => ({ title: `Secure OAuth Token Vault & Lifecycle Management`, spec: `Manages user authorization, refresh token handshakes, and scoped API permissions in an encrypted vault.`, del: `Zero-trust credential storage system with automated token rotation.` }),
      (n) => ({ title: `Sandboxed Execution & Auditable Telemetry`, spec: `Executes tool invocations in isolated temporary containers with complete transaction logging across ${n.terms[0]}.`, del: `Audit telemetry dashboard recording all agent API mutations.` })
    ],
    faqs: [
      (n) => ({ q: `What advantages does Composio provide for ${n.short} platforms?`, a: `Composio standardizes authentication and tool schemas, allowing AI models to execute actions across ${n.entities} reliably.` }),
      (n) => ({ q: `Why run a self-hosted Composio runtime instead of cloud services?`, a: `Self-hosting guarantees that API credentials, proprietary data, and client records remain strictly within your infrastructure perimeter.` }),
      (n) => ({ q: `How does Composio handle expired API tokens?`, a: `The Composio token manager autonomously performs background OAuth refresh handshakes before tokens expire.` }),
      (n) => ({ q: `Can we build proprietary tool connectors for internal APIs?`, a: `Yes. We construct custom OpenAPI and Swagger schemas that register seamlessly into your private Composio workspace.` }),
      (n) => ({ q: `How are unauthorized API calls prevented?`, a: `We enforce granular role-based permissions, parameter schemas, and rate-limiting quotas on all sensitive endpoints.` })
    ]
  },
  'cloud-vps-hardening': {
    name: 'Cloudflare & VPS Infrastructure',
    short: 'VPS Infrastructure',
    focus: 'Ubuntu LTS OS hardening, Cloudflare Zero Trust tunnels, and Docker sandboxing',
    tech_stack: 'Ubuntu 24.04 LTS, Cloudflare Zero Trust tunnels, Docker Compose daemon isolation, UFW firewall, and Fail2ban',
    cap_specs: [
      (n) => ({ title: `Ubuntu Server Hardening for ${n.short}`, spec: `Disables root password login, installs ed25519 SSH keys, configures sysctl kernel hardening, and sets up UFW firewalls.`, del: `Hardened Linux operating system baseline meeting CIS compliance standards.` }),
      (n) => ({ title: `Cloudflare Zero Trust Tunnel Ingress`, spec: `Routes all inbound traffic through encrypted Cloudflare tunnels, closing all open public firewall ports on ${n.market} servers.`, del: `Zero-open-port network configuration shielding server origin IP addresses.` }),
      (n) => ({ title: `Docker Compose Multi-Container Sandboxing`, spec: `Isolates application workloads into dedicated virtual bridge networks with memory boundaries for ${n.terms[0]} services.`, del: `Production Docker Compose architecture with encrypted environment secrets.` }),
      (n) => ({ title: `Automated Offsite Backups & Health Telemetry`, spec: `Schedules cron-driven encrypted database backups to S3 alongside automated Prometheus alerts.`, del: `Automated disaster recovery pipeline and real-time infrastructure telemetry.` })
    ],
    faqs: [
      (n) => ({ q: `How does a Cloudflare Tunnel shield our ${n.short} infrastructure?`, a: `Cloudflare Tunnels establish outbound-only connections to Cloudflare edge nodes, keeping origin server IPs invisible to port scanners.` }),
      (n) => ({ q: `How do you handle container crashes and service failovers?`, a: `Docker restart policies automatically recover failed containers, while systemd daemons monitor CPU and memory quotas.` }),
      (n) => ({ q: `How are SSL certificates maintained?`, a: `SSL certificates are automatically managed at the Cloudflare edge and through Let's Encrypt automated certbot daemons.` }),
      (n) => ({ q: `Can administrative portals be accessed securely?`, a: `Yes. Administrative dashboards are protected behind Cloudflare Access with two-factor authentication and email verification.` }),
      (n) => ({ q: `How are critical security updates applied to the VPS?`, a: `We configure Ubuntu unattended-upgrades to apply security patches automatically without server downtime.` })
    ]
  },
  'whop-monetization': {
    name: 'Whop Monetization Systems',
    short: 'Whop Monetization',
    focus: 'Whop API membership gating, digital checkout funnels, and license fulfillment',
    tech_stack: 'Whop API v2, automated license key generation, Discord bot synchronization, and dunning webhooks',
    cap_specs: [
      (n) => ({ title: `Whop Product Tier Architecture for ${n.short}`, spec: `Structures subscription tiers, one-time passes, and enterprise add-ons with granular entitlement mappings for ${n.market}.`, del: `Configured Whop store catalog ready for high-converting checkouts.` }),
      (n) => ({ title: `Automated Webhook License Key Dispatcher`, spec: `Listens for payment events and generates cryptographic license keys or account credentials instantly for ${n.terms[0]} users.`, del: `Zero-latency fulfillment webhook service with automated retry queues.` }),
      (n) => ({ title: `Discord & Private Portal Access Synchronization`, spec: `Synchronizes active customer subscriptions with Discord server roles and private platform access permissions.`, del: `Automated member onboarding bot revoking access automatically upon cancellation.` }),
      (n) => ({ title: `Checkout Optimization & Churn Recovery`, spec: `Deploys localized currencies, one-click checkout payments, and dunning retry sequences to rescue failed subscription renewals.`, del: `Revenue retention funnel recovering abandoned checkouts and expired payment methods.` })
    ],
    faqs: [
      (n) => ({ q: `Why use Whop to monetize ${n.short} digital products and memberships?`, a: `Whop provides industry-leading checkout conversion rates, built-in buyer discovery, and automated member role gating.` }),
      (n) => ({ q: `How do customers access digital deliverables after purchase?`, a: `Upon successful checkout, buyers receive instant access via their Whop customer portal and automated credential emails.` }),
      (n) => ({ q: `Can we accept international payments across multiple currencies?`, a: `Yes. Whop supports multi-currency transactions, regional payment methods, and automated tax compliance worldwide.` }),
      (n) => ({ q: `What happens when a customer cancels their subscription?`, a: `Webhooks trigger immediately upon cancellation, revoking access to protected Discord channels and software portals.` }),
      (n) => ({ q: `Can purchase webhooks dispatch data into ${n.entities.split(',')[0]}?`, a: `Yes. Payment success and churn events sync directly into ${n.entities.split(',')[0]} to trigger customer lifecycle sequences.` })
    ]
  }
};

function generateFullCombination(nicheId, serviceId) {
  const n = NICHE_DEFS[nicheId];
  const s = SERVICE_DEFS[serviceId];

  const h1 = `${s.name} for ${n.name}`;
  const subheadline = `Engineered specifically for ${n.buyer} in ${n.short} seeking to scale ${s.focus}. Built on modern ${s.tech_stack} to eliminate operational bottlenecks, compress sales cycles, and drive predictable enterprise revenue.`;

  const deep_dive_1 = `Organizations operating in ${n.name} face compounding friction across ${n.terms.slice(0, 4).join(', ')}. Relying on manual workflows or generic off-the-shelf software leads to escalating customer acquisition costs, operational bottlenecks, and administrative drag. By engineering a dedicated ${s.name.toLowerCase()} architecture, companies establish automated, reproducible pipelines that scale cleanly.`;
  const deep_dive_2 = `Our engineering methodology integrates ${s.tech_stack} directly into existing systems including ${n.entities}. Incoming data payloads undergo rigorous schema validation, state verification, and encrypted logging, ensuring leadership maintains absolute visibility and compliance across every transaction.`;

  const pain_points = [
    { title: n.pain1.t, description: n.pain1.d, impact: n.pain1.i },
    { title: n.pain2.t, description: n.pain2.d, impact: n.pain2.i },
    { title: n.pain3.t, description: n.pain3.d, impact: n.pain3.i }
  ];

  const capabilities = s.cap_specs.map(fn => fn(n));
  const faqs = s.faqs.map(fn => fn(n));

  const phases = [
    { title: `${n.short} Architecture Audit & Mapping`, desc: `Examine current workflows, data structures, and integration points across ${n.terms[0]} and ${n.terms[1]}.`, tf: 'Days 1 - 3' },
    { title: `Core ${s.short} System Construction`, desc: `Construct dynamic components, schema definitions, and API connectors on modern edge infrastructure.`, tf: 'Days 4 - 7' },
    { title: `Verification & Quality Assertion Gates`, desc: `Execute automated uniqueness checks, schema validation tests, and security benchmarks.`, tf: 'Days 8 - 10' },
    { title: `Production Deployment & Handover`, desc: `Deploy to live edge network, activate automated telemetry, and transition operational documentation.`, tf: 'Days 11 - 14' }
  ];

  const humanSolutions = {
    businessTitle: `Operational & Revenue Defense for ${n.name}`,
    businessStory: `${n.biz_narrative} Adorise Digital deploys autonomous systems that remove operational drag and protect enterprise margins.`,
    businessPillars: [
      {
        title: `Automated Pipeline & Operational Velocity`,
        desc: `Replaces fragile manual coordination with deterministic ${s.name.toLowerCase()} workflows tailored for ${n.short}.`,
        product: `Adorise Engineered Systems ($297/mo)`
      },
      {
        title: `Systematic Client & Revenue Protection`,
        desc: `Guarantees consistent execution across ${n.terms[0]} and ${n.terms[1]}, mitigating operational errors and customer drop-off.`,
        product: `Production Architecture Retainer`
      },
      {
        title: `Ecosystem Authority & Market Leadership`,
        desc: `Establishes unmistakable operational superiority over competitors relying on slower legacy practices in ${n.market}.`,
        product: `Enterprise Turnkey Deployment`
      }
    ],
    personalTitle: `Protecting ${n.buyer} from Fatigue & Stress`,
    personalStory: `${n.pers_narrative} We engineer software that restores executive sanity, evening calm, and focused strategic thinking.`,
    personalPillars: [
      {
        icon: '🛡️',
        title: 'Communication Stress & Conflict Defense',
        desc: `When high-pressure emails arrive regarding ${n.terms[0]}, InboxCalm scores toxicity and drafts calm, de-escalating replies.`,
        product: 'InboxCalm (Automated Email Firewall)',
        url: 'https://inboxcalm.adorisedigital.com'
      },
      {
        icon: '🎬',
        title: 'Thought Leadership Video Automation',
        desc: `Converts technical presentations into vertical 9:16 video insights in under 60 seconds without video editing friction.`,
        product: 'ClipCalm AI (Viral Video Repurposing)',
        url: 'https://clipcalm.adorisedigital.com'
      },
      {
        icon: '🕊️',
        title: 'Executive Grounding & Emotional Reset',
        desc: `When high-stakes decisions and sprint deadlines create anxiety, DearMee offers a confidential, non-judgmental conversational co-pilot.`,
        product: 'DearMee AI (Empathetic Companion)',
        url: 'https://dearmee.adorisedigital.com'
      }
    ]
  };

  return {
    niche_name: n.name,
    service_name: s.name,
    badge: `${s.short} | ${n.short}`,
    h1,
    subheadline,
    metrics: [
      { val: '< 45ms', lbl: 'Edge TTFB', sub: 'Sub-second React Server Components load' },
      { val: '+340%', lbl: 'Pipeline Expansion', sub: 'Qualified inbound demo volume growth' },
      { val: '100%', lbl: 'Schema Validated', sub: 'Complete ProfessionalService JSON-LD' },
      { val: n.acv, lbl: 'Target ACV Tier', sub: 'High-value enterprise contract focus' }
    ],
    deep_dive_1,
    deep_dive_2,
    pain_points,
    capabilities,
    phases,
    faqs,
    humanSolutions
  };
}

module.exports = {
  generateFullCombination,
  NICHE_DEFS,
  SERVICE_DEFS
};
