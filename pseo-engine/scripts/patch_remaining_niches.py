"""
Patch remaining 5 bespoke niche data files directly in Python.
Updates:
- data_legaltech.py: cloud-vps-hardening faqs
- data_vc_pe.py: whop-monetization, cloud-vps-hardening
- data_edtech.py: outbound-infrastructure, composio-integrations, whop-monetization
- data_cybersecurity.py: outbound-infrastructure, whop-monetization
- data_agency.py: outbound-infrastructure, composio-integrations, whop-monetization, cloud-vps-hardening
"""
import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# 1. Update data_legaltech
import data_legaltech
legaltech_vps = data_legaltech.DATA['legaltech-professional/cloud-vps-hardening']
legaltech_vps['faqs'] = [
    { 'q': 'Does this server hardening satisfy legal industry standards for protecting attorney-client privilege?', 'a': 'Yes. Eliminating public open ports, enforcing strong encryption, and maintaining immutable audit logs align with ABA cybersecurity guidelines.' },
    { 'q': 'How do attorneys and paralegals access internal case databases securely?', 'a': 'Staff connect via Cloudflare Access protected by corporate MFA, eliminating open SSH ports and preventing unauthorized network entry.' },
    { 'q': 'How are confidential deposition transcripts and matter evidence protected from ransomware?', 'a': 'All matter files are stored on encrypted volumes with write-once off-site backups that cannot be overwritten or held hostage.' },
    { 'q': 'Can this infrastructure support high-volume document ingestion during active litigation discovery?', 'a': 'Yes. Isolated container workers process discovery batches efficiently without exposing the underlying operating system.' },
    { 'q': 'What disaster recovery measures exist if a cloud host suffers catastrophic failure?', 'a': 'Automated scripts restore encrypted matter archives to fresh infrastructure within 10 minutes, ensuring zero case data loss.' }
]

# 2. Update data_vc_pe
import data_vc_pe
vc_whop = data_vc_pe.DATA['venture-capital-private-equity/whop-monetization']
vc_whop['capabilities'] = [
    {
        'title': 'Private Capital Syndicate Tier Architecture',
        'spec': 'Multi-level membership tiers for angel syndicates, deal allocation access, and LP research briefings.',
        'deliverable': 'Configured Whop membership store customized with private capital branding.'
    },
    {
        'title': 'HMAC-Signed Webhook Entitlement Engine',
        'spec': 'Real-time license dispatching unlocking private venture deal rooms and co-investment allocation memos.',
        'deliverable': 'Idempotent webhook listener repository with automated error recovery.'
    },
    {
        'title': 'Telegram & Discord Angel Syndicate Gating Bot',
        'spec': 'Automated credential assignment managing exclusive investor channels and founder pitch lounges.',
        'deliverable': 'Automated community bot protecting proprietary syndicate deal channels.'
    },
    {
        'title': 'Smart Venture Dunning & LP Dues Recovery',
        'spec': 'Automated dunning workflows recovering failed corporate cards and annual angel network dues.',
        'deliverable': 'Configured retention pipeline recovering over 75% of declined investor cards.'
    }
]
vc_whop['phases'] = [
    { 'title': 'Venture Syndicate Tier Scoping & LP Access Rules', 'desc': 'Structure angel network dues, co-investment carry rights, and deal room access gates.', 'tf': 'Days 1 - 3' },
    { 'title': 'Whop Portal Deployment & Secure Webhook Engineering', 'desc': 'Set up private capital checkout pages and deploy resilient webhook listeners.', 'tf': 'Days 4 - 7' },
    { 'title': 'Deal Allocation Gating & Community Bot Testing', 'desc': 'Verify automated member onboarding, Discord role provisioning, and research document unlocks.', 'tf': 'Days 8 - 10' },
    { 'title': 'Syndicate Launch & Real-Time LP Retention Telemetry', 'desc': 'Open syndicate memberships to invited angels with live cohort and retention metrics.', 'tf': 'Days 11 - 14' }
]
vc_whop['faqs'] = [
    { 'q': 'Can angel investors and LPs pay syndicate membership dues through corporate wires?', 'a': 'Yes. Whop accommodates wire payments, ACH transfers, Apple Pay, and corporate credit cards with automated receipts.' },
    { 'q': 'How do you safeguard proprietary deal allocation memos from being forwarded to outside investors?', 'a': 'Deal rooms enforce single-session authentication, dynamic watermarking, and instant credential revocation upon membership expiration.' },
    { 'q': 'What occurs when an angel investor fails to renew their annual syndicate membership?', 'a': 'Whop automatically sends a webhook trigger revoking deal room access and removing their Discord syndicate roles.' },
    { 'q': 'Can a venture fund offer tiered co-investment priority for institutional vs individual LPs?', 'a': 'Yes. Whop allows customized tiers granting first-look co-investment rights to premium institutional members.' },
    { 'q': 'Does Whop handle cross-border tax compliance for international venture syndicates?', 'a': 'Yes. Whop acts as merchant of record, automatically calculating and remitting applicable international taxes and VAT.' }
]

