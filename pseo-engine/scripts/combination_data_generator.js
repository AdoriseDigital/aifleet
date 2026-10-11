// Generator to test combination-specific data across all 70 combinations
const fs = require('fs');

const NICHES = {
  'b2b-saas': {
    name: 'B2B SaaS & Enterprise Software',
    short: 'B2B SaaS',
    acv: '$12,000 - $60,000/yr',
    persona: 'VP of Growth and Chief Technology Officers',
    focus: 'software integrations, competitor alternatives, and self-serve onboarding',
    context: 'cloud software platforms, ARR expansion, churn mitigation, and multi-tenant systems',
    stress: 'late-night sprint blockers, customer churn notifications, and investor updates'
  },
  'ecommerce-d2c': {
    name: 'High-Volume E-Commerce & D2C Brands',
    short: 'E-Commerce & D2C',
    acv: '$500,000 - $10M GMV',
    persona: 'E-Commerce Directors and Brand Founders',
    focus: 'catalog discoverability, promotional order surges, and customer support triage',
    context: 'Shopify Plus infrastructure, Klaviyo flows, SKU inventory, and return logistics',
    stress: 'supply chain shipping delays, ad account bans, and holiday ticket backlogs'
  },
  'fintech': {
    name: 'FinTech & Digital Financial Services',
    short: 'FinTech',
    acv: '$25,000 - $150,000/yr',
    persona: 'Chief Risk Officers, CFOs, and FinTech Founders',
    focus: 'institutional compliance, transaction data integrity, and automated risk underwriting',
    context: 'banking cores, ledger reconciliation, KYC/AML screening, and PCI-DSS standards',
    stress: 'regulatory compliance audits, payment settlement latency, and capital fraud exposure'
  },
  'healthtech-biotech': {
    name: 'HealthTech & Digital Health Platforms',
    short: 'HealthTech & Biotech',
    acv: '$30,000 - $120,000/yr',
    persona: 'Clinical Operations Directors and HealthTech CTOs',
    focus: 'HIPAA-compliant data containment, patient triage queues, and EHR connectivity',
    context: 'telehealth portals, electronic medical records, HL7/FHIR protocols, and clinical notes',
    stress: 'patient confidentiality liability, provider scheduling bottlenecks, and EHR API outages'
  },
  'proptech-realestate': {
    name: 'PropTech & Commercial Real Estate Platforms',
    short: 'PropTech & Real Estate',
    acv: '$15,000 - $80,000/yr',
    persona: 'Managing Brokers and Real Estate Asset Managers',
    focus: 'MLS feed ingestion, localized commercial landing pages, and investor deal distribution',
    context: 'commercial lease abstraction, regional property syndication, and tenant screening',
    stress: 'prolonged leasing vacancies, closing deal delays, and fragmented property data'
  },
  'legaltech-professional': {
    name: 'LegalTech & High-Ticket Professional Services',
    short: 'LegalTech & Advisory',
    acv: '$20,000 - $100,000/yr',
    persona: 'Managing Partners and Firm General Counsels',
    focus: 'ethical client acquisition, automated intake questionnaires, and matter onboarding',
    context: 'conflict checking, billable hour tracking, ABA compliance, and client retention',
    stress: 'grueling 80-hour billable weeks, client conflict disputes, and administrative overhead'
  },
  'venture-capital-private-equity': {
    name: 'Venture Capital & Private Equity Firms',
    short: 'VC & Private Equity',
    acv: '$50M - $1B AUM',
    persona: 'General Partners, Operating Partners, and Investment Directors',
    focus: 'proprietary deal sourcing, thesis outbound pipelines, and portfolio company monitoring',
    context: 'EBITDA expansion, LP reporting memos, CIM abstractions, and founder evaluation',
    stress: 'dry powder deployment timelines, missed proprietary dealflow, and partner friction'
  },
  'edtech': {
    name: 'EdTech & Online Learning Platforms',
    short: 'EdTech & Education',
    acv: '$10,000 - $50,000/yr',
    persona: 'Heads of Learning and EdTech Platform Founders',
    focus: 'curriculum discovery, asynchronous student support, and community membership gating',
    context: 'LMS platform integrations, cohort completion retention, and skill certification',
    stress: 'student drop-off after week two, manual grading fatigue, and subscription cancellations'
  },
  'cybersecurity': {
    name: 'Enterprise Cybersecurity & DevSecOps',
    short: 'Cybersecurity',
    acv: '$40,000 - $200,000/yr',
    persona: 'Chief Information Security Officers and DevSecOps Directors',
    focus: 'zero-trust perimeter defense, container isolation, and technical buyer enablement',
    context: 'SOC2 Type II, NIST frameworks, Cloudflare WAF, and CVE threat mitigation',
    stress: 'zero-day vulnerability notices, enterprise vendor risk reviews, and audit compliance'
  },
  'agency-consultancy': {
    name: 'Digital Agencies & High-Growth Consultancies',
    short: 'Agencies & Consultancies',
    acv: '$5,000 - $30,000/mo',
    persona: 'Agency Founders and Managing Directors',
    focus: 'predictable retainer acquisition, automated service delivery, and client reporting',
    context: 'client onboarding portals, scope creep boundaries, and billable team efficiency',
    stress: 'the feast-or-famine client cycle, scope creep negotiations, and client churn anxiety'
  }
};

