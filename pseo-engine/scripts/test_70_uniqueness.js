const fs = require('fs');
const path = require('path');

const manifest = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/batch_manifest.json'), 'utf8'));
const publishedSlugs = manifest.batches.flatMap(b => b.slugs);

const allCombos = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/all_70_combinations.json'), 'utf8'));
const allHuman = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/all_70_human_solutions.json'), 'utf8'));

const { buildHtmlPage, COMBINATIONS_DATA } = require('./compile_pseo.js');
const { HUMAN_VALUE_SOLUTIONS } = require('./human_solutions_data.js');

// Overwrite COMBINATIONS_DATA and HUMAN_VALUE_SOLUTIONS in memory
for (const [k, v] of Object.entries(allCombos)) {
  COMBINATIONS_DATA[k] = v;
}
for (const [k, v] of Object.entries(allHuman)) {
  HUMAN_VALUE_SOLUTIONS[k] = v;
}

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

console.log(`Generating simulated HTML for all ${publishedSlugs.length} slugs...`);
const pageWordSets = publishedSlugs.map(slug => {
  const parts = slug.replace(/^\//, '').replace(/\/$/, '').split('/');
  const nicheId = parts[1];
  const serviceId = parts[2];
  const html = buildHtmlPage(nicheId, serviceId);
  return {
    slug,
    wordSet: extractWordSet(html)
  };
});

let minDistance = 1.0;
let minPair = '';
let maxDistance = 0.0;
let totalDistance = 0;
let totalPairs = 0;
let violations = [];

for (let i = 0; i < pageWordSets.length; i++) {
  for (let j = i + 1; j < pageWordSets.length; j++) {
    totalPairs++;
    const dist = calculateJaccardDistance(pageWordSets[i].wordSet, pageWordSets[j].wordSet);
    totalDistance += dist;
    if (dist < minDistance) {
      minDistance = dist;
      minPair = `${pageWordSets[i].slug} vs ${pageWordSets[j].slug}`;
    }
    if (dist > maxDistance) {
      maxDistance = dist;
    }
    if (dist <= 0.35) {
      violations.push({
        pair: `${pageWordSets[i].slug} vs ${pageWordSets[j].slug}`,
        distance: `${(dist * 100).toFixed(2)}%`
      });
    }
  }
}

const avgDistance = totalDistance / totalPairs;
console.log(`\n=================================================================`);
console.log(`  JACCARD DISTANCE TEST RESULTS ACROSS ALL ${totalPairs} PAIRS`);
console.log(`=================================================================`);
console.log(`Minimum Uniqueness: ${(minDistance * 100).toFixed(2)}% (Threshold: > 35.0%)`);
console.log(`Average Uniqueness: ${(avgDistance * 100).toFixed(2)}%`);
console.log(`Maximum Uniqueness: ${(maxDistance * 100).toFixed(2)}%`);
console.log(`Lowest Pair:        ${minPair}`);
console.log(`Violations Count:   ${violations.length}`);
if (violations.length > 0) {
  console.log(`Violations:`, violations);
} else {
  console.log(`SUCCESS! 100% of pairs strictly exceed 35% uniqueness threshold.`);
}
console.log(`=================================================================\n`);
