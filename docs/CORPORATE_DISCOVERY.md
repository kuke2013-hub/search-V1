# Corporate Prospect Discovery — November 2026

## Status
The first company watchlist contains **16 sourced organisations** and **six employer-supported professional-role examples**. **These are research candidates, not confirmed buyers.** A company with an Office Manager is not necessarily purchasing photography.

## Scale to thousands without paid software
Use official [Companies House monthly Basic Company Data](https://download.companieshouse.gov.uk/). Download all seven ZIP parts from the current monthly snapshot, then run:

    python3 scripts/import_companies_house.py /path/to/BasicCompanyData-2026-11-01-part*.zip -o local/london_company_candidates.csv
    python3 scripts/build_people_queries.py local/london_company_candidates.csv -o local/people_research.csv --limit 2000

The first script streams ZIP/CSV members and filters for active companies with a London-area *registered* postcode and target 2007 SIC industry codes (finance, consulting, legal, property, construction, architecture, technology, recruitment and PR). It deduplicates by company number.

**It DOES NOT establish employee count, physical London office, or photography need.** Registered offices include accountants and company-formation addresses; holding companies can have no staff. Accounts categories are not valid employee-headcount substitutes. The 11+ employees requirement requires a separate official team/employee statement or suitable licensed company data.

## Find the right person
The second script generates targeted Google search links for LinkedIn professional profiles, employer staff pages and public X results for four role groups: office/workplace, HR/people, marketing/comms and executive support/operations. It does not scrape LinkedIn or fabricate usernames or people. Confirm each name and current role on the employer website where possible. Record original evidence, date, and matching profile URL; flag unverified titles instead of silently assuming they are current.

Rank (a) actual company fit (physical workplace, likely staff count, sector), (b) decision-maker role confidence, and (c) **observed buying trigger** separately. An office manager can arrange photography, but an HR, marketing, communications, operations or executive assistant role may own the decision. Do not turn a vacancy into a fabricated hire or a headshot request.

## Acquisition experiment
Pilot 100 companies with verified active London offices. For each, verify 11+ staff when evidence exists; look for an appropriate published work contact; record evidence of any real business trigger and compare reply/booking rates across groups. Scores are research priority only, not purchase probabilities.

## Rules and limitations
Current full bulk download was **not** accessible in the development environment, so **no thousands-company import has run**. Local synthetic-data tests do not prove production import completeness. Neither a current employees database nor automated recurring scans are enabled.

Use [ICO B2B marketing guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/) for lawful basis, opt-outs and privacy notices. Public professional names still count as personal information. No unauthorised scraping, personal-contact harvesting or automated unsolicited outreach. Preserve suppression and evidence provenance.

The source repo is public; the future CRM and commercial records should use authenticated backend storage.