const SERVICES = {
  'pseo-engine': {
    name: 'Programmatic SEO Engine',
    short: 'pSEO Engine',
    verb: 'scales organic inbound search visibility',
    tech: 'Next.js App Router, Incremental Static Regeneration, Schema.org microdata, and chunked XML sitemaps',
    metrics: [
      { val: '< 45ms', lbl: 'Edge TTFB', sub: 'Sub-second React Server Components load' },
      { val: '+340%', lbl: 'Pipeline Expansion', sub: 'Qualified inbound demo volume growth' },
      { val: '100%', lbl: 'Schema Validated', sub: 'Complete ProfessionalService JSON-LD' },
      { val: '$12k-$60k', lbl: 'Target ACV Tier', sub: 'High-value enterprise contract focus' }
    ]
  },
  'ai-agents': {
    name: 'Autonomous AI Agents',
    short: 'AI Agents',
    verb: 'automates multi-step decision workflows and customer inquiries',
    tech: 'LangGraph multi-agent orchestration, deterministic tool calling, and human-in-the-loop review checkpoints',
    metrics: [
      { val: '< 1.5s', lbl: 'Average Response Time', sub: 'Instantaneous automated resolution' },
      { val: '-68%', lbl: 'Support Ticket Volume', sub: 'Tier-1 customer inquiries automated' },
      { val: '99.9%', lbl: 'System Availability', sub: 'Redundant containerized agent clusters' },
      { val: '100%', lbl: 'Tool Calling Accuracy', sub: 'Deterministic schema validation gates' }
    ]
  },
  'web-app-engineering': {
    name: 'Next.js Web Engineering',
    short: 'Web Engineering',
    verb: 'constructs high-performance web applications and digital interfaces',
    tech: 'React Server Components, Next.js App Router, TypeScript, Tailwind CSS, and edge Prisma ORM',
    metrics: [
      { val: '< 30ms', lbl: 'Edge TTFB', sub: 'Sub-second React Server Components load' },
      { val: '99/100', lbl: 'Lighthouse Score', sub: 'Flawless Core Web Vitals rating' },
      { val: '0 CLS', lbl: 'Layout Shift', sub: 'Rock-solid visual stability' },
      { val: '100%', lbl: 'Type Safety', sub: 'End-to-end TypeScript validation' }
    ]
  },
  'outbound-infrastructure': {
    name: 'Cold Outbound & Lead Engine',
    short: 'Cold Outbound',
    verb: 'deploys multi-domain outbound prospecting infrastructure',
    tech: 'isolated secondary domains, automated mailbox warm-up, DNS security alignment, and social intent listening',
    metrics: [
      { val: '99.4%', lbl: 'Inbox Placement', sub: 'Pristine primary inbox delivery' },
      { val: '< 0.5%', lbl: 'Bounce Rate', sub: 'Real-time SMTP validation filtering' },
      { val: '58%', lbl: 'Average Open Rate', sub: 'Targeted executive subject line formulas' },
      { val: '100%', lbl: 'Domain Isolation', sub: 'Zero risk to primary brand domain' }
    ]
  },
  'composio-integrations': {
    name: 'Composio Agent Integrations',
    short: 'Composio Integrations',
    verb: 'bridges LLM agents to corporate APIs and SaaS platforms',
    tech: 'self-hosted Composio execution runtime, OAuth 2.0 PKCE token vaults, and sandboxed tool calling',
    metrics: [
      { val: '200+', lbl: 'Verified Tool Connectors', sub: 'Turnkey SaaS and database integrations' },
      { val: '< 80ms', lbl: 'Tool Execution Overhead', sub: 'Near-instantaneous function invocation' },
      { val: '0 Leak', lbl: 'Credential Exposure', sub: 'AES-256 encrypted token vault' },
      { val: '100%', lbl: 'Audit Logging', sub: 'Full transaction payload telemetry' }
    ]
  },
  'cloud-vps-hardening': {
    name: 'Cloudflare & VPS Infrastructure',
    short: 'VPS Infrastructure',
    verb: 'hardens server infrastructure and isolates containerized workloads',
    tech: 'Ubuntu LTS OS hardening, Cloudflare Zero Trust tunnels, Docker virtual networks, and UFW firewall rules',
    metrics: [
      { val: '100%', lbl: 'Zero-Trust Isolation', sub: 'Zero open public ports on origin servers' },
      { val: '99.99%', lbl: 'Infrastructure Uptime', sub: 'High-availability container health checks' },
      { val: '0 Root', lbl: 'Privilege Exposure', sub: 'Unprivileged container execution' },
      { val: '< 15min', lbl: 'Disaster Recovery RTO', sub: 'Automated off-site snapshot restores' }
    ]
  },
  'whop-monetization': {
    name: 'Whop Monetization Systems',
    short: 'Whop Monetization',
    verb: 'architects subscription tiers and automated digital product gating',
    tech: 'Whop API v2, automated license key provisioning, Discord role synchronization, and dunning webhooks',
    metrics: [
      { val: '+28%', lbl: 'Checkout Conversion', sub: 'Optimized frictionless payment funnels' },
      { val: '< 2min', lbl: 'Member Onboarding', sub: 'Instant automated role and license provisioning' },
      { val: '100%', lbl: 'Automated Gating', sub: 'Real-time subscription status synchronization' },
      { val: '$0 Fee', lbl: 'Custom Development Penalty', sub: 'Standard developer-friendly fee schedule' }
    ]
  }
};

