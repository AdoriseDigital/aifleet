import json
import os
import re

from test_combo_gen import NICHES, SERVICES

# Load existing Batch 1 combinations from compile_pseo.js to keep them identical
with open('pseo-engine/data/batch_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

published_slugs = []
for b in manifest['batches']:
    published_slugs.extend(b['slugs'])

def generate_entry(niche_id, service_id):
    n = NICHES[niche_id]
    s = SERVICES[service_id]

    h1 = f"{s['name']} for {n['name']}"
    subheadline = f"Engineered specifically for {n['buyer']} in {n['short']} seeking to scale {s['deliv_focus']}. Built on modern {s['tech']} to eliminate operational bottlenecks, compress sales cycles, and drive predictable enterprise revenue."

    deep_dive_1 = (
        f"Enterprises operating across {n['context']} face compounding operational friction when attempting to scale {s['deliv_focus']}. "
        f"Relying on manual labor, junior staff, or fragile off-the-shelf software leads to escalating overhead, slow turnaround times, and severe delivery bottlenecks. "
        f"Without automated systems calibrated to the regulatory standards of {n['reg']}, internal teams spend critical bandwidth firefighting administrative issues rather than executing core business strategy."
    )

    deep_dive_2 = (
        f"Adorise Digital deploys production-grade {s['name'].lower()} architecture that docks directly into existing enterprise environments including {n['stack']}. "
        f"Every inbound request, automated transaction, and background task executes through strict schema validation gates, encrypted environment vaults, and auditable telemetry. "
        f"By enforcing strict {n['reg']} compliance and deterministic error handling, leadership gains an unshakeable operational foundation that compounds business velocity over time."
    )

    pain1_title, pain1_desc, pain1_impact = n['pains'][0]
    pain2_title, pain2_desc, pain2_impact = n['pains'][1]
    pain3_title, pain3_desc, pain3_impact = n['pains'][2]

    pain_points = [
        {
            'title': f"{pain1_title} in {n['short']}",
            'description': f"When scaling {s['deliv_focus']}, {pain1_desc.lower()}",
            'impact': pain1_impact
        },
        {
            'title': f"{pain2_title} Across {n['short']} Operations",
            'description': f"Attempting to manage {s['short']} workflows manually leads to point-to-point tool failures: {pain2_desc.lower()}",
            'impact': pain2_impact
        },
        {
            'title': f"{pain3_title} Threatening Enterprise Margins",
            'description': f"In the absence of hardened {s['name'].lower()} infrastructure, {pain3_desc.lower()}",
            'impact': pain3_impact
        }
    ]

    capabilities = [
        {
            'title': f"Tailored {s['short']} Architecture for {n['short']}",
            'spec': f"Engineers production-grade {s['name']} infrastructure integrated directly with {n['stack']} adhering strictly to {n['reg']}.",
            'deliverable': f"Fully configured deployment repository with automated provisioning and infrastructure telemetry."
        },
        {
            'title': f"Deterministic Data Validation & Security Boundaries",
            'spec': f"Implements strict parameter schemas, cryptographic payload validation, and access controls protecting {n['context']}.",
            'deliverable': f"Zero-trust execution boundaries with automated transaction audit logging."
        },
        {
            'title': f"Automated Interoperability & System Connectors",
            'spec': f"Connects {s['short']} background pipelines seamlessly with existing corporate workflows and client management tools.",
            'deliverable': f"Hardened webhook and API bridges with automated retry queues and error notification dispatchers."
        },
        {
            'title': f"Continuous Performance Monitoring & SLA Enforcement",
            'spec': f"Deploys real-time telemetry dashboards tracking latency, throughput, error rates, and {n['metrics_arr']}.",
            'deliverable': f"Live telemetry dashboard with automated incident alerting webhooks."
        }
    ]

    phases = [
        {
            'title': f"Discovery & {n['short']} Workflow Audit",
            'desc': f"Audit current operational handoffs, data structures, and integration points across {n['stack']}.",
            'tf': 'Days 1 - 3'
        },
        {
            'title': f"Core {s['short']} Infrastructure Setup",
            'desc': f"Construct dynamic components, schema definitions, and API connectors on modern edge infrastructure.",
            'tf': 'Days 4 - 7'
        },
        {
            'title': f"Security & {n['reg']} Compliance Assertion",
            'desc': f"Execute automated stress tests, schema compliance checks, and security perimeter scans.",
            'tf': 'Days 8 - 10'
        },
        {
            'title': f"Production Deployment & Operational Handoff",
            'desc': f"Deploy to live edge network, activate automated telemetry, and transition complete documentation to internal teams.",
            'tf': 'Days 11 - 14'
        }
    ]

    faqs = [
        {
            'q': f"How does this {s['name']} deployment integrate into our existing {n['short']} environment?",
            'a': f"We engineer modular, decoupled components and standard API webhooks that dock cleanly into {n['stack']} without requiring structural refactoring."
        },
        {
            'q': f"How does the system ensure compliance with {n['reg']} standards?",
            'a': f"All data transactions are isolated, encrypted in transit and at rest, and validated against strict schema boundaries adhering to {n['reg']} guidelines."
        },
        {
            'q': f"What timeline is required before our {n['short']} team sees tangible results?",
            'a': f"Our structured 14-day delivery sprint ensures production deployment and live automated execution within two weeks of project kickoff."
        },
        {
            'q': f"Who retains ownership of the codebase, templates, and integration workflows?",
            'a': f"Your organization maintains 100% intellectual property ownership of all custom code, configuration files, and data assets produced during deployment."
        },
        {
            'q': f"How does this solution scale as our business volume increases?",
            'a': f"Engineered on edge CDNs and serverless runtimes, our architecture automatically absorbs traffic and transaction spikes with zero latency degradation."
        }
    ]

    human_solutions = {
        'businessTitle': f"Operational & Revenue Defense for {n['name']}",
        'businessStory': (
            f"Operating in {n['name']} demands absolute operational velocity. "
            f"When teams get stuck in manual administrative coordination across {n['context']}, strategic pipeline expansion grinds to a halt. "
            f"Our systems provide a durable technical moat that protects your operating margins."
        ),
        'businessPillars': [
            {
                'title': f"Automated Pipeline & Operational Velocity",
                'desc': f"Replaces fragile manual coordination with deterministic {s['name'].lower()} workflows tailored for {n['short']}.",
                'product': f"Adorise Engineered Systems ($297/mo)"
            },
            {
                'title': f"Systematic Client & Revenue Protection",
                'desc': f"Guarantees consistent execution across {n['context']}, mitigating operational errors and customer drop-off.",
                'product': f"Production Architecture Retainer"
            },
            {
                'title': f"Ecosystem Authority & Market Leadership",
                'desc': f"Establishes unmistakable operational superiority over competitors relying on slower legacy practices in {n['name']}.",
                'product': f"Enterprise Turnkey Deployment"
            }
        ],
        'personalTitle': f"Protecting {n['buyer']} from Executive Fatigue & Anxiety",
        'personalStory': (
            f"Behind every organization in {n['name']} are dedicated leaders bearing the psychological burden of {n['stress']}. "
            f"We engineer software that restores executive sanity, evening calm, and focused strategic thinking."
        ),
        'personalPillars': [
            {
                'icon': '🛡️',
                'title': 'Communication Stress & Conflict Defense',
                'desc': f"When high-pressure emails arrive regarding {n['context']}, InboxCalm scores toxicity and drafts calm, de-escalating replies.",
                'product': 'InboxCalm (Automated Email Firewall)',
                'url': 'https://inboxcalm.adorisedigital.com'
            },
            {
                'icon': '🎬',
                'title': 'Thought Leadership Video Automation',
                'desc': f"Converts technical presentations into vertical 9:16 video insights in under 60 seconds without video editing friction.",
                'product': 'ClipCalm AI (Viral Video Repurposing)',
                'url': 'https://clipcalm.adorisedigital.com'
            },
            {
                'icon': '🕊️',
                'title': 'Executive Grounding & Emotional Reset',
                'desc': f"When high-stakes decisions and sprint deadlines create anxiety, DearMee offers a confidential, non-judgmental conversational co-pilot.",
                'product': 'DearMee AI (Empathetic Companion)',
                'url': 'https://dearmee.adorisedigital.com'
            }
        ]
    }

    return {
        'niche_name': n['name'],
        'service_name': s['name'],
        'badge': f"{s['short']} | {n['short']}",
        'h1': h1,
        'subheadline': subheadline,
        'metrics': [
            {'val': '< 45ms', 'lbl': 'Edge TTFB', 'sub': 'Sub-second React Server Components load'},
            {'val': '+340%', 'lbl': 'Pipeline Expansion', 'sub': 'Qualified inbound demo volume growth'},
            {'val': '100%', 'lbl': 'Schema Validated', 'sub': 'Complete ProfessionalService JSON-LD'},
            {'val': n['acv'], 'lbl': 'Target ACV Tier', 'sub': 'High-value enterprise contract focus'}
        ],
        'deep_dive_1': deep_dive_1,
        'deep_dive_2': deep_dive_2,
        'pain_points': pain_points,
        'capabilities': capabilities,
        'phases': phases,
        'faqs': faqs,
        'humanSolutions': human_solutions
    }

combinations = {}
for s in published_slugs:
    parts = s.strip('/').split('/')
    niche_id = parts[1]
    service_id = parts[2]
    key = f"{niche_id}/{service_id}"
    combinations[key] = generate_entry(niche_id, service_id)

print(f"Generated {len(combinations)} combinations successfully.")
with open('pseo-engine/data/curated_combinations_data.json', 'w', encoding='utf-8') as f:
    json.dump(combinations, f, indent=2)
print("Saved to pseo-engine/data/curated_combinations_data.json.")
