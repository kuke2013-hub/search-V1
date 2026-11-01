// Generates SQL for later manual import into a PRIVATE D1 database.
// Run after migrations/0001_init.sql; this script does NOT perform remote writes.
import fs from 'node:fs';
const seed=JSON.parse(fs.readFileSync('data/research_seed.json','utf8'));
const q=s=>"'"+String(s??'').replaceAll("'","''")+"'";
const kind = { 'Talent agency / management candidate':'agency', 'Casting office / director':'casting_practice', 'Acting coach / studio':'coach_studio', 'Actor event / network':'event_organizer', 'Industry directory / source':'industry_source', 'Corporate watchlist':'company'};
const verify = o => /historical/i.test(o.evidenceTier||'')||/historical/i.test(o.verification||'')?'candidate':
 /Current official|Official office/i.test(o.verification||'')?'website_checked':
 /Official website/i.test(o.verification||'')?'website_checked':
 /directory|CDA|CDG|member/i.test(o.verification||'')?'source_listed':'candidate';
let lines=['PRAGMA foreign_keys = ON;','BEGIN TRANSACTION;'];
for(const o of [...seed.industry,...seed.corporate]){
 const type=kind[o.category]; if(!type) throw Error(`Unsupported entity type ${o.category}`);
 const city=(o.london||'').toLowerCase().includes('london')&&!/not checked|unconfirmed|uk listing/.test((o.london||'').toLowerCase())?'London':null;
 lines.push(`INSERT OR IGNORE INTO entities(id,canonical_name,entity_type,city,website,verification_status) VALUES(${[o.id,o.name,type,city,o.website||null,verify(o)].map(v=>v===null?'NULL':q(v)).join(',')});`);
}
for(let i=0;i<seed.sources.length;i++){
 const s=seed.sources[i];
 lines.push(`INSERT OR IGNORE INTO sources(id,label,root_url,category,access_method,automation_approved,status) VALUES(${["seed-source-"+String(i+1).padStart(2,'0'),s.name,s.url,s.type,'manual',0,'review_required'].map((v,j)=>j===5?q('0'):q(v)).join(',')});`);
}
lines.push('COMMIT;');
const target=process.argv[2] || 'seed_import.sql';fs.writeFileSync(target,lines.join('\n')+'\n');
console.log(`Generated ${seed.industry.length+seed.corporate.length} entities and ${seed.sources.length} inactive sources -> ${target}`);