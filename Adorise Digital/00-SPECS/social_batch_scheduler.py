#!/usr/bin/env python3
"""
Multi-Day Social Media Batch Scheduler & Omni-Channel Publisher
Author: Adorise Digital Engineering Desk

Generates and schedules 3 to 7 days of structured social media posts across:
- Instagram (ca_Op45N88E_Uz7)
- Facebook (ca_MgB81OXe5Y61)
- Pinterest (ca_-__zKRUT-1_J)
- Reddit (ca_bpi7ozDUBqyp)
- YouTube (ca_0yenexSvzmMY)
- Telegram (ca_kNPbIMecBajf)

Operates cleanly without any legacy K_ dependencies.
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(SCRIPT_DIR, "social_media_queue.json")
HISTORY_FILE = os.path.join(SCRIPT_DIR, "social_media_history.json")

ACTIVE_COMPOSIO_ACCOUNTS = {
    "instagram": "ca_Op45N88E_Uz7",
    "facebook": "ca_MgB81OXe5Y61",
    "pinterest": "ca_-__zKRUT-1_J",
    "reddit": "ca_bpi7ozDUBqyp",
    "youtube": "ca_0yenexSvzmMY",
    "telegram": "ca_kNPbIMecBajf"
}

DAILY_SLOTS = [
    {"slot": "Morning", "time": "08:30 UTC", "theme_type": "Authority, AI Systems & Book Wisdom"},
    {"slot": "Midday", "time": "13:00 UTC", "theme_type": "Case Studies, Emotional Stories & Teasers"},
    {"slot": "Evening", "time": "18:30 UTC", "theme_type": "Offer, Community & Reader Discussion"}
]

CONTENT_BANK = {
    "Morning": [
        {
            "hook": "Caregiving is not a task on a checklist; it is an invisible holding of hands in the dark.",
            "body": "When caring for someone with Alzheimer's or chronic pain, the hardest part isn't the physical routine—it's watching pieces of someone fade while still loving what remains.\n\nFrom 'After the Last Goodbye': True care begins when we stop measuring progress and start measuring presence.\n\nExplore the Care Collection: https://books.adorisedigital.com",
            "tags": "#CaregiverSupport #DementiaCare #CaregiverJourney #AdoriseBooks"
        },
        {
            "hook": "Most businesses lose 40+ hours every week on repetitive lead data entry and broken workflows.",
            "body": "Autonomous AI fleets flip the script:\n1. Radar signals detect commercial intent.\n2. Deterministic code cleans every coordinate.\n3. Contextual value lands in primary inboxes.\n\nScale without burning out your core team: https://adorisedigital.com",
            "tags": "#AIOperations #BusinessAutomation #DigitalAgency #GrowthHacking"
        }
    ],
    "Midday": [
        {
            "hook": "Behind every silent dinner is a couple who forgot how to ask about the little things.",
            "body": "In 'The Weekend Marriage', silence isn't the absence of words—it's the accumulation of things left unsaid for years.\n\nEarly novella preview launching this season under Adorise DigitalUSA.\n\nRead our upcoming catalog: https://books.adorisedigital.com",
            "tags": "#RelationshipNovella #FictionReads #EmotionalDrama #BookLovers"
        },
        {
            "hook": "Why 95% of AI-generated content sounds robotic and dead inside:",
            "body": "Machine loops, repetitive filler phrases, and single-shot generation ruin quality.\n\nOur 95%+ QA Gate enforces human rhythm, sensory descriptions, and strict EPUB3 standards across all 48 Adorise publications.\n\nDiscover the difference: https://adorisedigital.gumroad.com",
            "tags": "#PublishingStandards #IndieAuthor #QualityWriting #BookPublishing"
        }
    ],
    "Evening": [
        {
            "hook": "Late-night founder reminder: You don't burn out from hard work; you burn out from emotional clutter.",
            "body": "InboxCalm intercepts high-stress client emails, strips the venom, and delivers calm, reasoned responses in minutes.\n\nProtect your mental peace while closing deals.\n\nLearn more: https://inboxcalm.adorisedigital.com",
            "tags": "#FounderMentalHealth #Productivity #InboxCalm #WorkLifeBalance"
        },
        {
            "hook": "Anya Ravencroft — Dark Romantasy Novellas Arriving Soon.",
            "body": "Whispers in the stone, ancient bloodlines, and magic that demands a price.\n\nFor readers who crave slow-burn tension, atmospheric court intrigue, and fierce heroines.\n\nJoin the early reader list: https://books.adorisedigital.com",
            "tags": "#Romantasy #FantasyReads #AnyaRavencroft #BookTok #KindleReads"
        }
    ]
}


class SocialBatchScheduler:
    def __init__(self):
        self.queue_file = QUEUE_FILE
        self.history_file = HISTORY_FILE

    def generate_batch(self, days: int = 7) -> List[Dict]:
        """Generates a complete 3-day or 7-day social queue across all connected channels"""
        print(f"\n[SOCIAL SCHEDULER] Generating {days}-Day Omni-Channel Content Queue...")
        start_date = datetime.now()
        queue = []

        for d in range(days):
            current_day = start_date + timedelta(days=d)
            date_str = current_day.strftime("%Y-%m-%d")

            for slot_info in DAILY_SLOTS:
                slot_name = slot_info["slot"]
                slot_time = slot_info["time"]
                templates = CONTENT_BANK.get(slot_name, [])

                for platform, account_id in ACTIVE_COMPOSIO_ACCOUNTS.items():
                    chosen = random.choice(templates)
                    full_post = f"{chosen['hook']}\n\n{chosen['body']}\n\n{chosen['tags']}"
                    
                    queue.append({
                        "id": f"soc_{date_str}_{slot_name.lower()}_{platform}",
                        "scheduled_date": date_str,
                        "slot": slot_name,
                        "time": slot_time,
                        "platform": platform,
                        "composio_account_id": account_id,
                        "content": full_post,
                        "status": "queued",
                        "created_at": datetime.now().isoformat()
                    })

        with open(self.queue_file, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

        print(f"✅ Successfully queued {len(queue)} posts covering {days} days across {len(ACTIVE_COMPOSIO_ACCOUNTS)} platforms.")
        return queue


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    scheduler = SocialBatchScheduler()
    scheduler.generate_batch(days=days)
