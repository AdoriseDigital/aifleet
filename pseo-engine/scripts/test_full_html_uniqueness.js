// Full HTML simulation script to test exact verify_pseo.js uniqueness on generated HTML
const fs = require('fs');
const path = require('path');
const matrixData = require('../data/taxonomy_matrix.json');
const { getProductCTA } = require('./compile_pseo.js');

const NICHE_DATA = {
  'b2b-saas': {
    name: 'B2B SaaS & Enterprise Software',
    acv: '$12,000 - $60,000/yr',
    industry: 'cloud software and multi-tenant architectures',
    pain_points: [
      {
        title: 'High Customer Acquisition Cost (CAC) on Paid Ad Channels',
        description: 'Bidding wars on commercial software keywords push click costs over $60, creating unsustainable payback periods beyond 18 months.',
        impact: 'Compressed operating margins and depleted growth capital.'
      },
      {
        title: 'SDR Outbound Burnout and Domain Reputation Degradation',
        description: 'Junior sales reps blast unverified cold contact lists, triggering spam filters and burning primary corporate email domains.',
        impact: 'Permanent domain blacklisting and collapsed sales pipeline.'
      },
      {
        title: 'Engineering Capacity Siphoned into Marketing Integrations',
        description: 'Core product engineers spend critical sprint cycles building custom landing pages and third-party webhook integrations.',
        impact: 'Delayed product releases and competitor feature parity loss.'
      }
    ],
    niche_deep_dive: 'B2B software platforms face escalating market saturation where buyer discovery increasingly happens through specific integration comparisons, technical documentation, and role-based workflows rather than generic advertising.'
  },
  'ecommerce-d2c': {
    name: 'High-Volume E-Commerce & D2C Brands',
    acv: '$500,000 - $10M GMV',
    industry: 'retail commerce, digital storefronts, and omni-channel distribution',
    pain_points: [
      {
        title: 'Holiday and Product Drop Support Ticket Avalanches',
        description: 'Promotional traffic spikes overwhelm customer support staff with repetitive order tracking and return inquiries, pushing wait times past 14 hours.',
        impact: 'Customer churn, payment chargebacks, and lost repeat purchase revenue.'
      },
      {
        title: 'Paid Social ROAS Compression and Tracking Degradation',
        description: 'Rising CPMs on Meta and TikTok paired with privacy tracking limitations compress gross margins and inflate blended customer acquisition costs.',
        impact: 'Erratic cash flow and unsustainable advertising dependency.'
      },
      {
        title: 'Catalog Content Fragmentation and Duplicate Penalties',
        description: 'Managing product descriptions across thousands of SKU variants produces thin content that search engine crawlers penalize or de-index.',
        impact: 'Erosion of organic search rankings and lost organic merchandise traffic.'
      }
    ],
    niche_deep_dive: 'High-volume consumer brands operate on thin net margins where inventory holding costs, rapid fulfillment expectations, and customer retention dictate long-term brand enterprise valuation.'
  },
  'fintech': {
    name: 'FinTech & Digital Financial Services',
    acv: '$25,000 - $150,000/yr',
    industry: 'financial platforms, payment gateways, and banking infrastructure',
    pain_points: [
      {
        title: 'Strict Regulatory Compliance and SOC2 Type II Audit Burdens',
        description: 'Financial applications must maintain immutable audit trails, encryption standards, and strict verification protocols across every ledger mutation.',
        impact: 'Delayed production releases and expensive legal compliance penalties.'
      },
      {
        title: 'Legacy Core Banking Interoperability Latency',
        description: 'Connecting modern software with legacy banking providers causes transaction timeouts and fragile webhook synchronization issues.',
        impact: 'Transaction drops, ledger reconciliation errors, and frustrated institutional clients.'
      },
      {
        title: 'Escalating Overhead of Manual Fraud Underwriting',
        description: 'Human risk assessment teams cannot review high-frequency transactions in real time, causing onboarding delays and exposure to fraud.',
        impact: 'User drop-off during onboarding and mounting fraudulent chargeback losses.'
      }
    ],
    niche_deep_dive: 'Financial technology operators require uncompromising transactional integrity, zero ledger discrepancies, and audited encryption protocols capable of satisfying institutional banking regulators.'
  },
  'healthtech-biotech': {
    name: 'HealthTech & Digital Health Platforms',
    acv: '$30,000 - $120,000/yr',
    industry: 'clinical software, telemedicine, and healthcare data systems',
    pain_points: [
      {
        title: 'HIPAA and Protected Health Information (PHI) Security Risks',
        description: 'Strict statutory requirements govern how sensitive patient records are transferred, processed, and stored across distributed cloud environments.',
        impact: 'Catastrophic statutory penalties and loss of medical institutional accreditation.'
      },
      {
        title: 'EHR and EMR Interoperability Bottlenecks',
        description: 'Synchronizing clinical records with legacy electronic health record systems requires bespoke HL7 and FHIR API connectors.',
        impact: 'Fragmented provider schedules and delayed diagnostic reporting.'
      },
      {
        title: 'Patient Intake Friction and Telehealth Abandonment',
        description: 'Multi-step medical questionnaires cause prospective patients to abandon appointment bookings midway through onboarding.',
        impact: 'Sub-optimal clinic capacity utilization and lost healthcare revenue.'
      }
    ],
    niche_deep_dive: 'Digital health providers must scale clinical communication and telemedicine workflows while maintaining strict data containment protocols that satisfy healthcare compliance officers.'
  },
  'proptech-realestate': {
    name: 'PropTech & Commercial Real Estate Platforms',
    acv: '$15,000 - $80,000/yr',
    industry: 'commercial brokerage, asset syndication, and real estate portals',
    pain_points: [
      {
        title: 'Fragmented MLS and Commercial Property Listing Feeds',
        description: 'Ingesting disparate regional real estate listing feeds causes schema conflicts, outdated listing availability, and broken links.',
        impact: 'Inaccurate asset listings and degraded user trust on property portals.'
      },
      {
        title: 'Hyper-Local Search Ranking Visibility Barriers',
        description: 'Competing against national portals for localized neighborhood commercial queries requires massive page scale and structured geographical data.',
        impact: 'Inability to capture high-value buyer and tenant searches organically.'
      },
      {
        title: 'Slow Broker Lead Triage and Delayed Deal Sourcing',
        description: 'Inbound inquiries sit in general mailboxes for hours, allowing rival brokerages to contact prospective commercial tenants first.',
        impact: 'Lost commission opportunities and elongated leasing cycles.'
      }
    ],
    niche_deep_dive: 'Commercial real estate operators depend on hyper-local discovery, verified asset specifications, and rapid lead routing to maximize asset occupancy and transaction velocity.'
  },
  'legaltech-professional': {
    name: 'LegalTech & High-Ticket Professional Services',
    acv: '$20,000 - $100,000/yr',
    industry: 'law firms, accounting partnerships, and advisory practices',
    pain_points: [
      {
        title: 'Prohibitive Legal Keyword Search Advertising Costs',
        description: 'Commercial legal search terms exceed $100 per click on Google Ads, making paid acquisition financially risky for mid-sized practices.',
        impact: 'Excessive client acquisition costs and low conversion return on marketing capital.'
      },
      {
        title: 'Strict Professional Ethical Rules on Outbound Solicitation',
        description: 'Bar associations enforce rigid standards regarding direct marketing and prospective client communication.',
        impact: 'Risk of professional ethics complaints or brand damage from uncalibrated outreach.'
      },
      {
        title: 'Cumbersome Client Onboarding and Conflict Checking Overhead',
        description: 'Manual intake processes and conflict verification consume expensive attorney hours before billable work can begin.',
        impact: 'Delayed matter initiation and administrative overhead eating practice profits.'
      }
    ],
    niche_deep_dive: 'Professional partnerships require high-authority positioning, ethical compliance, and streamlined intake mechanisms to acquire high-value retainers without administrative drag.'
  },
  'venture-capital-private-equity': {
    name: 'Venture Capital & Private Equity Firms',
    acv: '$50M - $1B AUM',
    industry: 'investment management, fund syndication, and portfolio operations',
    pain_points: [
      {
        title: 'Heavy Reliance on Intermediary Brokered Dealflow',
        description: 'Competing in banker-led auctions inflates acquisition multiples and compresses fund internal rate of return (IRR).',
        impact: 'Depressed fund returns and excessive advisory fees paid to intermediaries.'
      },
      {
        title: 'Fragmented Portfolio KPI Tracking and Reporting',
        description: 'Gathering monthly financial metrics from dozens of portfolio companies involves manual spreadsheets and inconsistent reporting formats.',
        impact: 'Delayed reporting to limited partners and missed operational intervention windows.'
      },
      {
        title: 'Low Inbound Visibility with Bootstrapped Founders',
        description: 'High-performing bootstrapped operators seek investment partners with demonstrated operational capabilities rather than passive capital.',
        impact: 'Missing proprietary investment opportunities before competitive bidding begins.'
      }
    ],
    niche_deep_dive: 'Investment firms must build proprietary sourcing channels and automated portfolio intelligence systems to generate alpha in an increasingly competitive private equity landscape.'
  },
  'edtech': {
    name: 'EdTech & Online Learning Platforms',
    acv: '$10,000 - $50,000/yr',
    industry: 'digital curricula, university credentials, and learning platforms',
    pain_points: [
      {
        title: 'Severe Student Completion and Retention Drop-Off',
        description: 'Learners struggle with engagement in self-paced courses, causing completion rates to plunge below 15% after introductory units.',
        impact: 'Elevated student churn, reduced lifetime customer value, and negative reviews.'
      },
      {
        title: 'Course Catalog Taxonomy and Search Fragmentation',
        description: 'Organizing thousands of lectures, syllabi, and prerequisites into search-optimized hierarchies requires continuous engineering support.',
        impact: 'Poor organic discoverability for specialized training courses and degrees.'
      },
      {
        title: 'Weak Community Engagement and Monetization Funnels',
        description: 'Student discussions remain scattered across chat apps without converting participants into recurring members.',
        impact: 'Lost subscription revenue and diminished brand community affinity.'
      }
    ],
    niche_deep_dive: 'Educational platforms succeed by pairing structured learning pathways with automated support mechanisms that guide students from initial discovery to verified skill mastery.'
  },
  'cybersecurity': {
    name: 'Enterprise Cybersecurity & DevSecOps',
    acv: '$40,000 - $200,000/yr',
    industry: 'network security, vulnerability management, and infrastructure protection',
    pain_points: [
      {
        title: 'Extended Enterprise Sales Cycles and Technical Proofs of Concept',
        description: 'Enterprise security reviews require exhaustive documentation, SOC2 reports, and architectural verification.',
        impact: 'Sales cycles stretching beyond 9 months, tying up senior engineering capacity.'
      },
      {
        title: 'High Barrier in Explaining Technical Architecture to Buyers',
        description: 'Security vendors struggle to convey zero-trust network benefits without creating dense, inaccessible documentation.',
        impact: 'Lost opportunities with executive decision-makers who lack technical backgrounds.'
      },
      {
        title: 'Vulnerability Disclosure and Threat Surface Expansion',
        description: 'Managing public-facing services while preventing unauthorized ingress requires continuous server hardening.',
        impact: 'Risk of security incidents, unauthorized data access, and regulatory disclosure.'
      }
    ],
    niche_deep_dive: 'Cybersecurity enterprises must demonstrate absolute technical rigor, zero-trust network integrity, and clear architectural boundaries to earn the confidence of enterprise CISOs.'
  },
  'agency-consultancy': {
    name: 'Digital Agencies & High-Growth Consultancies',
    acv: '$5,000 - $30,000/mo',
    industry: 'professional services, growth consulting, and client delivery',
    pain_points: [
      {
        title: 'The Feast-or-Famine Pipeline Rollercoaster',
        description: 'Focusing exclusively on client fulfillment causes new business prospecting to halt, leading to sudden revenue dips.',
        impact: 'Unpredictable cash flow, hiring hesitation, and quarterly business anxiety.'
      },
      {
        title: 'Capacity Bottlenecks and Fulfillment Overwork',
        description: 'Senior agency directors spend hours performing manual fulfillment tasks instead of scaling agency operations.',
        impact: 'Capped agency revenue and severe leadership burnout.'
      },
      {
        title: 'Difficulty Proving Measurable Organic ROI to Retainer Clients',
        description: 'Traditional retainers take months to demonstrate progress, leading to premature client cancellations.',
        impact: 'High client turnover, lowered lifetime value, and perpetual sales hunting.'
      }
    ],
    niche_deep_dive: 'High-ticket agencies thrive when they decouple revenue growth from manual labor hours through automated acquisition systems and programmatic delivery frameworks.'
  }
};