function generateCombinationData(nicheId, serviceId) {
  const n = NICHES[nicheId];
  const s = SERVICES[serviceId];

  const h1 = `${s.name} for ${n.name}`;
  const subheadline = `Engineered specifically for ${n.persona} in ${n.short} seeking to scale ${s.short} workflows. Built on modern ${s.tech} to eliminate operational bottlenecks, compress sales cycles, and drive predictable enterprise revenue.`;

  const deep_dive_1 = `Organizations operating in ${n.name} face compounding friction across ${n.context}. Traditional methods relying on manual staff or generic tools fail when transaction volumes surge, leading to inflated operational expenditure and lost commercial momentum. By engineering a tailored ${s.name.toLowerCase()} pipeline, companies replace fragmented handoffs with deterministic, reproducible automation.`;
  const deep_dive_2 = `Our engineering approach couples ${s.tech} directly with existing enterprise systems in ${n.short}. Incoming data payloads undergo rigorous schema validation, state verification, and encrypted logging, ensuring leadership maintains complete governance over every operational transaction.`;

  const pain_points = [
    {
      title: `Escalating Manual Overhead in ${n.short}`,
      description: `Teams in ${n.name} spend critical labor hours manually coordinating ${n.focus}, creating severe operational delivery bottlenecks.`,
      impact: `Depressed revenue realization, higher cost per unit, and elongated conversion cycles.`
    },
    {
      title: `Fragile Point-to-Point Tools and Data Silos`,
      description: `Attempting to solve ${s.short} requirements with uncalibrated commercial off-the-shelf software leads to broken syncs and data loss across ${n.context}.`,
      impact: `Sub-optimal decision speed, increased human error rates, and security vulnerability exposure.`
    },
    {
      title: `Competitive Displacement from Faster Automated Rivals`,
      description: `Rival organizations adopting automated ${s.name.toLowerCase()} capture market share by executing ${n.focus} with 10x greater speed and lower margins.`,
      impact: `Erosion of customer market share and inability to maintain premium price points.`
    }
  ];

  const capabilities = [
    {
      title: `Tailored Architecture for ${n.short}`,
      spec: `Custom-engineered ${s.name} infrastructure aligned with ${n.context} and regulatory requirements.`,
      deliverable: `Production-ready deployment repository with automated configuration and telemetry.`
    },
    {
      title: `Deterministic Data Validation & Security`,
      spec: `Strict parameter enforcement and schema guards protecting transactions across ${n.focus}.`,
      deliverable: `Validated execution boundaries and automated transaction audit logs.`
    },
    {
      title: `Automated Workflow & System Interoperability`,
      spec: `Seamless API connectors synchronizing ${s.short} events with existing software and CRM suites.`,
      deliverable: `Turnkey integration bridge with automated retry queues and error handlers.`
    },
    {
      title: `Continuous Performance Telemetry & SLA Tracking`,
      spec: `Real-time health monitoring and metric dashboards tracking uptime, throughput, and error rates.`,
      deliverable: `Live telemetry dashboard with automated incident notification webhooks.`
    }
  ];

  const phases = [
    { title: `Systems Audit & ${n.short} Mapping`, desc: `Examine current workflows, data structures, and integration points across ${n.context}.`, tf: 'Days 1 - 3' },
    { title: `Core ${s.short} Architecture Setup`, desc: `Construct dynamic components, API adapters, and schema definitions on modern edge infrastructure.`, tf: 'Days 4 - 7' },
    { title: `Verification & Quality Assertion Gates`, desc: `Execute automated stress tests, schema compliance checks, and security perimeter scans.`, tf: 'Days 8 - 10' },
    { title: `Production Deployment & Handover`, desc: `Deploy to live edge network, activate automated monitoring, and transition operational documentation.`, tf: 'Days 11 - 14' }
  ];

  const faqs = [
    { q: `How does this ${s.name} deployment integrate into our existing ${n.short} environment?`, a: `We engineer modular, decoupled components and standard API webhooks that dock cleanly into your current stack without requiring structural refactoring.` },
    { q: `How does the system ensure compliance and data privacy for ${n.name}?`, a: `All data transactions are isolated, encrypted in transit and at rest, and validated against strict schema boundaries adhering to industry standards.` },
    { q: `What timeline is required before our team sees tangible operational results?`, a: `Our structured 14-day delivery sprint ensures production deployment and live automated execution within two weeks of initiation.` },
    { q: `Who retains ownership of the codebase, templates, and integration workflows?`, a: `Your organization maintains 100% intellectual property ownership of all custom code, configuration files, and data assets produced during deployment.` },
    { q: `How does this solution scale as our ${n.short} business expands?`, a: `Engineered on edge CDNs and serverless runtimes, our architecture automatically absorbs traffic and transaction spikes with zero latency degradation.` }
  ];

  const humanSolutions = {
    businessTitle: `Operational & Revenue Defense for ${n.name}`,
    businessStory: `Operating in ${n.name} demands absolute operational velocity. When teams get stuck in manual administrative coordination across ${n.context}, strategic pipeline expansion grinds to a halt. Our systems provide a durable technical moat that protects your operating margins.`,
    businessPillars: [
      {
        title: `Automated Pipeline & Operational Velocity`,
        desc: `Replaces fragile manual coordination with deterministic ${s.name.toLowerCase()} workflows tailored for ${n.short}.`,
        product: `Adorise Engineered Systems ($297/mo)`
      },
      {
        title: `Systematic Client & Revenue Protection`,
        desc: `Guarantees consistent execution across ${n.focus}, mitigating operational errors and customer drop-off.`,
        product: `Production Architecture Retainer`
      },
      {
        title: `Ecosystem Authority & Market Leadership`,
        desc: `Establishes unmistakable operational superiority over competitors relying on slower legacy practices.`,
        product: `Enterprise Turnkey Deployment`
      }
    ],
    personalTitle: `Protecting ${n.persona} from Executive Fatigue & Anxiety`,
    personalStory: `Behind every organization in ${n.name} are dedicated leaders bearing the psychological burden of ${n.stress}. We engineer software that restores executive sanity, evening calm, and focused strategic thinking.`,
    personalPillars: [
      {
        icon: '🛡️',
        title: 'Communication Stress & Conflict Defense',
        desc: `When high-pressure emails arrive regarding ${n.focus}, InboxCalm scores toxicity and drafts calm, de-escalating replies.`,
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
    metrics: s.metrics,
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
  generateCombinationData,
  NICHES,
  SERVICES
};
