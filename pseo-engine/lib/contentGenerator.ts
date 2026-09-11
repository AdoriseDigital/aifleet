import {
  ServiceInfo,
  NicheInfo,
  TechStackInfo,
  LocationInfo,
  GeneratedPageData,
  PainPoint,
  CoreCapability,
  WorkflowPhase,
  TrustMetric,
  FAQItem
} from '../types/pseo';
import { getProductCTA } from './whopCatalog';

// Niche Knowledge Matrix
const NICHE_PROFILES: Record<string, {
  industry_name: string;
  typical_acv: string;
  economic_metrics: {
    cac_benchmark: string;
    payback_period: string;
    target_kpi: string;
    revenue_upside: string;
  };
  context_prose: string;
  pain_points: PainPoint[];
  faq_focus: { q: string; a: string }[];
}> = {
  'b2b-saas': {
    industry_name: 'B2B SaaS & Enterprise Software',
    typical_acv: '$12,000 - $60,000/yr',
    economic_metrics: {
      cac_benchmark: '$35 - $90 per paid ad click',
      payback_period: '18 - 24 months on paid ads',
      target_kpi: '+340% qualified inbound pipeline',
      revenue_upside: 'Sub-45 day customer payback'
    },
    context_prose: 'B2B SaaS companies face escalating customer acquisition costs on paid search channels, while manual documentation and content production fail to capture high-intent buyers searching for specific software integrations, competitor alternatives, and automated workflows.',
    pain_points: [
      {
        title: 'Skyrocketing Paid Ad Customer Acquisition Costs',
        description: 'Bidding wars on commercial software keywords push click costs over $50, creating rented pipeline that evaporates the moment ad budgets are trimmed.',
        business_impact: 'Inflated payback periods exceeding 18-24 months and depressed operating margins.'
      },
      {
        title: 'Engineering Capacity Siphoned into Marketing Integrations',
        description: 'Product engineering teams spend precious sprints building CMS templates and custom landing pages rather than shipping core roadmap software features.',
        business_impact: 'Delayed product releases and competitor feature parity erosion.'
      },
      {
        title: 'Uncontrolled AI Content Thinness & De-indexing Penalties',
        description: 'Generic AI writing tools produce shallow, repetitive landing pages that search engines flag as low-quality, risking algorithmic penalties across the entire root domain.',
        business_impact: 'Domain authority degradation and lost organic buyer visibility.'
      }
    ],
    faq_focus: [
      {
        q: 'How does this integrate into our existing Next.js / Vercel product repository?',
        a: 'We engineer modular React Server Components and dynamic route parameters that mount cleanly under /solutions or /integrations without altering your primary application code.'
      },
      {
        q: 'How do you guarantee that technical SaaS documentation and metrics remain accurate?',
        a: 'Every page data record is validated against a strict JSON Schema with deterministic fallback rules and domain assertion gates, preventing hallucinated specifications.'
      }
    ]
  },
  'ecommerce-d2c': {
    industry_name: 'High-Volume E-Commerce & D2C Brands',
    typical_acv: '$500,000 - $10M GMV',
    economic_metrics: {
      cac_benchmark: '68% - 74% cart abandonment rate',
      payback_period: '14 - 30 days initial cohort',
      target_kpi: '+28% catalog search discovery',
      revenue_upside: '2.4x return on organic traffic'
    },
    context_prose: 'High-growth retail and D2C brands navigate volatile ad auction dynamics across Meta and Google, where product catalog search volume remains uncaptured due to static CMS page limits and unoptimized collection taxonomies.',
    pain_points: [
      {
        title: 'Meta and Google Ad Auction Margin Compression',
        description: 'Third-party tracking restrictions and rising cost-per-mille (CPM) rates squeeze contribution margins on direct response ad campaigns.',
        business_impact: 'Declining return on ad spend and diminished first-order profitability.'
      },
      {
        title: 'Massive Long-Tail Product Query Coverage Gaps',
        description: 'Shoppers execute precise multi-attribute searches (material, use case, size, geography), but static stores only maintain top-level collection pages.',
        business_impact: 'Lost organic transactions to aggressive marketplace aggregators.'
      },
      {
        title: 'Peak Traffic Conversion Drops from Clunky Catalog Navigation',
        description: 'Slow-loading category filters and sluggish mobile templates drive bounce rates up during commercial flash campaigns and peak seasons.',
        business_impact: 'High cart abandonment and wasted marketing acquisition dollars.'
      }
    ],
    faq_focus: [
      {
        q: 'Can this connect dynamically with Shopify Plus or BigCommerce product catalogs?',
        a: 'Yes. We ingest your product taxonomy via GraphQL webhooks and generate static edge landing pages updated automatically as inventory and pricing shift.'
      },
      {
        q: 'How does this prevent duplicate content across hundreds of similar product variants?',
        a: 'Each landing page generates distinct buyer intent angles, unique FAQ schema, localized delivery metrics, and custom value drivers with verified uniqueness.'
      }
    ]
  },
  'fintech': {
    industry_name: 'FinTech & Digital Financial Services',
    typical_acv: '$50,000 - $250,000/yr',
    economic_metrics: {
      cac_benchmark: '28% - 35% KYC drop-off rate',
      payback_period: '90 - 120 days compliance cycle',
      target_kpi: 'Sub-150ms edge validation response',
      revenue_upside: 'Zero compliance verification violations'
    },
    context_prose: 'Financial technology platforms operate under strict regulatory scrutiny, requiring deterministic data integrity, enterprise-grade encryption, and zero tolerance for compliance drift when communicating financial workflows.',
    pain_points: [
      {
        title: 'Regulatory Review Cycles Stalling Inbound Marketing',
        description: 'Strict SOC2 Type II, PCI-DSS, and financial disclosure guidelines prevent marketing teams from rapidly deploying targeted acquisition funnels.',
        business_impact: 'Multi-month pipeline delays while competitors capture emerging market share.'
      },
      {
        title: 'Severe Multi-Step KYC and Identity Verification Friction',
        description: 'Complex regulatory onboarding steps cause high abandonment among institutional finance officers and retail investors alike.',
        business_impact: 'High customer acquisition waste on qualified financial decision-makers.'
      },
      {
        title: 'Legacy Banking Core Latency and Unstable Integrations',
        description: 'Connecting modern frontend user experiences with legacy core banking databases frequently produces timeout errors and synchronization failures.',
        business_impact: 'Poor customer trust and costly manual reconciliation overhead.'
      }
    ],
    faq_focus: [
      {
        q: 'How does this comply with financial data confidentiality and disclosure mandates?',
        a: 'Our systems produce deterministic, audited static outputs with zero client data logging, ensuring full compliance with SOC2, GDPR, and financial advertising disclosures.'
      },
      {
        q: 'Can we configure custom approval workflows before programmatic landing pages publish?',
        a: 'Yes. We provide human-in-the-loop audit gates and automated schema verification scripts to confirm compliance prior to production release.'
      }
    ]
  },
  'healthtech-biotech': {
    industry_name: 'HealthTech & Digital Health Platforms',
    typical_acv: '$35,000 - $150,000/yr',
    economic_metrics: {
      cac_benchmark: '$120 - $380 patient acquisition CAC',
      payback_period: '6 - 9 month provider sales cycle',
      target_kpi: '100% HIPAA/BAA audit compliance',
      revenue_upside: '4.1x clinical partner pipeline'
    },
    context_prose: 'HealthTech innovators and clinical software providers must balance patient acquisition and provider onboarding with strict HIPAA safeguards, secure business associate agreements, and verified medical accuracy.',
    pain_points: [
      {
        title: 'HIPAA and Business Associate Agreement Friction',
        description: 'Deploying digital health funnels requires encrypted audit trails, strict data segregation, and zero-trust infrastructure to prevent protected health information leaks.',
        business_impact: 'Severe regulatory penalties and protracted enterprise security reviews.'
      },
      {
        title: 'Protracted Provider Onboarding and EHR Integration Delays',
        description: 'Legacy electronic health record integrations require custom HL7/FHIR mappings that stall clinical provider activation for months.',
        business_impact: 'Delayed contract realization and prolonged customer time-to-value.'
      },
      {
        title: 'Risk of Inaccurate Medical Terminology and Clinical Copy',
        description: 'Unverified automated generation can hallucinate medical claims or clinical indications, exposing digital health platforms to severe legal liability.',
        business_impact: 'Loss of physician credibility and regulatory enforcement actions.'
      }
    ],
    faq_focus: [
      {
        q: 'Is this architecture compatible with HIPAA security standards?',
        a: 'Absolutely. All programmatic pages render as static edge assets without storing or processing PHI, and all backends adhere to isolated zero-trust network configurations.'
      },
      {
        q: 'How do you ensure clinical terminology and protocol accuracy?',
        a: 'We utilize constrained prompt templates with negative constraints and strict factual lookup tables calibrated for specific medical specializations.'
      }
    ]
  },
  'proptech-realestate': {
    industry_name: 'PropTech & Commercial Real Estate Platforms',
    typical_acv: '$20M - $200M AUM',
    economic_metrics: {
      cac_benchmark: '38 - 54 average days on market',
      payback_period: 'Sub-60s MLS synchronization',
      target_kpi: '+45% regional metro lead capture',
      revenue_upside: '3.2% qualified investor conversion'
    },
    context_prose: 'Commercial real estate portals and PropTech platforms require hyper-localized programmatic assets that ingest MLS feeds, municipal zoning data, and capital market metrics to convert institutional investors and commercial tenants.',
    pain_points: [
      {
        title: 'Disparate Regional MLS and Listing Feed Fragmentation',
        description: 'PropTech aggregators struggle to normalize unstructured property feeds across multiple regional boards with incompatible data schemas.',
        business_impact: 'Stale listing metadata and missing commercial real estate inventory.'
      },
      {
        title: 'High-Ticket Investor Inquiries Dropping Due to Slow Response',
        description: 'Commercial investors submitting inquiries on high-value asset listings expect immediate technical packages; delayed replies cause immediate deal abandonment.',
        business_impact: 'Lost broker commissions and prolonged asset holding costs.'
      },
      {
        title: 'Inability to Rank for Hyper-Local Commercial Search Terms',
        description: 'Real estate portals fail to capture neighborhood-specific commercial keywords because authoring individual sub-market pages manually is cost-prohibitive.',
        business_impact: 'Dominance of legacy aggregators in lucrative regional metro areas.'
      }
    ],
    faq_focus: [
      {
        q: 'Can this generate localized pages for specific metropolitan markets and asset classes?',
        a: 'Yes. Our taxonomy matrix combines target property classes with regional metro coordinates to produce hyper-targeted, localized programmatic landing pages.'
      },
      {
        q: 'How quickly do property data and commercial metrics refresh?',
        a: 'Our build pipeline supports automated daily batch compilation with dynamic lastmod updates, ensuring search engines index fresh property insights.'
      }
    ]
  },
  'legaltech-professional': {
    industry_name: 'LegalTech & High-Ticket Professional Services',
    typical_acv: '$20,000 - $100,000/yr',
    economic_metrics: {
      cac_benchmark: '84% billable hour realization rate',
      payback_period: '10 min automated conflict triage',
      target_kpi: '92% corporate client retention',
      revenue_upside: '+$140k annual partner capacity'
    },
    context_prose: 'Law firms and specialized professional services demand impeccable technical precision, strict confidentiality protocols, and targeted practice area authority to attract corporate counsel and enterprise procurement leads.',
    pain_points: [
      {
        title: 'Partner Hours Consumed by Unqualified Intake Screening',
        description: 'Senior attorneys spend billable hours fielding out-of-scope inquiries and manually checking conflicts instead of executing client matters.',
        business_impact: 'Direct loss of billable revenue and partner burnout.'
      },
      {
        title: 'Strict Privilege and Data Confidentiality Compliance Constraints',
        description: 'Standard third-party SaaS applications do not meet the stringent data sovereignty and attorney-client privilege mandates required for legal practice.',
        business_impact: 'Ethics compliance risks and refusal of corporate clients to engage.'
      },
      {
        title: 'Stagnant Organic Pipeline for Specialized Corporate Practice Areas',
        description: 'High-margin practice groups rely almost entirely on word-of-mouth, failing to capture corporate legal departments searching for niche regulatory expertise.',
        business_impact: 'Vulnerability to macroeconomic cycles and lumpy quarterly retainers.'
      }
    ],
    faq_focus: [
      {
        q: 'Does this platform store or process confidential legal intake data?',
        a: 'No. All marketing and programmatic pages are deployed as public, high-speed static edge pages. Any client intake funnels route directly into your private, encrypted CRM.'
      },
      {
        q: 'Can pages be tailored to individual state jurisdictions and practice areas?',
        a: 'Yes. The taxonomy matrix maps exact state and practice parameters, adhering strictly to legal advertising rules and disclaimer requirements.'
      }
    ]
  },
  'venture-capital-private-equity': {
    industry_name: 'Venture Capital & Private Equity Firms',
    typical_acv: '$50M - $1B AUM',
    economic_metrics: {
      cac_benchmark: '300+ pitches screened monthly',
      payback_period: '14 day LP due diligence speed',
      target_kpi: '3.5x proprietary founder inbound',
      revenue_upside: 'Sub-4 minute automated pitch triage'
    },
    context_prose: 'Investment funds and private equity firms require high-signal inbound pipelines and automated portfolio operational visibility to triage hundreds of monthly pitch opportunities and demonstrate market leadership to limited partners.',
    pain_points: [
      {
        title: 'Analyst Time Depleted by Unstructured Pitch Deck Triage',
        description: 'Investment teams spend 20+ hours each week parsing unvetted business plans, missing high-conviction breakout opportunities in the backlog.',
        business_impact: 'Missed investment allocations and delayed deal execution velocity.'
      },
      {
        title: 'Fragmented Operational Reporting Across Portfolio Holdings',
        description: 'Operating partners lack real-time visibility into financial burn rates, runway metrics, and hiring velocity across diverse portfolio companies.',
        business_impact: 'Slow crisis response and elevated risk of portfolio write-downs.'
      },
      {
        title: 'Weak Digital Footprint for Sourcing Proprietary Founder Inbound',
        description: 'Funds without clear programmatic market thesis pages struggle to attract technical founders searching for sector-specialized capital partners.',
        business_impact: 'Reliance on contested, highly priced competitive auctions.'
      }
    ],
    faq_focus: [
      {
        q: 'How does programmatic SEO assist a private equity or venture capital fund?',
        a: 'It establishes deep programmatic authority across sector-specific themes (e.g. B2B AI, FinTech, Defense), converting searching founders into proprietary inbound deal flow.'
      },
      {
        q: 'Can we publish investment theses and portfolio market maps programmatically?',
        a: 'Yes. Our engine transforms your market theses into indexable, structured research pages that establish category leadership.'
      }
    ]
  },
  'edtech': {
    industry_name: 'EdTech & Online Learning Platforms',
    typical_acv: '$10,000 - $50,000/yr',
    economic_metrics: {
      cac_benchmark: '45% module completion rate',
      payback_period: '7.8 months community retention',
      target_kpi: '+52% course discovery footprint',
      revenue_upside: '$1,850 student lifetime value'
    },
    context_prose: 'Educational technology platforms and skill certification providers must capture prospective learners at the exact moment of career transition or skill curiosity, requiring extensive course taxonomy indexing and zero-friction activation.',
    pain_points: [
      {
        title: 'Severe Post-Module Learner Churn and Low Completion Rates',
        description: 'Students drop out when self-paced curriculums lack immediate interactive remediation and responsive technical feedback.',
        business_impact: 'Eroded subscription renewal rates and high customer acquisition churn.'
      },
      {
        title: 'Tens of Thousands of Unranked Lesson & Syllabus Queries',
        description: 'Vast course libraries remain hidden from search engines because curriculum databases are not structured as indexable landing pages.',
        business_impact: 'Unrealized organic search traffic and heavy reliance on paid student acquisition.'
      },
      {
        title: 'Operational Overhead in Mentor and Tutor Scheduling',
        description: 'Coordinating live 1-on-1 tutoring and student evaluations manually creates massive administrative overhead as cohort enrollments grow.',
        business_impact: 'Compressed educational gross margins and student support bottlenecks.'
      }
    ],
    faq_focus: [
      {
        q: 'How does programmatic SEO index our entire curriculum catalog?',
        a: 'We map courses, modules, skill competencies, and career transitions into a hierarchical taxonomy that automatically generates schema-rich course discovery pages.'
      },
      {
        q: 'Is Course and EducationalOrganization schema injected automatically?',
        a: 'Yes. All generated pages include Google-compliant Schema.org Course, Organization, and FAQ microdata to maximize rich search snippet capture.'
      }
    ]
  },
  'cybersecurity': {
    industry_name: 'Enterprise Cybersecurity & DevSecOps',
    typical_acv: '$40,000 - $200,000/yr',
    economic_metrics: {
      cac_benchmark: 'Mean time to detect < 4 minutes',
      payback_period: '-65% security analyst alert fatigue',
      target_kpi: '100% automated SOC audit readiness',
      revenue_upside: 'Sub-30 day enterprise procurement pass'
    },
    context_prose: 'Cybersecurity providers and DevSecOps teams must communicate complex zero-trust architectures, threat telemetry, and compliance certifications to enterprise CISOs without technical fluff or ambiguous claims.',
    pain_points: [
      {
        title: 'Exhausting Enterprise Procurement and Security Questionnaires',
        description: 'Security engineering teams waste hundreds of hours manually filling repetitive 250-question CAIQ and SIG enterprise vendor assessments.',
        business_impact: 'Protracted 9-12 month sales cycles and stalled deal progression.'
      },
      {
        title: 'Critical Vulnerabilities Obscured by Alert Fatigue',
        description: 'Security operations centers receive thousands of false positive telemetry alerts daily, drowning out genuine indicators of compromise.',
        business_impact: 'Elevated risk of undetected lateral movement and breach exposure.'
      },
      {
        title: 'Difficulty Translating Complex Threat Mitigation to Board Metrics',
        description: 'Security leadership struggles to articulate technical risk mitigation in commercial terms that resonate with CFOs and audit committees.',
        business_impact: 'Security budget reductions and postponed infrastructure upgrades.'
      }
    ],
    faq_focus: [
      {
        q: 'How does your engine convey complex zero-trust architecture without compromising proprietary methods?',
        a: 'We articulate technical capabilities through architectural specifications, security frameworks, and compliance standards while preserving proprietary code confidentiality.'
      },
      {
        q: 'Are these landing pages hosted on secure, DDoS-hardened edge networks?',
        a: 'Yes. All programmatic solutions deploy on Cloudflare global edge networks with automatic WAF filtering, DDoS mitigation, and TLS 1.3 encryption.'
      }
    ]
  },
  'agency-consultancy': {
    industry_name: 'Digital Agencies & High-Growth Consultancies',
    typical_acv: '$5,000 - $30,000/mo',
    economic_metrics: {
      cac_benchmark: '18% scope creep margin recovery',
      payback_period: 'Sub-48 hour client proposal turnaround',
      target_kpi: '+68% billable consultant utilization',
      revenue_upside: '14.5 month average client retainer'
    },
    context_prose: 'High-growth digital agencies and professional consultancies face client acquisition volatility, fulfillment capacity ceilings, and the challenge of scaling client organic search footprints without exponentially increasing headcount.',
    pain_points: [
      {
        title: 'Feast-or-Famine Inbound Retainer Acquisition Cycles',
        description: 'Agency founders oscillate between high-intensity client fulfillment and empty sales pipelines due to lack of a continuous, automated acquisition system.',
        business_impact: 'Revenue instability and inability to make strategic long-term hires.'
      },
      {
        title: 'Fulfillment Capacity Bottlenecks and Scope Creep Erosion',
        description: 'Manual delivery processes restrict how many accounts consultants can manage simultaneously, leading to margin erosion and delayed client deliverables.',
        business_impact: 'Depressed operating profit margins and client retention churn.'
      },
      {
        title: 'Inability to Deliver High-Volume pSEO Infrastructure to Clients',
        description: 'Traditional agency SEO teams cannot offer database-driven programmatic engines at scale without dedicated full-stack software engineers.',
        business_impact: 'Loss of lucrative enterprise retainers to specialized tech-enabled agencies.'
      }
    ],
    faq_focus: [
      {
        q: 'Can agencies white-label this programmatic SEO architecture for their own clients?',
        a: 'Yes. Our Next.js architecture and automated batch pipeline can be deployed directly into client repositories with custom brand tokens and tracking.'
      },
      {
        q: 'How quickly can our agency launch its first live cohort of programmatic landing pages?',
        a: 'The initial taxonomy matrix, component templates, and batch deployment are operational within 7 business days.'
      }
    ]
  }
};

