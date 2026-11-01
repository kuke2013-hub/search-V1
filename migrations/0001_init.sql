PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS entities (
  id TEXT PRIMARY KEY,
  canonical_name TEXT NOT NULL,
  entity_type TEXT NOT NULL CHECK(entity_type IN ('company','agency','casting_practice','school','coach_studio','event_organizer','industry_source')),
  city TEXT,
  website TEXT,
  verification_status TEXT NOT NULL DEFAULT 'candidate' CHECK(verification_status IN ('candidate','source_listed','website_checked','verified','rejected')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_entities_type_status ON entities(entity_type, verification_status);

CREATE TABLE IF NOT EXISTS sources (
  id TEXT PRIMARY KEY,
  label TEXT NOT NULL,
  root_url TEXT NOT NULL,
  category TEXT NOT NULL,
  access_method TEXT NOT NULL CHECK(access_method IN ('manual','public_api','rss','approved_web','internal')),
  automation_approved INTEGER NOT NULL DEFAULT 0 CHECK(automation_approved IN (0,1)),
  status TEXT NOT NULL DEFAULT 'review_required' CHECK(status IN ('review_required','active','paused','blocked','retired')),
  terms_checked_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_checks (
  id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL REFERENCES sources(id),
  checked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  outcome TEXT NOT NULL CHECK(outcome IN ('success','empty','blocked','failed','not_checked')),
  http_status INTEGER,
  content_hash TEXT,
  error_summary TEXT,
  discovered_count INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_source_checks_source_time ON source_checks(source_id,checked_at DESC);

CREATE TABLE IF NOT EXISTS signals (
  id TEXT PRIMARY KEY,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  source_id TEXT NOT NULL REFERENCES sources(id),
  source_url TEXT NOT NULL,
  signal_type TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  event_date TEXT,
  evidence_summary TEXT NOT NULL,
  evidence_hash TEXT NOT NULL,
  source_check_id TEXT REFERENCES source_checks(id),
  review_state TEXT NOT NULL DEFAULT 'pending' CHECK(review_state IN ('pending','accepted','rejected','stale')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(source_id,evidence_hash)
);
CREATE INDEX IF NOT EXISTS idx_signals_entity_time ON signals(entity_id,observed_at DESC);

CREATE TABLE IF NOT EXISTS opportunities (
  id TEXT PRIMARY KEY,
  entity_id TEXT NOT NULL REFERENCES entities(id),
  signal_id TEXT REFERENCES signals(id),
  segment TEXT NOT NULL CHECK(segment IN ('corporate','actor_partner','existing_client','inbound','direct_actor')),
  stage TEXT NOT NULL DEFAULT 'new' CHECK(stage IN ('new','research','qualified','approved','contacted','replied','quoted','booked','lost','closed')),
  evidence_score INTEGER CHECK(evidence_score BETWEEN 0 AND 100),
  score_reason TEXT,
  owner_note TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_opportunities_stage ON opportunities(stage,segment);

CREATE TABLE IF NOT EXISTS contacts (
  id TEXT PRIMARY KEY,
  entity_id TEXT REFERENCES entities(id),
  display_name TEXT,
  job_role TEXT,
  business_email TEXT,
  contact_kind TEXT NOT NULL CHECK(contact_kind IN ('general_business','named_employee','individual','unknown')),
  lawful_basis_review TEXT NOT NULL DEFAULT 'not_reviewed',
  privacy_notice_at TEXT,
  contact_checked_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS outreach (
  id TEXT PRIMARY KEY,
  opportunity_id TEXT NOT NULL REFERENCES opportunities(id),
  contact_id TEXT REFERENCES contacts(id),
  channel TEXT NOT NULL,
  draft_text TEXT,
  approval_state TEXT NOT NULL DEFAULT 'draft' CHECK(approval_state IN ('draft','approved','rejected')),
  sent_at TEXT,
  outcome TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS suppression (
  address_hmac TEXT PRIMARY KEY,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
  id TEXT PRIMARY KEY,
  entity_id TEXT REFERENCES entities(id),
  opportunity_id TEXT REFERENCES opportunities(id),
  booked_at TEXT NOT NULL,
  gross_amount_pence INTEGER NOT NULL CHECK(gross_amount_pence >= 0),
  estimated_cost_pence INTEGER CHECK(estimated_cost_pence >= 0),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scheduler_runs (
  id TEXT PRIMARY KEY,
  started_at TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('not_configured','running','success','partial','failed')),
  source_count INTEGER NOT NULL DEFAULT 0,
  completed_at TEXT,
  error_summary TEXT
);
