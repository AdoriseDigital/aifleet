// Test script to verify dynamic data generation and calculate pairwise Jaccard distance across all 70 combinations
const matrixData = require('../data/taxonomy_matrix.json');

const NICHE_PROFILES = {
  'b2b-saas': {
    name: 'B2B SaaS & Enterprise Software',
    acv: '$12,000 - $60,000/yr',
    industry: 'cloud software and multi-tenant architectures',
    pain1: { title: 'High Customer Acquisition Cost (CAC) on Paid Channels', desc: 'Bidding on commercial software keywords and paid social channels drives customer acquisition payback beyond 18 months.', impact: 'Compressed operating margins and depleted venture capital runway.' },
    pain2: { title: 'SDR Outbound Burnout and High Domain Bounce Rates', desc: 'Outbound sales teams burn through prospect lists using unvalidated contact data, triggering spam filters and domain blocks.', impact: 'Damaged corporate email reputation and stalled pipeline generation.' },
    pain3: { title: 'Engineering Sprints Siphoned by Non-Core Tooling', desc: 'Senior software developers spend weeks coding internal integrations and landing templates instead of shipping product roadmap items.', impact: 'Delayed release cycles and eroded competitive advantage.' },
    humanBusiness: 'SaaS leadership struggles with escalating CAC and unpredictable sales pipelines across competitive software categories.',
    humanPersonal: 'SaaS founders face severe mental fatigue, context-switching between sprint blockers, investor updates, and client churn escalations.'
  },
  'ecommerce-d2c': {
    name: 'High-Volume E-Commerce & D2C Brands',
    acv: '$500,000 - $10M GMV',
    industry: 'retail commerce, digital storefronts, and omni-channel distribution',
    pain1: { title: 'Peak Promotional Traffic Support Desk Overload', desc: 'Spikes during product drops and holidays overwhelm customer care desks, driving first response times beyond 12 hours.', impact: 'Customer churn, payment chargebacks, and lost repeat purchase volume.' },
    pain2: { title: 'Rising Paid Social Ad Costs and ROAS Volatility', desc: 'Algorithmic changes and tracking limitations reduce ROAS on paid channels, squeezing gross retail margins.', impact: 'Unpredictable profitability and unsustainable customer acquisition costs.' },
    pain3: { title: 'SKU Catalog Content Fragmentation', desc: 'Maintaining thousands of product detail descriptions and regional landing pages leads to thin, duplicate indexation.', impact: 'Algorithmic search penalties and loss of organic product ranking.' },
    humanBusiness: 'Brand executives navigate severe margin compression and operational inventory bottlenecks across digital sales channels.',
    humanPersonal: 'Brand operators endure chronic insomnia and anxiety watching real-time ad dashboards and fulfillment logistics.'
  },
  'fintech': {
    name: 'FinTech & Digital Financial Services',
    acv: '$25,000 - $150,000/yr',
    industry: 'financial platforms, payment gateways, and banking infrastructure',
    pain1: { title: 'Stringent Regulatory and SOC2 Audit Burdens', desc: 'Financial compliance demands rigid audit trails, encryption standards, and strict verification protocols across every system transaction.', impact: 'Delayed product deployment schedules and expensive legal compliance audits.' },
    pain2: { title: 'Legacy Banking Core Integration Latency', desc: 'Connecting modern software with legacy core banking providers causes transaction timeouts and fragile webhook connections.', impact: 'Failed payments, reconciliations discrepancies, and frustrated institutional clients.' },
    pain3: { title: 'Rising Costs of Manual Fraud Underwriting', desc: 'Human verification teams cannot keep pace with transaction velocity, slowing user onboarding and loan approvals.', impact: 'High customer drop-off during onboarding and exposure to fraudulent losses.' },
    humanBusiness: 'Financial technology leaders require ironclad compliance, zero transaction loss, and auditable infrastructure.',
    humanPersonal: 'FinTech executives carry immense personal liability and stress regarding regulatory scrutiny, system uptime, and capital security.'
  },
  'healthtech-biotech': {
    name: 'HealthTech & Digital Health Platforms',
    acv: '$30,000 - $120,000/yr',
    industry: 'clinical software, telemedicine, and healthcare data systems',
    pain1: { title: 'HIPAA and Protected Health Information (PHI) Exposure Risk', desc: 'Strict regulatory boundaries restrict how patient data is transferred, processed, and stored across distributed cloud servers.', impact: 'Catastrophic statutory penalties and loss of medical institutional trust.' },
    pain2: { title: 'EHR and EMR Interoperability Bottlenecks', desc: 'Exchanging clinical data with entrenched electronic health record systems requires bespoke HL7 and FHIR connectors.', impact: 'Fragmented provider schedules and delayed clinical diagnostic reporting.' },
    pain3: { title: 'Inpatient and Telehealth Intake Drop-Off', desc: 'Complex multi-step medical intake forms cause prospective patients to abandon appointment bookings midway.', impact: 'Reduced clinical capacity utilization and lost healthcare practice revenue.' },
    humanBusiness: 'HealthTech enterprises must scale clinician workflows and patient engagement while strictly guaranteeing medical confidentiality.',
    humanPersonal: 'Healthcare technology founders balance clinical governance, patient outcomes, and relentless technical delivery demands.'
  },
  'proptech-realestate': {
    name: 'PropTech & Commercial Real Estate Platforms',
    acv: '$15,000 - $80,000/yr',
    industry: 'commercial brokerage, asset syndication, and real estate portals',
    pain1: { title: 'Fragmented MLS and Property Listing Data Feeds', desc: 'Ingesting disparate regional real estate listing feeds causes schema conflicts, outdated listing statuses, and broken links.', impact: 'Inaccurate property listings and degraded user trust on commercial portals.' },
    pain2: { title: 'Hyper-Local Search Ranking Disadvantages', desc: 'Competing against entrenched national portals for localized neighborhood commercial queries requires massive page scale.', impact: 'Inability to capture high-value buyer and tenant searches organically.' },
    pain3: { title: 'Slow Manual Broker Lead Qualification and Routing', desc: 'Inbound inquiries sit in general mailboxes for hours, allowing rival brokerages to contact prospective tenants first.', impact: 'Lost commission opportunities and elongated commercial leasing cycles.' },
    humanBusiness: 'Real estate operators require automated asset visibility, regional search presence, and rapid buyer triage.',
    humanPersonal: 'Brokerage founders and asset managers struggle with round-the-clock deal pressure, frantic investor calls, and closing delays.'
  },
  'legaltech-professional': {
    name: 'LegalTech & High-Ticket Professional Services',
    acv: '$20,000 - $100,000/yr',
    industry: 'law firms, accounting partnerships, and advisory practices',
    pain1: { title: 'Prohibitive Search Advertising Click Costs', desc: 'Commercial legal search terms cost between $80 and $250 per click on Google Ads, making paid acquisition financially risky.', impact: 'Excessive client acquisition costs and low conversion return on marketing capital.' },
    pain2: { title: 'Strict Ethical Rules Governing Outbound Solicitation', desc: 'Bar associations enforce rigid standards regarding direct marketing and prospective client communication.', impact: 'Risk of bar sanctions or brand damage from uncalibrated marketing tactics.' },
    pain3: { title: 'Cumbersome Client Onboarding and Conflict Checking', desc: 'Manual client intake and conflict verification consume expensive associate hours before billable work begins.', impact: 'Delayed matter initiation and administrative overhead eating practice profits.' },
    humanBusiness: 'Professional firms need ethical, high-authority client acquisition and streamlined matter onboarding.',
    humanPersonal: 'Managing partners endure grueling 80-hour workweeks, billable hour pressures, and administrative burdens.'
  },
  'venture-capital-private-equity': {
    name: 'Venture Capital & Private Equity Firms',
    acv: '$50M - $1B AUM',
    industry: 'investment management, fund syndication, and portfolio operations',
    pain1: { title: 'High Reliance on Intermediary Brokered Dealflow', desc: 'Competing in banker-led auctions inflates acquisition multiples and compresses fund internal rate of return (IRR).', impact: 'Sub-optimal fund returns and excessive fees paid to third-party intermediaries.' },
    pain2: { title: 'Fragmented Portfolio KPI Tracking and Reporting', desc: 'Gathering monthly financials from dozens of portfolio companies involves manual spreadsheets and inconsistent metrics.', impact: 'Delayed reporting to limited partners and missed operational intervention windows.' },
    pain3: { title: 'Low Inbound Visibility with Bootstrapped Founders', desc: 'Top-quartile founders building profitable businesses seek investors with proven operational and technology capabilities.', impact: 'Missing proprietary investment opportunities before rivals enter the cap table.' },
    humanBusiness: 'Investment funds require proprietary thesis-driven sourcing and streamlined holding operations.',
    humanPersonal: 'General partners face immense pressure to deploy dry powder prudently while maintaining founder relationships.'
  },
  'edtech': {
    name: 'EdTech & Online Learning Platforms',
    acv: '$10,000 - $50,000/yr',
    industry: 'digital curricula, university credentials, and learning platforms',
    pain1: { title: 'Severe Student Completion and Retention Drop-Off', desc: 'Self-paced learners struggle with motivation, causing completion rates to plunge below 15% after introductory units.', impact: 'Elevated student churn, reduced lifetime customer value, and negative reviews.' },
    pain2: { title: 'Complex Course Catalog Taxonomy and Search Fragmentation', desc: 'Organizing thousands of lectures, syllabi, and skill prerequisites into search-friendly structures is manually intensive.', impact: 'Poor organic discoverability for specialized training courses and degrees.' },
    pain3: { title: 'Weak Community Engagement and Monetization Funnels', desc: 'Student discussions remain scattered across chat apps without converting participants into recurring members.', impact: 'Lost subscription revenue and diminished brand community affinity.' },
    humanBusiness: 'Educational institutions require scalable enrollment architectures and automated student support.',
    humanPersonal: 'Course creators and edtech founders face chronic burnout answering repetitive student questions around the clock.'
  },
  'cybersecurity': {
    name: 'Enterprise Cybersecurity & DevSecOps',
    acv: '$40,000 - $200,000/yr',
    industry: 'network security, vulnerability management, and infrastructure protection',
    pain1: { title: 'Extended Enterprise Sales Cycles and Technical Proofs of Concept', desc: 'Enterprise security reviews require exhaustive documentation, SOC2 reports, and architectural verification.', impact: 'Sales cycles stretching beyond 9 months, tying up senior engineering capacity.' },
    pain2: { title: 'High Barrier in Explaining Technical Architecture to Buyers', desc: 'Security vendors struggle to convey zero-trust network benefits without creating dense, inaccessible documentation.', impact: 'Lost opportunities with executive decision-makers who lack technical backgrounds.' },
    pain3: { title: 'Vulnerability Disclosure and Threat Surface Expansion', desc: 'Managing public-facing services while preventing unauthorized ingress requires continuous server hardening.', impact: 'Risk of security incidents, unauthorized data access, and regulatory disclosure.' },
    humanBusiness: 'Cybersecurity providers require authoritative technical positioning and verifiable zero-trust deployments.',
    humanPersonal: 'Security officers work in perpetual triage, constantly anticipating zero-day exploits and threat alerts.'
  },
  'agency-consultancy': {
    name: 'Digital Agencies & High-Growth Consultancies',
    acv: '$5,000 - $30,000/mo',
    industry: 'professional services, growth consulting, and client delivery',
    pain1: { title: 'The Feast-or-Famine Pipeline Rollercoaster', desc: 'Focusing exclusively on client fulfillment causes new business prospecting to halt, leading to sudden revenue dips.', impact: 'Unpredictable cash flow, hiring hesitation, and quarterly business anxiety.' },
    pain2: { title: 'Capacity Bottlenecks and Fulfillment Overwork', desc: 'Senior agency directors spend hours performing manual fulfillment tasks instead of scaling agency operations.', impact: 'Capped agency revenue and severe leadership burnout.' },
    pain3: { title: 'Difficulty Proving Measurable Organic ROI to Retainer Clients', desc: 'Traditional SEO retainers take months to demonstrate progress, leading to premature client cancellations.', impact: 'High client turnover, lowered lifetime value, and perpetual sales hunting.' },
    humanBusiness: 'Consulting agencies require predictable inbound retainers, automated fulfillment, and rapid ROI delivery.',
    humanPersonal: 'Agency owners endure relentless client demands, scope creep, and late-night slide deck preparation.'
  }
};

