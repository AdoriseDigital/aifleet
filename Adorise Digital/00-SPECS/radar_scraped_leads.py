import json
import random

def generate_radar_batch():
    industries = ["SaaS", "FinTech", "AI Automation", "Digital Agency", "Cloud Infrastructure", "Cybersecurity", "HealthTech"]
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Sam", "Chris", "Pat", "Jamie", "Riley", "Avery", "Dakota"]
    companies = ["Apex", "Vertex", "Quantum", "Nexus", "Pioneer", "Zenith", "Vanguard", "Synergy", "Omni", "Dynamic", "Nova", "Alpha"]
    
    batch = []
    for i in range(20):
        name = f"{random.choice(names)} {random.choice(names)}"
        company = f"{random.choice(companies)} {random.choice(industries)}"
        clean_company = company.lower().replace(' ', '')
        batch.append({
            "contact_name": name,
            "business_name": company,
            "email": f"lead{i+1}_{clean_company}@{clean_company}.io",
            "phone": f"+1555{random.randint(1000000, 9999999)}"
        })
    
    with open("radar_scraped_leads.json", "w", encoding="utf-8") as f:
        json.dump(batch, f, indent=2)
    print(f"[RADAR] Generated 20 high-volume leads into radar_scraped_leads.json")

if __name__ == "__main__":
    generate_radar_batch()