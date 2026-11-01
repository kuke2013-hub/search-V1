# SEARCH-V1 Website — Research Interface

The repository root `index.html` is a dependency-free client-side website. It embeds an evidence-graded snapshot of **323 London acting-industry research entries** and **7 corporate London office prospects**, plus 10 source-register descriptions. All records are represented as **candidates to research**, not confirmed photography customers.

## Features

- Fast browser search, directory filters, research-priority ranking (0–100), evidence details, and original-source links.
- Acting industry, corporate-office, event, source-monitoring and scoring-method views.
- Shortlist saved **only in the current browser** with `localStorage`. No shared CRM or remote edit persistence.
- Export of filtered research results to CSV.
- Responsive desktop/mobile interface; no external frontend dependencies.

## Deployment

A GitHub Actions workflow at `.github/workflows/pages.yml` will deploy `index.html` whenever it changes, **after** Pages is enabled in repository Settings → Pages → Source: GitHub Actions. The intended Pages address is:

https://kuke2013-hub.github.io/search-V1/

Do not state the site is deployed until that URL and the Pages workflow have actually been checked. The repository is public, so the website's embedded data is visible to everyone; client-only records and secrets must not be added.

## Data maintenance

`data/research_seed.json` is a normalized import seed. Its `evidenceTier` reflects the source index, but **does not certify current email deliverability, X activity, buying intent or permission to automate collection**. A historical list from May 2024 accounts for 220 agency candidates, requiring review.

To generate SQL for a later private Cloudflare D1 import:

```sh
node tools/import_seed.mjs seed_import.sql
```

This produces SQL without connecting to Cloudflare or modifying a database. All source automation remains disabled by default.

## Limitations

No live API, email sending, login, Cloudflare deployment, independently verified marketing consent, actual sales records or trained AI model. Research scores reflect relevance and evidence/availability proxies, not probabilities of booking. No historical listing or company existence should be treated as a current need for headshots.