// Service Capability Profiles
const SERVICE_PROFILES: Record<string, {
  short_name: string;
  badge: string;
  architecture_prose: string;
  core_capabilities: CoreCapability[];
  workflow_phases: WorkflowPhase[];
}> = {
  'pseo-engine': {
    short_name: 'Programmatic SEO Engine',
    badge: 'Automated Inbound Engineering',
    architecture_prose: 'We engineer database-backed Next.js page generation pipelines deployed on edge CDNs with dynamic JSON-LD structured data, validated content matrices, and automated XML sitemap ping routines.',
    core_capabilities: [
      {
        title: 'Multi-Variable Combinatorial Taxonomy Matrix',
        specification: 'Multi-variable data contracts mapping services, customer niches, tech stacks, and metropolitan locations into structured JSON schemas.',
        deliverable_output: 'Curated combinatorial keyword matrix targeting commercial search intent with zero query duplication.'
      },
      {
        title: 'Next.js App Router & Edge Server Components',
        specification: 'Incremental Static Regeneration and React Server Components delivering sub-45ms TTFB and 99+ Core Web Vitals.',
        deliverable_output: 'Production Next.js repository with automated static export and zero layout shift.'
      },
      {
        title: 'Automated Schema.org JSON-LD Microdata',
        specification: 'Deeply nested ProfessionalService, Organization, FAQPage, and BreadcrumbList structured data injected at build time.',
        deliverable_output: 'Schema markup passing Google Rich Results tests with zero warnings or errors.'
      },
      {
        title: 'Chunked XML Sitemaps & Search Engine Ping Routines',
        specification: 'Automated sitemap index and 5,000-URL chunked files with dynamic lastmod timestamps and direct GSC/IndexNow webhooks.',
        deliverable_output: 'Continuous indexation pipeline submitting new pages immediately upon generation.'
      }
    ],
    workflow_phases: [
      {
        phase_number: 1,
        title: 'Taxonomy & High-Intent Keyword Extraction',
        description: 'Map proprietary capability vectors, customer pain points, and commercial CPC tiers into structured database records.',
        timeframe: 'Days 1 - 3'
      },
      {
        phase_number: 2,
        title: 'Next.js Template & Schema Architecture',
        description: 'Construct responsive Next.js App Router dynamic routes with Tailwind CSS and validated JSON-LD microdata.',
        timeframe: 'Days 4 - 7'
      },
      {
        phase_number: 3,
        title: 'Content Verification & Anti-Spam Assertion Gates',
        description: 'Execute automated uniqueness checks, buzzword blacklist scans, and schema validation tests.',
        timeframe: 'Days 8 - 10'
      },
      {
        phase_number: 4,
        title: 'Edge Deployment & Automated Indexation',
        description: 'Deploy static assets to Cloudflare Pages and trigger GSC and IndexNow sitemap ping routines.',
        timeframe: 'Days 11 - 14'
      }
    ]
  },
  'ai-agents': {
    short_name: 'Autonomous AI Agents',
    badge: 'Agentic Workflow Engineering',
    architecture_prose: 'We architect production-grade autonomous agent clusters with deterministic tool execution, sandboxed Docker runtime environments, and human-in-the-loop governance.',
    core_capabilities: [
      {
        title: 'Deterministic LLM Tool Calling & Function Execution',
        specification: 'Type-safe JSON schema function calling connecting language models directly to enterprise databases, APIs, and file systems.',
        deliverable_output: 'Reliable execution pipelines with zero hallucinated parameters or unbounded loops.'
      },
      {
        title: 'Multi-Agent Orchestration & State Synchronization',
        specification: 'Event-driven message buses and distributed task workers coordinating multi-agent handoffs with persistent SQLite/Postgres logs.',
        deliverable_output: 'Autonomous background systems operating 24/7 without manual intervention.'
      },
      {
        title: 'Sandboxed Docker Runtime Execution',
        specification: 'Isolated container bridges running on Linux VPS with strict egress policies and volume boundaries.',
        deliverable_output: 'Secure execution environment isolating sensitive enterprise workflows.'
      },
      {
        title: 'Human-in-the-Loop Review & Approval Gates',
        specification: 'Interactive Telegram/Slack/Email approval triggers requiring explicit manager authorization prior to high-impact actions.',
        deliverable_output: 'Zero unverified transactions or unauthorized external data dispatches.'
      }
    ],
    workflow_phases: [
      {
        phase_number: 1,
        title: 'Agent Topology & Capability Mapping',
        description: 'Define agent roles, input/output schemas, permission boundaries, and external tool dependencies.',
        timeframe: 'Days 1 - 3'
      },
      {
        phase_number: 2,
        title: 'Tool Connector & Sandbox Engineering',
        description: 'Build authenticated REST/GraphQL tool connectors and isolate execution within Docker containers.',
        timeframe: 'Days 4 - 8'
      },
      {
        phase_number: 3,
        title: 'Multi-Agent Orchestration & State Persistence',
        description: 'Implement distributed queue workers and task state machines with automated retry logic.',
        timeframe: 'Days 9 - 12'
      },
      {
        phase_number: 4,
        title: 'Production Hardening & Verification',
        description: 'Execute stress testing, latency profiling, and security boundary audits before production cutover.',
        timeframe: 'Days 13 - 16'
      }
    ]
  },
  'web-app-engineering': {
    short_name: 'Next.js Web Engineering',
    badge: 'Full-Stack Edge Engineering',
    architecture_prose: 'We build ultra-fast, accessible web applications engineered with Next.js App Router, React Server Components, Tailwind CSS, and edge serverless runtimes.',
    core_capabilities: [
      {
        title: 'React Server Components & Streaming SSR',
        specification: 'Zero-client-bundle architecture streaming pre-rendered HTML directly from Cloudflare and Vercel edge networks.',
        deliverable_output: 'Sub-50ms Time to First Byte and perfect Core Web Vitals.'
      },
      {
        title: 'Type-Safe Full-Stack Architecture with TypeScript',
        specification: 'End-to-end type safety spanning database queries, API routes, and client-side component interfaces.',
        deliverable_output: 'Zero runtime type errors and rapid developer iteration velocity.'
      },
      {
        title: 'Accessible Tailwind Design Systems',
        specification: 'Radix UI and Tailwind CSS primitives delivering dark-mode native, accessible UI components.',
        deliverable_output: 'Responsive, WCAG AA compliant user interfaces with zero layout shift.'
      },
      {
        title: 'Edge Database & Caching Optimization',
        specification: 'Supabase PostgreSQL integration with pgvector, row-level security, and Redis edge caching layers.',
        deliverable_output: 'Low-latency data querying supporting high-concurrency user traffic.'
      }
    ],
    workflow_phases: [
      {
        phase_number: 1,
        title: 'Information Architecture & Data Modeling',
        description: 'Define database schemas, API route contracts, and component hierarchy specifications.',
        timeframe: 'Days 1 - 4'
      },
      {
        phase_number: 2,
        title: 'Frontend Component & Design System Build',
        description: 'Implement responsive React Server Components with Tailwind CSS and Radix accessibility primitives.',
        timeframe: 'Days 5 - 9'
      },
      {
        phase_number: 3,
        title: 'Backend API & Database Integration',
        description: 'Connect PostgreSQL databases, authentication providers, and edge caching middleware.',
        timeframe: 'Days 10 - 14'
      },
      {
        phase_number: 4,
        title: 'Performance Profiling & Edge Deployment',
        description: 'Execute Lighthouse audits, Core Web Vitals optimization, and edge CDN routing setup.',
        timeframe: 'Days 15 - 18'
      }
    ]
  },
  'outbound-infrastructure': {
    short_name: 'Cold Outbound & Lead Engine',
    badge: 'Autonomous Pipeline Systems',
    architecture_prose: 'We construct multi-channel intent scraping, social signal listening, and personalized cold outreach infrastructure delivering qualified conversations into your CRM.',
    core_capabilities: [
      {
        title: 'Multi-Channel Social Intent Radar',
        specification: 'Autonomous monitoring across X, Reddit, and LinkedIn detecting live buyer inquiries and high-intent pain point discussions.',
        deliverable_output: 'Continuous stream of qualified prospects expressing immediate purchasing intent.'
      },
      {
        title: 'Hardened Email Deliverability & DNS Architecture',
        specification: 'Multi-domain secondary mailbox configurations with automated SPF, DKIM, DMARC, and custom tracking domains.',
        deliverable_output: '99%+ inbox placement rate protecting your primary domain reputation.'
      },
      {
        title: 'Context-Aware AI Message Personalization',
        specification: 'Constrained LLM sequence generation citing specific prospect news, job postings, and technical stack configurations.',
        deliverable_output: 'Cold emails that read like meticulously researched personal notes, driving 8-15% reply rates.'
      },
      {
        title: 'Automated CRM Webhook & Lead Routing',
        specification: 'Real-time webhook synchronization sending positive replies directly to GoHighLevel, HubSpot, or Salesforce.',
        deliverable_output: 'Instant SMS and Slack notifications connecting sales reps to hot leads within 60 seconds.'
      }
    ],
    workflow_phases: [
      {
        phase_number: 1,
        title: 'Domain Provisioning & Deliverability Setup',
        description: 'Configure dedicated sending domains, DNS authentication records, and automated mailbox warmups.',
        timeframe: 'Days 1 - 4'
      },
      {
        phase_number: 2,
        title: 'ICP Modeling & Intent Scraper Calibration',
        description: 'Build targeted scrapers and social keyword filters targeting high-intent decision-maker personas.',
        timeframe: 'Days 5 - 8'
      },
      {
        phase_number: 3,
        title: 'Copy Engineering & Dynamic Sequences',
        description: 'Draft conversion-tested cold outreach sequences and calibrate context-aware personalization prompts.',
        timeframe: 'Days 9 - 12'
      },
      {
        phase_number: 4,
        title: 'Live Sending & CRM Pipeline Sync',
        description: 'Initiate graduated sending batches, monitor inbox placement, and connect real-time CRM routing.',
        timeframe: 'Days 13 - 16'
      }
    ]
  },
  'composio-integrations': {
    short_name: 'Composio Agent Integrations',
    badge: 'Self-Hosted Tool Execution',
    architecture_prose: 'We deploy hardened self-hosted Composio execution environments connecting LLM agents directly to 250+ enterprise services, SaaS platforms, and internal databases.',
    core_capabilities: [
      {
        title: 'Self-Hosted Composio Tool Server',
        specification: 'Containerized Composio service running on dedicated Linux VPS with encrypted local credential storage.',
        deliverable_output: 'Complete data sovereignty with zero third-party tool log interception.'
      },
      {
        title: 'OAuth2 Token Vault & Governance',
        specification: 'Automated token refresh mechanisms and granular permission scoping across integrated enterprise apps.',
        deliverable_output: 'Secure API execution with zero risk of credential expiration or leakage.'
      },
      {
        title: 'Bi-Directional Event Webhook Triggers',
        specification: 'Real-time event subscriptions turning external SaaS updates into actionable agent execution triggers.',
        deliverable_output: 'Event-driven automations executing in under 200ms upon external platform events.'
      },
      {
        title: 'Audit Logging & Anomaly Detection',
        specification: 'Structured JSON execution logs recording tool inputs, outputs, timestamps, and model tokens for compliance audits.',
        deliverable_output: 'Comprehensive audit trail satisfying enterprise security reviews.'
      }
    ],
    workflow_phases: [
      {
        phase_number: 1,
        title: 'VPS Infrastructure & Docker Isolation',
        description: 'Provision Linux host, configure firewall rules, and launch isolated Composio container bridges.',
        timeframe: 'Days 1 - 3'
      },
      {
        phase_number: 2,
        title: 'OAuth App Registration & Tool Connectors',
        description: 'Configure enterprise OAuth apps and verify authenticated API tool execution.',
        timeframe: 'Days 4 - 7'
      },
      {
        phase_number: 3,
        title: 'Agent Integration & Schema Mapping',
        description: 'Connect language model runtimes to Composio tool schemas with deterministic validation gates.',
        timeframe: 'Days 8 - 11'
      },
      {
        phase_number: 4,
        title: 'Security Audit & Enterprise Handoff',
        description: 'Perform penetration testing, token vault audits, and operational runbook handoff.',
        timeframe: 'Days 12 - 15'
      }
    ]
  },
  'whop-monetization': {
    short_name: 'Whop Monetization Infrastructure',
    badge: 'Digital Commerce Architecture',
    architecture_prose: 'We engineer automated Whop store memberships, access gating, and digital software storefronts connected to Discord communities, webhooks, and billing gateways.',
    core_capabilities: [
      {
        title: 'Whop SDK & API Storefront Integration',
        specification: 'Custom React storefront components interacting with Whop API for license validation, tier gating, and checkout.',
        deliverable_output: 'High-converting purchase funnels with sub-second checkout redirection.'
      },
      {
        title: 'Automated Community & Software License Gating',
        specification: 'Instant role assignment in Discord and immediate generation of API access tokens upon confirmed purchase.',
        deliverable_output: 'Zero manual onboarding friction for paying digital customers.'
      },
      {
        title: 'Dynamic Checkout Routing & Upsell Logic',
        specification: 'Context-aware checkout injection matching user search intent to free lead magnets or paid software subscriptions.',
        deliverable_output: 'Maximized Average Order Value and recurring subscription retention.'
      },
      {
        title: 'Financial Reconciliation & Webhook Pipelines',
        specification: 'Automated webhook listeners tracking renewals, cancellations, and disputes with instant accounting ledger sync.',
        deliverable_output: 'Real-time MRR analytics and automated customer lifecycle notifications.'
      }
    ],
    workflow_phases: [
      {
        phase_number: 1,
        title: 'Product Catalog & Pricing Tier Setup',
        description: 'Structure digital products, license tiers, recurring billing plans, and Whop store configurations.',
        timeframe: 'Days 1 - 3'
      },
      {
        phase_number: 2,
        title: 'Webhook & License Key Engineering',
        description: 'Deploy webhook listeners and build automated digital entitlement fulfillment pipelines.',
        timeframe: 'Days 4 - 7'
      },
      {
        phase_number: 3,
        title: 'Frontend Storefront & Checkout Flow',
        description: 'Embed high-converting checkout buttons and build dynamic CTA routing components.',
        timeframe: 'Days 8 - 11'
      },
      {
        phase_number: 4,
        title: 'Live Transaction Testing & Analytics',
        description: 'Execute end-to-end sandbox purchase tests, verify webhook fulfillment, and activate live store.',
        timeframe: 'Days 12 - 14'
      }
    ]
  },
  'cloud-vps-hardening': {
    short_name: 'Cloudflare & VPS Hardening',
    badge: 'Zero-Trust Infrastructure',
    architecture_prose: 'We configure Cloudflare Edge routing, DDoS mitigation, and hardened Docker Compose environments on dedicated Linux VPS instances with automated SSL and firewall controls.',
    core_capabilities: [
      {
        title: 'Cloudflare Edge WAF & Zero-Trust Tunneling',
        specification: 'Cloudflared zero-trust tunnels eliminating exposed public IP addresses and open inbound firewall ports.',
        deliverable_output: 'Complete infrastructure invisibility against automated vulnerability port scanners.'
      },
      {
        title: 'Hardened Docker Compose Bridge Networks',
        specification: 'Isolated container networks with read-only filesystems, strict memory limits, and non-root execution users.',
        deliverable_output: 'Defense-in-depth container security preventing lateral host escalation.'
      },
      {
        title: 'Automated SSL & Security Header Enforcement',
        specification: 'Automated TLS 1.3 certificate renewals paired with strict HSTS, CSP, and CORS HTTP headers.',
        deliverable_output: 'A+ SSL Labs security rating across all public domains and subdomains.'
      },
      {
        title: 'Automated System Monitoring & Failover',
        specification: 'Real-time CPU, RAM, and disk telemetry with automated container healthcheck restarts and alert notifications.',
        deliverable_output: '99.99% infrastructure uptime with zero unmonitored hardware outages.'
      }
    ],
    workflow_phases: [
      {
        phase_number: 1,
        title: 'Base OS Hardening & SSH Lockdown',
        description: 'Deploy Ubuntu LTS, disable password authentication, configure UFW firewall, and install fail2ban.',
        timeframe: 'Days 1 - 2'
      },
      {
        phase_number: 2,
        title: 'Docker Architecture & Network Isolation',
        description: 'Configure Docker daemon security parameters, non-root users, and isolated bridge networks.',
        timeframe: 'Days 3 - 5'
      },
      {
        phase_number: 3,
        title: 'Cloudflare Tunnel & Edge WAF Integration',
        description: 'Deploy cloudflared daemon, bind DNS records, and configure Edge WAF security policies.',
        timeframe: 'Days 6 - 8'
      },
      {
        phase_number: 4,
        title: 'Telemetry & Disaster Recovery Testing',
        description: 'Install monitoring agents, configure automated database backups, and run failover drills.',
        timeframe: 'Days 9 - 11'
      }
    ]
  }
};

