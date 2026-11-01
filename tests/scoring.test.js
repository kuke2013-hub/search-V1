import test from "node:test";
import assert from "node:assert/strict";
import { scoreOpportunity } from "../src/scoring.js";

const sample = {
  sourceStatus: "success",
  sourceUrl: "https://example.org/announcement",
  observedAt: "2026-11-01T00:00:00Z",
  evidenceSummary: "Published announcement",
  ratings: {
    evidence: 5, businessFit: 4, timing: 3, reachability: 4, potentialValue: 2
  }
};

test("well-formed evidence gets a rank, not a booking probability", () => {
  const result = scoreOpportunity(sample);
  assert.equal(result.rankable, true);
  assert.equal(result.score, 73);
  assert.equal(result.kind, "heuristic_not_probability");
  assert.equal(result.outreachEligible, false);
});

test("failed fetch does not produce a lead score", () => {
  assert.equal(scoreOpportunity({...sample, sourceStatus:"failed"}).rankable, false);
});
test("missing URL is not rankable", () => {
  assert.equal(scoreOpportunity({...sample, sourceUrl:""}).rankable, false);
});
test("missing evidence date is not rankable", () => {
  assert.equal(scoreOpportunity({...sample, observedAt:null}).rankable, false);
});
test("nonsensical user/AI ratings are rejected", () => {
  assert.equal(scoreOpportunity({...sample, ratings:{...sample.ratings, timing:99}}).rankable, false);
});
test("outreach eligibility needs explicit human and privacy approvals", () => {
  const c={...sample, humanApproved:true, privacyReviewed:true,
    contactVerified:true, suppressionChecked:true, suppressed:false};
  assert.equal(scoreOpportunity(c).outreachEligible, true);
  assert.equal(scoreOpportunity({...c, suppressed:true}).outreachEligible, false);
});
test("unknown suppression never passes outreach review", () => {
  const c={...sample, humanApproved:true, privacyReviewed:true,
    contactVerified:true, suppressionChecked:true};
  assert.equal(scoreOpportunity(c).outreachEligible, false);
});
test("unverified contact never passes outreach review", () => {
  const c={...sample, humanApproved:true, privacyReviewed:true,
    contactVerified:false, suppressionChecked:true, suppressed:false};
  assert.equal(scoreOpportunity(c).outreachEligible, false);
});