const SERVICE_DATA = {
  'pseo-engine': {
    name: 'Programmatic SEO Engine',
    badge: 'Automated Inbound Engineering',
    service_deep_dive: 'Our programmatic SEO engine deploys high-performance Next.js App Router routes powered by Incremental Static Regeneration. By compiling hundreds of structured, schema-validated landing pages on edge networks, your brand captures long-tail transactional searches without manual authoring.',
    capabilities: [
      { title: 'Combinatorial Keyword Matrix Engine', spec: 'Ingests niche data tables and maps commercial intent variations across services, locations, and buyer roles.', deliverable: 'Structured JSON taxonomy matrix with targeted keyword clustering.' },
      { title: 'Next.js App Router Edge Compilation', spec: 'Deploys server-rendered static templates with zero layout shift, Tailwind CSS styling, and sub-45ms TTFB.', deliverable: 'Production edge repository with automated static export.' },
      { title: 'Automated Schema.org Microdata Injection', spec: 'Embeds comprehensive ProfessionalService, Organization, FAQPage, and BreadcrumbList structured data.', deliverable: 'Rich Results validated JSON-LD schema blocks on all routes.' },
      { title: 'Dynamic XML Sitemap & Indexing Pipeline', spec: 'Automates sitemap chunking (5,000 URLs/file), dynamic lastmod timestamps, and automated search console pings.', deliverable: 'Continuous indexing pipeline submitting new pages directly to search engines.' }
    ],
    phases: [
      { title: 'Taxonomy & High-Intent Keyword Extraction', desc: 'Map proprietary features, integrations, and competitor comparisons.', tf: 'Days 1 - 3' },
      { title: 'Next.js Template & Schema Architecture', desc: 'Construct responsive Next.js dynamic routes with Tailwind CSS and JSON-LD microdata.', tf: 'Days 4 - 7' },
      { title: 'Content Verification & Anti-Spam Assertion Gates', desc: 'Execute automated uniqueness checks, buzzword blacklist scans, and schema tests.', tf: 'Days 8 - 10' },
      { title: 'Edge Deployment & Automated Indexation', desc: 'Deploy static assets to Cloudflare Pages and trigger GSC and IndexNow sitemap ping routines.', tf: 'Days 11 - 14' }
    ],
    faqs: [
      { q: 'How does programmatic SEO integrate into our existing domain?', a: 'We build modular Next.js route handlers that mount cleanly under your target subfolder or custom subdomain.' },
      { q: 'How do you prevent duplicate content penalties from search engines?', a: 'Every page features unique data variables, localized market metrics, distinct problem statements, and dynamic FAQs ensuring high mathematical uniqueness.' },
      { q: 'How quickly do programmatic pages begin ranking on Google?', a: 'With automated XML sitemap syndication and IndexNow API pings, search bots crawl new pages within 48 to 72 hours of edge deployment.' },
      { q: 'Can we connect demo request forms directly to our CRM?', a: 'Yes. Inbound form submissions trigger secure webhook payloads directly into HubSpot, Salesforce, or your chosen CRM.' },
      { q: 'Who retains intellectual property rights to the codebase?', a: 'Your organization owns 100% of the compiled Next.js templates, taxonomy matrices, and production assets.' }
    ],
    metrics: [
      { val: '< 45ms', lbl: 'Edge TTFB', sub: 'Sub-second React Server Components load' },
      { val: '+340%', lbl: 'Pipeline Expansion', sub: 'Qualified inbound demo volume growth' },
      { val: '100%', lbl: 'Schema Validated', sub: 'Complete ProfessionalService JSON-LD' },
      { val: '$12k-$60k', lbl: 'Target ACV Tier', sub: 'High-value enterprise contract focus' }
    ]
  },
  'ai-agents': {
    name: 'Autonomous AI Agents',
    badge: 'Agentic Workflow Engineering',
    service_deep_dive: 'We engineer deterministic autonomous agent swarms that execute complex business processes without human intervention. Built with robust tool-calling boundaries, state machines, and human-in-the-loop review checkpoints, our agents handle customer triage, data enrichment, and back-office operations.',
    capabilities: [
      { title: 'Multi-Agent Autonomous Orchestration', spec: 'Coordinates specialized LLM agents for task decomposition, verification, and autonomous execution.', deliverable: 'State-machine driven agent cluster with deterministic workflow logic.' },
      { title: 'Deterministic Tool-Calling Architecture', spec: 'Integrates external APIs, database drivers, and webhook triggers with strict parameter validation.', deliverable: 'Hardened tool schemas preventing hallucinated parameters or unauthorized actions.' },
      { title: 'Human-in-the-Loop Review Verification', spec: 'Routes high-stakes decisions and exceptions to human reviewers via Slack or web dashboard before execution.', deliverable: 'Approval checkpoint interface with auditable decision logs.' },
      { title: 'Self-Hosted High-Concurrency Runtime', spec: 'Runs containerized agent services on dedicated infrastructure with sub-second inference caching.', deliverable: 'Dockerized agent stack with automated scaling and health monitors.' }
    ],
    phases: [
      { title: 'Workflow Decomposition & Schema Design', desc: 'Deconstruct manual business processes into atomic tool actions and state transitions.', tf: 'Days 1 - 3' },
      { title: 'Agent Prompting & Guardrail Implementation', desc: 'Build deterministic system prompts, tool schemas, and validation boundary tests.', tf: 'Days 4 - 7' },
      { title: 'Human-in-the-Loop Review Gate Setup', desc: 'Configure Slack webhooks and exception triage queues for high-risk operations.', tf: 'Days 8 - 10' },
      { title: 'Containerized Deployment & Live Tuning', desc: 'Deploy Dockerized agent cluster with automated health checks and telemetry dashboards.', tf: 'Days 11 - 14' }
    ],
    faqs: [
      { q: 'How do autonomous agents prevent hallucinations during execution?', a: 'We enforce strict JSON Schema validation on all tool parameters, accompanied by deterministic fallback routines and boundary checks.' },
      { q: 'Can agents connect to our existing internal databases?', a: 'Yes. Agents connect securely through authenticated REST APIs, GraphQL endpoints, or read-only database replicas.' },
      { q: 'What happens when an agent encounters an edge case it cannot solve?', a: 'Uncertain requests trigger an immediate escalation event, pausing execution and notifying human operators via Slack or email.' },
      { q: 'How are sensitive API keys and client credentials protected?', a: 'Credentials are encrypted at rest using AES-256 and injected into agent runtimes via secure environment vaults.' },
      { q: 'What response latency can we expect for customer-facing agents?', a: 'Our optimized tool-calling pipelines achieve sub-1.5 second initial response times across text chat and webhook interfaces.' }
    ],
    metrics: [
      { val: '< 1.5s', lbl: 'Average Response Time', sub: 'Instantaneous automated resolution' },
      { val: '-68%', lbl: 'Support Ticket Volume', sub: 'Tier-1 customer inquiries automated' },
      { val: '99.9%', lbl: 'System Availability', sub: 'Redundant containerized agent clusters' },
      { val: '100%', lbl: 'Tool Calling Accuracy', sub: 'Deterministic schema validation gates' }
    ]
  },
  'web-app-engineering': {
    name: 'Next.js Web Engineering',
    badge: 'Modern Web Engineering',
    service_deep_dive: 'We construct high-performance, enterprise-grade web applications utilizing Next.js App Router, React Server Components, and TypeScript. Our architecture prioritizes sub-50ms edge rendering, zero layout shift, accessibility, and clean database integrations.',
    capabilities: [
      { title: 'React Server Components & App Router Architecture', spec: 'Builds modular page components that render on the server, eliminating client-side JavaScript overhead.', deliverable: 'Production Next.js application codebase with optimized bundle splitting.' },
      { title: 'Type-Safe Database Integration & API Routes', spec: 'Integrates PostgreSQL, Supabase, or MongoDB through Prisma ORM with comprehensive end-to-end typing.', deliverable: 'Type-safe database models, migrations, and validated server actions.' },
      { title: 'Enterprise UI Design & Component Systems', spec: 'Implements responsive, accessible UI components styled with Tailwind CSS and Framer Motion micro-interactions.', deliverable: 'Complete reusable design component library adhering to WCAG standards.' },
      { title: 'Continuous Integration & Edge Deployment CI/CD', spec: 'Configures automated GitHub Actions pipelines, linting gates, unit testing, and edge CDN deployments.', deliverable: 'Automated CI/CD pipeline deploying preview and production releases.' }
    ],
    phases: [
      { title: 'Information Architecture & Wireframing', desc: 'Map application route hierarchy, data schemas, and responsive user flows.', tf: 'Days 1 - 3' },
      { title: 'Frontend Component & Theme Construction', desc: 'Build reusable React Server Components with Tailwind CSS styling and fluid layouts.', tf: 'Days 4 - 7' },
      { title: 'Backend API & Database Connection', desc: 'Implement type-safe Prisma models, server actions, and third-party API routes.', tf: 'Days 8 - 10' },
      { title: 'Performance Optimization & Edge Deployment', desc: 'Audit bundle sizes, enforce Core Web Vitals, and deploy to edge production CDN.', tf: 'Days 11 - 14' }
    ],
    faqs: [
      { q: 'Why do you prioritize Next.js App Router over traditional SPA frameworks?', a: 'Next.js App Router provides server-rendered speed, superior SEO visibility, reduced client bundle sizes, and instant edge caching.' },
      { q: 'Can this web application scale to millions of monthly visitors?', a: 'Yes. By leveraging edge caching and serverless execution, our web architectures scale effortlessly with zero server maintenance.' },
      { q: 'How do you ensure zero cumulative layout shift (CLS)?', a: 'We enforce explicit font preloading, image aspect ratios, and server-side skeleton renders to eliminate layout reflows.' },
      { q: 'Do you provide full source code ownership upon project completion?', a: 'Yes. All source code, design systems, and deployment configurations are transferred directly to your organization GitHub repository.' },
      { q: 'How do you handle authentication and user session security?', a: 'We implement industry-standard authentication protocols including OAuth 2.0, magic links, and encrypted HTTP-only session cookies.' }
    ],
    metrics: [
      { val: '< 30ms', lbl: 'Edge TTFB', sub: 'Sub-second React Server Components load' },
      { val: '99/100', lbl: 'Lighthouse Score', sub: 'Flawless Core Web Vitals rating' },
      { val: '0 CLS', lbl: 'Layout Shift', sub: 'Rock-solid visual stability' },
      { val: '100%', lbl: 'Type Safety', sub: 'End-to-end TypeScript validation' }
    ]
  },
  'outbound-infrastructure': {
    name: 'Cold Outbound & Lead Engine',
    badge: 'Outbound Pipeline Engineering',
    service_deep_dive: 'We build enterprise cold email and lead generation infrastructure designed to maintain pristine sender reputation and 99%+ inbox placement. Our systems combine dedicated sending domains, automated mailbox warm-up routines, DNS security records, and AI-personalized copywriting.',
    capabilities: [
      { title: 'Multi-Domain Sending Infrastructure Setup', spec: 'Configures isolated secondary domains with Google Workspace and Microsoft 365 sending mailboxes.', deliverable: 'Turnkey domain portfolio configured with dedicated IP pools.' },
      { title: 'DNS Authentication & Deliverability Hardening', spec: 'Deploys 2048-bit DKIM keys, strict SPF records, DMARC policies, and custom tracking CNAME records.', deliverable: 'Fully authenticated DNS configurations passing deliverability audits.' },
      { title: 'Automated Mailbox Warm-Up & Health Monitoring', spec: 'Simulates organic peer-to-peer sending behavior over 21 days to establish sender authority with ISPs.', deliverable: 'Automated warm-up network with real-time reputation health alerts.' },
      { title: 'High-Intent Prospect Enrichment & Personalization', spec: 'Scrapes firmographic and social intent data, validating contact addresses to maintain sub-1% bounce rates.', deliverable: 'Enriched verified lead prospect lists with dynamic personalization tags.' }
    ],
    phases: [
      { title: 'Secondary Domain Acquisition & DNS Hardening', desc: 'Procure secondary domain variants, configure SPF/DKIM/DMARC records, and set up MX routing.', tf: 'Days 1 - 3' },
      { title: 'Mailbox Provisioning & Automated Ramp-Up', desc: 'Initialize Google Workspace and Microsoft 365 mailboxes and connect to warm-up network.', tf: 'Days 4 - 7' },
      { title: 'Prospect Scraping & Algorithmic Email Verification', desc: 'Extract high-intent decision-makers and scrub contact lists through real-time SMTP validators.', tf: 'Days 8 - 10' },
      { title: 'Campaign Sequence Activation & CRM Webhook Sync', desc: 'Launch multi-touch email sequences and route positive prospect replies to sales reps.', tf: 'Days 11 - 14' }
    ],
    faqs: [
      { q: 'Why do we need separate secondary domains for outbound outreach?', a: 'Using secondary domains protects your primary corporate domain reputation from spam complaints and temporary ISP rate-limits.' },
      { q: 'How long does it take to safely warm up a new cluster of mailboxes?', a: 'We adhere to a conservative 21-day algorithmic ramp-up schedule before launching full-scale outbound campaigns.' },
      { q: 'What email deliverability and open rates can we expect?', a: 'Our clients consistently maintain 99%+ deliverability and 45% to 65% open rates across warmed enterprise mailboxes.' },
      { q: 'How do you prevent emails from landing in Google and Outlook spam filters?', a: 'We implement strict DNS alignment, rotate across multiple sending inboxes, restrict daily volume per mailbox, and avoid spam trigger words.' },
      { q: 'Can outbound replies sync directly into our team sales inbox?', a: 'Yes. Incoming positive replies forward automatically to your account executives with lead context and notification alerts.' }
    ],
    metrics: [
      { val: '99.4%', lbl: 'Inbox Placement', sub: 'Pristine primary inbox delivery' },
      { val: '< 0.5%', lbl: 'Bounce Rate', sub: 'Real-time SMTP validation filtering' },
      { val: '58%', lbl: 'Average Open Rate', sub: 'Targeted executive subject line formulas' },
      { val: '100%', lbl: 'Domain Isolation', sub: 'Zero risk to primary brand domain' }
    ]
  },
  'composio-integrations': {
    name: 'Composio Agent Integrations',
    badge: 'Agent Tooling Architecture',
    service_deep_dive: 'We architect self-hosted Composio execution environments connecting AI models directly to over 200 software applications, databases, and enterprise platforms. By providing secure OAuth credential token vaults, function execution sandboxes, and audit logs, our integrations empower agents to act safely.',
    capabilities: [
      { title: 'Self-Hosted Composio Engine Runtime', spec: 'Deploys private Composio infrastructure on dedicated servers with zero third-party data leakage.', deliverable: 'Production Composio deployment with isolated container network.' },
      { title: '200+ SaaS Tool Connectors & Custom Actions', spec: 'Configures pre-built and bespoke action connectors for GitHub, Slack, Jira, Linear, HubSpot, and Google Workspace.', deliverable: 'Validated tool registry ready for autonomous LLM function calling.' },
      { title: 'Secure OAuth Token Vault & Credential Lifecycle', spec: 'Manages user authentication, token refresh flows, and scoped permission boundaries in an encrypted vault.', deliverable: 'Zero-trust credential storage system with automated token rotation.' },
      { title: 'Execution Sandboxing & Auditable Telemetry', spec: 'Executes third-party API mutations inside temporary sandbox containers with complete transaction logging.', deliverable: 'Audit dashboard recording agent tool invocations, inputs, and outputs.' }
    ],
    phases: [
      { title: 'Composio Server Deployment & Network Isolation', desc: 'Deploy containerized Composio runtime behind private Docker bridge networks.', tf: 'Days 1 - 3' },
      { title: 'SaaS App Authentication & Scoped OAuth Binding', desc: 'Register enterprise applications, configure OAuth client IDs, and map scopes.', tf: 'Days 4 - 7' },
      { title: 'Custom Action Schemas & Sandbox Validation', desc: 'Write custom OpenAPI definitions and test sandboxed function invocations.', tf: 'Days 8 - 10' },
      { title: 'Agent Integration & Audit Logging Activation', desc: 'Connect LLM runtime to Composio tool registry and activate auditable telemetry.', tf: 'Days 11 - 14' }
    ],
    faqs: [
      { q: 'What is Composio and how does it help our agent workflows?', a: 'Composio provides standard authentication, tool definitions, and API bindings so LLMs can interact with hundreds of SaaS platforms effortlessly.' },
      { q: 'Why run a self-hosted Composio runtime instead of cloud services?', a: 'Self-hosting keeps your corporate API tokens, internal databases, and client credentials entirely within your private cloud perimeter.' },
      { q: 'How does Composio handle OAuth refresh token expirations?', a: 'The Composio token manager monitors expiration timestamps and executes background refresh handshakes autonomously.' },
      { q: 'Can we create custom internal API tools for proprietary software?', a: 'Yes. We build custom OpenAPI and Swagger schemas that register seamlessly as callable tools in your Composio workspace.' },
      { q: 'How do you prevent agents from making unauthorized or dangerous API calls?', a: 'We configure strict role-based permission policies, parameter validation schemas, and rate-limiting thresholds on sensitive endpoints.' }
    ],
    metrics: [
      { val: '200+', lbl: 'Verified Tool Connectors', sub: 'Turnkey SaaS and database integrations' },
      { val: '< 80ms', lbl: 'Tool Execution Overhead', sub: 'Near-instantaneous function invocation' },
      { val: '0 Leak', lbl: 'Credential Exposure', sub: 'AES-256 encrypted token vault' },
      { val: '100%', lbl: 'Audit Logging', sub: 'Full transaction payload telemetry' }
    ]
  },
  'cloud-vps-hardening': {
    name: 'Cloudflare & VPS Infrastructure',
    badge: 'Zero-Trust Infrastructure',
    service_deep_dive: 'We deploy hardened, zero-trust cloud infrastructure on Ubuntu VPS servers behind Cloudflare edge proxies. Our setup isolates multi-container Docker workloads, eliminates open public ports via Cloudflare Tunnels, enforces SSH key-only access, and configures automated failover monitoring.',
    capabilities: [
      { title: 'Ubuntu Server Hardening & Kernel Optimization', spec: 'Disables root password login, configures SSH ed25519 key access, enables sysctl kernel protections, and audits open ports.', deliverable: 'Hardened Linux operating system baseline meeting CIS compliance standards.' },
      { title: 'Cloudflare Zero Trust Tunnel Configuration', spec: 'Routes all inbound web traffic through encrypted Cloudflare edge tunnels, closing all inbound firewall ports.', deliverable: 'Zero-open-port network configuration completely shielding server IP addresses.' },
      { title: 'Docker Compose Container Sandboxing', spec: 'Isolates applications into dedicated virtual bridge networks with resource quotas and unprivileged user execution.', deliverable: 'Production Docker Compose architecture with encrypted environment secrets.' },
      { title: 'Automated Snapshot Backups & Health Telemetry', spec: 'Deploys cron-driven encrypted database backups to offsite S3 buckets alongside automated system health alerts.', deliverable: 'Automated disaster recovery pipeline and Grafana/Prometheus telemetry.' }
    ],
    phases: [
      { title: 'Operating System Audit & Linux Hardening', desc: 'Install Ubuntu 24.04 LTS, disable password authentication, configure UFW, and install Fail2ban.', tf: 'Days 1 - 3' },
      { title: 'Cloudflare Zero Trust & Cloudflared Tunnel Setup', desc: 'Deploy cloudflared daemon, map ingress routing rules, and lock down origin IP firewalls.', tf: 'Days 4 - 7' },
      { title: 'Docker Bridge Isolation & Resource Quotas', desc: 'Structure multi-container compose files with internal networking and memory boundaries.', tf: 'Days 8 - 10' },
      { title: 'Automated Backups & Telemetry Alerting', desc: 'Schedule encrypted off-site database backups and configure real-time alert webhooks.', tf: 'Days 11 - 14' }
    ],
    faqs: [
      { q: 'How does a Cloudflare Tunnel protect our server from DDoS attacks?', a: 'Cloudflare Tunnels establish outbound-only connections to Cloudflare edge nodes, keeping your server IP address completely hidden from the public internet.' },
      { q: 'What happens if a Docker container crashes or experiences high memory usage?', a: 'Docker daemon restart policies immediately relaunch failed containers, while systemd monitors overall memory and CPU thresholds.' },
      { q: 'How do you handle automated SSL and TLS certificate renewals?', a: 'SSL certificates are managed automatically at the Cloudflare edge and through Let Encrypt automated certbot daemons.' },
      { q: 'Can we access internal administrative dashboards securely?', a: 'Yes. Administrative interfaces are protected behind Cloudflare Access with two-factor authentication and role-based email verification.' },
      { q: 'How often are security patches and updates applied to the VPS?', a: 'We configure unattended-upgrades on Ubuntu to apply critical operating system security patches automatically without downtime.' }
    ],
    metrics: [
      { val: '100%', lbl: 'Zero-Trust Isolation', sub: 'Zero open public ports on origin servers' },
      { val: '99.99%', lbl: 'Infrastructure Uptime', sub: 'High-availability container health checks' },
      { val: '0 Root', lbl: 'Privilege Exposure', sub: 'Unprivileged container execution' },
      { val: '< 15min', lbl: 'Disaster Recovery RTO', sub: 'Automated off-site snapshot restores' }
    ]
  },
  'whop-monetization': {
    name: 'Whop Monetization Systems',
    badge: 'Digital Monetization Systems',
    service_deep_dive: 'We build automated monetization systems and membership gating utilizing the Whop API and developer platform. From tier entitlement logic and digital product delivery to automated Discord role assignment and churn mitigation webhooks, we turn audience traffic into recurring revenue.',
    capabilities: [
      { title: 'Whop Product Tier Architecture & Entitlements', spec: 'Structures subscription tiers, one-time passes, and add-on products with granular permission entitlement mappings.', deliverable: 'Configured Whop store catalog ready for high-conversion checkouts.' },
      { title: 'Automated Webhook License Provisioning', spec: 'Listens for payment success events and issues cryptographic license keys or account credentials instantly.', deliverable: 'Zero-latency fulfillment webhook service with automated retry queues.' },
      { title: 'Discord & Community Access Synchronization', spec: 'Synchronizes active customer subscriptions with Discord server roles and private portal access permissions.', deliverable: 'Automated member onboarding bot revoking access automatically upon cancellation.' },
      { title: 'Checkout Optimization & Churn Mitigation', spec: 'Deploys localized checkout currency displays, frictionless one-click payments, and dunning workflows to rescue failed renewals.', deliverable: 'Revenue retention funnel recovering abandoned checkouts and expired payment methods.' }
    ],
    phases: [
      { title: 'Product Tier & Pricing Architecture Design', desc: 'Structure digital offerings, membership tiers, and permission entitlements inside Whop.', tf: 'Days 1 - 3' },
      { title: 'Webhook Listener & License Key Dispatcher', desc: 'Deploy edge webhook endpoints handling payment success, cancellation, and renewal events.', tf: 'Days 4 - 7' },
      { title: 'Discord Bot & Private Portal Gating', desc: 'Configure automatic role assignment and connect gated member areas.', tf: 'Days 8 - 10' },
      { title: 'Checkout Conversion & Dunning Optimization', desc: 'Set up localized currencies, abandoned checkout recovery, and payment retry logic.', tf: 'Days 11 - 14' }
    ],
    faqs: [
      { q: 'Why choose Whop over traditional payment platforms for digital products?', a: 'Whop offers industry-leading conversion rates, integrated affiliate portals, automatic Discord role management, and built-in buyer discovery.' },
      { q: 'How do customers access their digital products after purchase?', a: 'Upon completed checkout, buyers receive instant access via their Whop customer portal alongside automated email credentials.' },
      { q: 'Can we accept payments from international customers across multiple currencies?', a: 'Yes. Whop handles multi-currency transactions, regional payment methods, and automated sales tax compliance worldwide.' },
      { q: 'What happens when a customer cancels their recurring membership?', a: 'Webhooks trigger immediately upon cancellation or non-payment, revoking access to protected Discord channels and software portals.' },
      { q: 'Can we integrate Whop purchase events into our marketing email sequences?', a: 'Yes. Purchase and churn events dispatch webhook payloads into your email CRM to trigger automated customer lifecycle sequences.' }
    ],
    metrics: [
      { val: '+28%', lbl: 'Checkout Conversion', sub: 'Optimized frictionless payment funnels' },
      { val: '< 2min', lbl: 'Member Onboarding', sub: 'Instant automated role and license provisioning' },
      { val: '100%', lbl: 'Automated Gating', sub: 'Real-time subscription status synchronization' },
      { val: '$0 Fee', lbl: 'Custom Development Penalty', sub: 'Standard developer-friendly fee schedule' }
    ]
  }
};

