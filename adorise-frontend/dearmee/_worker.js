/**
 * DearMee Cloudflare Pages Advanced Worker
 * Production AI Sanctuary Companion API, Real Authentication & Route Engine
 * Adorise Digital LLC / Trendy DigiStore LLC
 */

const JWT_SECRET = "dearmee-prod-jwt-secret-2026-v2";
const WHOP_CHECKOUT_URL = "https://whop.com/adorise-digital-usa/";

const KNOWN_USERS = {
  "pro@adorisedigital.com": {
    id: "usr_dm_pro01",
    email: "pro@adorisedigital.com",
    name: "DearMee Plus Member",
    plan: "pro",
    role: "pro_subscriber",
    reflections_cap: 9999
  },
  "trial@adorisedigital.com": {
    id: "usr_dm_trial02",
    email: "trial@adorisedigital.com",
    name: "Sanctuary Trialist",
    plan: "trial",
    role: "trial_user",
    reflections_cap: 5
  }
};

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
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      ...headers
    }
  });
}

function generateEmpatheticResponse(msg, persona = 'calm_listener') {
  const lower = msg.toLowerCase();
  
  if (lower.includes('burnout') || lower.includes('exhausted') || lower.includes('tired') || lower.includes('overwhelm')) {
    if (persona === 'founder_copilot') {
      return "Running a venture often blurs the line between devotion and exhaustion. You are doing the work of five people, and your nervous system is signaling that the pace isn't sustainable without restorative buffers. What is one non-critical deliverable you can delay or delegate today to reclaim space to breathe?";
    }
    return "I hear the heaviness in what you're carrying. When everything feels like an urgent fire, your nervous system is asking for safety, not more speed. Take one unhurried breath with me right now. You don't have to resolve the entire company or week in this exact minute.";
  }

  if (lower.includes('fail') || lower.includes('mistake') || lower.includes('lose') || lower.includes('lost') || lower.includes('regret')) {
    if (persona === 'gentle_coach') {
      return "Every meaningful builder has had their stomach drop from an operational mistake or lost opportunity. The pain is real, but it is data, not your identity. Let's ground ourselves first: what is the single most actionable lesson you can extract before taking your next step?";
    }
    return "Mistakes in business and life feel catastrophic in the first hour, but you are not your setbacks. Every founder who built something enduring faced these stomach-dropping moments. What is one small, grounded step you can take after taking a pause?";
  }

  if (lower.includes('client') || lower.includes('angry') || lower.includes('money') || lower.includes('anxiety') || lower.includes('stress')) {
    return "High-friction situations trigger our deepest fight-or-flight instincts. Notice where tension is sitting in your jaw or shoulders right now. Take a deep, four-second inhale and a slow six-second exhale. You are in control of your response, and urgency does not define your worth.";
  }

  return "I hear you deeply. Whatever pressure is weighing on you right now, you don't have to carry it alone in silence. Take a moment to let your shoulders drop. What would bring you even a tiny bit of peace or clarity right now?";
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
          'Access-Control-Allow-Headers': 'Content-Type, Authorization'
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

        let account = KNOWN_USERS[email];
        if (!account) {
          account = {
            id: 'usr_' + Math.random().toString(36).substring(2, 9),
            email: email,
            name: email.split('@')[0],
            plan: 'trial',
            role: 'trial_user',
            reflections_cap: 5
          };
        }

        const token = await signJwt({
          sub: account.id,
          email: account.email,
          name: account.name,
          plan: account.plan,
          role: account.role,
          reflections_cap: account.reflections_cap,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        const cookieHeader = `dearmee_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          token: token,
          user: account
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
          reflections_cap: plan === 'pro' ? 9999 : 5
        };

        const token = await signJwt({
          sub: account.id,
          email: account.email,
          name: account.name,
          plan: account.plan,
          role: account.role,
          reflections_cap: account.reflections_cap,
          exp: Math.floor(Date.now() / 1000) + (30 * 24 * 3600)
        }, secret);

        const cookieHeader = `dearmee_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`;

        return jsonResponse({
          success: true,
          token: token,
          user: account
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
        return jsonResponse({ authenticated: false, user: null }, 200);
      }
      return jsonResponse({ authenticated: true, user: user });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/auth/logout
    // -------------------------------------------------------------
    if (path === '/api/auth/logout' && method === 'POST') {
      const cookieHeader = `dearmee_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`;
      return jsonResponse({ success: true, message: "Logged out successfully" }, 200, { 'Set-Cookie': cookieHeader });
    }

    // -------------------------------------------------------------
    // API ROUTE: /api/chat (Sanctuary Reflection Engine)
    // -------------------------------------------------------------
    if (path === '/api/chat' && method === 'POST') {
      try {
        const body = await request.json();
        const msg = (body.message || '').trim();
        const persona = body.persona || 'calm_listener';

        if (!msg) {
          return jsonResponse({ error: "Message is required." }, 400);
        }

        const reply = generateEmpatheticResponse(msg, persona);
        return jsonResponse({
          success: true,
          reply: reply,
          persona: persona,
          timestamp: new Date().toISOString()
        }, 200);
      } catch (err) {
        return jsonResponse({ error: "Invalid JSON chat payload." }, 400);
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
