// Advanced combinatorial engine ensuring >35% Jaccard Distance across ALL 70 combinations
// Incorporates service-specific pain points, capabilities, phases, FAQs, and human value architectures

const SERVICE_SCHEMAS = {
  'pseo-engine': {
    service_name: 'Programmatic SEO Engine',
    short: 'pSEO Engine',
    badge: 'Automated Inbound Engineering',
    service_deep_dive: 'Our programmatic SEO engine deploys high-performance Next.js App Router routes powered by Incremental Static Regeneration. By compiling hundreds of structured, schema-validated landing pages on edge networks, your brand captures long-tail transactional searches without manual authoring.',
    pain_templates: [
      (n) => ({ title: `Skyrocketing Paid Click Costs in ${n.short}`, description: `Bidding on commercial keywords for ${n.terms[0]} and ${n.terms[1]} pushes click costs over $60, making customer acquisition payback exceed 18 months.`, impact: `Depressed gross margins and unsustainable reliance on paid advertising networks.` }),
      (n) => ({ title: `Organic Discoverability Deficit Against National Portals`, description: `Legacy manual publishing cannot produce the volume of structured landing pages needed to rank for long-tail queries across ${n.market}.`, impact: `Erosion of organic search authority and surrender of buyer traffic to aggregators.` }),
      (n) => ({ title: `Thin Content Algorithmic Penalties`, description: `Uncalibrated generative AI tools publish generic, boilerplate articles that search engine crawlers penalize or de-index for low informational value.`, impact: `Algorithmic search penalties that suppress organic visibility across your primary domain.` })
    ],
    capabilities: [
      (n) => ({ title: `Combinatorial Keyword Matrix for ${n.short}`, spec: `Maps commercial search intent across ${n.terms[0]}, ${n.terms[1]}, competitor alternatives, and regional buyer queries into structured database tables.`, deliverable: `Structured JSON taxonomy matrix with targeted keyword clustering.` }),
      (n) => ({ title: `Next.js App Router & Edge Server Components`, spec: `Constructs server-rendered dynamic templates with zero layout shift, Tailwind CSS styling, and sub-45ms TTFB on global edge networks.`, deliverable: `Production Next.js repository with automated static export and zero layout shift.` }),
      (n) => ({ title: `Automated Schema.org Microdata Automation`, spec: `Embeds Rich Results validated ProfessionalService, Organization, FAQPage, and BreadcrumbList structured data on every compiled route.`, deliverable: `Schema markup passing Google Rich Results tests with zero warnings or errors.` }),
      (n) => ({ title: `Chunked XML Sitemaps with Automated Search Console Pings`, spec: `Automates sitemap chunking (max 5,000 URLs/file) with dynamic lastmod timestamps and automated search console pings.`, deliverable: `Continuous indexation pipeline submitting new pages immediately upon generation.` })
    ],
    phases: [
      (n) => ({ title: `Taxonomy & High-Intent Keyword Extraction`, desc: `Map proprietary software features, integrations, and competitor comparisons across ${n.terms[0]}.`, tf: 'Days 1 - 3' }),
      (n) => ({ title: `Next.js Template & Schema Architecture`, desc: `Construct responsive Next.js dynamic routes with Tailwind CSS and JSON-LD microdata for ${n.short}.`, tf: 'Days 4 - 7' }),
      (n) => ({ title: `Content Verification & Anti-Spam Assertion Gates`, desc: `Execute automated uniqueness checks, buzzword blacklist scans, and schema tests.`, tf: 'Days 8 - 10' }),
      (n) => ({ title: `Edge Deployment & Automated Indexation`, desc: `Deploy static assets to Cloudflare Pages and trigger GSC and IndexNow sitemap ping routines.`, tf: 'Days 11 - 14' })
    ],
    faqs: [
      (n) => ({ q: `How does programmatic SEO integrate into our existing ${n.short} domain?`, a: `We engineer modular Next.js route handlers that mount cleanly under /solutions or /integrations without altering your primary application code.` }),
      (n) => ({ q: `How do you guarantee technical accuracy for ${n.market}?`, a: `Every page data record is validated against a strict JSON Schema with deterministic fallback rules and domain assertion gates, preventing hallucinated specifications.` }),
      (n) => ({ q: `Can demo request forms connect directly with ${n.entities.split(',')[0]}?`, a: `Yes. Inbound demo requests and consultation forms dispatch encrypted webhooks directly into your CRM with automated lead attribution.` }),
      (n) => ({ q: `What payback period can ${n.short} leadership expect from organic search?`, a: `Our programmatic deployments typically achieve sub-45 day customer payback on initial cohorts, outperforming paid search ad channels by 3.4x.` }),
      (n) => ({ q: `Who owns the generated code, templates, and taxonomy data?`, a: `Your organization retains 100% full intellectual property rights to the compiled Next.js components, automation scripts, and database matrices.` })
    ],
    biz_pillars: [
      (n) => ({ title: `Programmatic Organic Lead Pipeline`, desc: `Deploys hundreds of comparison, integration, and alternative routes on Next.js edge caching, capturing high-intent ${n.short} buyers actively researching solutions.`, product: `pSEO Engine & AI Lead Generation ($297/mo)` }),
      (n) => ({ title: `Social Intent Prospect Radar`, desc: `Monitors real-time discussions across online forums for software pain points regarding ${n.terms[0]}, piping pre-qualified buyers directly to sales reps.`, product: `Scout Intent Radar & Outreach Pipeline` }),
      (n) => ({ title: `Daily Thought Leadership Omnipresence`, desc: `Establishes brand authority on autopilot with 30 to 60 high-signal posts per month formatted for LinkedIn and X.`, product: `AI Content Automation ($197/mo)` })
    ]
  },

  'ai-agents': {
    service_name: 'Autonomous AI Agents',
    short: 'Autonomous Agents',
    badge: 'Agentic Workflow Engineering',
    service_deep_dive: 'We engineer deterministic autonomous agent swarms that execute complex business processes without human intervention. Built with robust tool-calling boundaries, state machines, and human-in-the-loop review checkpoints, our agents handle customer triage, data enrichment, and back-office operations.',
    pain_templates: [
      (n) => ({ title: `Customer Triage Queue Backlogs in ${n.short}`, description: `Inquiry spikes and repetitive support tickets overwhelm human staff, driving first response times beyond 12 hours across ${n.market}.`, impact: `Customer dissatisfaction, elevated churn, and negative public reviews.` }),
      (n) => ({ title: `Costly Human Labor Siphoned into Repetitive Data Entry`, description: `Skilled staff spend hours manually copying records between ${n.entities} instead of focusing on high-leverage business growth.`, impact: `High operational overhead and avoidable manual transcription errors.` }),
      (n) => ({ title: `Uncontrolled AI Hallucination & Decision Risk`, description: `Off-the-shelf generative chat tools lack parameter guardrails, risking unauthorized promises, incorrect advice, or data leaks.`, impact: `Compliance violations, brand liability, and loss of institutional trust.` })
    ],
    capabilities: [
      (n) => ({ title: `Multi-Agent Autonomous Orchestration for ${n.short}`, spec: `Coordinates specialized LLM agents for task decomposition, verification, and autonomous execution across ${n.terms[0]} and ${n.terms[1]}.`, deliverable: `State-machine driven agent cluster with deterministic workflow logic.` }),
      (n) => ({ title: `Deterministic Tool-Calling Architecture`, spec: `Integrates directly with ${n.entities} using strict JSON Schema parameter validation preventing hallucinated inputs.`, deliverable: `Hardened tool schemas preventing unauthorized mutations or parameter drift.` }),
      (n) => ({ title: `Human-in-the-Loop Review Verification`, spec: `Routes high-stakes decisions regarding ${n.terms[2]} to human operators via Slack or web dashboard before execution.`, deliverable: `Approval checkpoint interface with auditable decision logs.` }),
      (n) => ({ title: `Self-Hosted High-Concurrency Runtime`, spec: `Runs containerized agent services on dedicated infrastructure with sub-second inference caching and error handling.`, deliverable: `Dockerized agent stack with automated scaling and health monitors.` })
    ],
    phases: [
      (n) => ({ title: `Workflow Decomposition & Schema Design`, desc: `Deconstruct manual ${n.short} processes into atomic tool actions and state transitions.`, tf: 'Days 1 - 3' }),
      (n) => ({ title: `Agent Prompting & Guardrail Implementation`, desc: `Build deterministic system prompts, tool schemas, and validation boundary tests for ${n.terms[0]}.`, tf: 'Days 4 - 7' }),
      (n) => ({ title: `Human-in-the-Loop Review Gate Setup`, desc: `Configure Slack webhooks and exception triage queues for sensitive operations.`, tf: 'Days 8 - 10' }),
      (n) => ({ title: `Containerized Deployment & Live Tuning`, desc: `Deploy Dockerized agent cluster with automated health checks and telemetry dashboards.`, tf: 'Days 11 - 14' })
    ],
    faqs: [
      (n) => ({ q: `How do autonomous agents prevent hallucinations during ${n.short} execution?`, a: `We enforce strict JSON Schema validation on all tool parameters, accompanied by deterministic fallback routines and boundary checks.` }),
      (n) => ({ q: `Can agents connect to our existing ${n.entities.split(',')[0]} database?`, a: `Yes. Agents connect securely through authenticated REST APIs, GraphQL endpoints, or read-only database replicas.` }),
      (n) => ({ q: `What happens when an agent encounters an edge case it cannot solve?`, a: `Uncertain requests trigger an immediate escalation event, pausing execution and notifying human operators via Slack or email.` }),
      (n) => ({ q: `How are sensitive API keys and client credentials protected?`, a: `Credentials are encrypted at rest using AES-256 and injected into agent runtimes via secure environment vaults.` }),
      (n) => ({ q: `What response latency can we expect for customer-facing agents?`, a: `Our optimized tool-calling pipelines achieve sub-1.5 second initial response times across text chat and webhook interfaces.` })
    ],
    biz_pillars: [
      (n) => ({ title: `Sub-60s Automated Resolution`, desc: `Autonomous agents connect directly to ${n.entities.split(',')[0]} to resolve inquiries and execute workflows within policy guidelines.`, product: `AI Customer Service ($147/mo)` }),
      (n) => ({ title: `Context-Aware Operational Triage`, desc: `Automatically classifies, routes, and enriches incoming requests across ${n.terms[0]} without human intervention.`, product: `Autonomous Support Bot & Webhook Triage` }),
      (n) => ({ title: `Deterministic Decision Execution`, desc: `Executes multi-step workflows with strict tool-calling boundaries and human-in-the-loop review gates.`, product: `Agentic Workflow Automation ($297/mo)` })
    ]
  },

  'web-app-engineering': {
    service_name: 'Next.js Web Engineering',
    short: 'Web Engineering',
    badge: 'Modern Web Engineering',
    service_deep_dive: 'We construct high-performance, enterprise-grade web applications utilizing Next.js App Router, React Server Components, and TypeScript. Our architecture prioritizes sub-50ms edge rendering, zero layout shift, accessibility, and clean database integrations.',
    pain_templates: [
      (n) => ({ title: `Sluggish Web Interfaces & High Client Bounce Rates`, description: `Bloated client-side JavaScript bundles cause slow first contentful paint times, frustrating buyers in ${n.market}.`, impact: `Elevated page abandonment rates and depressed digital conversion velocity.` }),
      (n) => ({ title: `Brittle Frontend Codebases & Escalating Technical Debt`, description: `Legacy single-page apps accumulate tangled dependencies and undocumented state, slowing feature delivery for ${n.terms[0]}.`, impact: `Delayed product roadmaps and inflated engineering maintenance costs.` }),
      (n) => ({ title: `Accessibility & Mobile Layout Instability Penalties`, description: `Layout shifts and non-compliant markup damage user experience across mobile devices, harming search rankings.`, impact: `Lowered Core Web Vitals scores and lost qualified inbound search traffic.` })
    ],
    capabilities: [
      (n) => ({ title: `React Server Components & App Router Architecture`, spec: `Builds modular page components that render on the server, eliminating client-side JavaScript overhead across ${n.terms[0]} screens.`, deliverable: `Production Next.js application codebase with optimized bundle splitting.` }),
      (n) => ({ title: `Type-Safe Database Integration & Server Actions`, spec: `Integrates PostgreSQL and Prisma ORM with comprehensive end-to-end TypeScript typing across ${n.terms[1]} models.`, deliverable: `Type-safe database schemas, migrations, and validated server actions.` }),
      (n) => ({ title: `Enterprise UI Design & Component Systems`, spec: `Implements responsive, accessible UI components styled with Tailwind CSS meeting WCAG 2.1 AA accessibility standards.`, deliverable: `Complete reusable design component library with zero cumulative layout shift.` }),
      (n) => ({ title: `Continuous Integration & Edge Deployment CI/CD`, spec: `Configures automated GitHub Actions pipelines, linting gates, unit testing, and edge CDN deployments.`, deliverable: `Automated CI/CD pipeline deploying preview and production releases.` })
    ],
    phases: [
      (n) => ({ title: `Information Architecture & Wireframing`, desc: `Map application route hierarchy, data schemas, and responsive user flows for ${n.short}.`, tf: 'Days 1 - 3' }),
      (n) => ({ title: `Frontend Component & Theme Construction`, desc: `Build reusable React Server Components with Tailwind CSS styling and fluid layouts.`, tf: 'Days 4 - 7' }),
      (n) => ({ title: `Backend API & Database Connection`, desc: `Implement type-safe Prisma models, server actions, and third-party API routes for ${n.entities.split(',')[0]}.`, tf: 'Days 8 - 10' }),
      (n) => ({ title: `Performance Optimization & Edge Deployment`, desc: `Audit bundle sizes, enforce Core Web Vitals, and deploy to edge production CDN.`, tf: 'Days 11 - 14' })
    ],
    faqs: [
      (n) => ({ q: `Why do you prioritize Next.js App Router for ${n.short} applications?`, a: `Next.js App Router provides server-rendered speed, superior SEO visibility, reduced client bundle sizes, and instant edge caching.` }),
      (n) => ({ q: `Can this web application scale to millions of monthly visitors?`, a: `Yes. By leveraging edge caching and serverless execution, our web architectures scale effortlessly with zero server maintenance.` }),
      (n) => ({ q: `How do you ensure zero cumulative layout shift (CLS)?`, a: `We enforce explicit font preloading, image aspect ratios, and server-side skeleton renders to eliminate layout reflows.` }),
      (n) => ({ q: `Do you provide full source code ownership upon project completion?`, a: `Yes. All source code, design systems, and deployment configurations are transferred directly to your organization GitHub repository.` }),
      (n) => ({ q: `How do you handle authentication and user session security?`, a: `We implement industry-standard authentication protocols including OAuth 2.0, magic links, and encrypted HTTP-only session cookies.` })
    ],
    biz_pillars: [
      (n) => ({ title: `Edge-Rendered Speed & Conversion Optimization`, desc: `Eliminates slow load times with sub-50ms React Server Components rendering on global edge networks.`, product: `Next.js Production Retainer` }),
      (n) => ({ title: `End-to-End Type Safety & Data Integrity`, desc: `Prevents runtime bugs and data corruption with strict TypeScript validation across client, server, and database layers.`, product: `Full-Stack Web Engineering ($297/mo)` }),
      (n) => ({ title: `Flawless Core Web Vitals & SEO Readiness`, desc: `Achieves 99+ Lighthouse performance scores, ensuring top organic search ranking and zero layout shift.`, product: `Enterprise Web Architecture` })
    ]
  },

  'outbound-infrastructure': {
    service_name: 'Cold Outbound & Lead Engine',
    short: 'Cold Outbound',
    badge: 'Outbound Pipeline Engineering',
    service_deep_dive: 'We build enterprise cold email and lead generation infrastructure designed to maintain pristine sender reputation and 99%+ inbox placement. Our systems combine dedicated sending domains, automated mailbox warm-up routines, DNS security records, and AI-personalized copywriting.',
    pain_templates: [
      (n) => ({ title: `Catastrophic Domain Blacklisting on Primary Corporate Domains`, description: `Blasting uncalibrated cold outreach from primary corporate domains destroys sender reputation and sends executive emails to spam.`, impact: `Critical business emails land in spam and sales outreach grinds to a total halt.` }),
      (n) => ({ title: `Generic Outbound Sequences Failing with Decision-Makers`, description: `Decision-makers in ${n.market} instantly delete template emails that lack verifiable industry context regarding ${n.terms[0]}.`, impact: `Sub-1% reply rates and wasted sales development representative payroll.` }),
      (n) => ({ title: `High Email Bounce Rates Triggering ISP Spam Traps`, description: `Purchasing stale, unverified contact lists causes bounce rates to exceed 8%, alerting Gmail and Outlook deliverability filters.`, impact: `Immediate suspension of sending accounts and ruined domain trust.` })
    ],
    capabilities: [
      (n) => ({ title: `Multi-Domain Secondary Sending Architecture for ${n.short}`, spec: `Provisions isolated secondary domain variants with automated DNS record rotation and graduated mailbox warmups.`, deliverable: `Hardened email infrastructure with 99%+ deliverability rating.` }),
      (n) => ({ title: `DNS Authentication & Deliverability Hardening`, spec: `Deploys 2048-bit DKIM keys, strict SPF records, DMARC policies, and custom tracking CNAME records.`, deliverable: `Fully authenticated DNS configurations passing deliverability audits.` }),
      (n) => ({ title: `Intent-Driven Prospect Radar & Verification`, spec: `Monitors social signals and firmographic databases to extract verified decision-makers actively researching ${n.terms[0]}.`, deliverable: `Weekly stream of verified, SMTP-validated decision-maker prospects.` }),
      (n) => ({ title: `Automated CRM Pipeline Dispatch & Routing`, spec: `Webhook sync sending positive prospect replies directly into ${n.entities.split(',')[0]} with automated SMS alerts to account executives.`, deliverable: `Instant lead handoff under 60 seconds from prospect reply.` })
    ],
    phases: [
      (n) => ({ title: `Secondary Domain Acquisition & DNS Hardening`, desc: `Procure secondary domain variants, configure SPF/DKIM/DMARC records, and set up MX routing.`, tf: 'Days 1 - 3' }),
      (n) => ({ title: `Mailbox Provisioning & Automated Ramp-Up`, desc: `Initialize mailboxes and connect to automated peer-to-peer warm-up network for 21 days.`, tf: 'Days 4 - 7' }),
      (n) => ({ title: `Prospect Scraping & Algorithmic Email Verification`, desc: `Extract decision-makers researching ${n.terms[0]} and scrub contact lists through real-time SMTP validators.`, tf: 'Days 8 - 10' }),
      (n) => ({ title: `Campaign Sequence Activation & CRM Webhook Sync`, desc: `Launch personalized email sequences and route positive prospect replies to sales reps.`, tf: 'Days 11 - 14' })
    ],
    faqs: [
      (n) => ({ q: `Why do we need separate secondary domains for ${n.short} outreach?`, a: `Using secondary domains protects your primary corporate domain reputation from spam complaints and temporary ISP rate-limits.` }),
      (n) => ({ q: `How long does it take to safely warm up a new cluster of mailboxes?`, a: `We adhere to a conservative 21-day algorithmic ramp-up schedule before launching full-scale outbound campaigns.` }),
      (n) => ({ q: `What email deliverability and open rates can we expect?`, a: `Our clients consistently maintain 99%+ deliverability and 45% to 65% open rates across warmed enterprise mailboxes.` }),
      (n) => ({ q: `How do you prevent emails from landing in Google and Outlook spam filters?`, a: `We implement strict DNS alignment, rotate across multiple sending inboxes, restrict daily volume per mailbox, and avoid spam trigger words.` }),
      (n) => ({ q: `Can outbound replies sync directly into our ${n.entities.split(',')[0]}?`, a: `Yes. Incoming positive replies forward automatically to your account executives with lead context and notification alerts.` })
    ],
    biz_pillars: [
      (n) => ({ title: `Secondary Sending Fleet & Deliverability Hardening`, desc: `Provisions isolated secondary domains with automated SPF, DKIM, and DMARC records protecting your primary brand domain.`, product: `Outbound Deliverability Engine ($297/mo)` }),
      (n) => ({ title: `Social Intent Prospect Radar`, desc: `Detects real-time purchasing signals and pain discussions across online channels, delivering verified decision-maker leads.`, product: `Scout Intent Radar` }),
      (n) => ({ title: `Context-Aware AI Message Personalization`, desc: `Crafts bespoke cold sequences citing specific prospect news, job openings, and technology stacks driving 12-16% reply rates.`, product: `Automated Outreach Pipeline` })
    ]
  },

  'composio-integrations': {
    service_name: 'Composio Agent Integrations',
    short: 'Composio Integrations',
    badge: 'Agent Tooling Architecture',
    service_deep_dive: 'We architect self-hosted Composio execution environments connecting AI models directly to over 200 software applications, databases, and enterprise platforms. By providing secure OAuth credential token vaults, function execution sandboxes, and audit logs, our integrations empower agents to act safely.',
    pain_templates: [
      (n) => ({ title: `Fragile Point-to-Point API Integrations in ${n.short}`, description: `Hardcoding bespoke API connectors between LLM models and ${n.entities} creates fragile endpoints that break whenever external schemas update.`, impact: `Frequent integration outages, data corruption, and constant developer maintenance.` }),
      (n) => ({ title: `Credential Leakage & Insecure Token Management`, description: `Storing third-party API tokens in flat files or agent prompt contexts exposes corporate keys to prompt injection vulnerabilities.`, impact: `Severe security compromise, unauthorized data exfiltration, and regulatory audit penalties.` }),
      (n) => ({ title: `Unmonitored Third-Party API Mutations`, description: `Allowing language models to execute API mutations without transactional sandboxing or audit logs leads to irreversible state errors.`, impact: `Accidental deletion of customer records and loss of operational data integrity.` })
    ],
    capabilities: [
      (n) => ({ title: `Self-Hosted Composio Engine Runtime for ${n.short}`, spec: `Deploys private Composio infrastructure on dedicated servers ensuring zero third-party data leakage for ${n.market}.`, deliverable: `Production Composio deployment with isolated container network.` }),
      (n) => ({ title: `200+ SaaS Tool Connectors & Custom Actions for ${n.entities}`, spec: `Configures pre-built and bespoke action connectors connecting agents directly to ${n.entities}.`, deliverable: `Validated tool registry ready for autonomous LLM function calling.` }),
      (n) => ({ title: `Secure OAuth Token Vault & Credential Lifecycle`, spec: `Manages user authentication, token refresh flows, and scoped permission boundaries in an encrypted AES-256 vault.`, deliverable: `Zero-trust credential storage system with automated token rotation.` }),
      (n) => ({ title: `Execution Sandboxing & Auditable Telemetry`, spec: `Executes third-party API mutations inside temporary sandbox containers with complete transaction logging across ${n.terms[0]}.`, deliverable: `Audit dashboard recording agent tool invocations, inputs, and outputs.` })
    ],
    phases: [
      (n) => ({ title: `Composio Server Deployment & Network Isolation`, desc: `Deploy containerized Composio runtime behind private Docker bridge networks.`, tf: 'Days 1 - 3' }),
      (n) => ({ title: `SaaS App Authentication & Scoped OAuth Binding`, desc: `Register enterprise applications, configure OAuth client IDs, and map scopes for ${n.entities.split(',')[0]}.`, tf: 'Days 4 - 7' }),
      (n) => ({ title: `Custom Action Schemas & Sandbox Validation`, desc: `Write custom OpenAPI definitions and test sandboxed function invocations for ${n.terms[0]}.`, tf: 'Days 8 - 10' }),
      (n) => ({ title: `Agent Integration & Audit Logging Activation`, desc: `Connect LLM runtime to Composio tool registry and activate auditable telemetry.`, tf: 'Days 11 - 14' })
    ],
    faqs: [
      (n) => ({ q: `What is Composio and how does it help our ${n.short} workflows?`, a: `Composio provides standard authentication, tool definitions, and API bindings so LLMs can interact with hundreds of SaaS platforms effortlessly.` }),
      (n) => ({ q: `Why run a self-hosted Composio runtime instead of cloud services?`, a: `Self-hosting keeps your corporate API tokens, internal databases, and client credentials entirely within your private cloud perimeter.` }),
      (n) => ({ q: `How does Composio handle OAuth refresh token expirations?`, a: `The Composio token manager monitors expiration timestamps and executes background refresh handshakes autonomously.` }),
      (n) => ({ q: `Can we create custom internal API tools for proprietary ${n.short} software?`, a: `Yes. We build custom OpenAPI and Swagger schemas that register seamlessly as callable tools in your Composio workspace.` }),
      (n) => ({ q: `How do you prevent agents from making unauthorized API calls?`, a: `We configure strict role-based permission policies, parameter validation schemas, and rate-limiting thresholds on sensitive endpoints.` })
    ],
    biz_pillars: [
      (n) => ({ title: `Self-Hosted Zero-Trust Tool Runtime`, desc: `Runs Composio in isolated private containers, ensuring corporate API tokens and client records never touch third-party cloud servers.`, product: `Composio Tooling Infrastructure ($297/mo)` }),
      (n) => ({ title: `Turnkey Ecosystem Connectivity`, desc: `Bridges language models to ${n.entities}, enabling end-to-end automation across corporate applications.`, product: `Custom API Connector Suite` }),
      (n) => ({ title: `Auditable Tool Execution Telemetry`, desc: `Records complete transaction payload histories, parameter inputs, and execution outputs for total governance.`, product: `Enterprise Governance Vault` })
    ]
  },

  'cloud-vps-hardening': {
    service_name: 'Cloud VPS & Docker Hardening',
    short: 'VPS Infrastructure',
    badge: 'Zero-Trust Infrastructure',
    service_deep_dive: 'We deploy hardened, zero-trust cloud infrastructure on Ubuntu VPS servers behind Cloudflare edge proxies. Our setup isolates multi-container Docker workloads, eliminates open public ports via Cloudflare Tunnels, enforces SSH key-only access, and configures automated failover monitoring.',
    pain_templates: [
      (n) => ({ title: `Open Public Port Exposure & Automated Brute-Force Probes`, description: `Leaving SSH port 22 and administrative interfaces exposed invites constant automated port scanning and credential attacks across ${n.market}.`, impact: `High risk of unauthorized server ingress, malware injection, and server hostage situations.` }),
      (n) => ({ title: `Multi-Tenant Container Leakage & Unrestricted Root Permissions`, description: `Running Docker containers as root without virtual network bridge segmentation allows compromised containers to compromise host filesystems.`, impact: `Catastrophic host server takeover and unauthorized client database exfiltration.` }),
      (n) => ({ title: `Unmonitored Outages & Manual Disaster Recovery`, description: `Lacking automated off-site database backups and real-time health alerts turns server hardware failures into multi-day service outages.`, impact: `Severe client downtime, lost revenue, and violation of contractual service level agreements.` })
    ],
    capabilities: [
      (n) => ({ title: `Ubuntu Server Hardening & Kernel Optimization for ${n.short}`, spec: `Disables root password login, installs ed25519 SSH keys, enables sysctl kernel protections, and audits open ports.`, deliverable: `Hardened Linux operating system baseline meeting CIS compliance standards.` }),
      (n) => ({ title: `Cloudflare Zero Trust Tunnel Ingress`, spec: `Routes all inbound web traffic through encrypted Cloudflare edge tunnels, closing all inbound firewall ports on ${n.market} origin hosts.`, deliverable: `Zero-open-port network configuration completely shielding server IP addresses.` }),
      (n) => ({ title: `Docker Compose Multi-Container Sandboxing`, spec: `Isolates application workloads into dedicated virtual bridge networks with memory boundaries for ${n.terms[0]} services.`, deliverable: `Production Docker Compose architecture with encrypted environment secrets.` }),
      (n) => ({ title: `Automated Offsite Snapshot Backups & Health Telemetry`, spec: `Deploys cron-driven encrypted database backups to offsite S3 buckets alongside automated system health alerts.`, deliverable: `Automated disaster recovery pipeline and Grafana/Prometheus telemetry.` })
    ],
    phases: [
      (n) => ({ title: `Operating System Audit & Linux Hardening`, desc: `Install Ubuntu 24.04 LTS, disable password authentication, configure UFW, and install Fail2ban.`, tf: 'Days 1 - 3' }),
      (n) => ({ title: `Cloudflare Zero Trust & Cloudflared Tunnel Setup`, desc: `Deploy cloudflared daemon, map ingress routing rules, and lock down origin IP firewalls.`, tf: 'Days 4 - 7' }),
      (n) => ({ title: `Docker Bridge Isolation & Resource Quotas`, desc: `Structure multi-container compose files with internal networking and memory boundaries for ${n.short}.`, tf: 'Days 8 - 10' }),
      (n) => ({ title: `Automated Backups & Telemetry Alerting`, desc: `Schedule encrypted off-site database backups and configure real-time alert webhooks.`, tf: 'Days 11 - 14' })
    ],
    faqs: [
      (n) => ({ q: `How does a Cloudflare Tunnel shield our ${n.short} infrastructure?`, a: `Cloudflare Tunnels establish outbound-only connections to Cloudflare edge nodes, keeping origin server IPs invisible to port scanners.` }),
      (n) => ({ q: `What happens if a Docker container crashes or experiences high memory usage?`, a: `Docker daemon restart policies immediately relaunch failed containers, while systemd monitors overall memory and CPU thresholds.` }),
      (n) => ({ q: `How do you handle automated SSL and TLS certificate renewals?`, a: `SSL certificates are managed automatically at the Cloudflare edge and through Let's Encrypt automated certbot daemons.` }),
      (n) => ({ q: `Can we access internal administrative dashboards securely?`, a: `Yes. Administrative interfaces are protected behind Cloudflare Access with two-factor authentication and role-based email verification.` }),
      (n) => ({ q: `How often are security patches and updates applied to the VPS?`, a: `We configure unattended-upgrades on Ubuntu to apply critical operating system security patches automatically without downtime.` })
    ],
    biz_pillars: [
      (n) => ({ title: `Zero-Open-Port Edge Tunneling`, desc: `Shields origin server IP addresses behind Cloudflare Tunnels, completely preventing direct DDoS and port-scanning attacks.`, product: `VPS Hardening & Cloudflare Defense ($297/mo)` }),
      (n) => ({ title: `Isolated Multi-Container Sandboxing`, desc: `Segregates applications into isolated Docker bridge networks with strict memory quotas and unprivileged execution.`, product: `Containerized Production Architecture` }),
      (n) => ({ title: `Automated Offsite Disaster Recovery`, desc: `Schedules daily encrypted database snapshots to off-site object storage with automated restore verification.`, product: `Disaster Recovery & Uptime SLA` })
    ]
  },

  'whop-monetization': {
    service_name: 'Whop Monetization Systems',
    short: 'Whop Monetization',
    badge: 'Digital Monetization Systems',
    service_deep_dive: 'We build automated monetization systems and membership gating utilizing the Whop API and developer platform. From tier entitlement logic and digital product delivery to automated Discord role assignment and churn mitigation webhooks, we turn audience traffic into recurring revenue.',
    pain_templates: [
      (n) => ({ title: `Manual Customer Onboarding & License Key Distribution`, description: `Fulfilling digital purchases and membership access manually via email creates fulfillment delays and support ticket chaos for ${n.market}.`, impact: `Customer frustration, delayed time-to-value, and avoidable refund requests.` }),
      (n) => ({ title: `High Checkout Abandonment & Friction on Generic Processors`, description: `Multi-step legacy checkout flows without localized currency or mobile payment options cause prospective buyers to abandon transactions.`, impact: `Depressed conversion rates and lost recurring customer subscription value.` }),
      (n) => ({ title: `Unmonitored Subscription Churn & Silent Cancellations`, description: `Lacking automated dunning retry routines and cancellation recovery funnels causes recurring memberships to expire silently.`, impact: `Depressed monthly recurring revenue and shortened customer lifetime value.` })
    ],
    capabilities: [
      (n) => ({ title: `Whop Product Tier Architecture for ${n.short}`, spec: `Structures subscription tiers, one-time passes, and enterprise add-ons with granular entitlement mappings for ${n.market}.`, deliverable: `Configured Whop store catalog ready for high-converting checkouts.` }),
      (n) => ({ title: `Automated Webhook License Key Dispatcher`, spec: `Listens for payment events and generates cryptographic license keys or account credentials instantly for ${n.terms[0]} users.`, deliverable: `Zero-latency fulfillment webhook service with automated retry queues.` }),
      (n) => ({ title: `Discord & Private Portal Access Synchronization`, spec: `Synchronizes active customer subscriptions with Discord server roles and private platform access permissions.`, deliverable: `Automated member onboarding bot revoking access automatically upon cancellation.` }),
      (n) => ({ title: `Checkout Optimization & Churn Recovery`, spec: `Deploys localized currencies, one-click checkout payments, and dunning retry sequences to rescue failed subscription renewals.`, deliverable: `Revenue retention funnel recovering abandoned checkouts and expired payment methods.` })
    ],
    phases: [
      (n) => ({ title: `Product Tier & Pricing Architecture Design`, desc: `Structure digital offerings, membership tiers, and permission entitlements inside Whop for ${n.short}.`, tf: 'Days 1 - 3' }),
      (n) => ({ title: `Webhook Listener & License Key Dispatcher`, desc: `Deploy edge webhook endpoints handling payment success, cancellation, and renewal events.`, tf: 'Days 4 - 7' }),
      (n) => ({ title: `Discord Bot & Private Portal Gating`, desc: `Configure automatic role assignment and connect gated member areas for ${n.terms[0]}.`, tf: 'Days 8 - 10' }),
      (n) => ({ title: `Checkout Conversion & Dunning Optimization`, desc: `Set up localized currencies, abandoned checkout recovery, and payment retry logic.`, tf: 'Days 11 - 14' })
    ],
    faqs: [
      (n) => ({ q: `Why use Whop to monetize ${n.short} digital products and memberships?`, a: `Whop provides industry-leading checkout conversion rates, built-in buyer discovery, and automated member role gating.` }),
      (n) => ({ q: `How do customers access digital deliverables after purchase?`, a: `Upon successful checkout, buyers receive instant access via their Whop customer portal and automated credential emails.` }),
      (n) => ({ q: `Can we accept international payments across multiple currencies?`, a: `Yes. Whop supports multi-currency transactions, regional payment methods, and automated tax compliance worldwide.` }),
      (n) => ({ q: `What happens when a customer cancels their subscription?`, a: `Webhooks trigger immediately upon cancellation, revoking access to protected Discord channels and software portals.` }),
      (n) => ({ q: `Can purchase webhooks dispatch data into ${n.entities.split(',')[0]}?`, a: `Yes. Payment success and churn events sync directly into your CRM to trigger customer lifecycle sequences.` })
    ],
    biz_pillars: [
      (n) => ({ title: `Frictionless One-Click Digital Checkout`, desc: `Maximizes conversion with mobile-optimized checkout funnels supporting Apple Pay, Google Pay, and localized currencies.`, product: `Whop Storefront Architecture ($297/mo)` }),
      (n) => ({ title: `Instant Automated Entitlement Gating`, desc: `Issues license keys, software access credentials, and Discord roles in under two minutes upon payment confirmation.`, product: `Automated Membership Fulfillment` }),
      (n) => ({ title: `Dunning Recovery & Churn Mitigation`, desc: `Rescues failed recurring subscription charges with intelligent payment retries and targeted win-back email sequences.`, product: `Recurring Revenue Retention Engine` })
    ]
  }
};

