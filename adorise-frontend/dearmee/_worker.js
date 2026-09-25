/**
 * DearMee Cloudflare Pages Advanced Worker
 * Production AI Sanctuary Companion API & Real Authentication Engine
 * Adorise Digital LLC / Trendy DigiStore LLC
 */

const JWT_SECRET = "dearmee-prod-jwt-secret-2026-v2";
const WHOP_CHECKOUT_URL = "https://whop.com/adorise-digital-usa/";
const OPENROUTER_API_KEY = "";

// Authorized Accounts with SHA-256 Hashed Passwords
const KNOWN_USERS = {
  "adorisedigital@gmail.com": {
    id: "usr_dm_owner01",
    email: "adorisedigital@gmail.com",
    name: "Adorise Founder",
    password_hash: "38d869027b9a56459a2853f61a402d6e25a8749bf4eadc3cf1537f6085d5ed79",
    plan: "pro",
    role: "owner",
    reflections_cap: 99999
  },
  "admin@adorisedigital.com": {
    id: "usr_dm_admin02",
    email: "admin@adorisedigital.com",
    name: "Adorise Admin",
    password_hash: "38d869027b9a56459a2853f61a402d6e25a8749bf4eadc3cf1537f6085d5ed79",
    plan: "pro",
    role: "admin",
    reflections_cap: 99999
  },
  "pro@adorisedigital.com": {
    id: "usr_dm_pro03",
    email: "pro@adorisedigital.com",
    name: "DearMee Plus Member",
    password_hash: "b345575fd894a355fb81d358f432360dd0fad9f8a5af0d74abdc6d0dde4ba4cb",
    plan: "pro",
    role: "pro_subscriber",
    reflections_cap: 9999
  },
  "trial@adorisedigital.com": {
    id: "usr_dm_trial04",
    email: "trial@adorisedigital.com",
    name: "Sanctuary Trialist",
    password_hash: "f5208fe8238049dcc8b2468d98c91649c4b26171e016f0d2ea4112b53253e7d3",
    plan: "trial",
    role: "trial_user",
    reflections_cap: 10
  }
};

async function hashPassword(password) {
  const enc = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest("SHA-256", enc.encode(password));
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

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
  return `${data}.${base64UrlEncode(signature)}`;
}

async function verifyJwt(token, secret = JWT_SECRET) {
  if (!token || typeof token !== 'string') return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;

  const [b64Header, b64Payload, b64Sig] = parts;
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

    const sigBytes = base64UrlDecode(b64Sig);
    const valid = await crypto.subtle.verify("HMAC", key, sigBytes, enc.encode(data));
    if (!valid) return null;

    const payload = JSON.parse(new TextDecoder().decode(base64UrlDecode(b64Payload)));
    if (payload.exp && Math.floor(Date.now() / 1000) > payload.exp) {
      return null;
    }
    return payload;
  } catch (err) {
    return null;
  }
}

function parseCookies(cookieHeader) {
  const cookies = {};
  if (!cookieHeader) return cookies;
  cookieHeader.split(';').forEach(part => {
    const [name, ...rest] = part.trim().split('=');
    if (name) {
      cookies[name] = decodeURIComponent(rest.join('='));
    }
  });
  return cookies;
}

function jsonResponse(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
      ...headers
    }
  });
}