vc_vps = data_vc_pe.DATA['venture-capital-private-equity/cloud-vps-hardening']
vc_vps['capabilities'] = [
    {
        'title': 'Zero-Port Virtual Diligence Vault Perimeter',
        'spec': 'Cloudflare Zero Trust tunnels shielding confidential investment data rooms and cap table databases.',
        'deliverable': 'Locked-down server configuration with zero listening ports on public interfaces.'
    },
    {
        'title': 'Hardware-Token MFA & Ephemeral SSH Bastion',
        'spec': 'Strict zero-trust access control requiring FIDO2 hardware keys for all server administration.',
        'deliverable': 'Automated intrusion prevention rules configured and verified.'
    },
    {
        'title': 'Sandboxed Docker Microservices for Pitch Deck Processing',
        'spec': 'Unprivileged container namespaces running financial modeling scripts and document analyzers.',
        'deliverable': 'Production Docker Compose templates hardened against container breakout.'
    },
    {
        'title': 'Encrypted Off-Site M&A Archive & Snapshot Engine',
        'spec': 'Automated hourly backups with GPG public-key encryption replicated to tamper-proof cold vaults.',
        'deliverable': 'Automated backup script with verified disaster recovery restore drill.'
    }
]
vc_vps['phases'] = [
    { 'title': 'Venture Security Assessment & Diligence Risk Audit', 'desc': 'Inspect server ports, evaluate access controls, and audit diligence data exposure.', 'tf': 'Days 1 - 3' },
    { 'title': 'Cloudflare Tunneling & Public Port Lockdown', 'desc': 'Route all VDR web traffic through encrypted tunnels while closing public firewall ports.', 'tf': 'Days 4 - 7' },
    { 'title': 'Diligence Worker Isolation & Least-Privilege Policies', 'desc': 'Run document ingestion pipelines under unprivileged service accounts with read-only storage.', 'tf': 'Days 8 - 10' },
    { 'title': 'Disaster Recovery Validation & Diligence Readiness Drill', 'desc': 'Test full data room recovery from encrypted backups and verify audit trails.', 'tf': 'Days 11 - 14' }
]
vc_vps['faqs'] = [
    { 'q': 'How does closing all public server ports protect sensitive venture dealrooms from corporate espionage?', 'a': 'With zero open listening ports, internet scanners cannot locate or probe your server IP, neutralizing automated exploit attempts.' },
    { 'q': 'How do investment partners and founders access private deal rooms securely?', 'a': 'Users authenticate through Cloudflare Access using corporate SSO and hardware MFA, eliminating vulnerable passwords.' },
    { 'q': 'How are proprietary cap tables and diligence documents protected from ransomware?', 'a': 'All files reside on encrypted filesystems backed up hourly to isolated cloud vaults with immutable versioning.' },
    { 'q': 'Can this server architecture support heavy diligence traffic during major portfolio funding rounds?', 'a': 'Yes. Cloudflare edge caching serves static assets globally while isolated origin containers scale to handle database queries.' },
    { 'q': 'How quickly can confidential diligence records be restored during a cloud provider outage?', 'a': 'Automated disaster recovery scripts restore encrypted snapshots to alternate infrastructure within 10 minutes.' }
]

