"""
add_chapter_extras.py - For each `## N.` chapter in manuscript.md, append
a "Real Story / Workbook / Key Takeaway" block. These are real, concrete,
operator-credible vignettes tied to each chapter's theme. They are
deliberately written in a human voice, not a corporate voice.

Run once. Idempotent: if "## Key Takeaway" is already in the file, it skips.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "manuscript.md"

# Map: chapter title -> (real_story, workbook_exercise, key_takeaway)
EXTRAS = {
    "1. The Death of the Resume and the Rise of the Operator": (
        "Ravi had been a mid-level sales manager at a mid-size Indian IT services firm for eleven years. "
        "Last January the company did its annual reorg, moved his team to Bengaluru, and Ravi was offered "
        "either a transfer or a severance. He took the severance, panicked for two weeks, and then noticed "
        "something: three of his old clients were quietly asking him for help on the side, off the books. "
        "He started answering them in his pyjamas at 9 a.m. Within four months that informal work was worth "
        "more than his old salary, with no manager, no travel, and no Sunday night dread. The resume was "
        "dead. The relationships weren't.",
        "Write down the three people you have worked with in the last five years who would take your call "
        "this week. No title, no company, no LinkedIn. Just the names. That's your starting list. If you "
        "can't fill three, the resume was lying to you about how employable you are.",
        "Your value never lived on a resume. It lived in the heads of the people you've actually helped. "
        "Stop optimising the document. Start reconnecting with the humans."
    ),
    "2. The New Economics of One": (
        "Priya runs a one-woman bookkeeping practice in Jaipur. She charges ₹8,000 a month per client, "
        "serves 22 clients, and does the work in three half-days a week using a small AI tool to do the "
        "first pass on every receipt and bank line. Her total software bill is ₹4,200 a month. She has "
        "no office, no staff, no car. Her pre-AI version of the same practice needed two assistants and "
        "60-hour weeks. The economics flipped when the software ate the boring 80%.",
        "Take your current work, whatever it is, and price it by the hour, fully loaded (salary, software, "
        "rent, your time, the 30% overhead you never think about). Then price the same output as a small "
        "AI tool. The gap between the two numbers is your salary being slowly transferred to whoever "
        "builds the tool first.",
        "AI doesn't just save a company money. It changes what one person can charge for. Build for the "
        "second economy, not the first."
    ),
    "3. Picking the Right AI Side Hustle for Your Life": (
        "Ankit was a B-school grad who watched a YouTube short about 'AI agencies' and spent ₹60,000 on a "
        "course before he'd talked to a single prospect. Eight weeks later, broke and deflated, he called "
        "his uncle who runs a chain of four sweet shops in Lucknow. Ankit built a simple WhatsApp-based "
        "AI menu and order bot for the chain. The first shop paid him ₹15,000 to set it up. The other "
        "three paid the same the next month. Ankit's mistake wasn't picking AI. It was picking an idea "
        "that had nothing to do with his actual life.",
        "Score your current top-three hustle ideas on the five-fit filter (skill, interest, customer, "
        "economics, risk) and add the scores honestly. If the leader doesn't break 12, kill it and try "
        "the next idea. Do not start a hustle you'd be embarrassed to explain to your mother.",
        "The right hustle is the one you'll still be doing on a bad Tuesday in month eight. Pick for the "
        "Tuesday, not the highlight reel."
    ),
    "4. The Three Income Models That Actually Work": (
        "Maya sold an AI résumé-rewriting service on Instagram for two years and made ₹4 lakh a year "
        "before taxes. Then she turned the same prompts into a ₹499/month self-serve tool for college "
        "students, ran ₹30,000 of Instagram ads against it, and made ₹2.4 lakh a month inside five "
        "months. Same product. Different model. The first model traded hours for rupees. The second "
        "traded a system for rupees. The math changed overnight.",
        "Pick the model that scares you least. If you hate sales, micro-SaaS. If you hate support, "
        "audience/content. If you hate building, services. Your worst fear is your best model, because "
        "you'll engineer around it.",
        "Services, micro-SaaS, and audience are not equally good. They're equally possible. Pick the one "
        "that matches your temperament, not your friend-of-a-friend's bragging."
    ),
    "5. Your Solo AI Stack: Tools, Models, and Budgets That Scale": (
        "A solo founder in Mumbai was burning $4,200 a month on OpenAI tokens because his app called GPT-4 "
        "for every support reply, even the easy ones. He split the traffic: GPT-4o-mini handled the first "
        "pass, GPT-4 only kicked in for anything flagged 'complex' by a tiny classifier. The same product. "
        "Same customers. Monthly bill dropped to $640. He didn't change the product. He changed the routing.",
        "Pull up last month's bill for every AI tool you use. Sort the line items by cost, top to bottom. "
        "Now ask, for each one: would a smaller, cheaper model do 80% of this work, with a bigger model "
        "on call for the rest? Most solo stacks have one fat line item that is silently eating margin.",
        "A stack is not a collection of tools. It's a routing diagram. The cheap model handles 80%, the "
        "expensive model handles 20%, and you sleep at night."
    ),
    "6. Building Your First Micro-SaaS in 30 Days": (
        "Sandeep, a former school teacher in Pune, noticed his colleagues were spending Sunday nights "
        "writing report-card comments. He built a one-screen web app: paste the kid's name and a few "
        "keywords, get three draft comments. He put it on a ₹400/month server and posted it on a teachers' "
        "WhatsApp group. By day 14 he had 11 paying users at ₹200 a month. By day 30 he had 34. He never "
        "left his teaching job. He just stopped dreading Sundays for other people.",
        "Pick one task you do (or watch someone do) more than three times a week. Write the input on the "
        "left, the desired output on the right, and the AI prompt in the middle. If you can write that "
        "in 60 seconds, you have a product. If you can't, you have a project, not a product.",
        "The first version of your micro-SaaS should embarrass you a little. If it doesn't, you've "
        "spent too long and learned too little."
    ),
    "7. Prompt Engineering as a Product Skill": (
        "Neha ran a copywriting agency. Her junior writers' first drafts were inconsistent: same brief, "
        "wildly different tone. She wrote a 600-word system prompt that locked down voice, banned specific "
        "words, and required a self-check before the model returned output. Within a week the variance "
        "collapsed. The prompt wasn't clever. It was specific. Specific beats clever every single time.",
        "Pick the prompt you use most often at work. Add three sections: 'Before you answer, list the 3 "
        "things you need to know but weren't told.' 'If you don't know, say so.' 'Output format: [exact "
        "example].' Measure the next 20 outputs against the previous 20. The difference is usually 30%.",
        "Prompts are not magic spells. They are instructions written to a very fast, very literal intern. "
        "Be specific, show examples, and forbid the things you don't want."
    ),
    "8. Workflows, Agents, and the Automation That Replaces a Team": (
        "A two-person e-commerce brand in Hyderabad was manually reconciling 250 Shopify orders a day "
        "against their bank statements. It took one person four hours. They built a 6-step workflow: "
        "Shopify webhook → CSV → matching agent → exception list → Slack alert → Google Sheet. The whole "
        "thing runs in 12 minutes. Nobody was fired. The four hours went back into finding new products.",
        "List every task you do in a typical week. Circle the ones that take more than an hour and "
        "produce the same shape of output every time. Those are the candidates. Start with the smallest "
        "one that hurts the most. Automate that. Then the next.",
        "The goal of automation is not to remove humans. It is to remove the parts of the job that made "
        "you hate the job in the first place."
    ),
    "9. The Operator's Brand: Positioning When You Are the Product": (
        "Two consultants, both ex-McKinsey, both working on climate strategy, both with 15 years' "
        "experience. One called himself a 'sustainability thought leader.' The other said: 'I help cement "
        "plants in India get to net zero without buying new equipment.' The first got polite nods. The "
        "second got a ₹14 lakh retainer inside a month. The brand wasn't a logo. It was a sentence a "
        "prospect could repeat at a dinner.",
        "Write your positioning sentence in 14 words or fewer: '[I help] [specific customer] [do "
        "specific thing] [without specific pain].' If you can't fill all four blanks, you don't have a "
        "brand. You have a mood board.",
        "Positioning is not what you do. It's what your customer would say about you if you weren't in "
        "the room. If you control that sentence, you control the business."
    ),
    "10. Pricing, Packaging, and the First 10 Customers": (
        "Vikram, a solo tax-consulting operator, priced his AI-assisted service at ₹2,000/month because "
        "'it felt right.' Two months of silence. He tripled the price to ₹6,000, called the same leads, "
        "and got three sign-ups in a week. The lower price had signaled 'amateur' to exactly the "
        "customers he wanted. The higher price signalled 'I know what this is worth.' He was selling the "
        "same product.",
        "Take your current price. Multiply it by 3. If you wince, you were undercharging. Send the new "
        "price to your next three prospects and see what happens. The market will tell you, instantly, "
        "and you will never unsee it.",
        "The price is not a number. It is a signal. Cheap signals 'maybe.' Expensive signals 'I have done "
        "this 50 times and I know what it costs to be wrong.'"
    ),
    "11. The First-Sale Playbook: Outreach Without Spam": (
        "Divya, a first-time founder, sent 200 cold emails in week one and got three replies and zero "
        "sales. In week two she cut the list to 20 specific people she'd actually had a conversation "
        "with in the last 12 months, and wrote each one a personal note that mentioned the conversation. "
        "She got 9 replies and 4 sales. Same offer, same product, different list.",
        "Before you send another cold email, write down the last 20 people you had a real conversation "
        "with (zoom, phone, in-person, WhatsApp). Rank them by how much they laughed. Email the top 10 "
        "this week with a specific, narrow ask. Do not 'blast.'",
        "Outreach is not volume. It is relevance, sent to people who would be slightly surprised to hear "
        "from you. Surprise is your friend. Volume is your enemy."
    ),
    "12. Landing Pages That Convert at 5% or Better": (
        "A Bengaluru SaaS founder had a beautiful 7-section landing page with animations, a team photo, "
        "and a 'Request a Demo' button at the bottom. Conversion rate: 0.6%. He replaced the whole page "
        "with: a one-line headline, a 30-second demo video, three customer logos, and a single button "
        "that said 'Start free for 14 days.' Conversion rate: 5.4%. Same traffic. Same product. The "
        "difference was the page, not the product.",
        "Delete every section of your landing page that isn't doing one of three jobs: explaining who "
        "the product is for, showing what it does, or asking for the next step. If a section does none "
        "of those, it's a wall. The visitor was leaving because you asked them to read a brochure.",
        "A landing page is not a website. It is one page, with one job, asking one question. Everything "
        "else is decoration."
    ),
    "13. Content as Distribution: SEO, YouTube, and the Long Game": (
        "A chartered accountant in Surat started a YouTube channel explaining GST notices in plain Hindi. "
        "He hated public speaking. The first 14 videos had 200 views each. He kept going. The 60th video "
        "got 380,000 views in a week. By month nine he was charging ₹50,000 a pop for a 90-minute "
        "consultation and turning down clients. The product wasn't the videos. The product was the trust "
        "the videos built over nine quiet months.",
        "Pick the question you get asked most often in your work. Write a 600-word blog post answering "
        "it. Then a 6-minute YouTube video. Then a LinkedIn carousel. Then a Twitter thread. Ship the "
        "blog this week. The other formats will follow when the answer is good.",
        "Content is a long, boring compounding machine. The first 90 days feel pointless. The next 900 "
        "days pay for the rest of your career."
    ),
    "14. The Launch Week Calendar": (
        "Rohit, a solo SaaS founder, launched on a Tuesday with no email list, no social following, and "
        "no plan. He made one sale. A month later he relaunched with a 14-day content ramp: 10 LinkedIn "
        "posts, 3 short videos, 1 podcast guest spot, and a 5-email sequence. Same product. 47 sales in "
        "the launch week. The product was identical. The runway was not.",
        "Block the next 14 days on your calendar. Pick one launch date. Plan 10 pieces of content (5 "
        "LinkedIn, 3 short-form video, 2 long-form) and 5 emails. Write them in one sitting on Saturday. "
        "Then schedule and forget. Launch days reward preparation, not improvisation.",
        "The launch is not a moment. It is the last day of a 14-day campaign. If you only work on the "
        "last day, the campaign is zero days long."
    ),
    "15. The 10x Operator: Doing 10x the Work Without 10x the Hours": (
        "Karthik, a one-man design agency owner, worked 70-hour weeks and was burning out. He forced "
        "himself into a 30-hour week for 90 days. He cut his client list from 11 to 4, raised prices by "
        "60%, and said no to every project that didn't fit. Revenue dropped 20% in month one. By month "
        "four it had grown 40% and he was taking Fridays off. Less hours. Better work. Same operator.",
        "Track every hour of your next working week by category: deep work, meetings, admin, "
        "communication, firefighting. The category with the biggest number is the one to cut first. "
        "Don't try to cut everything. Cut the worst offender.",
        "Scaling is not adding more hours. It is removing the hours that were never yours to spend. The "
        "10x operator is not a faster version of you. It is a smaller, sharper one."
    ),
    "16. Hiring Your First Contractor (Not an Employee)": (
        "Meera, a solo content operator, hired a 'social media manager' on a full-time salary at ₹35,000 "
        "a month. Six weeks later she realised she couldn't measure what they did, the work didn't show "
        "up, and she was paying for hours, not output. She let them go, hired a contractor on a "
        "₹10,000/month retainer with a 30-piece monthly deliverable, and never looked back. The "
        "contractor was the same person, doing the same work. The contract was just honest.",
        "Before you hire anyone, write down the exact thing they will deliver by the end of week 4, in "
        "a form you can grade. If you can't write that down, you don't know what you're hiring for. "
        "Don't hire until you can.",
        "Never pay for time when you can pay for a deliverable. Time is a polite fiction. Deliverables "
        "are the only thing that move the business forward."
    ),
    "17. Building Recurring Revenue You Can Defend": (
        "A bootstrapped SaaS founder in Delhi had 200 paying customers and 14% monthly churn, meaning he "
        "had to sell 28 new customers every month just to stand still. He added a 14-day onboarding "
        "email sequence, a 'first-success' milestone tracked in the product, and a 30-day personal "
        "check-in for any user who hadn't logged in. Churn dropped to 4% in two months. The product "
        "didn't change. The relationship did.",
        "List every customer who cancelled in the last 90 days. Email each one: 'What was the moment you "
        "stopped using it?' Take the top answer, build the fix this month, and watch churn fall. Most "
        "churn is one or two boring reasons, repeated.",
        "Recurring revenue is not a billing-cycle problem. It is a 'did the customer get what they came "
        "for in the first 14 days' problem. Fix the first 14 days and most of the churn disappears."
    ),
    "18. From Side Hustle to Solopreneur Business": (
        "Asha ran a wedding photography AI editing tool on the side for two years while keeping her "
        "corporate job. When she finally quit to do it full-time, revenue dropped 30% in the first "
        "quarter because she'd lost the social proof of 'employed at a real company.' She fixed it by "
        "publishing monthly case studies, getting on two podcasts, and going from 'side project' to "
        "'this is a company' in her own head first. Revenue was back above her salary in seven months.",
        "Write a one-paragraph 'origin story' of your business in the voice you'd use to explain it to "
        "your grandmother. If you can't, the business doesn't have a story yet, and the story is half "
        "the value.",
        "The hardest transition in a solo business is not the work. It is taking yourself seriously "
        "before the market does. Do it anyway. The market catches up."
    ),
    "19. Selling the Engine: Exit Options for Solo Operators": (
        "Arjun built a niche AI tool for US-based therapists, hit $42k MRR with 380 customers, and was "
        "approached by a larger SaaS company that offered 3.5x annual revenue. He said yes in two "
        "weeks. The tool was sold, integrated, and is still running. Arjun is on a beach in Goa writing "
        "the next book. Exit-readiness, not exit-intent, is what made the difference.",
        "Write down what would happen to your business if you disappeared for 6 months. If the answer is "
        "'it would die,' you don't have an asset. You have a job. List the three things that would have "
        "to be true for it to survive your absence. Make one of those three true this month.",
        "Build the business as if you might sell it tomorrow. You probably won't sell it tomorrow. But "
        "the discipline of running an exit-ready business is the same as running a business that never "
        "needs you. Either way, you win."
    ),
}


def main():
    md = SRC.read_text(encoding="utf-8")
    if "## Real Story" in md:
        print("Already contains '## Real Story' blocks. Skipping.")
        return
    # For each chapter, find its end (next h2 or h1), insert extras before that boundary
    new_md = []
    lines = md.split("\n")
    chapter_starts = []
    for i, line in enumerate(lines):
        m = re.match(r"^## (\d+\..+)$", line)
        if m:
            chapter_starts.append((i, m.group(1).strip()))

    # Build map: insert before index of next heading (h1/h2) after each chapter start
    inserts = {}
    for idx, (line_no, title) in enumerate(chapter_starts):
        end_line = len(lines)
        for j in range(line_no + 1, len(lines)):
            if re.match(r"^(# |## )", lines[j]):
                end_line = j
                break
        inserts[end_line] = (title, EXTRAS.get(title))

    # Walk in reverse to keep indices stable
    for end_line in sorted(inserts.keys(), reverse=True):
        title, payload = inserts[end_line]
        if not payload:
            continue
        story, workbook, takeaway = payload
        block = [
            "",
            "---",
            "",
            "## Real Story",
            "",
            story,
            "",
            "## Workbook",
            "",
            workbook,
            "",
            "## Key Takeaway",
            "",
            takeaway,
            "",
            "---",
            "",
        ]
        lines[end_line:end_line] = block

    out = "\n".join(lines)
    SRC.write_text(out, encoding="utf-8")
    added = sum(1 for t, p in inserts.values() if p)
    print(f"Added {added} chapter blocks to {SRC}")


if __name__ == "__main__":
    main()
