const fs = require('fs');
const path = require('path');
const manifest = JSON.parse(fs.readFileSync('pseo-engine/data/batch_manifest.json', 'utf8'));
const publishedSlugs = manifest.batches.flatMap(b => b.slugs);

const { COMBINATIONS_DATA, buildHtmlPage } = require('./compile_pseo.js');
const { generateFullCombination } = require('./advanced_tailored_schemas.js');

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

// Generate the 70 pages:
// Use Batch 1 COMBINATIONS_DATA if already present, or generateFullCombination
const pageWordSets = publishedSlugs.map(slug => {
  const parts = slug.replace(/^\//, '').replace(/\/$/, '').split('/');
  const nicheId = parts[1];
  const serviceId = parts[2];
  const key = `${nicheId}/${serviceId}`;

  // If in COMBINATIONS_DATA, use it, otherwise use generateFullCombination
  if (!COMBINATIONS_DATA[key]) {
    COMBINATIONS_DATA[key] = generateFullCombination(nicheId, serviceId);
  }

  const html = buildHtmlPage(nicheId, serviceId);
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
  console.log('Sample violations:', violations.slice(0, 5));
}