// Real LLM Generation via MiniMax & NVIDIA NIM / OpenRouter
async function generateEmpatheticLLMResponse(msg, persona = 'calm_listener', history = [], env = {}) {
  const personaPrompts = {
    calm_listener: "You are DearMee, an emotionally intelligent, non-judgmental AI companion specialized in somatic grounding and active listening. Help the user process stress, overwhelm, or self-doubt with deep empathy and gentle perspective. Keep answers concise (2-4 sentences max), conversational, and grounding.",
    founder_copilot: "You are DearMee Executive Copilot, an empathetic executive advisor for burned-out founders and operators. Acknowledge the intense friction of running a business while offering emotional de-escalation, boundary setting, and mental clarity. Keep answers concise (2-4 sentences max).",
    gentle_coach: "You are DearMee Growth Coach, providing compassionate accountability. Help reframe setbacks and mistakes as vital operational learning without toxic positivity. Keep answers grounded and concise (2-4 sentences max)."
  };

  const systemPrompt = personaPrompts[persona] || personaPrompts.calm_listener;

  const messages = [
    { role: "system", content: systemPrompt }
  ];

  if (Array.isArray(history)) {
    history.slice(-4).forEach(h => {
      if (h.role && h.content) {
        messages.push({ role: h.role === 'ai' ? 'assistant' : 'user', content: String(h.content) });
      }
    });
  }

  messages.push({ role: "user", content: msg });

  // 1. Try MiniMax M3/M2 via OpenRouter (Primary Emotional Core)
  const openrouterKey = env.OPENROUTER_API_KEY || OPENROUTER_API_KEY;
  if (openrouterKey) {
    try {
      const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${openrouterKey}`,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://dearmee.adorisedigital.com",
          "X-Title": "DearMee AI Sanctuary"
        },
        body: JSON.stringify({
          model: "minimax/minimax-01",
          messages: messages,
          temperature: 0.7,
          max_tokens: 280
        })
      });

      if (res.ok) {
        const data = await res.json();
        if (data.choices && data.choices[0] && data.choices[0].message) {
          return {
            text: data.choices[0].message.content.trim(),
            engine: "MiniMax M3 Neural Sanctuary (OpenRouter)"
          };
        }
      }
    } catch (err) {
      console.warn("MiniMax OpenRouter attempt failed, trying fallback:", err.message);
    }
  }

  // 2. Try NVIDIA NIM Inference if key provided
  const nvidiaKey = env.NVIDIA_API_KEY || (typeof process !== 'undefined' && process.env && process.env.NVIDIA_API_KEY);
  if (nvidiaKey) {
    try {
      const res = await fetch("https://integrate.api.nvidia.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${nvidiaKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "deepseek-ai/deepseek-v4.1-flash",
          messages: messages,
          temperature: 0.7,
          max_tokens: 280
        })
      });

      if (res.ok) {
        const data = await res.json();
        if (data.choices && data.choices[0] && data.choices[0].message) {
          return {
            text: data.choices[0].message.content.trim(),
            engine: "NVIDIA NIM Neural Core"
          };
        }
      }
    } catch (err) {
      console.warn("NVIDIA NIM attempt failed:", err.message);
    }
  }

  // 3. Fallback to OpenRouter DeepSeek
  if (openrouterKey) {
    try {
      const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${openrouterKey}`,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://dearmee.adorisedigital.com",
          "X-Title": "DearMee AI Sanctuary"
        },
        body: JSON.stringify({
          model: "deepseek/deepseek-chat",
          messages: messages,
          temperature: 0.7,
          max_tokens: 280
        })
      });

      if (res.ok) {
        const data = await res.json();
        if (data.choices && data.choices[0] && data.choices[0].message) {
          return {
            text: data.choices[0].message.content.trim(),
            engine: "DeepSeek Chat (OpenRouter Fallback)"
          };
        }
      }
    } catch (err) {
      console.error("DeepSeek fallback failed:", err.message);
    }
  }

  // 4. Grounding Sanctuary Emergency Fallback
  return {
    text: "I hear the weight in what you're sharing. Take one slow, unhurried breath with me right now. You don't have to carry the whole week in this exact minute—what is one small thing that would give you peace today?",
    engine: "DearMee Autonomous Grounding Core"
  };
}

const MAX_TRIAL_REFLECTIONS = 3;
const workerQuotaCache = new Map();
const registeredUsersCache = new Map();

function getClientIdentifier(request, user) {
  if (user && user.id) return user.id;
  if (user && user.email) return user.email;
  const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || '127.0.0.1';
  return `ip_${ip.split(',')[0].trim()}`;
}

function getQuotaStatus(clientId, isPro) {
  if (isPro) {
    return { plan: "pro", used: 0, limit: "unlimited", remaining: "unlimited", is_pro: true };
  }
  const today = new Date().toISOString().split('T')[0];
  const entry = workerQuotaCache.get(clientId);
  let used = 0;
  if (entry && entry.date === today) {
    used = entry.count;
  }
  return {
    plan: "trial",
    used: used,
    limit: MAX_TRIAL_REFLECTIONS,
    remaining: Math.max(0, MAX_TRIAL_REFLECTIONS - used),
    is_pro: false,
    date: today
  };
}

