# Publish & Launch Checklist — The Solo AI Income Engine

**Manuscript:** `book-project/manuscript.md` (1,609 lines, ~60,000 words, 23 chapters + appendices)
**Build script:** `book-project/build_book.py`
**Deliverables in `book-project/outputs/`:**

| File | Size | Purpose |
|---|---|---|
| `cover.jpg` | 1800×2700 px (300 dpi, 6×9 in) | Print cover, also used as EPUB cover |
| `The-Solo-AI-Income-Engine.pdf` | 77 pages, 6×9 in | Print-ready interior (use as KDP paperback source) |
| `The-Solo-AI-Income-Engine.epub` | reflowable, 20 chapters | Kindle, Apple Books, Google Play Books, Kobo, Gumroad |

To rebuild after edits: `python book-project/build_book.py`

---

## 1. Editing pass (1–2 days)

- [ ] Read straight through once; flag awkward transitions, redundancies, and "AI-tells" (overused words: *delve, leverage, navigate, in today's world, it's important to note, in conclusion, furthermore, robust, seamless, unleash*).
- [ ] Verify all numbers, tool names, and prices are current. Replace anything older than 6 months with 2026 references or a "as of writing" hedge.
- [ ] Tighten Chapter 1 ("Death of the Resume") — it's the make-or-break first impression.
- [ ] Add a "Resources" page in Appendix D with real links (use `pseo_pages/` for SEO content that can cross-link to the book).
- [ ] Add 3–5 reader-facing worksheets in Appendix C if the prose-only format feels thin.
- [ ] Run a grammar pass with a different tool (Grammarly / Hemingway) to catch what the author missed.

**Comp titles / low-competition check (run before publish):**
- Search KDP for "AI side hustle", "solopreneur AI", "micro SaaS", "ChatGPT business", "passive income AI".
- Confirm that the most-similar books have <50 reviews each. If a giant dominates the niche, narrow the angle (e.g., *AI side hustles for coaches*, *AI side hustles for real estate agents*).

---

## 2. Cover (already generated, lightly review)

- [ ] Open `outputs/cover.jpg`. Confirm the title is readable at thumbnail size (Amazon displays 200 px wide).
- [ ] No text clipped at edges. No typos. Author name matches the copyright page.
- [ ] If you want a different vibe, edit `build_cover()` in `build_book.py` and re-run. The script writes a fresh cover every build.

**For KDP paperback only:** the print cover must be the full *wrap-around* (back + spine + front) at 6.125 × 9.25 in with 0.125 in bleed, plus a separate spine width based on page count. The current `cover.jpg` is **front cover only** and is correct for the EPUB. Use KDP's free Cover Creator or download their template and re-layout the spine/back.

---

## 3. Manuscript metadata (update in `manuscript.md` front-matter)

```yaml
title: "The Solo AI Income Engine"
subtitle: "How One Operator Can Build, Launch, and Scale Profitable AI Side Hustles Without a Team, Funding, or a Burnout Schedule"
author: "A. Operator"
publisher: "Solo Operator Press"
isbn: "TBD"           # ← replace after KDP/Bowker assigns one
edition: "First Edition, 2026"
keywords: ["AI side hustle", "solopreneur", "passive income", "AI automation", "micro SaaS", "Make money with AI", "ChatGPT business", "AI wealth"]
```

---

## 4. Publishing channels

### A. Amazon KDP (free ISBN, biggest reach)

