export interface NicheInfo {
  id: string;
  name: string;
  slug_part: string;
  typical_acv?: string;
  critical_pain_points?: string[];
  economic_metrics?: {
    cac_benchmark: string;
    payback_period: string;
    target_kpi: string;
    revenue_upside: string;
  };
}

export interface ServiceInfo {
  id: string;
  name: string;
  short_name: string;
  slug_part: string;
  description: string;
  category?: string;
  target_buyers: string[];
  core_deliverables: string[];
}

export interface TechStackInfo {
  id: string;
  name: string;
  slug_part: string;
  category: string;
  key_benefits: string;
}

export interface LocationInfo {
  id: string;
  name: string;
  city: string;
  state?: string;
  country: string;
  is_global?: boolean;
  commercial_score?: number;
}

export interface CombinationRecord {
  id: string;
  slug: string;
  primary_keyword: string;
  secondary_keywords: string[];
  search_intent: string;
  cpc_tier: string;
  priority: string;
  service: {
    id: string;
    name: string;
    short_name: string;
  };
  niche: {
    id: string;
    name: string;
    typical_acv?: string;
  };
  tech_stack: {
    id: string;
    name: string;
    category?: string;
  };
  location: {
    id: string;
    name: string;
    city: string;
    country: string;
  };
  value_proposition_hook: string;
  target_buyer_roles: string[];
}

export interface PainPoint {
  title: string;
  description: string;
  business_impact: string;
}

export interface CoreCapability {
  title: string;
  specification: string;
  deliverable_output: string;
}

export interface WorkflowPhase {
  phase_number: number;
  title: string;
  description: string;
  timeframe: string;
}

export interface TrustMetric {
  value: string;
  label: string;
  subtext: string;
}

export interface FAQItem {
  question: string;
  answer: string;
  category: string;
}

export interface WhopProductCTA {
  title: string;
  price: string;
  url: string;
  type: 'free' | 'paid';
  ctaText: string;
  badge: string;
  intentCluster: string;
}

export interface GeneratedPageData {
  slug: string;
  canonical_url: string;
  meta_title: string;
  meta_description: string;
  primary_keyword: string;
  secondary_keywords: string[];
  service: ServiceInfo;
  niche: NicheInfo;
  tech_stack: TechStackInfo;
  location: LocationInfo;
  hero: {
    badge: string;
    h1: string;
    subheadline: string;
    trust_metrics: TrustMetric[];
  };
  pain_points_section: {
    eyebrow: string;
    heading: string;
    context_prose: string;
    pain_points: PainPoint[];
  };
  solution_section: {
    eyebrow: string;
    heading: string;
    architecture_prose: string;
    core_capabilities: CoreCapability[];
    workflow_phases: WorkflowPhase[];
  };
  whop_cta: WhopProductCTA;
  faqs: FAQItem[];
  structured_data: {
    service: any;
    organization: any;
    faq_page: any;
    breadcrumb_list: any;
  };
}
