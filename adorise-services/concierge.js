/**
 * Adorise Mika — AI Concierge
 * Consultative, concise AI assistant for Adorise Digital.
 * Identifies visitor requirements, suggests tailored DFY packages,
 * captures lead contact (Email compulsory, Phone optional with graceful skip),
 * and provides instant Text + Voice Audio responses.
 */

(function() {
  const SERVICES = {
    content: {
      name: "AI Content Automation",
      price: "$197/mo",
      setup_waived: true,
      summary: "30-60 authority posts/mo for LinkedIn, X & Instagram with automated scheduling. Zero manual writing.",
      link: "/services/#pricing"
    },
    outreach: {
      name: "Cold Outreach Engine",
      price: "$497/mo",
      setup_waived: true,
      summary: "1,500 targeted cold emails/mo, multi-inbox rotation, AI warmup & automated reply handling.",
      link: "/services/#pricing"
    },
    hunter: {
      name: "Autonomous Lead Hunter & Outreach",
      price: "$797/mo",
      setup_waived: true,
      summary: "500 verified B2B leads from Scout + 3,000 multi-channel outreach touches/mo.",
      link: "/services/#pricing"
    },
    suite: {
      name: "Full Autonomous AI Operations Suite",
      price: "$997/mo",
      setup_waived: true,
      summary: "Complete growth fleet: 1,000 leads, 5,000 touches, 60 posts & 24/7 AI customer service agent.",
      link: "/services/#pricing"
    }
  };

  let voiceEnabled = false;
  let recognition = null;
  let isListening = false;

  let conversationState = {
    email: null,
    phone: null,
    requirement: null,
    step: "greeting"
  };

  function extractContact(text) {
    const emailMatch = text.match(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/);
    const phoneMatch = text.match(/(\+?[0-9]{1,4}?[-.\s]?\(?[0-9]{2,4}?\)?[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4})/);
    return {
      email: emailMatch ? emailMatch[1] : null,
      phone: phoneMatch ? phoneMatch[1] : null
    };
  }

  function saveLead(email, phone, requirement) {
    try {
      const leads = JSON.parse(localStorage.getItem("adorise_leads") || "[]");
      leads.push({
        email: email,
        phone: phone || "Not provided",
        requirement: requirement || "General Inquiry",
        timestamp: new Date().toISOString()
      });
      localStorage.setItem("adorise_leads", JSON.stringify(leads));
    } catch(e) {}
  }

  function speakText(text) {
    if (!voiceEnabled || !('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      const cleanText = text.replace(/[*#_`\[\]\(\)]/g, '').replace(/https?:\/\/\S+/g, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 1.05;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    } catch (e) {}
  }

  function getConsultativeResponse(userText) {
    const contact = extractContact(userText);
    const lower = userText.toLowerCase();

    // 1. If user provided an email
    if (contact.email) {
      conversationState.email = contact.email;
      if (contact.phone) conversationState.phone = contact.phone;
      saveLead(conversationState.email, conversationState.phone, conversationState.requirement);
      
      if (conversationState.requirement) {
        return "Thank you! I've noted your email (**" + conversationState.email + "**) and reserved your **$49 setup fee waiver** (code: `FOUNDERFREE`).\n\n" +
               "Based on your requirements, here is your recommended package:\n\n" +
               buildRequirementDetails(conversationState.requirement) +
               "\n\nWould you like me to connect you with an engineer, or proceed directly to checkout?";
      } else {
        return "Thank you! I've noted your email (**" + conversationState.email + "**) and reserved your **$49 setup fee waiver** (code: `FOUNDERFREE`).\n\n" +
               "To recommend the best package for you: **What is your primary business goal right now?**\n\n" +
               renderRequirementChips();
      }
    }

    // 2. Check for requirement selection
    if (lower.includes("lead") || lower.includes("prospect") || lower.includes("outreach") || lower.includes("cold email") || lower.includes("client")) {
      conversationState.requirement = "leads";
      return buildRequirementResponse("leads");
    } else if (lower.includes("content") || lower.includes("social") || lower.includes("post") || lower.includes("linkedin") || lower.includes("x") || lower.includes("twitter")) {
      conversationState.requirement = "content";
      return buildRequirementResponse("content");
    } else if (lower.includes("support") || lower.includes("chatbot") || lower.includes("ticket") || lower.includes("customer")) {
      conversationState.requirement = "support";
      return buildRequirementResponse("support");
    } else if (lower.includes("full") || lower.includes("all") || lower.includes("suite") || lower.includes("scale") || lower.includes("enterprise")) {
      conversationState.requirement = "suite";
      return buildRequirementResponse("suite");
    } else if (lower.includes("burnout") || lower.includes("calm") || lower.includes("email stress") || lower.includes("dearmee")) {
      return "For personal burnout and stressful client emails, we recommend:\n\n" +
             "• **InboxCalm**: Automated firewall that de-escalates stressful emails in 3 minutes ([inboxcalm.adorisedigital.com](https://inboxcalm.adorisedigital.com/)).\n" +
             "• **DearMee**: Empathetic AI personal companion ([dearmee.adorisedigital.com](https://dearmee.adorisedigital.com/)).\n\n" +
             askEmailClosing();
    } else if (lower.includes("setup") || lower.includes("fee") || lower.includes("discount") || lower.includes("founderfree")) {
      return "The standard setup fee is $49. Today, use coupon code **FOUNDERFREE** at checkout to get **100% Free Setup ($0 fee)** on any DFY package!\n\n" +
             "Which service are you looking to launch?\n\n" +
             renderRequirementChips();
    } else if (lower.includes("pricing") || lower.includes("price") || lower.includes("cost")) {
      return "Here are our 4 fixed-price Done-For-You packages (all include 100% Free Setup with code `FOUNDERFREE`):\n\n" +
             "1. **AI Content Automation**: $197/mo (30-60 authority posts/mo)\n" +
             "2. **Cold Outreach Engine**: $497/mo (1,500 targeted emails/mo)\n" +
             "3. **Autonomous Lead Hunter**: $797/mo (500 Scout leads + 3,000 touches)\n" +
             "4. **Full Autonomous AI Suite**: $997/mo (Complete end-to-end fleet)\n\n" +
             "Which matches your current goal?\n\n" +
             renderRequirementChips();
    }

    return "Got it! To match the exact solution for your business:\n\n" +
           "What is your #1 priority right now?\n\n" +
           renderRequirementChips() +
           "\n\n*(Feel free to drop your business email below to receive our full pricing & architecture deck)*";
  }

  function renderRequirementChips() {
    return "<div class=\"ac-chips\">" +
           "<span class=\"ac-chip\" data-q=\"Need B2B Leads & Cold Outreach\">🎯 Get B2B Leads</span>" +
           "<span class=\"ac-chip\" data-q=\"Need AI Social Media Content\">📱 Content & Social</span>" +
           "<span class=\"ac-chip\" data-q=\"Need 24/7 AI Customer Support\">🤖 24/7 Support Bot</span>" +
           "<span class=\"ac-chip\" data-q=\"Need Full Autonomous AI Suite\">⚡ Full Autonomous Fleet</span>" +
           "</div>";
  }

  function buildRequirementDetails(reqType) {
    if (reqType === "leads") {
      return "• **Cold Outreach Engine ($497/mo)** or **Autonomous Lead Hunter ($797/mo)**\n" +
             "• 500-1,500 verified B2B leads/mo with zero bounced emails.\n" +
             "• High-deliverability multi-inbox rotation landing in primary inboxes.\n" +
             "• 100% Free Setup ($0 fee) with code `FOUNDERFREE`.\n\n" +
             "👉 [View Outreach Packages](/services/#pricing)";
    } else if (reqType === "content") {
      return "• **AI Content Automation ($197/mo)**\n" +
             "• 30-60 high-impact posts/mo across LinkedIn, X & Instagram.\n" +
             "• Multi-channel AI scheduling completely replacing expensive SaaS.\n" +
             "• 100% Free Setup ($0 fee) with code `FOUNDERFREE`.\n\n" +
             "👉 [View Content Package](/services/#pricing)";
    } else if (reqType === "support") {
      return "• **Autonomous Customer Support Bot**\n" +
             "• 24/7 instant ticket resolution across web, email, and social.\n" +
             "• Escalates complex inquiries to your team automatically.\n\n" +
             "👉 [View Support Packages](/services/#pricing)";
    } else {
      return "• **Full Autonomous AI Operations Suite ($997/mo)**\n" +
             "• 1,000 verified leads + 5,000 outreach touches/mo.\n" +
             "• 60 authority social posts + 24/7 AI Customer Support.\n" +
             "• Dedicated account architect & priority execution.\n\n" +
             "👉 [View Full Suite](/services/#pricing)";
    }
  }

  function buildRequirementResponse(reqType) {
    let rec = buildRequirementDetails(reqType);
    if (!conversationState.email) {
      rec += "\n\n" + askEmailClosing();
    } else {
      rec += "\n\nReady to proceed? Use code **FOUNDERFREE** at checkout on our [Services Page](/services/#pricing), or message support at **[support@adorisedigital.com](mailto:support@adorisedigital.com)**.";
    }
    return rec;
  }

  function askEmailClosing() {
    return "💡 **Where should I send your proposal & lock in your $49 setup waiver?**\n\n" +
           "Drop your **business email** below *(phone is optional)*, or contact our team directly at **[support@adorisedigital.com](mailto:support@adorisedigital.com)**.";
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
        width: 395px;
        max-width: calc(100vw - 32px);
        height: 580px;
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
        padding: 14px 16px;
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
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: white;
        font-size: 15px;
        position: relative;
      }
      .ac-online-dot {
        position: absolute;
        bottom: -2px;
        right: -2px;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #10b981;
        border: 2px solid #090d16;
      }
      .ac-title {
        font-size: 13.5px;
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
        padding: 14px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        background: #06090f;
      }
      .ac-msg {
        max-width: 88%;
        padding: 10px 13px;
        border-radius: 14px;
        font-size: 13px;
        line-height: 1.45;
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
        font-weight: 600;
      }
      .ac-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
      }
      .ac-chip {
        background: rgba(6, 182, 212, 0.12);
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: #22d3ee;
        font-size: 11.5px;
        font-weight: 600;
        padding: 5px 10px;
        border-radius: 999px;
        cursor: pointer;
        transition: all 0.2s;
      }
      .ac-chip:hover {
        background: rgba(6, 182, 212, 0.3);
        border-color: #22d3ee;
        transform: translateY(-1px);
      }
      .ac-footer {
        padding: 12px;
        background: #090d16;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        display: flex;
        gap: 8px;
        align-items: center;
      }
      /* Highly Visible Microphone / Talk Button */
      .ac-mic-btn {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(99, 102, 241, 0.25));
        color: #22d3ee;
        border: 1.5px solid rgba(6, 182, 212, 0.6);
        height: 38px;
        padding: 0 12px;
        border-radius: 12px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 700;
        font-family: inherit;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.25);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        white-space: nowrap;
        flex-shrink: 0;
      }
      .ac-mic-btn:hover {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.45), rgba(99, 102, 241, 0.45));
        border-color: #38bdf8;
        color: #ffffff;
        box-shadow: 0 0 18px rgba(6, 182, 212, 0.5);
        transform: translateY(-1px);
      }
      .ac-mic-btn.listening {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: #ffffff;
        border-color: #fca5a5;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.7);
        animation: acPulse 1s infinite;
      }
      .ac-mic-svg {
        display: inline-block;
        vertical-align: middle;
      }
      .ac-input {
        flex: 1;
        background: #111827;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #f8fafc;
        padding: 9px 12px;
        border-radius: 12px;
        font-size: 12.5px;
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
      @keyframes acPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.06); }
        100% { transform: scale(1); }
      }
    `;
    document.head.appendChild(style);

    const btn = document.createElement('div');
    btn.id = 'adorise-concierge-btn';
    btn.innerHTML = `
      <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;"></span>
      <span>Adorise Mika</span>
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
            <div class="ac-title">Adorise Mika — AI Concierge</div>
            <div class="ac-subtitle">Consultative AI Architect • 24/7 Live</div>
          </div>
        </div>
        <div class="ac-header-actions">
          <button class="ac-icon-btn" id="ac-voice-toggle" title="Toggle Voice (Text-to-Speech)">🔊</button>
          <button class="ac-icon-btn" id="ac-close-btn" title="Close Chat">✕</button>
        </div>
      </div>
      <div class="ac-body" id="ac-messages">
        <div class="ac-msg ac-msg-bot">
          👋 Hi, I'm <strong>Adorise Mika</strong>.<br><br>
          What is your primary business or operational requirement right now?<br>
          <div class="ac-chips">
            <span class="ac-chip" data-q="Need B2B Leads & Cold Outreach">🎯 B2B Leads & Outreach</span>
            <span class="ac-chip" data-q="Need AI Social Media Content">📱 Social Media & Content</span>
            <span class="ac-chip" data-q="Need 24/7 AI Customer Support">🤖 Customer Support Bot</span>
            <span class="ac-chip" data-q="Need Full Autonomous AI Suite">⚡ Full Autonomous Fleet</span>
          </div>
        </div>
      </div>
      <div class="ac-footer">
        <button class="ac-mic-btn" id="ac-mic-btn" title="Click to speak with Adorise Mika">
          <svg class="ac-mic-svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
          <span class="ac-mic-text">Talk</span>
        </button>
        <input type="text" class="ac-input" id="ac-input" placeholder="Type requirement or enter email...">
        <button class="ac-send-btn" id="ac-send-btn" title="Send message">➤</button>
      </div>
    `;
    document.body.appendChild(modal);

    const msgContainer = document.getElementById('ac-messages');
    const inputEl = document.getElementById('ac-input');
    const sendBtn = document.getElementById('ac-send-btn');
    const micBtn = document.getElementById('ac-mic-btn');
    const micText = micBtn.querySelector('.ac-mic-text');
    const voiceToggle = document.getElementById('ac-voice-toggle');
    const closeBtn = document.getElementById('ac-close-btn');

    btn.addEventListener('click', () => {
      modal.classList.toggle('active');
      if (modal.classList.contains('active')) inputEl.focus();
    });

    closeBtn.addEventListener('click', () => modal.classList.remove('active'));

    voiceToggle.addEventListener('click', () => {
      voiceEnabled = !voiceEnabled;
      voiceToggle.classList.toggle('active', voiceEnabled);
      if (voiceEnabled) {
        speakText("Voice mode on. I am ready to speak with you.");
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
        const reply = getConsultativeResponse(text);
        addMessage(reply, false);
        speakText(reply);
      }, 300);
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
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        isListening = true;
        micBtn.classList.add('listening');
        if (micText) micText.textContent = "Listening...";
      };
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        handleUserInput(transcript);
      };
      recognition.onerror = () => {
        isListening = false;
        micBtn.classList.remove('listening');
        if (micText) micText.textContent = "Talk";
      };
      recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('listening');
        if (micText) micText.textContent = "Talk";
      };

      micBtn.addEventListener('click', () => {
        if (!isListening) {
          try { recognition.start(); } catch(e) {}
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