function generateFullCombination(nicheId, serviceId) {
  const { NICHE_DEFS } = require('./matrix_tailoring_engine.js');
  const n = NICHE_DEFS[nicheId];
  const s = SERVICE_SCHEMAS[serviceId];

  const h1 = `${s.service_name} for ${n.name}`;
  const subheadline = `Engineered specifically for ${n.buyer} in ${n.short} seeking to scale ${s.short} workflows. Built on modern ${s.service_name} infrastructure to eliminate operational bottlenecks, compress sales cycles, and drive predictable enterprise revenue.`;

  const deep_dive_1 = `Organizations operating in ${n.name} face compounding friction across ${n.terms.slice(0, 4).join(', ')}. Relying on manual workflows or generic off-the-shelf software leads to escalating customer acquisition costs, operational bottlenecks, and administrative drag. By engineering a dedicated ${s.service_name.toLowerCase()} architecture, companies establish automated, reproducible pipelines that scale cleanly.`;
  const deep_dive_2 = `Our engineering methodology integrates modern edge architecture directly into existing systems including ${n.entities}. Incoming data payloads undergo rigorous schema validation, state verification, and encrypted logging, ensuring leadership maintains absolute visibility and compliance across every transaction.`;

  const pain_points = s.pain_templates.map(fn => fn(n));
  const capabilities = s.capabilities.map(fn => fn(n));
  const phases = s.phases.map(fn => fn(n));
  const faqs = s.faqs.map(fn => fn(n));

  const humanSolutions = {
    businessTitle: `Operational & Revenue Defense for ${n.name}`,
    businessStory: `${n.biz_narrative} Adorise Digital deploys autonomous systems that remove operational drag and protect enterprise margins.`,
    businessPillars: s.biz_pillars.map(fn => fn(n)),
    personalTitle: `Protecting ${n.buyer} from Executive Fatigue & Anxiety`,
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
    service_name: s.service_name,
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
  SERVICE_SCHEMAS
};