const SERVICE_PROFILES = {
  'pseo-engine': {
    name: 'Programmatic SEO Engine',
    shortName: 'pSEO Engine',
    badge: 'Automated Inbound Engineering',
    deepDive: 'Our programmatic SEO engine deploys high-performance Next.js App Router routes powered by Incremental Static Regeneration. By compiling hundreds of structured, schema-validated landing pages on edge networks, your brand captures long-tail transactional searches without manual authoring.',
    techSpec: 'Edge-cached SSR, sub-45ms TTFB, automated XML sitemap chunking, IndexNow protocols, and complete JSON-LD microdata.',
    cap1: { title: 'Combinatorial Keyword Matrix Engine', spec: 'Ingests niche data tables and maps commercial intent variations across services, locations, and buyer roles.', deliverable: 'Structured JSON taxonomy matrix with targeted keyword clustering.' },
    cap2: { title: 'Next.js App Router Edge Compilation', spec: 'Deploys server-rendered static templates with zero layout shift, Tailwind CSS styling, and sub-45ms TTFB.', deliverable: 'Production edge repository with automated static export.' },
    cap3: { title: 'Automated Schema.org Microdata Injection', spec: 'Embeds comprehensive ProfessionalService, Organization, FAQPage, and BreadcrumbList structured data.', deliverable: 'Rich Results validated JSON-LD schema blocks on all routes.' },
    cap4: { title: 'Dynamic XML Sitemap & Indexing Pipeline', spec: 'Automates sitemap chunking (5,000 URLs/file), dynamic lastmod timestamps, and automated search console pings.', deliverable: 'Continuous indexing pipeline submitting new pages directly to search engines.' },
    faq1: { q: 'How does programmatic SEO integrate into our existing domain?', a: 'We build modular Next.js route handlers that mount seamlessly under your target subfolder or custom subdomain.' },
    faq2: { q: 'How do you prevent duplicate content penalties from search engines?', a: 'Every page features unique data variables, localized market metrics, distinct problem statements, and dynamic FAQs ensuring high mathematical uniqueness.' },
    faq3: { q: 'How quickly do programmatic pages begin ranking on Google?', a: 'With automated XML sitemap syndication and IndexNow API pings, search bots crawl new pages within 48 to 72 hours of edge deployment.' },
    faq4: { q: 'Can we connect demo request forms directly to our CRM?', a: 'Yes. Inbound form submissions trigger secure webhook payloads directly into HubSpot, Salesforce, or your chosen CRM.' },
    faq5: { q: 'Who retains intellectual property rights to the codebase?', a: 'Your organization owns 100% of the compiled Next.js templates, taxonomy matrices, and production assets.' },
    businessPillar: { title: 'Scalable Inbound Organic Engine', desc: 'Captures commercial intent search queries at scale, replacing expensive paid ad clicks with durable organic rankings.' },
    metric: { val: '+340%', lbl: 'Pipeline Expansion', sub: 'Qualified organic demo requests' }
  },
  'ai-agents': {
    name: 'Autonomous AI Agents & Agentic Workflows',
    shortName: 'Autonomous AI Agents',
    badge: 'Agentic Workflow Engineering',
    deepDive: 'We engineer deterministic autonomous agent swarms that execute complex business processes without human intervention. Built with robust tool-calling boundaries, state machines, and human-in-the-loop review checkpoints, our agents handle customer triage, data enrichment, and back-office operations.',
    techSpec: 'Multi-agent orchestration, LangGraph state management, sandboxed tool execution, token streaming, and function-calling schemas.',
    cap1: { title: 'Multi-Agent Autonomous Orchestration', spec: 'Coordinates specialized LLM agents for task decomposition, verification, and autonomous execution.', deliverable: 'State-machine driven agent cluster with deterministic workflow logic.' },
    cap2: { title: 'Deterministic Tool-Calling Architecture', spec: 'Integrates external APIs, database drivers, and webhook triggers with strict parameter validation.', deliverable: 'Hardened tool schemas preventing hallucinated parameters or unauthorized actions.' },
    cap3: { title: 'Human-in-the-Loop Review Verification', spec: 'Routes high-stakes decisions and exceptions to human reviewers via Slack or web dashboard before execution.', deliverable: 'Approval checkpoint interface with auditable decision logs.' },
    cap4: { title: 'Self-Hosted High-Concurrency Runtime', spec: 'Runs containerized agent services on dedicated infrastructure with sub-second inference caching.', deliverable: 'Dockerized agent stack with automated scaling and health monitors.' },
    faq1: { q: 'How do autonomous agents prevent hallucinations during execution?', a: 'We enforce strict JSON Schema validation on all tool parameters, accompanied by deterministic fallback routines and boundary checks.' },
    faq2: { q: 'Can agents connect to our existing internal databases?', a: 'Yes. Agents connect securely through authenticated REST APIs, GraphQL endpoints, or read-only database replicas.' },
    faq3: { q: 'What happens when an agent encounters an edge case it cannot solve?', a: 'Uncertain requests trigger an immediate escalation event, pausing execution and notifying human operators via Slack or email.' },
    faq4: { q: 'How are sensitive API keys and client credentials protected?', a: 'Credentials are encrypted at rest using AES-256 and injected into agent runtimes via secure environment vaults.' },
    faq5: { q: 'What response latency can we expect for customer-facing agents?', a: 'Our optimized tool-calling pipelines achieve sub-1.5 second initial response times across text chat and webhook interfaces.' },
    businessPillar: { title: '24/7 Autonomous Operations', desc: 'Automates repetitive triage, customer inquiries, and data entry workflows with sub-second latency and verified accuracy.' },
    metric: { val: '< 1.5s', lbl: 'Average Response Time', sub: 'Instantaneous automated resolution' }
  },
  'web-app-engineering': {
    name: 'Full-Stack Next.js & Web App Engineering',
    shortName: 'Next.js Web Engineering',
    badge: 'Modern Web Engineering',
    deepDive: 'We construct high-performance, enterprise-grade web applications utilizing Next.js App Router, React Server Components, and TypeScript. Our architecture prioritizes sub-50ms edge rendering, zero layout shift, accessibility, and clean database integrations.',
    techSpec: 'React Server Components, Next.js App Router, TypeScript, Tailwind CSS, Prisma ORM, and edge serverless runtimes.',
    cap1: { title: 'React Server Components & App Router Architecture', spec: 'Builds modular page components that render on the server, eliminating client-side JavaScript overhead.', deliverable: 'Production Next.js application codebase with optimized bundle splitting.' },
    cap2: { title: 'Type-Safe Database Integration & API Routes', spec: 'Integrates PostgreSQL, Supabase, or MongoDB through Prisma ORM with comprehensive end-to-end typing.', deliverable: 'Type-safe database models, migrations, and validated server actions.' },
    cap3: { title: 'Enterprise UI Design & Component Systems', spec: 'Implements responsive, accessible UI components styled with Tailwind CSS and Framer Motion micro-interactions.', deliverable: 'Complete reusable design component library adhering to WCAG standards.' },
    cap4: { title: 'Continuous Integration & Edge Deployment CI/CD', spec: 'Configures automated GitHub Actions pipelines, linting gates, unit testing, and edge CDN deployments.', deliverable: 'Automated CI/CD pipeline deploying preview and production releases.' },
    faq1: { q: 'Why do you prioritize Next.js App Router over traditional SPA frameworks?', a: 'Next.js App Router provides server-rendered speed, superior SEO visibility, reduced client bundle sizes, and instant edge caching.' },
    faq2: { q: 'Can this web application scale to millions of monthly visitors?', a: 'Yes. By leveraging edge caching and serverless execution, our web architectures scale effortlessly with zero server maintenance.' },
    faq3: { q: 'How do you ensure zero cumulative layout shift (CLS)?', a: 'We enforce explicit font preloading, image aspect ratios, and server-side skeleton renders to eliminate layout reflows.' },
    faq4: { q: 'Do you provide full source code ownership upon project completion?', a: 'Yes. All source code, design systems, and deployment configurations are transferred directly to your organization GitHub repository.' },
    faq5: { q: 'How do you handle authentication and user session security?', a: 'We implement industry-standard authentication protocols including OAuth 2.0, magic links, and encrypted HTTP-only session cookies.' },
    businessPillar: { title: 'High-Converting Digital Presence', desc: 'Builds blazing-fast web applications with 99+ Core Web Vitals, elevating user conversion and brand authority.' },
    metric: { val: '99/100', lbl: 'Lighthouse Score', sub: 'Flawless Core Web Vitals rating' }
  },
  'outbound-infrastructure': {
    name: 'Cold Outbound Infrastructure & Lead Engine',
    shortName: 'Cold Outbound Engine',
    badge: 'Outbound Pipeline Engineering',
    deepDive: 'We build enterprise cold email and lead generation infrastructure designed to maintain pristine sender reputation and 99%+ inbox placement. Our systems combine dedicated sending domains, automated mailbox warm-up routines, DNS security records, and AI-personalized copywriting.',
    techSpec: 'SPF, DKIM, DMARC, custom tracking domains, mailbox rotation clusters, real-time MX validation, and CRM webhook pipelines.',
    cap1: { title: 'Multi-Domain Sending Infrastructure Setup', spec: 'Configures isolated secondary domains with Google Workspace and Microsoft 365 sending mailboxes.', deliverable: 'Turnkey domain portfolio configured with dedicated IP pools.' },
    cap2: { title: 'DNS Authentication & Deliverability Hardening', spec: 'Deploys 2048-bit DKIM keys, strict SPF records, DMARC policies, and custom tracking CNAME records.', deliverable: 'Fully authenticated DNS configurations passing deliverability audits.' },
    cap3: { title: 'Automated Mailbox Warm-Up & Health Monitoring', spec: 'Simulates organic peer-to-peer sending behavior over 21 days to establish sender authority with ISPs.', deliverable: 'Automated warm-up network with real-time reputation health alerts.' },
    cap4: { title: 'High-Intent Prospect Enrichment & Personalization', spec: 'Scrapes firmographic and social intent data, validating contact addresses to maintain sub-1% bounce rates.', deliverable: 'Enriched verified lead prospect lists with dynamic personalization tags.' },
    faq1: { q: 'Why do we need separate secondary domains for outbound outreach?', a: 'Using secondary domains protects your primary corporate domain reputation from spam complaints and temporary ISP rate-limits.' },
    faq2: { q: 'How long does it take to safely warm up a new cluster of mailboxes?', a: 'We adhere to a conservative 21-day algorithmic ramp-up schedule before launching full-scale outbound campaigns.' },
    faq3: { q: 'What email deliverability and open rates can we expect?', a: 'Our clients consistently maintain 99%+ deliverability and 45% to 65% open rates across warmed enterprise mailboxes.' },
    faq4: { q: 'How do you prevent emails from landing in Google and Outlook spam filters?', a: 'We implement strict DNS alignment, rotate across multiple sending inboxes, restrict daily volume per mailbox, and avoid spam trigger words.' },
    faq5: { q: 'Can outbound replies sync directly into our team sales inbox?', a: 'Yes. Incoming positive replies forward automatically to your account executives with lead context and notification alerts.' },
    businessPillar: { title: 'Predictable Outbound Dealflow', desc: 'Fills sales calendars with qualified decision-makers through hardened email infrastructure and verified contact data.' },
    metric: { val: '99.4%', lbl: 'Inbox Placement', sub: 'Pristine primary inbox delivery' }
  },
  'composio-integrations': {
    name: 'Composio Tooling & API Orchestration',
    shortName: 'Composio Integrations',
    badge: 'Agent Tooling Architecture',
    deepDive: 'We architect self-hosted Composio execution environments connecting AI models directly to over 200 software applications, databases, and enterprise platforms. By providing secure OAuth credential token vaults, function execution sandboxes, and audit logs, our integrations empower agents to act safely.',
    techSpec: 'Self-hosted Composio runtime, OAuth 2.0 PKCE token management, Docker sandboxing, rate limiting, and webhook dispatchers.',
    cap1: { title: 'Self-Hosted Composio Engine Runtime', spec: 'Deploys private Composio infrastructure on dedicated servers with zero third-party data leakage.', deliverable: 'Production Composio deployment with isolated container network.' },
    cap2: { title: '200+ SaaS Tool Connectors & Custom Actions', spec: 'Configures pre-built and bespoke action connectors for GitHub, Slack, Jira, Linear, HubSpot, and Google Workspace.', deliverable: 'Validated tool registry ready for autonomous LLM function calling.' },
    cap3: { title: 'Secure OAuth Token Vault & Credential Lifecycle', spec: 'Manages user authentication, token refresh flows, and scoped permission boundaries in an encrypted vault.', deliverable: 'Zero-trust credential storage system with automated token rotation.' },
    cap4: { title: 'Execution Sandboxing & Auditable Telemetry', spec: 'Executes third-party API mutations inside temporary sandbox containers with complete transaction logging.', deliverable: 'Audit dashboard recording agent tool invocations, inputs, and outputs.' },
    faq1: { q: 'What is Composio and how does it help our agent workflows?', a: 'Composio provides standard authentication, tool definitions, and API bindings so LLMs can interact with hundreds of SaaS platforms effortlessly.' },
    faq2: { q: 'Why run a self-hosted Composio runtime instead of cloud services?', a: 'Self-hosting keeps your corporate API tokens, internal databases, and client credentials entirely within your private cloud perimeter.' },
    faq3: { q: 'How does Composio handle OAuth refresh token expirations?', a: 'The Composio token manager monitors expiration timestamps and executes background refresh handshakes autonomously.' },
    faq4: { q: 'Can we create custom internal API tools for proprietary software?', a: 'Yes. We build custom OpenAPI and Swagger schemas that register seamlessly as callable tools in your Composio workspace.' },
    faq5: { q: 'How do you prevent agents from making unauthorized or dangerous API calls?', a: 'We configure strict role-based permission policies, parameter validation schemas, and rate-limiting thresholds on sensitive endpoints.' },
    businessPillar: { title: 'Unified Ecosystem Connectivity', desc: 'Bridges language models to existing software stacks, enabling end-to-end automation across corporate apps.' },
    metric: { val: '200+', lbl: 'Verified Tool Connectors', sub: 'Turnkey SaaS and database integrations' }
  },
  'cloud-vps-hardening': {
    name: 'Cloud VPS & Docker Infrastructure Hardening',
    shortName: 'VPS & Cloud Infrastructure',
    badge: 'Zero-Trust Infrastructure',
    deepDive: 'We deploy hardened, zero-trust cloud infrastructure on Ubuntu VPS servers behind Cloudflare edge proxies. Our setup isolates multi-container Docker workloads, eliminates open public ports via Cloudflare Tunnels, enforces SSH key-only access, and configures automated failover monitoring.',
    techSpec: 'Ubuntu 24.04 LTS hardening, Cloudflare Zero Trust tunnels, Docker Compose daemon isolation, UFW firewalls, and Fail2ban.',
    cap1: { title: 'Ubuntu Server Hardening & Kernel Optimization', spec: 'Disables root password login, configures SSH ed25519 key access, enables sysctl kernel protections, and audits open ports.', deliverable: 'Hardened Linux operating system baseline meeting CIS compliance standards.' },
    cap2: { title: 'Cloudflare Zero Trust Tunnel Configuration', spec: 'Routes all inbound web traffic through encrypted Cloudflare edge tunnels, closing all inbound firewall ports.', deliverable: 'Zero-open-port network configuration completely shielding server IP addresses.' },
    cap3: { title: 'Docker Compose Container Sandboxing', spec: 'Isolates applications into dedicated virtual bridge networks with resource quotas and unprivileged user execution.', deliverable: 'Production Docker Compose architecture with encrypted environment secrets.' },
    cap4: { title: 'Automated Snapshot Backups & Health Telemetry', spec: 'Deploys cron-driven encrypted database backups to offsite S3 buckets alongside automated system health alerts.', deliverable: 'Automated disaster recovery pipeline and Grafana/Prometheus telemetry.' },
    faq1: { q: 'How does a Cloudflare Tunnel protect our server from DDoS attacks?', a: 'Cloudflare Tunnels establish outbound-only connections to Cloudflare edge nodes, keeping your server IP address completely hidden from the public internet.' },
    faq2: { q: 'What happens if a Docker container crashes or experiences high memory usage?', a: 'Docker daemon restart policies immediately relaunch failed containers, while systemd monitors overall memory and CPU thresholds.' },
    faq3: { q: 'How do you handle automated SSL and TLS certificate renewals?', a: 'SSL certificates are managed automatically at the Cloudflare edge and through Let Encrypt automated certbot daemons.' },
    faq4: { q: 'Can we access internal administrative dashboards securely?', a: 'Yes. Administrative interfaces are protected behind Cloudflare Access with two-factor authentication and role-based email verification.' },
    faq5: { q: 'How often are security patches and updates applied to the VPS?', a: 'We configure unattended-upgrades on Ubuntu to apply critical operating system security patches automatically without downtime.' },
    businessPillar: { title: 'Bulletproof Operational Security', desc: 'Protects mission-critical applications and customer data from unauthorized ingress, DDoS attacks, and downtime.' },
    metric: { val: '100%', lbl: 'Zero-Trust Isolation', sub: 'Zero open public ports on origin servers' }
  },
  'whop-monetization': {
    name: 'Whop Store & Digital Monetization Engine',
    shortName: 'Whop Monetization Systems',
    badge: 'Digital Monetization Systems',
    deepDive: 'We build automated monetization systems and membership gating utilizing the Whop API and developer platform. From tier entitlement logic and digital product delivery to automated Discord role assignment and churn mitigation webhooks, we turn audience traffic into recurring revenue.',
    techSpec: 'Whop API v2, webhook listeners, license key provisioning, Discord bot gating, checkout optimization, and Stripe integration.',
    cap1: { title: 'Whop Product Tier Architecture & Entitlements', spec: 'Structures subscription tiers, one-time passes, and add-on products with granular permission entitlement mappings.', deliverable: 'Configured Whop store catalog ready for high-conversion checkouts.' },
    cap2: { title: 'Automated Webhook License Provisioning', spec: 'Listens for payment success events and issues cryptographic license keys or account credentials instantly.', deliverable: 'Zero-latency fulfillment webhook service with automated retry queues.' },
    cap3: { title: 'Discord & Community Access Synchronization', spec: 'Synchronizes active customer subscriptions with Discord server roles and private portal access permissions.', deliverable: 'Automated member onboarding bot revoking access automatically upon cancellation.' },
    cap4: { title: 'Checkout Optimization & Churn Mitigation', spec: 'Deploys localized checkout currency displays, frictionless one-click payments, and dunning workflows to rescue failed renewals.', deliverable: 'Revenue retention funnel recovering abandoned checkouts and expired payment methods.' },
    faq1: { q: 'Why choose Whop over traditional payment platforms for digital products?', a: 'Whop offers industry-leading conversion rates, integrated affiliate portals, automatic Discord role management, and built-in buyer discovery.' },
    faq2: { q: 'How do customers access their digital products after purchase?', a: 'Upon completed checkout, buyers receive instant access via their Whop customer portal alongside automated email credentials.' },
    faq3: { q: 'Can we accept payments from international customers across multiple currencies?', a: 'Yes. Whop handles multi-currency transactions, regional payment methods, and automated sales tax compliance worldwide.' },
    faq4: { q: 'What happens when a customer cancels their recurring membership?', a: 'Webhooks trigger immediately upon cancellation or non-payment, revoking access to protected Discord channels and software portals.' },
    faq5: { q: 'Can we integrate Whop purchase events into our marketing email sequences?', a: 'Yes. Purchase and churn events dispatch webhook payloads into your email CRM to trigger automated customer lifecycle sequences.' },
    businessPillar: { title: 'Automated Revenue Realization', desc: 'Converts digital audience traffic into recurring cash flow through frictionless checkouts and automated digital fulfillment.' },
    metric: { val: '+28%', lbl: 'Checkout Conversion', sub: 'Optimized frictionless payment funnels' }
  }
};