function generateFullPageHtml(nicheId, serviceId) {
  const n = NICHE_DATA[nicheId];
  const s = SERVICE_DATA[serviceId];
  const whopCta = getProductCTA(serviceId);
  const slug = `/solutions/${nicheId}/${serviceId}/`;
  const canonicalUrl = `https://adorisedigital.com${slug}`;
  const title = `${s.name} for ${n.name} | Adorise Digital`;
  const subheadline = `Engineered specifically for ${n.name} to eliminate operational bottlenecks, compress sales cycles, and drive predictable enterprise revenue with ${s.name.toLowerCase()}.`;

  return `<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
</head>
<body class="bg-slate-950 text-slate-100">
  <aside id="geo-enterprise-banner">
    <a href="https://services.adorisedigital.com">Enterprise Advisory</a>
  </aside>

  <main class="pseo-main min-h-screen">
    <nav aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/solutions/">Solutions</a></li>
        <li><a href="/solutions/${nicheId}/">${n.name}</a></li>
        <li>${s.name}</li>
      </ol>
    </nav>

    <section class="hero">
      <span class="badge">${s.badge} | ${n.name}</span>
      <h1>${s.name} for ${n.name}</h1>
      <p class="subheadline">${subheadline}</p>
      
      <div class="ctas">
        <a href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult">Schedule Technical Audit</a>
        <a href="${whopCta.url}">${whopCta.ctaText}</a>
      </div>

      <div class="social-proof">
        <span>★★★★★ 4.9/5 SLA Rating • Trusted by founders scaling automation across North America & Europe</span>
      </div>

      <div class="metrics">
        ${s.metrics.map(m => `
          <div class="metric-card">
            <div class="val">${m.val}</div>
            <div class="lbl">${m.lbl}</div>
            <div class="sub">${m.sub}</div>
          </div>
        `).join('')}
      </div>
    </section>

    <section class="architecture-brief">
      <h2>How Adorise Digital Solves ${n.name} Friction with ${s.name}</h2>
      <p>${s.service_deep_dive}</p>
      <p>${n.niche_deep_dive}</p>
    </section>

    <section class="industry-friction">
      <h2>Why Standard Approaches Fail in ${n.name}</h2>
      <p>Uncalibrated tools and generic manual processes fail to address the core industry friction points across ${n.industry}.</p>
      <div class="pains">
        ${n.pain_points.map((pp, idx) => `
          <div class="pain-card">
            <span class="num">0${idx+1}</span>
            <h3>${pp.title}</h3>
            <p>${pp.description}</p>
            <span class="impact">${pp.impact}</span>
          </div>
        `).join('')}
      </div>
    </section>

    <section class="lead-magnet">
      <h3>Working on ${n.name} Automation?</h3>
      <p>Download the complete production checklist, prompt templates, and architecture schema from our 48-book library (Instant Free Download).</p>
      <form action="https://books.adorisedigital.com" method="GET">
        <input type="email" placeholder="founder@yourcompany.com" required />
        <button type="submit">Get Free Access &rarr;</button>
      </form>
    </section>

    <section class="human-solutions">
      <h2>Solving Painful Problems in Both Your Business & Personal Life</h2>
      <div class="business-col">
        <h3>Operational & Revenue Defense for ${n.name}</h3>
        <p>${n.niche_deep_dive}</p>
        <div class="pillar">
          <h4>${s.capabilities[0].title}</h4>
          <p>${s.capabilities[0].spec}</p>
        </div>
        <div class="pillar">
          <h4>${s.capabilities[1].title}</h4>
          <p>${s.capabilities[1].spec}</p>
        </div>
      </div>
      <div class="personal-col">
        <h3>Protecting Leaders in ${n.name} from Fatigue</h3>
        <p>Operating a high-growth organization in ${n.industry} creates severe decision overload, late-night anxiety, and communication friction.</p>
        <div class="pillar">
          <h4>InboxCalm Email Defense</h4>
          <p>Filters hostile communication and drafts calm replies.</p>
        </div>
        <div class="pillar">
          <h4>ClipCalm Content Automation</h4>
          <p>Repurposes long-form presentations into short videos.</p>
        </div>
      </div>
    </section>

    <section class="system-capabilities">
      <h2>High-Performance ${s.name} Architecture</h2>
      <div class="caps">
        ${s.capabilities.map((cap, idx) => `
          <div class="cap-card">
            <span class="num">${idx+1}</span>
            <h3>${cap.title}</h3>
            <p>${cap.spec}</p>
            <span class="del">Deliverable: ${cap.deliverable}</span>
          </div>
        `).join('')}
      </div>

      <div class="phases">
        <h3>Production Rollout Milestones</h3>
        ${s.phases.map(ph => `
          <div class="phase-card">
            <span class="tf">${ph.tf}</span>
            <h4>${ph.title}</h4>
            <p>${ph.desc}</p>
          </div>
        `).join('')}
      </div>
    </section>

    <section class="whop-product">
      <h3>Deploy ${whopCta.title} for ${n.name}</h3>
      <p>Target Intent: ${whopCta.intentCluster}. Available with instant self-service activation.</p>
      <div class="price">${whopCta.price}</div>
      <a href="${whopCta.url}">${whopCta.ctaText}</a>
      <p class="micro-proof">🛡️ Trusted by founders and operators automating client acquisition across North America and Europe.</p>
    </section>

    <section class="faq">
      <h2>Frequently Asked Questions</h2>
      ${s.faqs.map(f => `
        <div class="faq-item">
          <h3>${f.q}</h3>
          <p>${f.a}</p>
        </div>
      `).join('')}
    </section>

    <section class="related">
      <h3>Related Solutions & Architecture Blueprints</h3>
      <a href="https://books.adorisedigital.com">Browse All 48 Books & Blueprints &rarr;</a>
    </section>

    <section class="ready-cta">
      <h2>Ready to Build Your ${s.name}?</h2>
      <a href="https://services.adorisedigital.com">Schedule Engineering Call</a>
      <p class="micro-proof">✓ Trusted by founders and operators automating client acquisition across North America and Europe.</p>
    </section>
  </main>
</body>
</html>`;
}