# 3. Update data_edtech
import data_edtech
edtech_outbound = data_edtech.DATA['edtech/outbound-infrastructure']
edtech_outbound['capabilities'] = [
    {
        'title': 'Higher Education Outreach Infrastructure',
        'spec': 'Dedicated educational secondary domains configured with SPF, DKIM, and strict DMARC to bypass university filters.',
        'deliverable': 'Warmed domain cluster with dedicated IP routing for educational partnerships.'
    },
    {
        'title': 'Multi-Mailbox Rotation for EdTech Sales',
        'spec': 'Distribute superintendent and faculty outreach across 15+ warmed Google Workspace and Microsoft 365 accounts.',
        'deliverable': 'Cleaned prospect database with verified direct corporate email addresses.'
    },
    {
        'title': 'FERPA & Educational Compliance Architecture',
        'spec': 'Strict opt-out adherence and privacy-compliant academic contact enrichment pipelines.',
        'deliverable': 'Multi-stage educational peer cadence delivering high institutional response rates.'
    },
    {
        'title': 'Automated Academic Demo Scheduling Engine',
        'spec': 'Friction-free calendar booking integration accommodating academic semester schedules and office hours.',
        'deliverable': 'Real-time alert dispatcher notifying academic sales teams instantly.'
    }
]
edtech_outbound['phases'] = [
    { 'title': 'EdTech Domain Setup & DNS Protocol Verification', 'desc': 'Provision secondary domains and configure 2048-bit DKIM keys and strict DMARC enforcement.', 'tf': 'Days 1 - 3' },
    { 'title': 'Academic Mailbox Warming & Sender Trust Ramp', 'desc': 'Warm up sending accounts through verified educational peer networks over a 21-day schedule.', 'tf': 'Days 4 - 7' },
    { 'title': 'Department Head Persona Segmentation & Sequence Tuning', 'desc': 'Craft value-focused academic copy and test deliverability across university mail servers.', 'tf': 'Days 8 - 10' },
    { 'title': 'Campaign Rollout & Institutional Demo Pipeline Sync', 'desc': 'Launch cold outreach and synchronize positive educator replies with sales workflows.', 'tf': 'Days 11 - 14' }
]
edtech_outbound['faqs'] = [
    { 'q': 'Why do cold outreach emails to university deans and school superintendents bounce?', 'a': 'Educational institutions employ strict spam filters like Google Workspace for Education and Cisco IronPort; authenticated domains are required to reach the inbox.' },
    { 'q': 'What daily email volume is recommended when prospecting academic leaders?', 'a': 'We limit volume to 30 emails per inbox daily across distributed accounts to maintain exceptional domain reputation.' },
    { 'q': 'Does outbound email prospecting comply with academic privacy guidelines and FERPA?', 'a': 'Yes. Campaigns target publicly available faculty contact info for professional institutional evaluation only.' },
    { 'q': 'How long does it take to establish pristine deliverability on new EdTech domains?', 'a': 'The automated warming cycle runs for 3 to 4 weeks before launching high-volume outbound campaigns.' },
    { 'q': 'Can educators book software demonstrations directly from their mobile devices?', 'a': 'Yes. Calendar links are mobile-responsive and automatically account for campus timezones and academic calendar availability.' }
]

edtech_composio = data_edtech.DATA['edtech/composio-integrations']
edtech_composio['capabilities'] = [
    {
        'title': 'Self-Hosted EdTech Composio Tool Gateway',
        'spec': 'Sandboxed Composio runtime connecting AI agents to Canvas LMS, Blackboard, and Google Classroom APIs.',
        'deliverable': 'Turnkey Composio infrastructure repository configured for campus operations.'
    },
    {
        'title': 'Canvas & Google Classroom Tool Schemas',
        'spec': 'Deterministic function calling for grading submissions, creating course announcements, and tracking attendance.',
        'deliverable': 'Verified academic tool library with strict argument typing and schema gates.'
    },
    {
        'title': 'Student Information System (SIS) Synchronization Bridge',
        'spec': 'Bi-directional student record updates between LMS platforms and student billing databases.',
        'deliverable': 'Automated workflow updating academic records across campus systems.'
    },
    {
        'title': 'FERPA-Compliant Data Masking & Guardrail Middleware',
        'spec': 'Stripping student personally identifiable information before passing prompts to LLM execution contexts.',
        'deliverable': 'Configured guardrail middleware preventing student privacy exposure.'
    }
]
edtech_composio['phases'] = [
    { 'title': 'Academic System Audit & API Scope Mapping', 'desc': 'Map Canvas LMS, Blackboard, and student database endpoints and define permitted agent tools.', 'tf': 'Days 1 - 3' },
    { 'title': 'Composio Container Deployment & Token Vault Setup', 'desc': 'Deploy self-hosted Composio gateways with encrypted credential storage in isolated VPCs.', 'tf': 'Days 4 - 7' },
    { 'title': 'LMS Tool Orchestration & Guardrail Testing', 'desc': 'Execute 300+ automated tests verifying safe assignment grading and student record queries.', 'tf': 'Days 8 - 10' },
    { 'title': 'Production Campus Deployment & Telemetry Activation', 'desc': 'Connect live course workflows with real-time audit logging and instructor oversight.', 'tf': 'Days 11 - 14' }
]
edtech_composio['faqs'] = [
    { 'q': 'Can AI agents submit grades directly into Canvas LMS without teacher review?', 'a': 'No. Our guardrail middleware requires explicit instructor approval before committing any grades or academic records.' },
    { 'q': 'How does Composio connect to learning management systems like Blackboard or Canvas?', 'a': 'Composio integrates via official LTI and REST API protocols with scoped, least-privilege administrative tokens.' },
    { 'q': 'Is student data protected when AI agents call learning tools through Composio?', 'a': 'Yes. All student PII is masked locally before tool execution, ensuring compliance with FERPA data privacy mandates.' },
    { 'q': 'Can this integration automatically schedule Zoom tutoring sessions for struggling students?', 'a': 'Yes. When an agent detects a student requesting help, it can query tutor availability and issue calendar invites.' },
    { 'q': 'What happens if a school district API experiences downtime during peak school hours?', 'a': 'The Composio gateway buffers requests and implements exponential backoff to ensure zero lost student submissions.' }
]

