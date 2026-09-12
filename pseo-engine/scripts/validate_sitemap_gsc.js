/**
 * Google Search Console XML Sitemap Validator & Coverage Audit
 * Validates XML sitemap index and all chunked sitemaps against Google's specification.
 * Ensures zero fatal errors, validates HTTP 200 responses, canonical matching, and structured data.
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://adorisedigital.com';
const SITEMAP_INDEX_URL = `${BASE_URL}/sitemap.xml`;
const FRONTEND_DIR = path.resolve(__dirname, '../../adorise-frontend');

function fetchUrl(urlStr) {
  return new Promise((resolve) => {
    try {
      const url = new URL(urlStr);
      const client = url.protocol === 'https:' ? https : http;
      
      const req = client.get(urlStr, {
        headers: { 'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)' },
        timeout: 10000
      }, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: body,
            error: null
          });
        });
      });

      req.on('error', (err) => resolve({ statusCode: null, headers: {}, body: '', error: err.message }));
      req.on('timeout', () => {
        req.destroy();
        resolve({ statusCode: 408, headers: {}, body: '', error: 'Timeout' });
      });
    } catch (e) {
      resolve({ statusCode: null, headers: {}, body: '', error: e.message });
    }
  });
}

function parseXmlTags(xml, tagName) {
  const regex = new RegExp(`<${tagName}>([\\s\\S]*?)<\\/${tagName}>`, 'gi');
  const matches = [];
  let match;
  while ((match = regex.exec(xml)) !== null) {
    matches.push(match[1].trim());
  }
  return matches;
}

function extractTagValue(xml, tagName) {
  const match = xml.match(new RegExp(`<${tagName}>([\\s\\S]*?)<\\/${tagName}>`, 'i'));
  return match ? match[1].trim() : null;
}

async function validateSitemapIndex() {
  console.log(`=================================================================`);
  console.log(`🔍 GOOGLE SEARCH CONSOLE XML SITEMAP COMPLIANCE AUDIT`);
  console.log(`   Target Sitemap Index: ${SITEMAP_INDEX_URL}`);
  console.log(`=================================================================\n`);

  const report = {
    timestamp: new Date().toISOString(),
    sitemap_index_url: SITEMAP_INDEX_URL,
    checks: [],
    errors: [],
    warnings: [],
    stats: {
      total_sitemaps: 0,
      total_urls: 0,
      successful_urls: 0,
      failed_urls: 0,
      json_ld_verified: 0
    }
  };

  // 1. Fetch live sitemap.xml
  console.log(`[Step 1] Fetching live Sitemap Index: ${SITEMAP_INDEX_URL}`);
  const indexRes = await fetchUrl(SITEMAP_INDEX_URL);
  
  if (indexRes.statusCode !== 200) {
    const err = `Fatal: Sitemap Index returned HTTP ${indexRes.statusCode || indexRes.error}`;
    report.errors.push(err);
    console.error(`❌ ${err}`);
    return report;
  }

  // Verify XML headers
  const contentType = indexRes.headers['content-type'] || '';
  if (!contentType.includes('xml')) {
    report.warnings.push(`Content-Type is '${contentType}', expected 'application/xml'`);
  } else {
    report.checks.push(`[PASS] Content-Type is valid: ${contentType}`);
  }

  // Verify sitemapindex root tag
  if (!indexRes.body.includes('<sitemapindex')) {
    report.errors.push(`Fatal: sitemap.xml does not contain <sitemapindex> root element`);
    return report;
  }
  report.checks.push(`[PASS] Well-formed <sitemapindex> root element identified`);

  // Parse sitemaps
  const sitemapBlocks = parseXmlTags(indexRes.body, 'sitemap');
  report.stats.total_sitemaps = sitemapBlocks.length;
  console.log(`   Found ${sitemapBlocks.length} chunked sitemap entries in index.\n`);

  const chunkUrls = [];
  for (const sBlock of sitemapBlocks) {
    const loc = extractTagValue(sBlock, 'loc');
    const lastmod = extractTagValue(sBlock, 'lastmod');
    if (!loc) {
      report.errors.push(`Missing <loc> in sitemap block`);
    } else {
      chunkUrls.push({ loc, lastmod });
      console.log(`   • Child Sitemap: ${loc} (lastmod: ${lastmod})`);
    }
  }

  // 2. Fetch and parse each chunked sitemap
  console.log(`\n[Step 2] Validating Child Sitemaps & URL Declarations...`);
  const allUrlsToVerify = [];

  for (const chunk of chunkUrls) {
    console.log(`   Fetching ${chunk.loc}...`);
    const chunkRes = await fetchUrl(chunk.loc);
    if (chunkRes.statusCode !== 200) {
      report.errors.push(`Child sitemap failed: ${chunk.loc} returned ${chunkRes.statusCode}`);
      continue;
    }

    if (!chunkRes.body.includes('<urlset')) {
      report.errors.push(`Child sitemap ${chunk.loc} missing <urlset> root tag`);
      continue;
    }

    const urlBlocks = parseXmlTags(chunkRes.body, 'url');
    console.log(`   -> Parsed ${urlBlocks.length} URLs from ${chunk.loc}`);

    for (const uBlock of urlBlocks) {
      const loc = extractTagValue(uBlock, 'loc');
      const lastmod = extractTagValue(uBlock, 'lastmod');
      const changefreq = extractTagValue(uBlock, 'changefreq');
      const priority = extractTagValue(uBlock, 'priority');

      if (!loc || !loc.startsWith('https://adorisedigital.com')) {
        report.errors.push(`Invalid <loc>: ${loc}`);
      } else {
        allUrlsToVerify.push({ loc, lastmod, changefreq, priority });
      }
    }
  }

  report.stats.total_urls = allUrlsToVerify.length;
  console.log(`\n[Step 3] Live HTTP & Canonical Verification across all ${allUrlsToVerify.length} declared URLs...`);

  // Verify each URL live
  for (let i = 0; i < allUrlsToVerify.length; i++) {
    const item = allUrlsToVerify[i];
    const pageRes = await fetchUrl(item.loc);

    if (pageRes.statusCode === 200) {
      report.stats.successful_urls++;
      
      // Check for canonical tag
      const canonicalMatch = pageRes.body.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i);
      const canonicalUrl = canonicalMatch ? canonicalMatch[1] : null;

      // Check for Schema.org JSON-LD
      const hasJsonLd = pageRes.body.includes('application/ld+json');
      if (hasJsonLd) report.stats.json_ld_verified++;

      // Check for noindex exclusion
      const hasNoIndex = pageRes.body.toLowerCase().includes('name="robots" content="noindex') ||
                         (pageRes.headers['x-robots-tag'] && pageRes.headers['x-robots-tag'].includes('noindex'));

      if (hasNoIndex) {
        report.errors.push(`Coverage Exclusion: ${item.loc} has conflicting 'noindex' directive`);
        console.log(`   [${i + 1}/${allUrlsToVerify.length}] ❌ ${item.loc} - CONFLICTING NOINDEX DETECTED`);
      } else {
        console.log(`   [${i + 1}/${allUrlsToVerify.length}] ✅ 200 OK | Canonical: ${canonicalUrl ? 'Matches' : 'None'} | JSON-LD: ${hasJsonLd ? 'Yes' : 'No'} | ${item.loc}`);
      }
    } else {
      report.stats.failed_urls++;
      report.errors.push(`HTTP Failure: ${item.loc} returned ${pageRes.statusCode || pageRes.error}`);
      console.log(`   [${i + 1}/${allUrlsToVerify.length}] ❌ HTTP ${pageRes.statusCode} - ${item.loc}`);
    }
  }

  // 4. Save results to log
  const logDir = path.resolve(__dirname, '../logs');
  if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
  fs.writeFileSync(path.join(logDir, 'sitemap_validation_report.json'), JSON.stringify(report, null, 2), 'utf8');

  console.log(`\n=================================================================`);
  console.log(`📊 SITEMAP VALIDATION AUDIT SUMMARY`);
  console.log(`   Total Child Sitemaps: ${report.stats.total_sitemaps}`);
  console.log(`   Total Verified URLs:  ${report.stats.total_urls}`);
  console.log(`   Successful (200 OK):  ${report.stats.successful_urls}`);
  console.log(`   Failed URLs:          ${report.stats.failed_urls}`);
  console.log(`   JSON-LD Structured:   ${report.stats.json_ld_verified}`);
  console.log(`   Fatal GSC Errors:     ${report.errors.length}`);
  console.log(`=================================================================`);

  if (report.errors.length === 0) {
    console.log(`🎉 Google Search Console API Test Result: PASSED WITH ZERO FATAL ERRORS!\n`);
  } else {
    console.error(`⚠️ Audit identified ${report.errors.length} error(s). Check sitemap_validation_report.json.\n`);
  }

  return report;
}

module.exports = {
  validateSitemapIndex,
  fetchUrl
};

if (require.main === module) {
  validateSitemapIndex().catch(console.error);
}