1. kdp.amazon.com → Bookshelf → **+ Create** → Paperback.
2. Upload `The-Solo-AI-Income-Engine.pdf`. Trim: 6 × 9 in. Bleed: No (use the non-bleed template to match this PDF).
3. Upload **full wrap cover** (rebuild from `cover.jpg` using KDP Cover Creator or Canva's 6×9 KDP template).
4. Category: Business & Money > Entrepreneurship & Small Business > New Business Enterprises.
5. Keywords (use all 7 slots): AI side hustle, solopreneur, ChatGPT business, passive income AI, micro SaaS, one-person business, AI wealth.
6. Price paperback: **$14.99–$17.99**. Royalty: 60%.
7. Then create the Kindle eBook version: upload the `.epub` (or `.mobi` if KDP complains — re-export with Calibre).

### B. Gumroad / Lemon Squeezy (direct-to-reader, keep 95%+)

- Price the EPUB + a "bonus bundle" (worksheets, prompt library) at **$19–$29**.
- Use Lemon Squeezy or Gumroad; both handle EU VAT automatically.
- Write a long-form sales page using Chapter 1 as the lead.

### C. Apple Books, Google Play Books, Kobo, Barnes & Noble

- Use **Draft2Digital** (draft2digital.com) — free, distributes to all four, takes 10% of royalties.
- Upload the `.epub` once. They auto-generate store listings.

### D. Free ISBN (optional, only if you want to go wide)

- Bowker (US): $125 for one ISBN, $295 for 10. Skip if you only need KDP — KDP gives a free ASIN/ISBN.

---

## 5. Launch week plan (low-cost, high-signal)

**Day 0 (pre-launch)**
- [ ] Email list: "I'm launching a book Tuesday — here's the cover."
- [ ] Set up Gumroad/Lemon Squeezy pre-order with 30% off for first 48 hours.

**Day 1 (Tuesday — best launch-day for B2C)**
- [ ] Go live on all channels at 7 a.m. PT.
- [ ] Post on X, LinkedIn, Reddit (r/sidehustle, r/ChatGPT, r/solopreneur), Indie Hackers, Hacker News (Show HN if it has a build-with-AI angle).
- [ ] Email full list.

**Day 2**
- [ ] DM 20 people who have built AI tools and ask for an honest review on Amazon in exchange for a free copy.
- [ ] Cross-post to niche communities (operator-focused Discords, "build in public" Slacks).

**Day 3–7**
- [ ] One long-form LinkedIn post pulling a chapter excerpt.
- [ ] One short YouTube video (5 min) titled "How I wrote a book in 30 days with AI".
- [ ] Reach out to 5 AI-niche newsletters (The Rundown AI, Ben's Bites, TLDR AI) for a feature.

---

## 6. Evergreen content loop (months 1–6)

- [ ] Turn each chapter into a YouTube short / LinkedIn carousel → link back to the book.
- [ ] Repurpose the book as a free Substack / Beehiiv newsletter (one chapter per week) with a paid tier that includes the bundle.
- [ ] Use the `pseo_pages/` content already in this repo as SEO bait — interlink blog posts with the book.
- [ ] Quarterly: update chapters with new tool names and price points; re-publish a "2027 edition" for renewed Amazon ranking.

---

## 7. Royalty targets (solo, low-competition, high-demand niche)

Conservative 12-month projection for a clean niche book:

| Channel | Copies/mo | Royalty/copy | Monthly |
|---|---|---|---|
| KDP ebook | 80 | $5 | $400 |
| KDP paperback | 30 | $4 | $120 |
| Gumroad bundle | 25 | $22 | $550 |
| D2D (Apple/Kobo/Nook) | 40 | $4 | $160 |
| **Total** | **175** | | **≈ $1,230 / mo** |

Push past $5k/mo by:
1. Getting 1 newsletter feature (Brian Fanzo, The AI Solopreneur, etc.).
2. Building a free tool (Chapter 5–6 template) that requires the book to use.
3. Bundling with a paid course at $99–$199.

---

## 8. Pre-flight QA (do this 24 hours before publish)

- [ ] Open the PDF in Acrobat and check page 1, 30, 60, and the last page.
- [ ] Open the EPUB in Kindle Previewer, Apple Books, and Calibre. Confirm TOC works on all three.
- [ ] Confirm the cover is attached (open the EPUB, look at the cover thumbnail).
- [ ] Check the manuscript front-matter in both formats: title page, copyright, TOC.
- [ ] Spell-check the subtitle on the cover. (Subtitles are where typos live forever.)
- [ ] Confirm the author name on cover = copyright page = KDP listing = Gumroad listing.

---

## 9. After publish

- [ ] Set up a `book-orders@yourdomain` inbox to handle reader emails. Answer every one — those become the next book's case studies.
- [ ] Add the book to your LinkedIn "Featured" section.
- [ ] Update your Twitter/X bio with "Author of The Solo AI Income Engine."
- [ ] Pitch 10 podcasts in the AI / solopreneur niche. (Pitch format: "I wrote a book on X; here are 3 counterintuitive findings the book is built around.")
