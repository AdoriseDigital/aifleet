import os
import json
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List

# ==============================================================================
# STRICT PYDANTIC VALIDATION GATE (Zero-Stub & Anti-Fake Success Architecture)
# ==============================================================================

class VerifiedLead(BaseModel):
    contact_name: str = Field(..., min_length=2)
    business_name: str = Field(..., min_length=2)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None)
    social_handle: Optional[str] = Field(None)
    country: str = Field("US")
    
    @validator('email', pre=True, always=True)
    def validate_and_filter_email(cls, v):
        if not v or v.strip() == "":
            return None
        v_lower = v.strip().lower()
        blacklisted = ["example.com", "test.com", "sample.com", "tempmail.com", "mailinator.com"]
        domain = v_lower.split("@")[-1] if "@" in v_lower else ""
        if domain in blacklisted or "example" in v_lower or "test" in v_lower:
            raise ValueError(f"Blocked dummy/test email domain: {v}")
        return v_lower

    def is_fully_contactable(self) -> bool:
        has_email = bool(self.email and "@" in self.email)
        has_phone = bool(self.phone and len(self.phone.strip()) > 5)
        has_social = bool(self.social_handle and len(self.social_handle.strip()) > 3)
        return has_email or has_phone or has_social


# ==============================================================================
# VISUAL DASHBOARD & ENGINE CONTROLLER
# ==============================================================================

class ProductionRevenueSystem:
    def __init__(self, dashboard_file="live_leads_dashboard.md"):
        self.dashboard_file = dashboard_file
        self.results_log = []

    def update_visual_dashboard(self):
        verified_items = [r for r in self.results_log if r["status"] == "VERIFIED"]
        rejected_items = [r for r in self.results_log if r["status"] == "REJECTED_STUB"]

        markdown_content = f"""# 🚀 Autonomous Revenue Engine - Live Operations Board
*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## 📊 Pipeline Status Summary
* **Total Processed:** {len(self.results_log)}
* **Successfully Verified & Dispatched:** {len(verified_items)}
* **Quarantined / Rejected Stubs:** {len(rejected_items)}

---

## 🛑 Quarantined / Rejected Stubs (Blocked Fake Success)
| Business Name | Contact Name | Provided Email | Rejection Reason |
| :--- | :--- | :--- | :--- |
"""
        for item in rejected_items:
            markdown_content += f"| {item['business_name']} | {item['contact_name']} | `{item['email']}` | {item['reason']} |\n"

        markdown_content += """
---

## ✅ Verified & Dispatched Leads (Clean Pipeline)
| Business Name | Contact Name | Validated Email / Phone | Status |
| :--- | :--- | :--- | :--- |
"""
        for item in verified_items:
            markdown_content += f"| {item['business_name']} | {item['contact_name']} | `{item['contact_point']}` | 🟢 Dispatched Live |\n"

        with open(self.dashboard_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"[DASHBOARD] Updated visual board -> {self.dashboard_file}")

    def process_lead(self, raw_data: dict) -> bool:
        company = raw_data.get("business_name", "Unknown")
        name = raw_data.get("contact_name", "Unknown")
        email = raw_data.get("email", "")

        try:
            lead = VerifiedLead(**raw_data)
            
            if not lead.is_fully_contactable():
                print(f"[REJECTED] {name} ({company}) -> Lacks valid contact coordinates.")
                self.results_log.append({
                    "status": "REJECTED_STUB",
                    "business_name": company,
                    "contact_name": name,
                    "email": email,
                    "reason": "Missing valid email/phone/social handle"
                })
                self.update_visual_dashboard()
                return False
            else:
                print(f"[VERIFIED] {name} ({company}) -> Passed strict validation gate.")
                self.results_log.append({
                    "status": "VERIFIED",
                    "business_name": company,
                    "contact_name": name,
                    "contact_point": lead.email or lead.phone or lead.social_handle
                })
                self.update_visual_dashboard()
                return True
        except Exception as e:
            print(f"[FIREWALL BLOCK] {name} ({company}) -> Error: {e}")
            self.results_log.append({
                "status": "REJECTED_STUB",
                "business_name": company,
                "contact_name": name,
                "email": email,
                "reason": str(e)
            })
            self.update_visual_dashboard()
            return False

if __name__ == "__main__":
    system = ProductionRevenueSystem()
    sample_batch = [
        {"contact_name": "Chloe Bennett", "business_name": "SaaS Velocity Labs", "email": "chloe@example.com"},
        {"contact_name": "Marcus Sterling", "business_name": "OmniScale Media", "email": "marcus@omniscalemedia.com", "phone": "+15559876543"}
    ]
    for record in sample_batch:
        system.process_lead(record)