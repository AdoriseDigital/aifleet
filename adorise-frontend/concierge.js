/**
 * Adorise Digital - Autonomous AI Concierge (Mika)
 * Real-time Text + Voice Audio Interactive Agent
 * Handles Service Inquiries, Pricing, Setup Fee Waivers, App Navigation, and Support Routing
 */

(function() {
  const KB = [
    {
      keywords: ['service', 'package', 'offer', 'pricing', 'cost', 'plan', 'dfy', 'done for you', 'hire', 'buy'],
      response: "We offer 4 Done-For-You Autonomous AI Growth Packages:\n\n" +
        "1. **AI Content Automation ($197/mo)**: 30-60 authority posts/mo across X, LinkedIn & Instagram + automated scheduling.\n" +
        "2. **Cold Outreach Engine ($497/mo)**: 1,500 targeted cold emails/mo, multi-inbox rotation, automated warmups & reply handling.\n" +
        "3. **Autonomous Lead Hunter & Outreach ($797/mo)**: 500 qualified B2B leads from Scout + 3,000 multi-channel outreach touches/mo.\n" +
        "4. **Full Autonomous AI Operations Suite ($997/mo)**: Complete end-to-end growth fleet (1,000 leads, 5,000 touches, 60 posts, 24/7 AI support agent).\n\n" +
        "Explore all packages & checkout directly at [services.adorisedigital.com](https://services.adorisedigital.com/)."
    },
    {
      keywords: ['setup fee', 'setup', '49', 'coupon', 'discount', 'founderfree', 'waive', 'free setup', 'code'],
      response: "Standard setup is $49 for our 7-day white-glove onboarding. However, for our Today Only Flash Launch, use coupon code **FOUNDERFREE** at checkout to get **100% FREE SETUP ($0 setup fee)**! This is reserved for the first 5 founding clients."
    },
    {
      keywords: ['scout', 'leads', 'lead gen', 'radar', 'prospecting'],
      response: "Adorise Scout is our Autonomous Programmatic Customer Hunter. It tracks high-intent leads across social channels and Google, extracts verified contacts, and drafts custom pitches. Access it at [scout.adorisedigital.com](https://scout.adorisedigital.com/)."
    },
    {
      keywords: ['outreach', 'cold email', 'email', 'instantly', 'inbox'],
      response: "Adorise Outreach is our high-deliverability cold email infrastructure with multi-mailbox rotation and automated AI warmup, guaranteeing your pitches land in the primary inbox. Explore it at [outreach.adorisedigital.com](https://outreach.adorisedigital.com/)."
    },
    {
      keywords: ['social', 'postiz', 'schedule', 'blotato', 'content', 'linkedin', 'twitter', 'x'],
      response: "Adorise Social is our AI Content Studio & Scheduler. Post seamlessly to 25+ platforms including LinkedIn, X, Instagram, TikTok, and YouTube with automated video and copy generation. Launch it at [social.adorisedigital.com](https://social.adorisedigital.com/)."
    },
    {
      keywords: ['dearmee', 'journal', 'mental', 'stress', 'companion', 'emotional'],
      response: "DearMee is an empathetic personal companion and subconscious reflection engine. It helps you process burnout, track emotional clarity, and gain peace of mind. Visit [dearmee.adorisedigital.com](https://dearmee.adorisedigital.com/)."
    },
    {
      keywords: ['clipcalm', 'video', 'shorts', 'reels', 'tiktok', 'clip'],
      response: "ClipCalm AI is our automated video cutter that extracts high-engagement hooks from long-form content, crops to 9:16 vertical, and generates viral short-form clips. Check it out at [clipcalm.adorisedigital.com](https://clipcalm.adorisedigital.com/)."
    },
    {
      keywords: ['inboxcalm', 'calm', 'firewall', 'toxic email', 'email stress'],
      response: "InboxCalm acts as an automated firewall for stressful emails. Simply forward difficult client emails, and our AI drafts calm, de-escalating, professional responses in minutes. Available at [inboxcalm.adorisedigital.com](https://inboxcalm.adorisedigital.com/)."
    },
    {
      keywords: ['book', '13', 'reading', 'ebook', 'library'],
      response: "Our 13-Book Transformation Collection covers Health, Wealth, Relationships, and Spirituality. Grounded in actionable wisdom and AI leverage. Discover the books at [books.adorisedigital.com](https://books.adorisedigital.com/)."
    },
    {
      keywords: ['contact', 'support', 'help', 'human', 'talk', 'email', 'telegram', 'reach', 'question'],
      response: "You can reach our team directly anytime:\n\n" +
        "• **Official Support Email**: [support@adorisedigital.com](mailto:support@adorisedigital.com) (Average response under 4 hours)\n" +
        "• **24/7 Telegram Concierge**: [@AdoriseSupportBot](https://t.me/AdoriseSupportBot)\n\n" +
        "We are here to assist with onboarding, custom enterprise workflows, and technical support."
    },
    {
      keywords: ['about', 'who are you', 'what is adorise', 'company', 'founder'],
      response: "Adorise Digital builds Level 4 Autonomous AI infrastructure and Done-For-You operational fleets. We eliminate friction across Health, Wealth, Relationships, and Spirituality, giving businesses and founders their time, revenue, and peace of mind back."
    }
  ];

  const defaultResponse = "Thanks for your question! As your AI Concierge, I can assist you with our **Done-For-You AI Packages** ($197 - $997/mo), our **$49 setup fee waiver** (code: `FOUNDERFREE`), or our autonomous apps (Scout, Outreach, Social, DearMee, ClipCalm, InboxCalm).\n\nFor custom enterprise inquiries or human assistance, feel free to email **support@adorisedigital.com** or chat on Telegram at **@AdoriseSupportBot**.";

  let voiceEnabled = false;
  let recognition = null;
  let isListening = false;

  function speakText(text) {
    if (!voiceEnabled || !('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      const cleanText = text.replace(/[*#_`\[\]\(\)]/g, '').replace(/https?:\/\/\S+/g, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 1.05;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn("Speech synthesis error:", e);
    }
  }

  function getAnswer(input) {
    const lower = input.toLowerCase();
    for (let entry of KB) {
      if (entry.keywords.some(k => lower.includes(k))) {
        return entry.response;
      }
    }
    return defaultResponse;
  }

  function initWidget() {
    const style = document.createElement('style');
    style.textContent = `
      #adorise-concierge-btn {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, #06b6d4, #6366f1);
        color: #fff;
        padding: 12px 20px;
        border-radius: 9999px;
        box-shadow: 0 10px 25px -5px rgba(6, 182, 212, 0.4), 0 8px 10px -6px rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        cursor: pointer;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        font-size: 14px;
        font-weight: 700;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      }
      #adorise-concierge-btn:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 15px 30px -5px rgba(6, 182, 212, 0.6);
      }
      #adorise-concierge-modal {
        position: fixed;
        bottom: 90px;
        right: 24px;
        width: 380px;
        max-width: calc(100vw - 32px);
        height: 560px;
        max-height: calc(100vh - 120px);
        background: #090d16;
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 30px rgba(6, 182, 212, 0.15);
        z-index: 9999;
        display: none;
        flex-direction: column;
        overflow: hidden;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        backdrop-filter: blur(16px);
      }
      #adorise-concierge-modal.active {
        display: flex;
        animation: acFadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      }
      @keyframes acFadeIn {
        from { opacity: 0; transform: translateY(15px) scale(0.96); }
        to { opacity: 1; transform: translateY(0) scale(1); }
      }
      .ac-header {
        padding: 16px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(9, 13, 22, 0.95));
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      .ac-header-info {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .ac-avatar {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: white;
        font-size: 16px;
        position: relative;
      }
      .ac-online-dot {
        position: absolute;
        bottom: -2px;
        right: -2px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10b981;
        border: 2px solid #090d16;
      }
      .ac-title {
        font-size: 14px;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1.2;
      }
      .ac-subtitle {
        font-size: 11px;
        color: #94a3b8;
      }
      .ac-header-actions {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .ac-icon-btn {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #cbd5e1;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        transition: all 0.2s;
      }
      .ac-icon-btn:hover {
        background: rgba(255, 255, 255, 0.15);
        color: #fff;
      }
      .ac-icon-btn.active {
        background: #06b6d4;
        color: #030712;
        border-color: #06b6d4;
      }
      .ac-body {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        background: #06090f;
      }
      .ac-msg {
        max-width: 85%;
        padding: 10px 14px;
        border-radius: 14px;
        font-size: 13px;
        line-height: 1.5;
        word-break: break-word;
      }
      .ac-msg-bot {
        align-self: flex-start;
        background: #111827;
        border: 1px solid rgba(148, 163, 184, 0.15);
        color: #e2e8f0;
        border-top-left-radius: 4px;
      }
      .ac-msg-user {
        align-self: flex-end;
        background: linear-gradient(135deg, #0284c7, #4f46e5);
        color: #ffffff;
        border-top-right-radius: 4px;
      }
      .ac-msg a {
        color: #38bdf8;
        text-decoration: underline;
      }
      .ac-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
      }
      .ac-chip {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.25);
        color: #22d3ee;
        font-size: 11px;
        font-weight: 600;
        padding: 5px 10px;
        border-radius: 999px;
        cursor: pointer;
        transition: all 0.2s;
      }
      .ac-chip:hover {
        background: rgba(6, 182, 212, 0.25);
        border-color: #22d3ee;
      }
      .ac-footer {
        padding: 12px;
        background: #090d16;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        display: flex;
        gap: 8px;
        align-items: center;
      }
      .ac-input {
        flex: 1;
        background: #111827;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #f8fafc;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 13px;
        outline: none;
      }
      .ac-input:focus {
        border-color: #06b6d4;
      }
      .ac-send-btn {
        background: #06b6d4;
        color: #040812;
        border: none;
        width: 36px;
        height: 36px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
      }
      .ac-send-btn:hover {
        background: #22d3ee;
      }
      .ac-mic-btn {
        background: #1e293b;
        color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.2);
        width: 36px;
        height: 36px;
        border-radius: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        transition: all 0.2s;
      }
      .ac-mic-btn.listening {
        background: #ef4444;
        color: white;
        animation: acPulse 1s infinite;
      }
      @keyframes acPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.08); }
        100% { transform: scale(1); }
      }
    `;
    document.head.appendChild(style);

    const btn = document.createElement('div');
    btn.id = 'adorise-concierge-btn';
    btn.innerHTML = `
      <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;"></span>
      <span>AI Concierge</span>
      <span style="background:rgba(0,0,0,0.25);padding:2px 8px;border-radius:8px;font-size:11px;">Voice + Text</span>
    `;
    document.body.appendChild(btn);

    const modal = document.createElement('div');
    modal.id = 'adorise-concierge-modal';
    modal.innerHTML = `
      <div class="ac-header">
        <div class="ac-header-info">
          <div class="ac-avatar">
            M
            <span class="ac-online-dot"></span>
          </div>
          <div>
            <div class="ac-title">Mika — AI Concierge</div>
            <div class="ac-subtitle">Online • 24/7 Sales & Support</div>
          </div>
        </div>
        <div class="ac-header-actions">
          <button class="ac-icon-btn" id="ac-voice-toggle" title="Toggle Voice Response (Text-to-Speech)">🔊</button>
          <a href="https://t.me/AdoriseSupportBot" target="_blank" rel="noopener" class="ac-icon-btn" title="Open Telegram Support">✈️</a>
          <button class="ac-icon-btn" id="ac-close-btn" title="Close Chat">✕</button>
        </div>
      </div>
      <div class="ac-body" id="ac-messages">
        <div class="ac-msg ac-msg-bot">
          👋 Welcome to <strong>Adorise Digital</strong>! I'm Mika, your Autonomous AI Concierge.<br><br>
          I can guide you through our Done-For-You AI Growth packages, help you claim our <strong>$49 setup fee waiver</strong> (code: <code>FOUNDERFREE</code>), or connect you with human support.<br><br>
          <em>Tap a topic below or speak directly:</em>
          <div class="ac-chips">
            <span class="ac-chip" data-q="What services do you offer?">🔥 DFY Packages</span>
            <span class="ac-chip" data-q="How do I get free setup?">🎁 Free $49 Setup</span>
            <span class="ac-chip" data-q="Tell me about Adorise Scout">🎯 Scout Leads</span>
            <span class="ac-chip" data-q="How can I contact support?">📞 Contact Support</span>
          </div>
        </div>
      </div>
      <div class="ac-footer">
        <button class="ac-mic-btn" id="ac-mic-btn" title="Hold/Click to speak">🎙️</button>
        <input type="text" class="ac-input" id="ac-input" placeholder="Ask anything (e.g. pricing, setup fee)...">
        <button class="ac-send-btn" id="ac-send-btn">➤</button>
      </div>
    `;
    document.body.appendChild(modal);

    const msgContainer = document.getElementById('ac-messages');
    const inputEl = document.getElementById('ac-input');
    const sendBtn = document.getElementById('ac-send-btn');
    const micBtn = document.getElementById('ac-mic-btn');
    const voiceToggle = document.getElementById('ac-voice-toggle');
    const closeBtn = document.getElementById('ac-close-btn');

    btn.addEventListener('click', () => {
      modal.classList.toggle('active');
      if (modal.classList.contains('active')) {
        inputEl.focus();
      }
    });

    closeBtn.addEventListener('click', () => {
      modal.classList.remove('active');
    });

    voiceToggle.addEventListener('click', () => {
      voiceEnabled = !voiceEnabled;
      voiceToggle.classList.toggle('active', voiceEnabled);
      if (voiceEnabled) {
        speakText("Voice mode enabled. I will read answers aloud to you.");
      } else {
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      }
    });

    function formatMarkdown(text) {
      return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code style="background:rgba(255,255,255,0.1);padding:2px 6px;border-radius:4px;">$1</code>')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
        .replace(/\n/g, '<br>');
    }

    function addMessage(text, isUser = false) {
      const msgDiv = document.createElement('div');
      msgDiv.className = `ac-msg ${isUser ? 'ac-msg-user' : 'ac-msg-bot'}`;
      msgDiv.innerHTML = isUser ? text : formatMarkdown(text);
      msgContainer.appendChild(msgDiv);
      msgContainer.scrollTop = msgContainer.scrollHeight;
    }

    function handleUserInput(text) {
      if (!text || !text.trim()) return;
      addMessage(text, true);
      inputEl.value = '';

      setTimeout(() => {
        const reply = getAnswer(text);
        addMessage(reply, false);
        speakText(reply);
      }, 350);
    }

    sendBtn.addEventListener('click', () => handleUserInput(inputEl.value));
    inputEl.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleUserInput(inputEl.value);
    });

    msgContainer.addEventListener('click', (e) => {
      if (e.target.classList.contains('ac-chip')) {
        const query = e.target.getAttribute('data-q');
        handleUserInput(query);
      }
    });

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        isListening = true;
        micBtn.classList.add('listening');
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        handleUserInput(transcript);
      };

      recognition.onerror = () => {
        isListening = false;
        micBtn.classList.remove('listening');
      };

      recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('listening');
      };

      micBtn.addEventListener('click', () => {
        if (!isListening) {
          try {
            recognition.start();
          } catch (e) {
            console.warn(e);
          }
        } else {
          recognition.stop();
        }
      });
    } else {
      micBtn.style.display = 'none';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWidget);
  } else {
    initWidget();
  }
})();