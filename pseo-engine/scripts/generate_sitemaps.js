/**
 * Automated Chunked XML Sitemap Engine
 * Generates XML sitemap index and chunked sitemaps (max 5,000 URLs per file)
 * with dynamic lastmod timestamps per Google Search Console specification.
 */

const fs = require('fs');
const path = require('path');

const MAX_URLS_PER_SITEMAP = 5000;
const BASE_URL = 'https://adorisedigital.com';

function generateSitemaps(publishedSlugs, outputDirs) {
  console.log(`\n=======================================================`);
  console.log(`🗺️ GENERATING CHUNKED XML SITEMAPS (Max: ${MAX_URLS_PER_SITEMAP} URLs/file)`);
  console.log(`=======================================================`);

  const nowIso = new Date().toISOString();

  // Baseline core URLs
  const coreUrls = [
    { loc: `${BASE_URL}/`, priority: '1.0', changefreq: 'daily' },
    { loc: `${BASE_URL}/solutions/`, priority: '0.9', changefreq: 'daily' },
    { loc: `${BASE_URL}/services/`, priority: '0.9', changefreq: 'weekly' },
    { loc: `${BASE_URL}/scout/`, priority: '0.8', changefreq: 'weekly' },
    { loc: `${BASE_URL}/outreach/`, priority: '0.8', changefreq: 'weekly' },
    { loc: `${BASE_URL}/dearmee/`, priority: '0.8', changefreq: 'weekly' },
    { loc: `${BASE_URL}/books/`, priority: '0.8', changefreq: 'weekly' },
    { loc: `${BASE_URL}/social/`, priority: '0.8', changefreq: 'weekly' }
  ];

  // Add all programmatic URLs
  const pseoUrls = publishedSlugs.map(slug => {
    const clean = slug.startsWith('/') ? slug : `/${slug}`;
    const formatted = clean.endsWith('/') ? clean : `${clean}/`;
    return {
      loc: `${BASE_URL}${formatted}`,
      priority: '0.8',
      changefreq: 'weekly'
    };
  });

  const allUrls = [...coreUrls, ...pseoUrls];
  console.log(`Total URLs to index: ${allUrls.length}`);

  // Chunk URLs into groups of MAX_URLS_PER_SITEMAP
  const chunks = [];
  for (let i = 0; i < allUrls.length; i += MAX_URLS_PER_SITEMAP) {
    chunks.push(allUrls.slice(i, i + MAX_URLS_PER_SITEMAP));
  }

  const sitemapFilenames = [];

  outputDirs.forEach(outDir => {
    const sitemapsSubDir = path.join(outDir, 'sitemaps');
    if (!fs.existsSync(sitemapsSubDir)) fs.mkdirSync(sitemapsSubDir, { recursive: true });

    chunks.forEach((chunk, idx) => {
      const sitemapNum = idx + 1;
      const sitemapFileName = `sitemap-${sitemapNum}.xml`;
      sitemapFilenames.push(sitemapFileName);

      let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
      xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

      chunk.forEach(item => {
        xml += `  <url>\n`;
        xml += `    <loc>${item.loc}</loc>\n`;
        xml += `    <lastmod>${nowIso}</lastmod>\n`;
        xml += `    <changefreq>${item.changefreq}</changefreq>\n`;
        xml += `    <priority>${item.priority}</priority>\n`;
        xml += `  </url>\n`;
      });

      xml += `</urlset>\n`;

      const destPath = path.join(sitemapsSubDir, sitemapFileName);
      fs.writeFileSync(destPath, xml, 'utf8');
      console.log(`[OK] Generated chunked sitemap: ${destPath} (${chunk.length} URLs)`);
    });

    // Generate Sitemap Index at root (sitemap.xml)
    let indexXml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
    indexXml += `<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

    chunks.forEach((_, idx) => {
      const sitemapNum = idx + 1;
      indexXml += `  <sitemap>\n`;
      indexXml += `    <loc>${BASE_URL}/sitemaps/sitemap-${sitemapNum}.xml</loc>\n`;
      indexXml += `    <lastmod>${nowIso}</lastmod>\n`;
      indexXml += `  </sitemap>\n`;
    });

    indexXml += `</sitemapindex>\n`;

    const indexPath = path.join(outDir, 'sitemap.xml');
    fs.writeFileSync(indexPath, indexXml, 'utf8');
    console.log(`[OK] Generated root Sitemap Index: ${indexPath}`);
  });

  return {
    totalUrls: allUrls.length,
    chunksCount: chunks.length,
    lastmod: nowIso
  };
}

module.exports = {
  generateSitemaps,
  MAX_URLS_PER_SITEMAP,
  BASE_URL
};

if (require.main === module) {
  const manifestPath = path.resolve(__dirname, '../data/batch_manifest.json');
  let slugs = [];
  if (fs.existsSync(manifestPath)) {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    slugs = manifest.batches.flatMap(b => b.slugs);
  } else {
    slugs = [
      '/solutions/b2b-saas/pseo-engine',
      '/solutions/ecommerce-d2c/ai-agents',
      '/solutions/fintech/outbound-infrastructure',
      '/solutions/healthtech-biotech/ai-agents',
      '/solutions/proptech-realestate/pseo-engine',
      '/solutions/legaltech-professional/ai-agents',
      '/solutions/venture-capital-private-equity/outbound-infrastructure',
      '/solutions/edtech/pseo-engine',
      '/solutions/cybersecurity/cloud-vps-hardening',
      '/solutions/agency-consultancy/pseo-engine',
      '/solutions/b2b-saas/outbound-infrastructure',
      '/solutions/ecommerce-d2c/pseo-engine'
    ];
  }

  const targets = [
    path.resolve(__dirname, '../../adorise-frontend'),
    path.resolve(__dirname, '../public')
  ];
  generateSitemaps(slugs, targets);
}
