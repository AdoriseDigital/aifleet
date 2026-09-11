# Hermes ComfyUI + Kaggle Video Generation Pipeline
**Adorise Digital — Autonomous Social Media Production Engine**

---

## 1. Overview & Objective
This pipeline enables **Hermes** to generate high-converting, viral **9:16 vertical video shorts** (for TikTok, YouTube Shorts, Instagram Reels, and X) using **ComfyUI headless rendering on Kaggle's free GPU infrastructure (NVIDIA Tesla T4 x2 / 30 hours free compute per week)**.

By leveraging Kaggle's cloud GPUs rather than straining local VPS CPU resources, Adorise Digital achieves **zero-cost video production** for social authority building and client acquisition.

---

## 2. Infrastructure & Connected Integrations

| Component | Provider / Tool | Composio Account ID | Operational Role |
| :--- | :--- | :--- | :--- |
| **Cloud GPU Compute** | **Kaggle API** | `ca_8QkxxxK8S0Zc` | Headless execution of ComfyUI / Diffusers video models on dual Tesla T4 GPUs. |
| **Short-Form Distribution (X & TikTok)** | **Buffer.com** | Direct OAuth | Queued dispatch of rendered vertical shorts and carousel posts. |
| **Short-Form Distribution (Meta)** | **Facebook Pages** | `ca_MgB81OXe5Y61` | Direct upload of video reels to Adorise Digital brand page. |
| **Long-Form & Shorts Distribution** | **YouTube** | `ca_0yenexSvzmMY` | Direct upload of vertical shorts with SEO-optimized tags and descriptions. |
| **Local Pipeline Controller** | [`K_kaggle_comfy_video.py`](file:///C:/Users/HOME_PC/Documents/antigravity/calm-carson/Adorise%20Digital/00-SPECS/K_revenue_system/K_kaggle_comfy_video.py) | Internal | Orchestrates job dispatch, status monitoring, and output download. |

---

## 3. End-to-End Operational Workflow for Hermes

```
[1. Hermes / Gemini Scripting]
       │
       ▼ (Generates 15-30s hook script, camera motion, and visual prompts)
[2. Kaggle Kernel Dispatch via Composio]
       │
       ▼ (Dual NVIDIA T4 GPU boots headless ComfyUI / Diffusers pipeline)
[3. GPU Video Rendering & FFmpeg Stitching]
       │
       ▼ (Compiles 1080x1920 9:16 MP4 with dynamic audio & captions)
[4. Output Download via Kaggle API]
       │
       ▼ (Pulls finished MP4 from /kaggle/working/)
[5. Multi-Platform Social Syndication]
       ├── Buffer: Scheduled to TikTok & X (Twitter)
       ├── Composio: Pushed to Facebook Page Reels
       └── Composio: Uploaded to YouTube Shorts
```

---

## 4. Video Formats & Campaign Themes
1. **InboxCalm De-Escalator Shorts**:
   * Visual: Chaotic red-tinted inbox dissolving into calm emerald envelopes.
   * Hook: *"Never reply to an angry client email while triggered. Forward it to calm@ai.goadorisedigital.com instead."*
2. **ClipCalm Repurposing Shorts**:
   * Visual: Long YouTube podcast splitting into 3 dynamic captioned vertical shorts.
   * Hook: *"Stop paying $1,000/mo to video editors. Turn any long video into 10 viral clips on autopilot."*
3. **DearMee Founder Mental Health Shorts**:
   * Visual: Late-night founder laptop glow transitioning to soothing voice co-pilot orb.
   * Hook: *"Founder loneliness is real. Here is how top CEOs decompress without burning out."*
4. **Autonomous AI Operations**:
   * Visual: Multi-agent flowcharts routing leads, support tickets, and content without human intervention.
   * Hook: *"How we scaled our agency using autonomous AI agents."*

---

## 5. Verification & Health Check
Run the automated pipeline health check at any time:
```powershell
python "C:\Users\HOME_PC\Documents\antigravity\calm-carson\Adorise Digital\00-SPECS\K_revenue_system\K_kaggle_comfy_video.py"
```
**Current Status:**
* `Kaggle status: {'connected': True, 'active_accounts': 1, 'account_ids': ['ca_8QkxxxK8S0Zc']}`
* **Pipeline:** Verified, connected, and ready for Hermes execution.
