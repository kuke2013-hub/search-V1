import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const seed=JSON.parse(fs.readFileSync(new URL('../data/research_seed.json',import.meta.url),'utf8'));
const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
test('snapshot contains exactly the research records used in this site',()=>{
 assert.equal(seed.industry.length,323);
 assert.equal(seed.corporate.length,7);
 assert.equal(seed.sources.length,10);
});
test('every entry has an identity, a category and an original source',()=>{
 for(const o of [...seed.industry,...seed.corporate]){
  assert.ok(o.id);assert.ok(o.name);assert.ok(o.category);
  assert.match(o.source,/^https:\/\//);
 }
});
test('every corporate seed prospect has its own London office evidence',()=>{
 for(const o of seed.corporate){assert.match(o.london,/London/);assert.match(o.verification,/Official office page/);}
});
test('published site contains no claims of automatic lead collection',()=>{
 assert.match(html,/0 live monitors/);
 assert.match(html,/not a live lead feed/);
 assert.match(html,/not likelihood of booking/);
});
test('site has embedded complete snapshot and no third-party script dependency',()=>{
 assert.match(html,/<script id="seed-data" type="application\/json">/);
 assert.ok(!/<script\s+src=/i.test(html));
 const match=html.match(/<script id="seed-data" type="application\/json">([\s\S]*?)<\/script>/);
 assert.ok(match);const embedded=JSON.parse(match[1]);
 assert.equal(embedded.industry.length,323);
 assert.equal(embedded.corporate.length,7);
});