function extractWordSet(text) {
  const stripped = text.replace(/<[^>]+>/g, ' ').toLowerCase();
  const words = stripped.match(/[a-z]{3,}/g) || [];
  return new Set(words);
}

function calculateJaccardDistance(setA, setB) {
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return 1 - (intersection.size / union.size);
}

// Generate sample text for each combination and check uniqueness
const niches = Object.keys(NICHE_PROFILES);
const services = Object.keys(SERVICE_PROFILES);

const generatedWordSets = [];

niches.forEach(nicheId => {
  services.forEach(serviceId => {
    const n = NICHE_PROFILES[nicheId];
    const s = SERVICE_PROFILES[serviceId];
    
    // Construct rich sample text
    const sampleText = `
      ${n.name} ${s.name} ${s.badge} ${n.industry} ${n.acv}
      ${s.deepDive}
      ${s.techSpec}
      ${n.pain1.title} ${n.pain1.desc} ${n.pain1.impact}
      ${n.pain2.title} ${n.pain2.desc} ${n.pain2.impact}
      ${n.pain3.title} ${n.pain3.desc} ${n.pain3.impact}
      ${s.cap1.title} ${s.cap1.spec} ${s.cap1.deliverable}
      ${s.cap2.title} ${s.cap2.spec} ${s.cap2.deliverable}
      ${s.cap3.title} ${s.cap3.spec} ${s.cap3.deliverable}
      ${s.cap4.title} ${s.cap4.spec} ${s.cap4.deliverable}
      ${s.faq1.q} ${s.faq1.a}
      ${s.faq2.q} ${s.faq2.a}
      ${s.faq3.q} ${s.faq3.a}
      ${s.faq4.q} ${s.faq4.a}
      ${s.faq5.q} ${s.faq5.a}
      ${n.humanBusiness} ${s.businessPillar.title} ${s.businessPillar.desc}
      ${n.humanPersonal}
      ${s.metric.val} ${s.metric.lbl} ${s.metric.sub}
    `;
    
    generatedWordSets.push({
      slug: `/solutions/${nicheId}/${serviceId}`,
      nicheId,
      serviceId,
      wordSet: extractWordSet(sampleText)
    });
  });
});

console.log(`Generated ${generatedWordSets.length} combination profiles.`);

let minDistance = 1.0;
let minPair = '';
let underThreshold = 0;
let totalPairs = 0;

for (let i = 0; i < generatedWordSets.length; i++) {
  for (let j = i + 1; j < generatedWordSets.length; j++) {
    totalPairs++;
    const dist = calculateJaccardDistance(generatedWordSets[i].wordSet, generatedWordSets[j].wordSet);
    if (dist < minDistance) {
      minDistance = dist;
      minPair = `${generatedWordSets[i].slug} vs ${generatedWordSets[j].slug}`;
    }
    if (dist <= 0.35) {
      underThreshold++;
      console.log(`VIOLATION: ${generatedWordSets[i].slug} vs ${generatedWordSets[j].slug}: ${(dist*100).toFixed(2)}%`);
    }
  }
}

console.log(`Total Pairs Tested: ${totalPairs}`);
console.log(`Minimum Uniqueness: ${(minDistance * 100).toFixed(2)}%`);
console.log(`Minimum Pair: ${minPair}`);
console.log(`Pairs under 35%: ${underThreshold}`);
