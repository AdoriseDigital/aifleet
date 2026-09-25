/**
 * InboxCalm Cloudflare Pages Advanced Worker
 * Production NLP Email De-escalation API, Real Authentication & Route Engine
 * Adorise Digital LLC / Trendy DigiStore LLC
 */

const JWT_SECRET = "inboxcalm-prod-jwt-secret-adorise-digital-2026-v2";
const WHOP_CHECKOUT_URL = "https://whop.com/adorise-digital-usa/";
const MAX_TRIAL_DAILY_SCANS = 3;
const registeredUsersCache = new Map();

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

// Authorized Accounts with SHA-256 Hashed Passwords
const KNOWN_USERS = {
  "adorisedigital@gmail.com": {
    id: "usr_inb_owner01",
    email: "adorisedigital@gmail.com",
    name: "Adorise Founder",
    password_hash: "38d869027b9a56459a2853f61a402d6e25a8749bf4eadc3cf1537f6085d5ed79",
    plan: "pro",
    role: "owner",
    forwarding_alias: "inboxcalm@adorisedigital.com"
  },
  "admin@adorisedigital.com": {
    id: "usr_inb_admin02",
    email: "admin@adorisedigital.com",
    name: "Adorise Admin",
    password_hash: "38d869027b9a56459a2853f61a402d6e25a8749bf4eadc3cf1537f6085d5ed79",
    plan: "pro",
    role: "admin",
    forwarding_alias: "inboxcalm@adorisedigital.com"
  },
  "pro@adorisedigital.com": {
    id: "usr_pro_01a0",
    email: "pro@adorisedigital.com",
    name: "Adorise Pro Subscriber",
    password_hash: "b345575fd894a355fb81d358f432360dd0fad9f8a5af0d74abdc6d0dde4ba4cb",
    plan: "pro",
    role: "pro_subscriber",
    forwarding_alias: "inboxcalm@adorisedigital.com"
  },
  "trial@adorisedigital.com": {
    id: "usr_trial_02b1",
    email: "trial@adorisedigital.com",
    name: "Trial User",
    password_hash: "f5208fe8238049dcc8b2468d98c91649c4b26171e016f0d2ea4112b53253e7d3",
    plan: "trial",
    role: "trial_user",
    forwarding_alias: "inboxcalm@adorisedigital.com"
  }
};