edtech_whop = data_edtech.DATA['edtech/whop-monetization']
edtech_whop['capabilities'] = [
    {
        'title': 'Cohort Tuition & Student Tier Architecture',
        'spec': 'Multi-tiered pricing managing bootcamp tuition, monthly tutoring passes, and alumni community access.',
        'deliverable': 'Configured Whop membership store customized with modern educational academy branding.'
    },
    {
        'title': 'Real-Time Student LMS Webhook Provisioning Engine',
        'spec': 'Instant webhook dispatching unlocking video modules, homework sandboxes, and code repositories.',
        'deliverable': 'Idempotent webhook listener repository with automated error recovery.'
    },
    {
        'title': 'Discord & Slack Student Campus Community Gating',
        'spec': 'Automated role management admitting enrolled students to study halls and mentoring channels.',
        'deliverable': 'Automated community bot protecting proprietary campus channels and study materials.'
    },
    {
        'title': 'Automated Student Dunning & Tuition Recovery',
        'spec': 'Gentle payment reminder sequences and card retry logic recovering declined student installment plans.',
        'deliverable': 'Configured retention pipeline recovering over 75% of declined student payment cards.'
    }
]
edtech_whop['phases'] = [
    { 'title': 'Curriculum Tier Strategy & Tuition Scoping', 'desc': 'Structure course tiers, homework review limits, and live tutoring office hour access.', 'tf': 'Days 1 - 3' },
    { 'title': 'Whop Storefront Configuration & Webhook Pipeline', 'desc': 'Create student checkout flows on Whop and deploy HMAC-verified webhook listeners.', 'tf': 'Days 4 - 7' },
    { 'title': 'Campus Gating & Course Unlock Testing', 'desc': 'Test student enrollment workflows, Discord role assignments, and downloadable asset unlocks.', 'tf': 'Days 8 - 10' },
    { 'title': 'Cohort Launch & Enrollment Telemetry Monitoring', 'desc': 'Open course registration with real-time student conversion and churn tracking.', 'tf': 'Days 11 - 14' }
]
edtech_whop['faqs'] = [
    { 'q': 'Can students pay course tuition in monthly installments or split payments?', 'a': 'Yes. Whop natively supports flexible installment payment plans, recurring monthly subscriptions, and upfront tuition discounts.' },
    { 'q': 'How do you stop students from sharing course credentials and pirating video lessons?', 'a': 'LMS portals enforce concurrent session limits and bind video stream access to authenticated student Discord or email credentials.' },
    { 'q': 'What happens when a student cancels their recurring tutoring subscription?', 'a': 'Whop automatically sends a webhook revocation, removing access to live office hours and tutor scheduling portals immediately.' },
    { 'q': 'Can university departments purchase bulk course licenses for entire student cohorts?', 'a': 'Yes. Whop supports team and institutional licensing allowing educators to manage group enrollments with ease.' },
    { 'q': 'Does Whop handle global VAT and sales tax compliance for international students?', 'a': 'Yes. Whop operates as the merchant of record, automatically calculating and remitting digital service taxes across 100+ countries.' }
]

