// Transparent heuristic, NOT a trained prediction or booking probability.
const WEIGHTS = Object.freeze({
  evidence: 25,
  businessFit: 20,
  timing: 20,
  reachability: 15,
  potentialValue: 20
});

export function scoreOpportunity(candidate) {
  if (!candidate || !["success", "manual_verified"].includes(candidate.sourceStatus)) {
    return { rankable: false, score: null, reason: "No successful source verification" };
  }
  if (typeof candidate.sourceUrl !== "string" || !/^https:\/\//i.test(candidate.sourceUrl)) {
    return { rankable: false, score: null, reason: "No original HTTPS evidence URL" };
  }
  if (!candidate.observedAt || !Number.isFinite(Date.parse(candidate.observedAt)) ||
      typeof candidate.evidenceSummary !== "string" || !candidate.evidenceSummary.trim()) {
    return { rankable: false, score: null, reason: "Evidence date or summary missing" };
  }
  const ratings = candidate.ratings ?? {};
  for (const field of Object.keys(WEIGHTS)) {
    if (!Number.isInteger(ratings[field]) || ratings[field] < 0 || ratings[field] > 5) {
      return { rankable: false, score: null, reason: `Missing/invalid assessed rating: ${field}` };
    }
  }
  const score = Math.round(Object.entries(WEIGHTS)
    .reduce((total, [field, weight]) => total + weight * ratings[field] / 5, 0));
  return {
    rankable: true,
    score,
    kind: "heuristic_not_probability",
    // Explicit, fail-closed review gates. This does not send anything.
    outreachEligible: candidate.humanApproved === true &&
      candidate.privacyReviewed === true &&
      candidate.contactVerified === true &&
      candidate.suppressionChecked === true &&
      candidate.suppressed === false
  };
}