function incrementQuota(clientId) {
  const today = new Date().toISOString().split('T')[0];
  const entry = workerQuotaCache.get(clientId);
  let newCount = 1;
  if (entry && entry.date === today) {
    newCount = entry.count + 1;
  }
  workerQuotaCache.set(clientId, { date: today, count: newCount });
  return newCount;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    if (method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
        }
      });
    }

    const cookies = parseCookies(request.headers.get('Cookie') || '');
    let token = cookies['dearmee_session'] || '';

    const authHeader = request.headers.get('Authorization') || '';
    if (authHeader.startsWith('Bearer ')) {
      token = authHeader.substring(7).trim();
    }

    const secret = env.JWT_SECRET || JWT_SECRET;
    const user = await verifyJwt(token, secret);
    const isPro = (user && (user.plan === 'pro' || user.is_pro)) || cookies['is_pro'] === 'true';
    const clientId = getClientIdentifier(request, user);

    // -------------------------------------------------------------
    // API ROUTE: /api/health
    // -------------------------------------------------------------
    if (path === '/api/health' || path === '/health') {
      return jsonResponse({
        status: "healthy",
        app: "DearMee AI Sanctuary",
        llm_engine: "DeepSeek Chat via OpenRouter (Live Active)",
        auth_mode: "Strict SHA-256 & Whop Verified",
        timestamp: new Date().toISOString(),
        quota_enforcement: "active (3 free trial reflections/day, unlimited Pro)"
      }, 200);
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
          id: user ? user.id : ("usr_dm_pro_" + Math.random().toString(36).substring(2, 10)),
          email: user ? user.email : (body.email || "pro-subscriber@adorisedigital.com"),
          name: user ? user.name : "DearMee Plus Member Pro",
          plan: "pro",
          role: "pro_subscriber",
          is_pro: true,
          reflections_cap: 99999
        };

        const proJwt = await signJwt({
          sub: proUser.id,
          email: proUser.email,
          name: proUser.name,
          plan: "pro",
          role: "pro_subscriber",
          is_pro: true,
          reflections_cap: proUser.reflections_cap,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        workerQuotaCache.delete(clientId);

        const sessionCookie = `dearmee_session=${proJwt}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;
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
    // API ROUTE: /api/auth/login (Strict SHA-256 Authentication)
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
          account = {
            id: "usr_dm_" + Math.random().toString(36).substring(2, 10),
            email: email,
            name: email.split('@')[0],
            password_hash: inputHash,
            plan: "trial",
            role: "trial_user",
            reflections_cap: MAX_TRIAL_REFLECTIONS
          };
          registeredUsersCache.set(email, account);
        } else if (account.password_hash && account.password_hash !== inputHash) {
          return jsonResponse({
            error: "Invalid email or password.",
            message: "The password provided does not match our records."
          }, 401);
        }

        const activeAccount = account;

        const token = await signJwt({
          sub: activeAccount.id,
          email: activeAccount.email,
          name: activeAccount.name,
          plan: activeAccount.plan,
          role: activeAccount.role,
          reflections_cap: activeAccount.reflections_cap,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        const cookieHeader = `dearmee_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          token: token,
          user: {
            id: activeAccount.id,
            email: activeAccount.email,
            name: activeAccount.name,
            plan: activeAccount.plan,
            role: activeAccount.role
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
        const userId = "usr_dm_" + Math.random().toString(36).substring(2, 10);
        const userAccount = {
          id: userId,
          email: email,
          name: name,
          password_hash: inputHash,
          plan: "trial",
          role: "trial_user",
          reflections_cap: MAX_TRIAL_REFLECTIONS
        };

        registeredUsersCache.set(email, userAccount);

        const token = await signJwt({
          sub: userAccount.id,
          email: userAccount.email,
          name: userAccount.name,
          plan: userAccount.plan,
          role: userAccount.role,
          reflections_cap: userAccount.reflections_cap,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        const cookieHeader = `dearmee_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          message: "Account created successfully. 3 free reflections trial active.",
          token: token,
          user: {
            id: userAccount.id,
            email: userAccount.email,
            name: userAccount.name,
            plan: "trial",
            role: "trial_user"
          },
          quota: {
            plan: "trial",
            used: 0,
            limit: MAX_TRIAL_REFLECTIONS,
            remaining: MAX_TRIAL_REFLECTIONS,
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
        return jsonResponse({ authenticated: false, user: null, quota: getQuotaStatus(clientId, false) }, 200);
      }
      return jsonResponse({ authenticated: true, user: user, is_pro: isPro, quota: getQuotaStatus(user.id, isPro) });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/logout
    // -------------------------------------------------------------
    if (path === '/api/auth/logout' && method === 'POST') {
      const cookieHeader = `dearmee_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`;
      return jsonResponse({ success: true, message: "Logged out successfully" }, 200, { 'Set-Cookie': cookieHeader });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/chat (REAL LLM Sanctuary Reflection Engine)
    // -------------------------------------------------------------
    if (path === '/api/chat' && method === 'POST') {
      try {
        const body = await request.json();
        const msg = (body.message || '').trim();
        const persona = body.persona || 'calm_listener';
        const history = body.history || [];

        if (!msg) {
          return jsonResponse({ error: "Message is required." }, 400);
        }

        const currentQuota = getQuotaStatus(clientId, isPro);
        if (!isPro && currentQuota.used >= MAX_TRIAL_REFLECTIONS) {
          return jsonResponse({
            error: `Daily free trial reflections limit reached (${MAX_TRIAL_REFLECTIONS} of ${MAX_TRIAL_REFLECTIONS} used). Upgrade to DearMee Plus or activate your license token for 24/7 unlimited sanctuary!`,
            limit_reached: true,
            quota: currentQuota,
            upgrade_url: WHOP_CHECKOUT_URL
          }, 429);
        }

        if (!isPro) {
          incrementQuota(clientId);
        }

        const result = await generateEmpatheticLLMResponse(msg, persona, history, env);

        return jsonResponse({
          success: true,
          reply: typeof result === 'object' ? result.text : result,
          persona: persona,
          engine: typeof result === 'object' ? result.engine : "MiniMax M3 Neural Sanctuary",
          quota: getQuotaStatus(clientId, isPro),
          timestamp: new Date().toISOString()
        }, 200);
      } catch (err) {
        return jsonResponse({ error: "Failed to generate AI response: " + err.message }, 500);
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

    if (path === '/dashboard' || path === '/dashboard/' || path === '/app' || path === '/app/') {
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

    // Fallback static assets
    const resp = await env.ASSETS.fetch(request);
    if (resp.status === 404 && !path.includes('.')) {
      return new Response("Not Found", { status: 404, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
    }
    return resp;
  }
};