# 4. Update data_cybersecurity
import data_cybersecurity
cyber_outbound = data_cybersecurity.DATA['cybersecurity/outbound-infrastructure']
cyber_outbound['capabilities'] = [
    {
        'title': 'Hardened Enterprise Security Outreach Architecture',
        'spec': 'Dedicated secondary domains with SPF, 2048-bit DKIM, and strict DMARC rejection policies passing Proofpoint and Defender filters.',
        'deliverable': 'Warmed domain cluster with dedicated IP routing for cybersecurity business development.'
    },
    {
        'title': 'Multi-Mailbox Rotation for Cybersecurity Prospecting',
        'spec': 'Rotating outreach across 20+ warmed corporate mailboxes with conservative daily sending caps.',
        'deliverable': 'Cleaned prospect database with verified direct corporate email addresses.'
    },
    {
        'title': 'Zero-Spam High-Intent Prospecting Protocol',
        'spec': 'Strictly validated B2B email verifications and customized security executive value propositions.',
        'deliverable': 'Multi-stage security peer cadence delivering industry-leading reply rates.'
    },
    {
        'title': 'Direct CISO Calendar Discovery Scheduling',
        'spec': 'Automated meeting links designed for enterprise security executives with instant calendar hold confirmations.',
        'deliverable': 'Real-time alert dispatcher notifying security sales engineers instantly.'
    }
]
cyber_outbound['phases'] = [
    { 'title': 'Security Domain Setup & Cryptographic Protocol Verification', 'desc': 'Provision secondary domains and configure 2048-bit DKIM keys, SPF, and DMARC enforcement.', 'tf': 'Days 1 - 3' },
    { 'title': 'Algorithmic Mailbox Warming & Deliverability Ramp', 'desc': 'Gradually build reputation through enterprise peer mailboxes over a 21-day warming period.', 'tf': 'Days 4 - 7' },
    { 'title': 'CISO Persona Segmentation & Technical Messaging Review', 'desc': 'Craft concise, executive-level technical copy and validate deliverability against corporate firewalls.', 'tf': 'Days 8 - 10' },
    { 'title': 'Campaign Activation & Qualified Meeting Pipeline Sync', 'desc': 'Launch outreach sequences and sync qualified security leader responses with your sales CRM.', 'tf': 'Days 11 - 14' }
]
cyber_outbound['faqs'] = [
    { 'q': 'Why do emails to CISOs and security leaders frequently get quarantined?', 'a': 'Enterprise security organizations deploy aggressive mail filters like Proofpoint, Mimecast, and Defender; strict DMARC and warmed dedicated domains are mandatory.' },
    { 'q': 'What is the recommended daily sending limit when reaching out to enterprise security executives?', 'a': 'We enforce a strict limit of 25 to 30 emails per inbox daily to safeguard domain reputation and avoid automated filter triggers.' },
    { 'q': 'Does cold outreach to security executives risk our primary corporate domain reputation?', 'a': 'No. All prospecting runs on isolated secondary domains, shielding your primary operational domain from spam complaints.' },
    { 'q': 'How long does it take to prepare fresh domains for cybersecurity outreach?', 'a': 'Our automated warm-up engine runs for 3 to 4 weeks to establish pristine sender reputation before active prospecting begins.' },
    { 'q': 'Can prospective security leaders book technical briefings directly from their mobile phones?', 'a': 'Yes. Calendar booking links are mobile-responsive and coordinate directly with your sales engineering team schedule.' }
]

cyber_whop = data_cybersecurity.DATA['cybersecurity/whop-monetization']
cyber_whop['capabilities'] = [
    {
        'title': 'Threat Intelligence Tier & License Architecture',
        'spec': 'Gating zero-day vulnerability alerts, IOC threat feeds, and offensive security playbooks.',
        'deliverable': 'Configured Whop membership store customized with high-security branding.'
    },
    {
        'title': 'Encrypted Webhook Exploit Entitlement Engine',
        'spec': 'Secure HMAC-verified webhook listeners distributing dynamic license keys for private tooling repositories.',
        'deliverable': 'Idempotent webhook listener repository with automated error recovery.'
    },
    {
        'title': 'Discord & Matrix Red Team War Room Gating',
        'spec': 'Real-time role provisioning for exclusive cybersecurity research lounges and CTF team channels.',
        'deliverable': 'Automated community bot protecting proprietary research channels and payload repos.'
    },
    {
        'title': 'Automated Corporate Dunning & Security Subscription Recovery',
        'spec': 'Recovers failed enterprise security card payments with corporate invoicing and dunning schedules.',
        'deliverable': 'Configured retention pipeline recovering over 75% of declined corporate cards.'
    }
]
cyber_whop['phases'] = [
    { 'title': 'Intel Feed Tier Strategy & Entitlement Mapping', 'desc': 'Define subscription tiers for independent researchers, red teams, and enterprise SOCs.', 'tf': 'Days 1 - 3' },
    { 'title': 'Whop Storefront Configuration & Webhook Gateway Setup', 'desc': 'Deploy secure Whop checkout pages and build hardened webhook listener endpoints.', 'tf': 'Days 4 - 7' },
    { 'title': 'Research Repository Gating & Role Testing', 'desc': 'Verify automated GitHub repository invitations, Discord role assignments, and payload unlocks.', 'tf': 'Days 8 - 10' },
    { 'title': 'Production Launch & Security Researcher Telemetry', 'desc': 'Launch research subscriptions with real-time token tracking and access revocation auditing.', 'tf': 'Days 11 - 14' }
]
cyber_whop['faqs'] = [
    { 'q': 'Can enterprise security teams pay via corporate procurement purchase orders?', 'a': 'Yes. Whop supports corporate purchase orders, wire transfers, and corporate cards with automated VAT and sales tax invoicing.' },
    { 'q': 'How do you prevent unauthorized sharing of proprietary threat intelligence feeds?', 'a': 'Gated feeds enforce API key rotation, IP-binding, and concurrency limits to prevent credential sharing among unauthorized users.' },
    { 'q': 'What occurs when a security researcher cancels their monthly threat feed subscription?', 'a': 'Whop dispatches an instant webhook revocation, removing private GitHub repo access and Discord researcher roles immediately.' },
    { 'q': 'Can a cybersecurity firm offer team licenses for multi-member SOC analysis units?', 'a': 'Yes. Whop supports team seat allocations where security managers can invite analysts under a single billing plan.' },
    { 'q': 'Does Whop manage global tax compliance for international security research sales?', 'a': 'Yes. Whop operates as merchant of record, collecting and remitting applicable software taxes and VAT internationally.' }
]

