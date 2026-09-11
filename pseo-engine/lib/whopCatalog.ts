import { WhopProductCTA } from '../types/pseo';

export const WHOP_PRODUCTS: Record<string, WhopProductCTA> = {
  inboxcalm: {
    title: 'InboxCalm',
    price: 'Free',
    url: 'https://inboxcalm.adorisedigital.com',
    type: 'free',
    ctaText: 'Try Free De-escalation',
    badge: 'Executive Anti-Toxicity Firewall',
    intentCluster: 'Email conflict, hostile emails, client de-escalation, executive communication'
  },
  clipcalm: {
    title: 'ClipCalm AI',
    price: 'Free',
    url: 'https://clipcalm.adorisedigital.com',
    type: 'free',
    ctaText: 'Clip First 3 Videos Free',
    badge: 'Autonomous Viral Video Repurposing',
    intentCluster: 'YouTube to Shorts, podcast clipping, viral video clips, video repurposing'
  },
  customer_service: {
    title: 'AI Customer Service',
    price: '$147 / mo',
    url: 'https://whop.com/adorise-digital-usa/',
    type: 'paid',
    ctaText: 'Deploy AI Customer Support ($147/mo)',
    badge: '24/7 Autonomous Voice & Ticket Agents',
    intentCluster: 'AI voice agents, 24/7 customer support automation, real-time client chat'
  },
  content_automation: {
    title: 'AI Content Automation',
    price: '$197 / mo',
    url: 'https://whop.com/adorise-digital-usa/',
    type: 'paid',
    ctaText: 'Automate Content Engine ($197/mo)',
    badge: 'Multi-Channel Calendar & pSEO Engine',
    intentCluster: 'Social media scheduling, Postiz workflows, automated content calendars'
  },
  lead_generation: {
    title: 'AI Lead Generation',
    price: '$297 / mo',
    url: 'https://whop.com/adorise-digital-usa/',
    type: 'paid',
    ctaText: 'Launch Lead Generation ($297/mo)',
    badge: 'Multi-Channel Social Intent Radar & Cold Outreach',
    intentCluster: 'B2B prospecting, cold outreach automation, social intent monitoring'
  },
  automation_suite: {
    title: 'AI Automation Suite',
    price: '$497 / mo',
    url: 'https://whop.com/adorise-digital-usa/',
    type: 'paid',
    ctaText: 'Get Complete Automation Suite ($497/mo)',
    badge: 'Enterprise n8n & Composio Orchestration',
    intentCluster: 'Agency workflow orchestration, n8n agency systems, full-stack automation'
  }
};

/**
 * Dynamically selects high-converting Whop checkout or free tool URL based on service category / ID
 */
export function getProductCTA(categoryOrServiceId: string): WhopProductCTA {
  const key = (categoryOrServiceId || '').toLowerCase();

  switch (key) {
    case 'customer-service':
    case 'voice-agent':
    case 'ai-agents':
      return WHOP_PRODUCTS.customer_service;

    case 'content-automation':
    case 'social-media':
    case 'pseo-engine':
      return WHOP_PRODUCTS.content_automation;

    case 'lead-generation':
    case 'cold-outreach':
    case 'outbound-infrastructure':
      return WHOP_PRODUCTS.lead_generation;

    case 'agency-suite':
    case 'full-automation':
    case 'web-app-engineering':
    case 'composio-integrations':
    case 'cloud-vps-hardening':
      return WHOP_PRODUCTS.automation_suite;

    case 'video-clipping':
      return WHOP_PRODUCTS.clipcalm;

    default:
      return WHOP_PRODUCTS.inboxcalm;
  }
}
