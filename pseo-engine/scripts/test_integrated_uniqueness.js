// Test full compile_pseo with generateCombinationData fallback
const fs = require('fs');
const path = require('path');
const manifest = JSON.parse(fs.readFileSync('pseo-engine/data/batch_manifest.json', 'utf8'));
const publishedSlugs = manifest.batches.flatMap(b => b.slugs);

const { COMBINATIONS_DATA, buildHtmlPage } = require('./compile_pseo.js');
const { generateCombinationData } = require('./combination_data_generator.js');

// Temporary monkey-patch compile_pseo for this test
// In compile_pseo.js, we can wire generateCombinationData directly into getCombinationData!

function extractWordSet(text) {
  const mainMatch = text.match(/<main[\s\S]*?<\/main>/);
  const content = mainMatch ? mainMatch[0] : text;
  const stripped = content.replace(/<[^>]+>/g, ' ').toLowerCase();
  const words = stripped.match(/[a-z]{3,}/g) || [];
  return new Set(words);
}

function calculateJaccardDistance(setA, setB) {
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return 1 - (intersection.size / union.size);
}

// Generate the 70 pages
const pageWordSets = publishedSlugs.map(slug => {
  const parts = slug.replace(/^\//, '').replace(/\/$/, '').split('/');
  const nicheId = parts[1];
  const serviceId = parts[2];

  // If slug is in COMBINATIONS_DATA, use buildHtmlPage directly
  // Otherwise use buildHtmlPage with data from generateCombinationData
  let html;
  const key = `${nicheId}/${serviceId}`;
  if (COMBINATIONS_DATA[key]) {
    html = buildHtmlPage(nicheId, serviceId);
  } else {
    // We can simulate what buildHtmlPage does with generateCombinationData
    const data = generateCombinationData(nicheId, serviceId);
    // Let's inject into COMBINATIONS_DATA temporarily
    COMBINATIONS_DATA[key] = data;
    html = buildHtmlPage(nicheId, serviceId);
    delete COMBINATIONS_DATA[key];
  }

  return {
    slug,
    wordSet: extractWordSet(html)
  };
});

let minDistance = 1.0;
let minPair = '';
let violations = [];
let totalPairs = 0;

for (let i = 0; i < pageWordSets.length; i++) {
  for (let j = i + 1; j < pageWordSets.length; j++) {
    totalPairs++;
    const dist = calculateJaccardDistance(pageWordSets[i].wordSet, pageWordSets[j].wordSet);
    if (dist < minDistance) {
      minDistance = dist;
      minPair = `${pageWordSets[i].slug} vs ${pageWordSets[j].slug}`;
    }
    if (dist <= 0.35) {
      violations.push({
        pair: `${pageWordSets[i].slug} vs ${pageWordSets[j].slug}`,
        distance: (dist * 100).toFixed(2) + '%'
      });
    }
  }
}

console.log(`Total Pairs Tested: ${totalPairs}`);
console.log(`Minimum Uniqueness: ${(minDistance * 100).toFixed(2)}% (Threshold: > 35.0%)`);
console.log(`Minimum Pair: ${minPair}`);
console.log(`Violations Count: ${violations.length}`);
if (violations.length > 0) {
  console.log('Sample violations:', violations.slice(0, 10));
}