# 5. Update data_agency
import data_agency
agency_outbound = data_agency.DATA['agency-consultancy/outbound-infrastructure']
agency_outbound['capabilities'] = [
    {
        'title': 'High-Ticket Agency Prospecting Infrastructure',
        'spec': 'Dedicated secondary domains with SPF, DKIM, and strict DMARC configured to pass enterprise brand email gateways.',
        'deliverable': 'Warmed domain cluster with dedicated IP routing for agency business development.'
    },
    {
        'title': 'Multi-Mailbox Rotation for B2B Client Acquisition',
        'spec': 'Distribute CMO and marketing director outreach across 20+ warmed Google Workspace and Office 365 accounts.',
        'deliverable': 'Cleaned prospect database with verified direct corporate email addresses.'
    },
    {
        'title': 'Hyper-Personalized Agency Pitch Sequence Architecture',
        'spec': 'Custom domain routing ensuring marketing audit pitches and case study outreach land in primary inboxes.',
        'deliverable': 'Multi-stage marketing peer cadence delivering industry-leading reply rates.'
    },
    {
        'title': 'Automated Brand Discovery Calendar Scheduling',
        'spec': 'Seamless discovery booking integration qualifying prospective brand clients and syncing with agency calendars.',
        'deliverable': 'Real-time alert dispatcher notifying agency business development teams instantly.'
    }
]
agency_outbound['phases'] = [
    { 'title': 'Agency Domain Setup & Cryptographic Verification', 'desc': 'Provision secondary domains and configure 2048-bit DKIM keys, SPF, and DMARC enforcement.', 'tf': 'Days 1 - 3' },
    { 'title': 'Strategic Mailbox Warming & Sender Trust Ramp', 'desc': 'Warm up client acquisition inboxes through verified enterprise peer pools over a 21-day schedule.', 'tf': 'Days 4 - 7' },
    { 'title': 'CMO Persona Segmentation & Campaign Verification', 'desc': 'Structure compelling agency case study sequences and verify inbox deliverability.', 'tf': 'Days 8 - 10' },
    { 'title': 'Campaign Activation & Qualified Strategy Call Sync', 'desc': 'Launch outreach sequences and sync qualified brand calls directly with your agency CRM.', 'tf': 'Days 11 - 14' }
]
agency_outbound['faqs'] = [
    { 'q': 'Why do cold agency outreach emails to brand CMOs often land in spam?', 'a': 'Enterprise marketing leaders receive dozens of generic pitches daily; authenticated secondary domains and clean deliverability records are essential.' },
    { 'q': 'What is the optimal daily sending volume for agency client acquisition?', 'a': 'We recommend 25 to 35 emails per mailbox daily across distributed accounts to maintain pristine sender reputation and avoid spam filters.' },
    { 'q': 'How does using dedicated secondary domains protect our primary agency website?', 'a': 'All prospecting runs on separate domains, completely isolating your main corporate domain from any deliverability risks.' },
    { 'q': 'How long does it take to ramp up a new agency outbound lead generation system?', 'a': 'The automated warm-up cycle takes 3 to 4 weeks before launching live outreach campaigns to prospective enterprise clients.' },
    { 'q': 'Can prospective clients book agency strategy calls directly from their mobile phones?', 'a': 'Yes. Calendar links are mobile-optimized and automatically coordinate with your senior strategist live availability.' }
]

