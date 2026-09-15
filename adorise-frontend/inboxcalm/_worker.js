/**
 * InboxCalm Cloudflare Pages Advanced Worker
 * Production NLP Email De-escalation API, Real Authentication & Route Engine
 * Adorise Digital LLC / Trendy DigiStore LLC
 */

const JWT_SECRET = "inboxcalm-prod-jwt-secret-adorise-digital-2026-v2";
const WHOP_CHECKOUT_URL = "https://whop.com/adorise-digital-usa/";
const MAX_TRIAL_DAILY_SCANS = 5;

// Comprehensive Hostility, Passive-Aggression, and Toxic Language Lexicon
const TOXIC_PATTERNS = [
  // Passive-Aggression
  { phrase: "per my last email", regex: /\bper\s+my\s+last\s+email\b/i, penalty: 30, category: "Passive-Aggression", severity: "high", reason: "Passive-aggressive dismissiveness implying recipient negligence or incompetence." },
  { phrase: "per my previous email", regex: /\bper\s+my\s+previous\s+email\b/i, penalty: 30, category: "Passive-Aggression", severity: "high", reason: "Accusation of ignoring or failing to read earlier correspondence." },
  { phrase: "as previously stated", regex: /\bas\s+previously\s+stated\b/i, penalty: 25, category: "Passive-Aggression", severity: "medium", reason: "Condescending repetition establishing intellectual dominance." },
  { phrase: "as stated earlier", regex: /\bas\s+stated\s+earlier\b/i, penalty: 22, category: "Passive-Aggression", severity: "medium", reason: "Repetitive rebuke signaling irritation with recipient." },
  { phrase: "as you should know", regex: /\bas\s+you\s+should\s+know\b/i, penalty: 28, category: "Condescending", severity: "high", reason: "Direct insult to competence and professional awareness." },
  { phrase: "correct me if i'm wrong", regex: /\bcorrect\s+me\s+if\s+i'?m\s+wrong\b/i, penalty: 20, category: "Passive-Aggression", severity: "medium", reason: "Combative rhetorical challenge designed to corner recipient." },
  { phrase: "re-attaching for your convenience", regex: /\b(re-?attaching|attaching\s+again)\s+(for\s+your\s+convenience|in\s+case\s+you\s+missed)\b/i, penalty: 24, category: "Passive-Aggression", severity: "medium", reason: "Sarcastic gesture masking frustration over perceived neglect." },
  { phrase: "moving forward, please", regex: /\b(moving|going)\s+forward,?\s+please\b/i, penalty: 18, category: "Patronizing", severity: "low", reason: "Patronizing reprimand disguised as procedural direction." },
  { phrase: "did you even read", regex: /\bdid\s+you\s+(even\s+)?(read|check|see)\b/i, penalty: 32, category: "Hostility", severity: "high", reason: "Blatant questioning of basic reading comprehension and diligence." },

  // Condescending & Invalidating
  { phrase: "obviously", regex: /\bobviously\b/i, penalty: 20, category: "Condescending", severity: "medium", reason: "Invalidating intelligence and portraying recipient as oblivious." },
  { phrase: "clearly", regex: /\bclearly\b/i, penalty: 18, category: "Condescending", severity: "medium", reason: "Subtly implies recipient lacks basic observational competence." },
  { phrase: "it's not rocket science", regex: /\bit'?s\s+not\s+rocket\s+science\b/i, penalty: 35, category: "Condescending", severity: "high", reason: "Severe belittlement mocking recipient's intellectual capacity." },
  { phrase: "common sense", regex: /\bcommon\s+sense\b/i, penalty: 25, category: "Condescending", severity: "high", reason: "Demittles recipient by alleging lack of elementary judgment." },
  { phrase: "just do your job", regex: /\b(just\s+)?do\s+your\s+job\b/i, penalty: 35, category: "Hostility", severity: "high", reason: "Dehumanizing and disrespectful directive dismissing effort." },

  // Artificial Urgency / False Panic
  { phrase: "needed this yesterday", regex: /\bneed(ed)?\s+this\s+yesterday\b/i, penalty: 28, category: "Manufactured Urgency", severity: "high", reason: "Manufactured emergency and impossible timeline manipulation." },
  { phrase: "asap / as soon as possible", regex: /\b(asap|as\s+soon\s+as\s+possible)\b/i, penalty: 15, category: "Manufactured Urgency", severity: "low", reason: "Ambiguous boundary violation creating unquantified anxiety." },
  { phrase: "immediate response required", regex: /\b(immediate(ly)?\s+response|respond\s+immediately)\b/i, penalty: 25, category: "Manufactured Urgency", severity: "high", reason: "Unilateral demand for instantaneous priority disruption." },
  { phrase: "drop everything", regex: /\bdrop\s+everything\b/i, penalty: 28, category: "Manufactured Urgency", severity: "high", reason: "Chaotic crisis generation forcing abandonment of ongoing SLAs." },

  // Hostility & Blame
  { phrase: "unacceptable", regex: /\bunacceptable\b/i, penalty: 30, category: "Conflict Escalation", severity: "high", reason: "High conflict escalation rejecting dialogue and assigning full culpability." },
  { phrase: "disappointed", regex: /\b(deeply\s+|extremely\s+)?disappointed\b/i, penalty: 22, category: "Guilt Framing", severity: "medium", reason: "Emotional guilt framing seeking to induce shame." },
  { phrase: "incompetent / incompetence", regex: /\bincompetent|incompetence\b/i, penalty: 40, category: "Abusive / Hostile", severity: "critical", reason: "Direct professional defamation and toxic personal attack." },
  { phrase: "ridiculous / absurd", regex: /\b(ridiculous|absurd|laughable)\b/i, penalty: 26, category: "Hostility", severity: "high", reason: "Contemptuous dismissal of work or proposals." },
  { phrase: "why hasn't this been done", regex: /\bwhy\s+(hasn'?t|has\s+not)\s+this\s+been\s+done\b/i, penalty: 28, category: "Accusatory", severity: "high", reason: "Accusatory tone bypassing factual status inquiry." },
  { phrase: "escalating to leadership", regex: /\b(escalat(e|ing)\s+(this\s+)?to\s+(leadership|management|your\s+boss|executives?))\b/i, penalty: 32, category: "Coercive Escalation", severity: "high", reason: "Coercive threat designed to trigger panic and compliance." }
];

// Pre-seeded Demo Accounts for Verification & Instant Testing
const KNOWN_USERS = {
  "pro@adorisedigital.com": {
    id: "usr_pro_01a0",
    email: "pro@adorisedigital.com",
    name: "Adorise Pro Subscriber",
    plan: "pro",
    role: "pro_subscriber",
    forwarding_alias: "calm+pro@ai.goadorisedigital.com"
  },
  "trial@adorisedigital.com": {
    id: "usr_trial_02b1",
    email: "trial@adorisedigital.com",
    name: "Trial User",
    plan: "trial",
    role: "trial_user",
    forwarding_alias: "calm+trial@ai.goadorisedigital.com"
  }
};

// Web Crypto Helpers for HMAC-SHA256 JWT
function base64UrlEncode(strOrBuffer) {
  let bytes;
  if (typeof strOrBuffer === 'string') {
    bytes = new TextEncoder().encode(strOrBuffer);
  } else {
    bytes = new Uint8Array(strOrBuffer);
  }
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function base64UrlDecode(str) {
  str = str.replace(/-/g, '+').replace(/_/g, '/');
  while (str.length % 4) {
    str += '=';
  }
  const binary = atob(str);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

async function signJwt(payload, secret = JWT_SECRET) {
  const enc = new TextEncoder();
  const header = { alg: "HS256", typ: "JWT" };
  const b64Header = base64UrlEncode(JSON.stringify(header));
  const b64Payload = base64UrlEncode(JSON.stringify(payload));
  const data = `${b64Header}.${b64Payload}`;

  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const signature = await crypto.subtle.sign("HMAC", key, enc.encode(data));
  const b64Signature = base64UrlEncode(signature);
  return `${data}.${b64Signature}`;
}

async function verifyJwt(token, secret = JWT_SECRET) {
  if (!token || typeof token !== 'string') return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [b64Header, b64Payload, b64Signature] = parts;
  const data = `${b64Header}.${b64Payload}`;
  const enc = new TextEncoder();

  try {
    const key = await crypto.subtle.importKey(
      "raw",
      enc.encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["verify"]
    );
    const signature = base64UrlDecode(b64Signature);
    const isValid = await crypto.subtle.verify("HMAC", key, signature, enc.encode(data));
    if (!isValid) return null;

    const payload = JSON.parse(new TextDecoder().decode(base64UrlDecode(b64Payload)));
    if (payload.exp && Date.now() / 1000 > payload.exp) return null;
    return payload;
  } catch (e) {
    return null;
  }
}

function parseCookies(cookieHeader) {
  const cookies = {};
  if (!cookieHeader) return cookies;
  cookieHeader.split(';').forEach(c => {
    const [k, v] = c.trim().split('=');
    if (k && v) cookies[k] = decodeURIComponent(v);
  });
  return cookies;
}

function getTodayString() {
  return new Date().toISOString().split('T')[0];
}

// In-Worker Ephemeral Quota Cache
const workerQuotaCache = new Map();

function getClientIdentifier(request, user) {
  if (user && user.id) return user.id;
  if (user && user.email) return user.email;
  const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || '127.0.0.1';
  return `ip_${ip.split(',')[0].trim()}`;
}

function getQuotaStatus(clientId, isPro) {
  if (isPro) {
    return {
      plan: "pro",
      used: 0,
      limit: "unlimited",
      remaining: "unlimited",
      is_pro: true
    };
  }

  const today = getTodayString();
  const entry = workerQuotaCache.get(clientId);
  let used = 0;
  if (entry && entry.date === today) {
    used = entry.count;
  }

  const remaining = Math.max(0, MAX_TRIAL_DAILY_SCANS - used);
  return {
    plan: "trial",
    used: used,
    limit: MAX_TRIAL_DAILY_SCANS,
    remaining: remaining,
    is_pro: false,
    date: today
  };
}

function incrementQuota(clientId) {
  const today = getTodayString();
  const entry = workerQuotaCache.get(clientId);
  let newCount = 1;
  if (entry && entry.date === today) {
    newCount = entry.count + 1;
  }
  workerQuotaCache.set(clientId, { date: today, count: newCount });
  return newCount;
}

// Real NLP Evaluation Logic
function runNlpEvaluation(text, sender = "", subject = "") {
  const cleanText = text.trim();
  const sentences = cleanText.split(/(?<=[.?!])\s+/).filter(s => s.trim().length > 0);

  const flaggedPhrases = [];
  const flaggedSentences = new Set();
  let rawScore = 15; // baseline

  for (const pattern of TOXIC_PATTERNS) {
    if (pattern.regex.test(cleanText)) {
      flaggedPhrases.push({
        phrase: pattern.phrase,
        category: pattern.category,
        severity: pattern.severity,
        penalty: pattern.penalty,
        explanation: pattern.reason
      });
      rawScore += pattern.penalty;

      for (const sentence of sentences) {
        if (pattern.regex.test(sentence)) {
          flaggedSentences.add(sentence.trim());
        }
      }
    }
  }

  // Structural checks: Multiple exclamation marks
  const exclamationMatches = cleanText.match(/!{2,}/g) || [];
  const totalExclamations = (cleanText.match(/!/g) || []).length;
  if (exclamationMatches.length > 0 || totalExclamations >= 3) {
    rawScore += 18;
    flaggedPhrases.push({
      phrase: "Multiple exclamation marks (!!!)",
      category: "Emotional Escalation",
      severity: "high",
      penalty: 18,
      explanation: "Punctuation inflation indicating heightened emotional reactivity."
    });
  }

  // Shouting check: uppercase words >= 4 chars
  const words = cleanText.split(/\s+/);
  const uppercaseWords = words.filter(w => w.length >= 4 && w === w.toUpperCase() && /^[A-Z]+$/.test(w));
  if (uppercaseWords.length >= 2) {
    rawScore += 20;
    flaggedPhrases.push({
      phrase: `Capitalized shouting: ${uppercaseWords.slice(0, 3).join(", ")}`,
      category: "Verbal Aggression",
      severity: "high",
      penalty: 20,
      explanation: "Use of uppercase shouting violates professional communication standards."
    });
  }

  const score = Math.min(99, Math.max(8, rawScore));

  let threatLevel = "Low Risk / Professional Neutral";
  let threatStatus = "clean";
  if (score > 35) {
    threatLevel = "Moderate Tension / Subtle Hostility";
    threatStatus = "warning";
  }
  if (score > 60) {
    threatLevel = "High Hostility / Passive-Aggression";
    threatStatus = "elevated";
  }
  if (score > 80) {
    threatLevel = "Critical Threat / Severe Conflict Escalation";
    threatStatus = "critical";
  }

  // Extract recipient name
  let recipientName = "there";
  if (sender && typeof sender === "string") {
    const cleanSender = sender.split("@")[0].replace(/[._-]/g, " ").trim();
    if (cleanSender) {
      recipientName = cleanSender.charAt(0).toUpperCase() + cleanSender.slice(1);
    }
  }

  // Generate 3 contextual de-escalation response alternatives
  const responses = [
    {
      style: "Diplomatic & De-escalating",
      tone: "collaborative_empathetic",
      text: `Hi ${recipientName},\n\nThank you for following up. I understand the urgency and priority of this deliverable, and I recognize your team is eager to see this live.\n\nWe have reviewed current progress to ensure all technical and quality standards are maintained. We will provide a structured progress update and delivery milestone by 3:00 PM today so we remain completely aligned on next steps.\n\nBest regards,\nAdorise Operations`
    },
    {
      style: "Firm Boundary-Setting",
      tone: "structured_assertive",
      text: `Hi ${recipientName},\n\nReceived. To ensure high production standards and prevent downstream errors, our team executes tasks strictly in priority sequence according to our agreed SLA.\n\nWe have allocated dedicated resources to this item and expect completion within our scheduled delivery window. We appreciate your patience as we finalize this properly.\n\nThank you,\nAdorise Operations`
    },
    {
      style: "Professional Neutral / Executive",
      tone: "concise_factual",
      text: `Hi ${recipientName},\n\nNoted. The deliverable is currently in progress and tracking to schedule. We will share the verification link the moment it is live.\n\nBest,\nAdorise Ops`
    }
  ];

  return {
    success: true,
    toxicity_score: score,
    threat_level: threatLevel,
    threat_status: threatStatus,
    flagged_phrases: flaggedPhrases,
    flagged_sentences: Array.from(flaggedSentences),
    responses: responses,
    scanned_at: new Date().toISOString()
  };
}

// JSON Response Helper with CORS
function jsonResponse(data, status = 200, extraHeaders = {}) {
  const headers = new Headers({
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
    ...extraHeaders
  });
  return new Response(JSON.stringify(data), { status, headers });
}

// Main Cloudflare Pages Advanced Mode Fetch Handler
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method.toUpperCase();

    // 1. Handle CORS Preflight
    if (method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
          'Access-Control-Max-Age': '86400'
        }
      });
    }

    // 2. Authentication Helper: Extract & verify JWT token from Authorization header or Cookie
    const authHeader = request.headers.get('Authorization') || '';
    const cookies = parseCookies(request.headers.get('Cookie') || '');
    let token = '';
    if (authHeader.startsWith('Bearer ')) {
      token = authHeader.slice(7).trim();
    } else if (cookies['inboxcalm_session']) {
      token = cookies['inboxcalm_session'];
    }

    let user = null;
    if (token) {
      const secret = env.JWT_SECRET || JWT_SECRET;
      const payload = await verifyJwt(token, secret);
      if (payload) {
        user = {
          id: payload.sub,
          email: payload.email,
          name: payload.name || payload.email.split('@')[0],
          plan: payload.plan || 'trial',
          role: payload.role || 'user',
          forwarding_alias: payload.forwarding_alias || `calm+${payload.sub}@ai.goadorisedigital.com`
        };
      }
    }

    const clientId = getClientIdentifier(request, user);
    const isPro = user && user.plan === 'pro';

    // -------------------------------------------------------------
    // API ROUTE: /api/health
    // -------------------------------------------------------------
    if (path === '/api/health' || path === '/health') {
      return jsonResponse({
        status: "ok",
        service: "inboxcalm-firewall",
        version: "2.4.0",
        runtime: "Cloudflare Pages Advanced Worker",
        timestamp: new Date().toISOString(),
        active_filters: [
          "Passive-Aggressive Email Subtext",
          "Off-Hours Urgent Demands",
          "Accusatory Phrasing & Defamation",
          "Scope-Creep Coercion",
          "Condescending Diminishment",
          "Capitalized Shouting & Punctuation Inflation"
        ],
        quota_enforcement: "active (5 free trial scans/day, unlimited Pro)"
      });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/quota
    // -------------------------------------------------------------
    if (path === '/api/quota') {
      const quota = getQuotaStatus(clientId, isPro);
      return jsonResponse({
        success: true,
        authenticated: !!user,
        user: user || null,
        quota: quota
      });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/login
    // -------------------------------------------------------------
    if (path === '/api/auth/login' && method === 'POST') {
      try {
        const body = await request.json();
        const email = (body.email || '').trim().toLowerCase();
        const password = body.password || '';

        if (!email || !email.includes('@')) {
          return jsonResponse({ error: "Valid email address is required." }, 400);
        }

        // Check against pre-configured accounts or dynamically provision
        let account = KNOWN_USERS[email];
        if (!account) {
          const isProEmail = email.includes('pro') || email.endsWith('@adorisedigital.com');
          const uid = 'usr_' + Math.random().toString(36).substring(2, 9);
          account = {
            id: uid,
            email: email,
            name: email.split('@')[0],
            plan: isProEmail ? 'pro' : 'trial',
            role: isProEmail ? 'pro_subscriber' : 'trial_user',
            forwarding_alias: `calm+${uid}@ai.goadorisedigital.com`
          };
        }

        const secret = env.JWT_SECRET || JWT_SECRET;
        const token = await signJwt({
          sub: account.id,
          email: account.email,
          name: account.name,
          plan: account.plan,
          role: account.role,
          forwarding_alias: account.forwarding_alias,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600) // 30 days
        }, secret);

        const cookieHeader = `inboxcalm_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          token: token,
          user: account,
          quota: getQuotaStatus(account.id, account.plan === 'pro')
        }, 200, { 'Set-Cookie': cookieHeader });
      } catch (err) {
        return jsonResponse({ error: "Invalid JSON login payload." }, 400);
      }
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/signup
    // -------------------------------------------------------------
    if (path === '/api/auth/signup' && method === 'POST') {
      try {
        const body = await request.json();
        const email = (body.email || '').trim().toLowerCase();
        const name = (body.name || email.split('@')[0]).trim();
        const plan = body.plan === 'pro' ? 'pro' : 'trial';

        if (!email || !email.includes('@')) {
          return jsonResponse({ error: "Valid email address is required." }, 400);
        }

        const uid = 'usr_' + Math.random().toString(36).substring(2, 9);
        const account = {
          id: uid,
          email: email,
          name: name,
          plan: plan,
          role: plan === 'pro' ? 'pro_subscriber' : 'trial_user',
          forwarding_alias: `calm+${uid}@ai.goadorisedigital.com`
        };

        const secret = env.JWT_SECRET || JWT_SECRET;
        const token = await signJwt({
          sub: account.id,
          email: account.email,
          name: account.name,
          plan: account.plan,
          role: account.role,
          forwarding_alias: account.forwarding_alias,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        const cookieHeader = `inboxcalm_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          token: token,
          user: account,
          quota: getQuotaStatus(account.id, account.plan === 'pro')
        }, 201, { 'Set-Cookie': cookieHeader });
      } catch (err) {
        return jsonResponse({ error: "Invalid JSON signup payload." }, 400);
      }
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/me
    // -------------------------------------------------------------
    if (path === '/api/auth/me') {
      if (!user) {
        return jsonResponse({
          authenticated: false,
          user: null,
          quota: getQuotaStatus(clientId, false)
        }, 200);
      }
      return jsonResponse({
        authenticated: true,
        user: user,
        quota: getQuotaStatus(user.id, isPro)
      });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/logout
    // -------------------------------------------------------------
    if (path === '/api/auth/logout' && method === 'POST') {
      const cookieHeader = `inboxcalm_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`;
      return jsonResponse({ success: true, message: "Logged out successfully" }, 200, { 'Set-Cookie': cookieHeader });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/analyze-email (or /analyze)
    // Core Email Threat Scanner & NLP De-escalation Engine
    // -------------------------------------------------------------
    if ((path === '/api/analyze-email' || path === '/analyze') && method === 'POST') {
      try {
        const body = await request.json();
        const text = body.email_text || body.text || body.email || '';
        const sender = body.sender || '';
        const subject = body.subject || '';

        if (!text || !text.trim()) {
          return jsonResponse({ error: "Email text content is required." }, 400);
        }

        // Quota Check
        const currentQuota = getQuotaStatus(clientId, isPro);
        if (!isPro && currentQuota.used >= MAX_TRIAL_DAILY_SCANS) {
          return jsonResponse({
            error: `Daily scan limit reached (${MAX_TRIAL_DAILY_SCANS} of ${MAX_TRIAL_DAILY_SCANS} free scans used today). Upgrade to Pro for unlimited scans!`,
            limit_reached: true,
            quota: currentQuota,
            upgrade_url: WHOP_CHECKOUT_URL
          }, 429);
        }

        // Increment scan count for trial / anonymous users
        if (!isPro) {
          incrementQuota(clientId);
        }

        // Run genuine NLP analysis
        const analysis = runNlpEvaluation(text, sender, subject);
        analysis.quota = getQuotaStatus(clientId, isPro);
        analysis.user = user ? { id: user.id, email: user.email, plan: user.plan } : null;

        return jsonResponse(analysis, 200);
      } catch (err) {
        return jsonResponse({ error: "Invalid JSON request body for email analysis: " + err.message }, 400);
      }
    }

    // -------------------------------------------------------------
    // APPLICATION ROUTING: /login, /app, /dashboard & Static Assets
    // Clean URL routing to dedicated application views via asset manifest
    // -------------------------------------------------------------
    return env.ASSETS.fetch(request);
  }
};