/**
 * Generate fully populated, unique, schema-compliant page data for any [niche]/[service] combination
 */
export function generatePageData(
  serviceInfo: ServiceInfo,
  nicheInfo: NicheInfo,
  techStackInfo?: TechStackInfo,
  locationInfo?: LocationInfo
): GeneratedPageData {
  const nicheProfile = NICHE_PROFILES[nicheInfo.id] || NICHE_PROFILES['b2b-saas'];
  const serviceProfile = SERVICE_PROFILES[serviceInfo.id] || SERVICE_PROFILES['pseo-engine'];

  const techStack = techStackInfo || {
    id: 'nextjs-typescript',
    name: 'Next.js & TypeScript',
    slug_part: 'nextjs-typescript',
    category: 'Frontend & Full-Stack',
    key_benefits: 'React Server Components, edge SSR, and automated schema injection.'
  };

  const location = locationInfo || {
    id: 'global',
    name: 'Global / Remote',
    city: 'Worldwide',
    country: 'Global',
    is_global: true
  };

  const slug = `/solutions/${nicheInfo.id}/${serviceInfo.id}`;
  const canonicalUrl = `https://adorisedigital.com${slug}`;

  // Deterministic, high-intent title and description
  const metaTitle = `${serviceProfile.short_name} for ${nicheProfile.industry_name} | Adorise Digital`;
  const metaDescription = `Scale ${nicheProfile.industry_name} with enterprise ${serviceProfile.short_name.toLowerCase()}. Built with ${techStack.name} for sub-45ms edge performance, schema compliance, and ${nicheProfile.economic_metrics.target_kpi}.`;

  // Dynamic Whop CTA based on Mika's directive
  const whopCta = getProductCTA(serviceInfo.id);

  // Dynamic trust metrics tailored to niche & service
  const trustMetrics: TrustMetric[] = [
    {
      value: '< 45ms',
      label: 'Edge TTFB',
      subtext: 'Global CDN sub-second page loads'
    },
    {
      value: nicheProfile.economic_metrics.target_kpi,
      label: 'Target Outcome',
      subtext: nicheProfile.economic_metrics.revenue_upside
    },
    {
      value: '100%',
      label: 'Schema Validated',
      subtext: 'Google Rich Results compliant JSON-LD'
    },
    {
      value: nicheProfile.typical_acv,
      label: 'Target Market ACV',
      subtext: nicheProfile.economic_metrics.cac_benchmark
    }
  ];

  // Dynamic FAQs tailored specifically to this combination
  const dynamicFaqs: FAQItem[] = [
    ...nicheProfile.faq_focus.map(f => ({
      question: f.q,
      answer: f.a,
      category: 'technical'
    })),
    {
      question: `What makes Adorise Digital's ${serviceProfile.short_name} unique for ${nicheInfo.name}?`,
      answer: `We do not sell generic templates or unverified AI output. We engineer customized ${techStack.name} software pipelines specifically addressing ${nicheProfile.pain_points[0].title.toLowerCase()} and delivering ${nicheProfile.economic_metrics.target_kpi} with mathematical verification.`,
      category: 'architecture'
    },
    {
      question: `How quickly can this system deploy into our production environment?`,
      answer: `Our phased implementation delivers an initial operational deployment within 14 business days, complete with automated testing and continuous monitoring.`,
      category: 'timeline'
    },
    {
      question: `Who owns the underlying code, data schemas, and integrations?`,
      answer: `Your organization retains 100% full intellectual property ownership of all custom schemas, Next.js components, and API integration code upon deployment.`,
      category: 'commercial'
    }
  ];

  // Structured Data (Schema.org JSON-LD microdata)
  const structuredData = {
    service: {
      '@context': 'https://schema.org',
      '@type': 'ProfessionalService',
      'name': `Adorise Digital — ${serviceProfile.short_name} for ${nicheProfile.industry_name}`,
      'description': metaDescription,
      'url': canonicalUrl,
      'parentOrganization': {
        '@type': 'Organization',
        'name': 'Adorise Digital',
        'url': 'https://adorisedigital.com'
      },
      'areaServed': location.is_global ? 'Global' : location.name,
      'priceRange': '$$$$',
      'hasOfferCatalog': {
        '@type': 'OfferCatalog',
        'name': `${serviceProfile.short_name} Deliverables`,
        'itemListElement': serviceProfile.core_capabilities.map(c => ({
          '@type': 'Offer',
          'name': c.title,
          'description': c.specification
        }))
      }
    },
    organization: {
      '@context': 'https://schema.org',
      '@type': 'Organization',
      'name': 'Adorise Digital',
      'url': 'https://adorisedigital.com',
      'logo': 'https://adorisedigital.com/logo.png',
      'sameAs': [
        'https://github.com/AdoriseDigital',
        'https://whop.com/adorise-digital-usa/'
      ]
    },
    faq_page: {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      'mainEntity': dynamicFaqs.map(f => ({
        '@type': 'Question',
        'name': f.question,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': f.answer
        }
      }))
    },
    breadcrumb_list: {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      'itemListElement': [
        {
          '@type': 'ListItem',
          'position': 1,
          'name': 'Home',
          'item': 'https://adorisedigital.com/'
        },
        {
          '@type': 'ListItem',
          'position': 2,
          'name': 'Solutions',
          'item': 'https://adorisedigital.com/solutions/'
        },
        {
          '@type': 'ListItem',
          'position': 3,
          'name': nicheInfo.name,
          'item': `https://adorisedigital.com/solutions/${nicheInfo.id}/`
        },
        {
          '@type': 'ListItem',
          'position': 4,
          'name': serviceProfile.short_name,
          'item': canonicalUrl
        }
      ]
    }
  };

  return {
    slug,
    canonical_url: canonicalUrl,
    meta_title: metaTitle,
    meta_description: metaDescription,
    primary_keyword: `${serviceProfile.short_name.toLowerCase()} for ${nicheInfo.name.toLowerCase()}`,
    secondary_keywords: [
      `${nicheInfo.id} ${serviceInfo.id}`,
      `enterprise ${serviceProfile.short_name.toLowerCase()}`,
      `${techStack.slug_part} ${nicheInfo.id}`,
      `automated ${serviceInfo.id}`
    ],
    service: serviceInfo,
    niche: nicheInfo,
    tech_stack: techStack,
    location,
    hero: {
      badge: `${serviceProfile.badge} | ${nicheInfo.name}`,
      h1: `${serviceProfile.short_name} for ${nicheProfile.industry_name}`,
      subheadline: `Scale your ${nicheInfo.name} operations with enterprise ${serviceProfile.short_name.toLowerCase()}. Engineered on ${techStack.name} to resolve ${nicheProfile.pain_points[0].title.toLowerCase()} and achieve ${nicheProfile.economic_metrics.target_kpi}.`,
      trust_metrics: trustMetrics
    },
    pain_points_section: {
      eyebrow: `Industry Friction in ${nicheInfo.name}`,
      heading: `Why Standard Approaches Fail in ${nicheProfile.industry_name}`,
      context_prose: nicheProfile.context_prose,
      pain_points: nicheProfile.pain_points
    },
    solution_section: {
      eyebrow: `Engineered System Architecture`,
      heading: `High-Performance ${serviceProfile.short_name} Architecture`,
      architecture_prose: serviceProfile.architecture_prose,
      core_capabilities: serviceProfile.core_capabilities,
      workflow_phases: serviceProfile.workflow_phases
    },
    whop_cta: whopCta,
    faqs: dynamicFaqs,
    structured_data: structuredData
  };
}