agency_composio = data_agency.DATA['agency-consultancy/composio-integrations']
agency_composio['capabilities'] = [
    {
        'title': 'Self-Hosted Agency Composio Tool Gateway',
        'spec': 'Sandboxed Composio runtime connecting AI agents to HubSpot, ClickUp, Asana, and Slack APIs.',
        'deliverable': 'Turnkey Composio infrastructure repository configured for agency operations.'
    },
    {
        'title': 'Project Management & Client Reporting Tool Schemas',
        'spec': 'Deterministic function calling for creating client deliverables, updating task statuses, and logging hours.',
        'deliverable': 'Verified agency tool library with strict argument typing and schema gates.'
    },
    {
        'title': 'HubSpot & CRM Client Deal Synchronization Bridge',
        'spec': 'Bidirectional deal tracking and proposal status updates triggered by agent workflows.',
        'deliverable': 'Automated workflow updating client records across sales and management systems.'
    },
    {
        'title': 'Client Data Isolation & Credential Safeguard Vault',
        'spec': 'AES-256 encrypted OAuth token storage ensuring client credentials remain private and isolated.',
        'deliverable': 'Configured guardrail middleware preventing client credential leakage.'
    }
]
agency_composio['phases'] = [
    { 'title': 'Agency Tool Stack Audit & API Scope Mapping', 'desc': 'Map ClickUp, HubSpot, and Slack API permissions and define permitted agent tool boundaries.', 'tf': 'Days 1 - 3' },
    { 'title': 'Composio Container Deployment & OAuth Vault Setup', 'desc': 'Deploy self-hosted Composio gateways with encrypted credential storage in isolated VPCs.', 'tf': 'Days 4 - 7' },
    { 'title': 'Agency Tool Orchestration & Automated Policy Testing', 'desc': 'Run 300+ simulated task updates, time entries, and client status reporting tests.', 'tf': 'Days 8 - 10' },
    { 'title': 'Production Agency Deployment & Live Telemetry Activation', 'desc': 'Connect live agency project queues with real-time audit logging and account director alerts.', 'tf': 'Days 11 - 14' }
]
agency_composio['faqs'] = [
    { 'q': 'Can AI agents update client project boards in ClickUp or Asana automatically?', 'a': 'Yes. Agents can create tasks, assign team members, and update milestone statuses based on client deliverables.' },
    { 'q': 'How does Composio connect to agency CRMs like HubSpot or Salesforce?', 'a': 'Composio integrates via official OAuth REST APIs with granular, least-privilege permissions configured for your account.' },
    { 'q': 'Are our client API keys and proprietary assets secure inside Composio?', 'a': 'Yes. All credentials reside in an encrypted vault on your private server, never visible in LLM context windows.' },
    { 'q': 'Can this integration generate automated weekly client progress reports in Slack?', 'a': 'Yes. Agents query project management tools, compile milestone updates, and post polished summaries into dedicated client Slack channels.' },
    { 'q': 'What happens if a project management tool API experiences temporary rate limits?', 'a': 'The Composio gateway automatically queues requests with exponential backoff, ensuring zero lost task updates or client notifications.' }
]

agency_whop = data_agency.DATA['agency-consultancy/whop-monetization']
agency_whop['capabilities'] = [
    {
        'title': 'Productized Agency Retainer Tier Architecture',
        'spec': 'Multi-tiered subscription models for recurring marketing retainers, design sprints, and SEO maintenance packages.',
        'deliverable': 'Configured Whop membership store customized with creative agency branding.'
    },
    {
        'title': 'Client Workspace Webhook Provisioning Engine',
        'spec': 'Instant webhook dispatching granting subscribers access to private Slack channels, Notion portals, and Figma boards.',
        'deliverable': 'Idempotent webhook listener repository with automated error recovery.'
    },
    {
        'title': 'Slack & Discord VIP Client Lounge Gating',
        'spec': 'Automated client onboarding and role management based on real-time subscription status.',
        'deliverable': 'Automated community bot protecting proprietary client communication channels.'
    },
    {
        'title': 'Automated Retainer Dunning & Cash Flow Defense',
        'spec': 'Automated billing retry logic and branded reminder emails recovering declined corporate credit cards.',
        'deliverable': 'Configured retention pipeline recovering over 75% of declined corporate cards.'
    }
]
agency_whop['phases'] = [
    { 'title': 'Agency Package Strategy & Retainer Tier Scoping', 'desc': 'Structure productized service deliverables, turnaround SLAs, and client seat allocations.', 'tf': 'Days 1 - 3' },
    { 'title': 'Whop Storefront Configuration & Webhook Gateway Setup', 'desc': 'Build branded agency checkout funnels and deploy HMAC-verified webhook listeners.', 'tf': 'Days 4 - 7' },
    { 'title': 'Client Portal Access Gating & Onboarding Flow Testing', 'desc': 'Test automated client onboarding, Slack channel invites, and project board unlocks.', 'tf': 'Days 8 - 10' },
    { 'title': 'Productized Service Launch & Agency MRR Telemetry', 'desc': 'Launch recurring retainer plans with real-time revenue, churn, and client retention tracking.', 'tf': 'Days 11 - 14' }
]
agency_whop['faqs'] = [
    { 'q': 'Can agency clients pay ongoing retainers via credit card, ACH, or corporate invoice?', 'a': 'Yes. Whop supports all major credit cards, ACH transfers, Apple Pay, and automated PDF invoicing for agency retainers.' },
    { 'q': 'What happens when an agency client cancels or pauses their monthly subscription?', 'a': 'The Whop webhook immediately downgrades the account, pausing active service tickets and updating Slack channel permissions.' },
    { 'q': 'Can we offer custom add-ons and scope expansions on top of monthly retainers?', 'a': 'Yes. Whop allows clients to purchase one-time deliverable boosts or add-on packages directly from their customer portal.' },
    { 'q': 'Does Whop handle international sales tax compliance for cross-border agency clients?', 'a': 'Yes. Whop acts as the merchant of record, handling global tax compliance and VAT collection across international jurisdictions.' },
    { 'q': 'How does productizing agency services through Whop improve agency cash flow?', 'a': 'Upfront automated recurring billing eliminates accounts receivable delays, scope creep disputes, and manual invoice chasing.' }
]

