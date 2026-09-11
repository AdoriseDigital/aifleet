/**
 * Automated Google Search Console & IndexNow Ping Engine
 * Notifies search engines of new pSEO batches and updated sitemaps.
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const SITEMAP_URL = 'https://adorisedigital.com/sitemap.xml';
const HOST = 'adorisedigital.com';
const INDEXNOW_KEY = 'adorise-indexnow-key-2026';

function sendGetRequest(urlStr) {
  return new Promise((resolve) => {
    try {
      const url = new URL(urlStr);
      const client = url.protocol === 'https:' ? https : http;
      
      const req = client.get(urlStr, { timeout: 8000 }, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          resolve({
            url: urlStr,
            statusCode: res.statusCode,
            success: res.statusCode >= 200 && res.statusCode < 400,
            responseSnippet: body.slice(0, 120).trim()
          });
        });
      });

      req.on('error', (err) => {
        resolve({
          url: urlStr,
          statusCode: null,
          success: false,
          error: err.message
        });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({
          url: urlStr,
          statusCode: 408,
          success: false,
          error: 'Request timeout'
        });
      });
    } catch (e) {
      resolve({
        url: urlStr,
        statusCode: null,
        success: false,
        error: e.message
      });
    }
  });
}

function sendIndexNowPost(urlList) {
  return new Promise((resolve) => {
    try {
      const payload = JSON.stringify({
        host: HOST,
        key: INDEXNOW_KEY,
        keyLocation: `https://${HOST}/${INDEXNOW_KEY}.txt`,
        urlList: urlList.map(u => u.startsWith('http') ? u : `https://${HOST}${u.startsWith('/') ? u : '/' + u}`)
      });

      const options = {
        hostname: 'api.indexnow.org',
        port: 443,
        path: '/indexnow',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Content-Length': Buffer.byteLength(payload)
        },
        timeout: 8000
      };

      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          resolve({
            endpoint: 'https://api.indexnow.org/indexnow',
            statusCode: res.statusCode,
            success: res.statusCode === 200 || res.statusCode === 202,
            response: body
          });
        });
      });

      req.on('error', (err) => {
        resolve({
          endpoint: 'https://api.indexnow.org/indexnow',
          statusCode: null,
          success: false,
          error: err.message
        });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({
          endpoint: 'https://api.indexnow.org/indexnow',
          statusCode: 408,
          success: false,
          error: 'Timeout'
        });
      });

      req.write(payload);
      req.end();
    } catch (e) {
      resolve({
        endpoint: 'https://api.indexnow.org/indexnow',
        statusCode: null,
        success: false,
        error: e.message
      });
    }
  });
}

async function triggerIndexingPings(newSlugs = []) {
  console.log(`\n=======================================================`);
  console.log(`📡 EXECUTING SEARCH ENGINE INDEXATION PING ROUTINES`);
  console.log(`=======================================================`);

  const results = {
    timestamp: new Date().toISOString(),
    sitemap_url: SITEMAP_URL,
    pings: []
  };

  // 1. Google Search Console Sitemap Ping
  const gscUrl = `https://www.google.com/ping?sitemap=${encodeURIComponent(SITEMAP_URL)}`;
  console.log(`Pinging Google Search Console: ${gscUrl}`);
  const gscRes = await sendGetRequest(gscUrl);
  results.pings.push({ engine: 'Google Search Console', ...gscRes });
  console.log(`  -> GSC Status: ${gscRes.statusCode || gscRes.error} (Success: ${gscRes.success})`);

  // 2. Bing Sitemap Ping
  const bingUrl = `https://www.bing.com/ping?sitemap=${encodeURIComponent(SITEMAP_URL)}`;
  console.log(`Pinging Bing Search: ${bingUrl}`);
  const bingRes = await sendGetRequest(bingUrl);
  results.pings.push({ engine: 'Bing', ...bingRes });
  console.log(`  -> Bing Status: ${bingRes.statusCode || bingRes.error} (Success: ${bingRes.success})`);

  // 3. IndexNow API Ping
  if (newSlugs.length > 0) {
    console.log(`Submitting ${newSlugs.length} URLs to IndexNow API...`);
    const indexNowRes = await sendIndexNowPost(newSlugs);
    results.pings.push({ engine: 'IndexNow', ...indexNowRes, submitted_urls: newSlugs.length });
    console.log(`  -> IndexNow Status: ${indexNowRes.statusCode || indexNowRes.error} (Success: ${indexNowRes.success})`);
  }

  // Save audit log
  const logDir = path.resolve(__dirname, '../logs');
  if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
  
  const logPath = path.join(logDir, 'indexing_audit.log');
  const logEntry = `[${results.timestamp}] Indexed ${newSlugs.length} URLs. GSC: ${gscRes.statusCode || 'ERR'}, Bing: ${bingRes.statusCode || 'ERR'}\n`;
  fs.appendFileSync(logPath, logEntry, 'utf8');

  const jsonReportPath = path.join(logDir, 'latest_ping_report.json');
  fs.writeFileSync(jsonReportPath, JSON.stringify(results, null, 2), 'utf8');

  console.log(`[OK] Indexing audit log updated: ${logPath}`);
  return results;
}

module.exports = {
  triggerIndexingPings,
  SITEMAP_URL,
  HOST
};

if (require.main === module) {
  const sampleSlugs = [
    '/solutions/b2b-saas/pseo-engine/',
    '/solutions/ecommerce-d2c/ai-agents/',
    '/solutions/fintech/outbound-infrastructure/'
  ];
  triggerIndexingPings(sampleSlugs);
}