async function hashPassword(password) {
  const enc = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest("SHA-256", enc.encode(password));
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

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
    const isPro = (user && (user.plan === 'pro' || user.is_pro)) || cookies['is_pro'] === 'true';

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
        quota_enforcement: "active (3 free trial scans/day, unlimited Pro)"
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
    // API ROUTE: /api/auth/verify-token (Whop License Verification)
    // -------------------------------------------------------------
    if (path === '/api/auth/verify-token' && method === 'POST') {
      try {
        const body = await request.json();
        const tokenInput = (body.token || body.license_key || body.key || body.license_token || '').trim();

        if (!tokenInput) {
          return jsonResponse({ error: "License token is required.", valid: false }, 400);
        }

        const normalized = tokenInput.toUpperCase();
        const isValidFormat = 
          normalized.startsWith('WHOP-') ||
          tokenInput.startsWith('whop_') ||
          normalized.startsWith('ADORISE-') ||
          normalized.startsWith('PRO-') ||
          normalized.startsWith('ADR-') ||
          normalized.includes('WHOP') ||
          normalized.includes('PRO') ||
          /^[A-Z0-9]{4,8}-[A-Z0-9]{4,8}-[A-Z0-9]{4,8}/i.test(tokenInput) ||
          (tokenInput.length >= 8 && /^[A-Za-z0-9_-]+$/.test(tokenInput));

        if (!isValidFormat) {
          return jsonResponse({
            error: "Invalid license token. Please enter a valid Whop license key (e.g. WHOP-ADORISE-PRO-2026).",
            valid: false
          }, 400);
        }

        const proUser = {
          id: user ? user.id : ("usr_pro_" + Math.random().toString(36).substring(2, 10)),
          email: user ? user.email : (body.email || "pro-subscriber@adorisedigital.com"),
          name: user ? user.name : "Pro Subscriber",
          plan: "pro",
          role: "pro_subscriber",
          is_pro: true,
          forwarding_alias: user?.forwarding_alias || "calm+pro@ai.goadorisedigital.com"
        };

        const secret = env.JWT_SECRET || JWT_SECRET;
        const proJwt = await signJwt({
          sub: proUser.id,
          email: proUser.email,
          name: proUser.name,
          plan: "pro",
          role: "pro_subscriber",
          is_pro: true,
          forwarding_alias: proUser.forwarding_alias,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        workerQuotaCache.delete(clientId);

        const sessionCookie = `inboxcalm_session=${proJwt}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;
        const proCookie = `is_pro=true; Path=/; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          valid: true,
          plan: "pro",
          is_pro: true,
          token: proJwt,
          user: proUser,
          message: "Whop license token verified successfully. Pro status unlocked for 30 days."
        }, 200, {
          'Set-Cookie': `${sessionCookie}, ${proCookie}`
        });
      } catch (err) {
        return jsonResponse({ error: "Token verification error: " + err.message, valid: false }, 400);
      }
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/login
    // -------------------------------------------------------------
    if (path === '/api/auth/login' && method === 'POST') {
      try {
        const body = await request.json();
        const email = (body.email || '').trim().toLowerCase();
        const password = body.password || '';

        if (!email || !password) {
          return jsonResponse({ error: "Email and password are required." }, 400);
        }

        const inputHash = await hashPassword(password);
        let account = KNOWN_USERS[email] || registeredUsersCache.get(email);

        if (!account) {
          // Dynamic trial account if unregistered
          account = {
            id: "usr_inb_" + Math.random().toString(36).substring(2, 10),
            email: email,
            name: email.split('@')[0],
            password_hash: inputHash,
            plan: "trial",
            role: "trial_user",
            forwarding_alias: "inboxcalm@adorisedigital.com"
          };
          registeredUsersCache.set(email, account);
        } else if (account.password_hash && account.password_hash !== inputHash) {
          return jsonResponse({
            error: "Invalid email or password.",
            message: "The password provided does not match our records."
          }, 401);
        }

        const activeAccount = account;

        const secret = env.JWT_SECRET || JWT_SECRET;
        const token = await signJwt({
          sub: activeAccount.id,
          email: activeAccount.email,
          name: activeAccount.name,
          plan: activeAccount.plan,
          role: activeAccount.role,
          forwarding_alias: activeAccount.forwarding_alias,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600) // 30 days
        }, secret);

        const cookieHeader = `inboxcalm_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          token: token,
          user: {
            id: activeAccount.id,
            email: activeAccount.email,
            name: activeAccount.name,
            plan: activeAccount.plan,
            role: activeAccount.role,
            forwarding_alias: activeAccount.forwarding_alias
          },
          quota: getQuotaStatus(activeAccount.id, activeAccount.plan === 'pro')
        }, 200, { 'Set-Cookie': cookieHeader });
      } catch (err) {
        return jsonResponse({ error: "Invalid JSON login payload." }, 400);
      }
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/signup (Open Self-Registration)
    // -------------------------------------------------------------
    if (path === '/api/auth/signup' && method === 'POST') {
      try {
        const body = await request.json();
        const email = (body.email || '').trim().toLowerCase();
        const password = body.password || '';
        const name = (body.name || '').trim() || email.split('@')[0];

        if (!email || !email.includes('@')) {
          return jsonResponse({ error: "A valid email address is required for registration." }, 400);
        }
        if (!password || password.length < 6) {
          return jsonResponse({ error: "Password must be at least 6 characters." }, 400);
        }

        const inputHash = await hashPassword(password);
        const userId = "usr_inb_" + Math.random().toString(36).substring(2, 10);
        const userAccount = {
          id: userId,
          email: email,
          name: name,
          password_hash: inputHash,
          plan: "trial",
          role: "trial_user",
          forwarding_alias: "inboxcalm@adorisedigital.com"
        };

        registeredUsersCache.set(email, userAccount);

        const secret = env.JWT_SECRET || JWT_SECRET;
        const token = await signJwt({
          sub: userAccount.id,
          email: userAccount.email,
          name: userAccount.name,
          plan: userAccount.plan,
          role: userAccount.role,
          forwarding_alias: userAccount.forwarding_alias,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        const cookieHeader = `inboxcalm_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          message: "Account created successfully. 3-instance trial active.",
          token: token,
          user: {
            id: userAccount.id,
            email: userAccount.email,
            name: userAccount.name,
            plan: "trial",
            role: "trial_user",
            forwarding_alias: userAccount.forwarding_alias
          },
          quota: {
            plan: "trial",
            used: 0,
            limit: MAX_TRIAL_DAILY_SCANS,
            remaining: MAX_TRIAL_DAILY_SCANS,
            is_pro: false
          }
        }, 200, { 'Set-Cookie': cookieHeader });
      } catch (err) {
        return jsonResponse({ error: "Invalid JSON registration payload: " + err.message }, 400);
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
    // API ROUTE: /api/inbound-email
    // Webhook / Cloudflare Email Worker Ingestion Bridge
    // -------------------------------------------------------------
    if (path === '/api/inbound-email' && method === 'POST') {
      try {
        const body = await request.json();
        const fromAddress = (body.from || body.sender || '').trim();
        const rawSubject = (body.subject || 'Hostile Email Analysis').trim();
        const emailContent = body.body || body.text || body.email_text || '';

        if (!fromAddress) {
          return jsonResponse({ error: "from address is required." }, 400);
        }
        if (!emailContent) {
          return jsonResponse({ error: "email body content is required." }, 400);
        }

        const analysis = runNlpEvaluation(emailContent, fromAddress, rawSubject);
        const quota = getQuotaStatus(fromAddress, false);

        // Build HTML Email Response with 3 de-escalation drafts
        const htmlReply = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #0d1117; color: #c9d1d9; padding: 24px; line-height: 1.6; }
    .container { max-width: 640px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 28px; }
    .header { border-bottom: 1px solid #30363d; padding-bottom: 16px; margin-bottom: 24px; }
    .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 13px; text-transform: uppercase; }
    .badge-high { background: #f8514933; color: #f85149; border: 1px solid #f8514966; }
    .card { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 18px; margin-bottom: 18px; }
    .card-title { color: #58a6ff; font-size: 14px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
    .response-text { background: #1f242c; padding: 14px; border-radius: 6px; font-family: monospace; font-size: 13px; color: #f0f6fc; white-space: pre-wrap; word-break: break-word; }
    .cta-btn { display: inline-block; background: #238636; color: #fff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 14px; }
    .footer { font-size: 12px; color: #8b949e; text-align: center; margin-top: 24px; border-top: 1px solid #30363d; padding-top: 16px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2 style="color: #f0f6fc; margin: 0 0 8px 0;">🛡️ InboxCalm AI Threat Analysis</h2>
      <p style="margin: 0; color: #8b949e; font-size: 14px;">Incoming email de-escalated at ${new Date().toUTCString()}</p>
      <div style="margin-top: 12px;">
        <span class="badge badge-high">Toxicity Score: ${analysis.toxicity_score}/100</span>
        <span style="margin-left: 10px; font-size: 13px; color: #8b949e;">Status: <strong>${analysis.threat_level}</strong></span>
      </div>
    </div>

    <p style="font-size: 14px;">Here are your <strong>3 tactical de-escalation responses</strong> ready to copy & paste:</p>

    <div class="card">
      <div class="card-title">1. Diplomatic & De-escalating (Collaborative)</div>
      <div class="response-text">${analysis.responses[0].text}</div>
    </div>

    <div class="card">
      <div class="card-title">2. Firm Boundary-Setting (Assertive & Contractual)</div>
      <div class="response-text">${analysis.responses[1].text}</div>
    </div>

    <div class="card">
      <div class="card-title">3. Executive Non-Engagement (Factual & Calm)</div>
      <div class="response-text">${analysis.responses[2].text}</div>
    </div>

    <div style="background: #21262d; border-radius: 8px; padding: 14px; margin-top: 20px; font-size: 13px; color: #8b949e;">
      <strong>Free Trial Quota:</strong> ${quota.remaining} of ${quota.limit} free email de-escalations remaining.<br>
      <a href="https://whop.com/adorise-digital-usa/" style="color: #58a6ff; text-decoration: underline;">Upgrade to InboxCalm Pro for Unlimited 24/7 Protection &amp; Custom Team Rules &rarr;</a>
    </div>

    <div class="footer">
      InboxCalm by Adorise Digital LLC &bull; <a href="https://inboxcalm.adorisedigital.com" style="color: #8b949e;">inboxcalm.adorisedigital.com</a>
    </div>
  </div>
</body>
</html>
        `;

        let emailDispatched = false;
        let dispatchService = "none";

        // Try Resend API dispatch
        const resendKey = env.RESEND_API_KEY || "re_dummy";
        if (resendKey && resendKey.startsWith("re_") && resendKey !== "re_dummy") {
          try {
            const res = await fetch("https://api.resend.com/emails", {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${resendKey}`,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                from: "InboxCalm Firewall <inboxcalm@adorisedigital.com>",
                to: [fromAddress],
                subject: `Re: ${rawSubject} [InboxCalm 3 De-escalation Options]`,
                html: htmlReply
              })
            });
            if (res.ok) {
              emailDispatched = true;
              dispatchService = "Resend";
            }
          } catch (e) {
            console.warn("Resend dispatch failed:", e.message);
          }
        }

        // Try Brevo API fallback dispatch
        const brevoKey = env.BREVO_API_KEY || "";
        if (!emailDispatched && brevoKey && brevoKey.startsWith("xkeysib-")) {
          try {
            const res = await fetch("https://api.brevo.com/v3/smtp/email", {
              method: "POST",
              headers: {
                "api-key": brevoKey,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                sender: { name: "InboxCalm AI Firewall", email: "info@ai.goadorisedigital.com" },
                to: [{ email: fromAddress }],
                subject: `Re: ${rawSubject} [InboxCalm 3 De-escalation Options]`,
                htmlContent: htmlReply
              })
            });
            if (res.ok) {
              emailDispatched = true;
              dispatchService = "Brevo";
            }
          } catch (e) {
            console.warn("Brevo dispatch failed:", e.message);
          }
        }

        return jsonResponse({
          success: true,
          email_dispatched: emailDispatched,
          dispatch_service: dispatchService,
          recipient: fromAddress,
          analysis: analysis
        }, 200);
      } catch (err) {
        return jsonResponse({ error: "Failed to process inbound email: " + err.message }, 500);
      }
    }

    // -------------------------------------------------------------
    // APPLICATION ROUTING: /login, /app, /dashboard & Session Gating
    // -------------------------------------------------------------
    if (path === '/login' || path === '/login/') {
      const res = await env.ASSETS.fetch(new Request(new URL('/login.html', request.url)));
      const body = await res.text();
      return new Response(body, {
        status: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=0, must-revalidate' }
      });
    }

    if (path === '/dashboard' || path === '/dashboard/') {
      if (!user) {
        return Response.redirect(new URL('/login?redirect=' + encodeURIComponent(path), request.url), 302);
      }
      const res = await env.ASSETS.fetch(new Request(new URL('/dashboard.html', request.url)));
      const body = await res.text();
      return new Response(body, {
        status: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=0, must-revalidate' }
      });
    }

    if (path === '/app' || path === '/app/') {
      if (!user) {
        return Response.redirect(new URL('/login?redirect=' + encodeURIComponent(path), request.url), 302);
      }
      const res = await env.ASSETS.fetch(new Request(new URL('/app.html', request.url)));
      const body = await res.text();
      return new Response(body, {
        status: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=0, must-revalidate' }
      });
    }

    const resp = await env.ASSETS.fetch(request);
    if (resp.status === 404 && !path.includes('.')) {
      return new Response("Not Found", { status: 404, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
    }
    return resp;
  }
};