agency_vps = data_agency.DATA['agency-consultancy/cloud-vps-hardening']
agency_vps['capabilities'] = [
    {
        'title': 'Multi-Tenant Agency Staging Perimeter',
        'spec': 'Outbound-only Cloudflare Tunnels isolating staging websites and client review environments with zero open ports.',
        'deliverable': 'Locked-down server configuration with zero listening ports on public interfaces.'
    },
    {
        'title': 'Cloudflare Access White-Label Client Portals',
        'spec': 'Securing preview environments behind Google Workspace or Magic Link authentication for client approvals.',
        'deliverable': 'Automated intrusion prevention rules configured and verified.'
    },
    {
        'title': 'Isolated Docker Staging Containers',
        'spec': 'Sandboxing client CMS instances in unprivileged containers with dedicated CPU and memory limits.',
        'deliverable': 'Production Docker Compose templates hardened against container breakout.'
    },
    {
        'title': 'Automated GPG-Encrypted Snapshot & Client Site Backup Pipeline',
        'spec': 'Nightly automated database and media snapshots synced to secure off-site cloud storage.',
        'deliverable': 'Automated backup script with verified disaster recovery restore drill.'
    }
]
agency_vps['phases'] = [
    { 'title': 'Agency Infrastructure Audit & Vulnerability Assessment', 'desc': 'Review staging server ports, container configurations, and client database access controls.', 'tf': 'Days 1 - 3' },
    { 'title': 'Cloudflare Tunneling & Staging Server Port Lockdown', 'desc': 'Eliminate public listening ports and configure zero-trust access for agency staff and clients.', 'tf': 'Days 4 - 7' },
    { 'title': 'Multi-Tenant Container Sandboxing & Resource Isolation', 'desc': 'Sandbox client application instances into isolated Docker networks with resource limits.', 'tf': 'Days 8 - 10' },
    { 'title': 'Disaster Recovery Validation & Client Hand-off Testing', 'desc': 'Simulate complete server restore from encrypted backups and verify audit trail reporting.', 'tf': 'Days 11 - 14' }
]
agency_vps['faqs'] = [
    { 'q': 'How do clients review staging web applications if all server ports are closed?', 'a': 'Clients authenticate through Cloudflare Access using their email or magic link, accessing preview URLs securely without public port exposure.' },
    { 'q': 'How does container isolation protect multiple client websites on a shared VPS?', 'a': 'Each client instance runs in an isolated Docker container with its own network namespace, preventing cross-tenant data leaks.' },
    { 'q': 'How do agency developers deploy updates to hardened servers without SSH port exposure?', 'a': 'Developers deploy via GitHub Actions and authenticated Cloudflare Zero Trust tunnels, eliminating open SSH ports on public IPs.' },
    { 'q': 'How are client database backups secured against ransomware or accidental deletion?', 'a': 'Automated cron jobs encrypt daily database snapshots with GPG and replicate them to immutable, off-site cloud object storage.' },
    { 'q': 'Will Cloudflare Zero Trust caching improve staging site performance for remote clients?', 'a': 'Yes. Cloudflare edge caching serves static assets and media files from edge nodes worldwide, accelerating client review sessions.' }
]

# Write back each file cleanly
def write_module(filepath, data_dict, docstring):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'"""\n{docstring}\n"""\nimport json\n\nDATA = ')
        json.dump(data_dict, f, indent=4)
        f.write('\n')

write_module(os.path.join(SCRIPT_DIR, 'data_legaltech.py'), data_legaltech.DATA, 'LegalTech & High-Ticket Professional Services - Bespoke Data')
write_module(os.path.join(SCRIPT_DIR, 'data_vc_pe.py'), data_vc_pe.DATA, 'Venture Capital & Private Equity Firms - Bespoke Data')
write_module(os.path.join(SCRIPT_DIR, 'data_edtech.py'), data_edtech.DATA, 'EdTech & Digital Academies - Bespoke Data')
write_module(os.path.join(SCRIPT_DIR, 'data_cybersecurity.py'), data_cybersecurity.DATA, 'Cybersecurity & SecOps Solutions - Bespoke Data')
write_module(os.path.join(SCRIPT_DIR, 'data_agency.py'), data_agency.DATA, 'Agency & Professional Consultancy Operations - Bespoke Data')

print('All 5 remaining modules successfully patched and saved!')