function extractWordSet(text) {
  const mainMatch = text.match(/<main[\s\S]*?<\/main>/);
  const content = mainMatch ? mainMatch[0] : text;
  const stripped = content.replace(/<[^>]+>/g, ' ').toLowerCase();
  const words = stripped.match(/[a-z]{3,}/g) || [];
  return new Set(words);
}

function calculateJaccardDistance(setA, setB) {
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return 1 - (intersection.size / union.size);
}

// Generate all 70 full HTML pages and test
const niches = Object.keys(NICHE_DATA);
const services = Object.keys(SERVICE_DATA);

const pages = [];
niches.forEach(nid => {
  services.forEach(sid => {
    const html = generateFullPageHtml(nid, sid);
    pages.push({
      slug: `/solutions/${nid}/${sid}`,
      wordSet: extractWordSet(html)
    });
  });
});

console.log(`Generated ${pages.length} full HTML pages in memory.`);

let minDistance = 1.0;
let minPair = '';
let violations = 0;
let totalPairs = 0;

for (let i = 0; i < pages.length; i++) {
  for (let j = i + 1; j < pages.length; j++) {
    totalPairs++;
    const dist = calculateJaccardDistance(pages[i].wordSet, pages[j].wordSet);
    if (dist < minDistance) {
      minDistance = dist;
      minPair = `${pages[i].slug} vs ${pages[j].slug}`;
    }
    if (dist <= 0.35) {
      violations++;
      console.log(`VIOLATION: ${pages[i].slug} vs ${pages[j].slug}: ${(dist*100).toFixed(2)}%`);
    }
  }
}

console.log(`Total Pairs Tested: ${totalPairs}`);
console.log(`Minimum Uniqueness: ${(minDistance * 100).toFixed(2)}% (Threshold: > 35.0%)`);
console.log(`Minimum Pair: ${minPair}`);
console.log(`Violations: ${violations}`);
