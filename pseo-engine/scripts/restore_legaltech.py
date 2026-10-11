import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COMBOS_PATH = os.path.join(SCRIPT_DIR, '../data/all_70_combinations.json')
HUMAN_PATH = os.path.join(SCRIPT_DIR, '../data/all_70_human_solutions.json')
TARGET_PATH = os.path.join(SCRIPT_DIR, 'data_legaltech.py')

with open(COMBOS_PATH, 'r', encoding='utf-8') as f:
    all_combos = json.load(f)

with open(HUMAN_PATH, 'r', encoding='utf-8') as f:
    all_human = json.load(f)

legal_keys = [
    'legaltech-professional/pseo-engine',
    'legaltech-professional/web-app-engineering',
    'legaltech-professional/outbound-infrastructure',
    'legaltech-professional/composio-integrations',
    'legaltech-professional/whop-monetization',
    'legaltech-professional/cloud-vps-hardening'
]

data = {}
for k in legal_keys:
    if k in all_combos:
        data[k] = dict(all_combos[k])
        if k in all_human:
            data[k]['humanSolutions'] = all_human[k]

# Also ensure legaltech-professional/cloud-vps-hardening has the bespoke faqs
if 'legaltech-professional/cloud-vps-hardening' in data:
    data['legaltech-professional/cloud-vps-hardening']['faqs'] = [
        { 'q': 'Does this server hardening satisfy legal industry standards for protecting attorney-client privilege?', 'a': 'Yes. Eliminating public open ports, enforcing strong encryption, and maintaining immutable audit logs align with ABA cybersecurity guidelines.' },
        { 'q': 'How do attorneys and paralegals access internal case databases securely?', 'a': 'Staff connect via Cloudflare Access protected by corporate MFA, eliminating open SSH ports and preventing unauthorized network entry.' },
        { 'q': 'How are confidential deposition transcripts and matter evidence protected from ransomware?', 'a': 'All matter files are stored on encrypted volumes with write-once off-site backups that cannot be overwritten or held hostage.' },
        { 'q': 'Can this infrastructure support high-volume document ingestion during active litigation discovery?', 'a': 'Yes. Isolated container workers process discovery batches efficiently without exposing the underlying operating system.' },
        { 'q': 'What disaster recovery measures exist if a cloud host suffers catastrophic failure?', 'a': 'Automated scripts restore encrypted matter archives to fresh infrastructure within 10 minutes, ensuring zero case data loss.' }
    ]

with open(TARGET_PATH, 'w', encoding='utf-8') as f:
    f.write('"""\nLegalTech & High-Ticket Professional Services - Bespoke Data\n"""\n\nDATA = ')
    json.dump(data, f, indent=4)
    f.write('\n')

print("Successfully restored data_legaltech.py!")
