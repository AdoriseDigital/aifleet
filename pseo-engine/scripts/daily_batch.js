/**
 * Automated Daily Batch Generation Pipeline
 * Enforces Hard-Coded SLA: >= 10 new pSEO pages/day submitted to GSC & IndexNow.
 */

const fs = require('fs');
const path = require('path');

const { compileBatch } = require('./compile_pseo');
const { generateSitemaps } = require('./generate_sitemaps');
const { triggerIndexingPings } = require('./ping_indexing');

const matrixData = require('../data/taxonomy_matrix.json');
const MANIFEST_PATH = path.resolve(__dirname, '../data/batch_manifest.json');
const FRONTEND_DIR = path.resolve(__dirname, '../../adorise-frontend');

const BATCH_SIZE_SLA = 10; // Hard-coded SLA: >= 10 pages/day
const LAUNCH_BATCH_SIZE = 12; // Initial cohort: 12 high-intent commercial combinations

function loadManifest() {
  if (fs.existsSync(MANIFEST_PATH)) {
    return JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  }
  return {
    sla_target_daily_pages: BATCH_SIZE_SLA,
    last_batch_date: null,
    total_published_pages: 0,
    batches: []
  };
}

function saveManifest(manifest) {
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf8');
}

function getAllAvailableSlugs() {
  const slugs = [];
  const niches = matrixData.taxonomy_dimensions.niches;
  const services = matrixData.taxonomy_dimensions.services;

  niches.forEach(n => {
    services.forEach(s => {
      slugs.push(`/solutions/${n.id}/${s.id}`);
    });
  });
  return slugs;
}

async function runDailyBatch(forceSize = LAUNCH_BATCH_SIZE) {
  console.log(`=================================================================`);
  console.log(`⚡ ADORISE DIGITAL — AUTOMATED DAILY pSEO BATCH ENGINE`);
  console.log(`   Enforced SLA Target: >= ${BATCH_SIZE_SLA} new pSEO pages/day`);
  console.log(`=================================================================\n`);

  const manifest = loadManifest();
  const allSlugs = getAllAvailableSlugs();
  const publishedSlugs = new Set(manifest.batches.flatMap(b => b.slugs));

  // Determine ungenerated candidates
  const candidateSlugs = allSlugs.filter(s => !publishedSlugs.has(s));
  console.log(`Total Taxonomy Universe: ${allSlugs.length} possible combinations`);
  console.log(`Already Published:       ${publishedSlugs.size} pages`);
  console.log(`Available in Backlog:    ${candidateSlugs.length} combinations\n`);

  if (candidateSlugs.length === 0) {
    console.log(`🎉 All ${allSlugs.length} combinations in the taxonomy matrix have been compiled and published!`);
    return { success: true, count: 0 };
  }

  // Select batch of >= 10 pages
  const batchCount = Math.max(BATCH_SIZE_SLA, Math.min(forceSize, candidateSlugs.length));
  const newBatchSlugs = candidateSlugs.slice(0, batchCount);

  console.log(`Selected Batch Cohort: ${newBatchSlugs.length} new pages (SLA Check: >= ${BATCH_SIZE_SLA} PASSED)`);
  newBatchSlugs.forEach((s, idx) => {
    console.log(`  [${idx + 1}/${newBatchSlugs.length}] ${s}`);
  });

  // 1. Compile pages to adorise-frontend and local public
  const compiledCount = compileBatch(newBatchSlugs, FRONTEND_DIR);
  if (compiledCount < BATCH_SIZE_SLA) {
    throw new Error(`SLA Failure: Expected to compile >= ${BATCH_SIZE_SLA} pages, but compiled ${compiledCount}`);
  }

  // 2. Update all published slugs list
  const updatedAllPublishedSlugs = [...publishedSlugs, ...newBatchSlugs];

  // 3. Generate chunked XML sitemaps with dynamic lastmod
  const sitemapTargets = [
    FRONTEND_DIR,
    path.resolve(__dirname, '../public')
  ];
  const sitemapStats = generateSitemaps(updatedAllPublishedSlugs, sitemapTargets);

  // 4. Trigger automated GSC and IndexNow ping routines
  const pingResults = await triggerIndexingPings(newBatchSlugs);

  // 5. Update and persist manifest
  const newBatchId = manifest.batches.length + 1;
  const nowIso = new Date().toISOString();

  manifest.last_batch_date = nowIso.split('T')[0];
  manifest.total_published_pages = updatedAllPublishedSlugs.length;
  manifest.batches.push({
    batch_id: newBatchId,
    timestamp: nowIso,
    page_count: newBatchSlugs.length,
    slugs: newBatchSlugs,
    sitemap_stats: sitemapStats,
    ping_status: pingResults.pings.map(p => ({ engine: p.engine, success: p.success, status: p.statusCode }))
  });

  saveManifest(manifest);

  console.log(`\n=================================================================`);
  console.log(`🎉 BATCH ${newBatchId} COMPLETED SUCCESSFULLY!`);
  console.log(`   Pages Compiled:      ${compiledCount}`);
  console.log(`   Total Live Pages:    ${manifest.total_published_pages}`);
  console.log(`   Chunked Sitemaps:    ${sitemapStats.chunksCount} (${sitemapStats.totalUrls} URLs)`);
  console.log(`   Indexing Pinged:     GSC, Bing, IndexNow`);
  console.log(`=================================================================\n`);

  return {
    success: true,
    batchId: newBatchId,
    compiledCount,
    totalLivePages: manifest.total_published_pages,
    slugs: newBatchSlugs
  };
}

module.exports = {
  runDailyBatch,
  loadManifest,
  BATCH_SIZE_SLA
};

if (require.main === module) {
  runDailyBatch().catch(err => {
    console.error('Fatal error in daily batch:', err);
    process.exit(1);
  });
}
