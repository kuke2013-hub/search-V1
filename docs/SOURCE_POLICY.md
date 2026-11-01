# Source access, verification and privacy policy

**This is a research policy, not legal advice.** Every source is disabled for automation until its access rules and intended use have been reviewed.

| Source | Intended use | V1 access position | Primary link |
|---|---|---|---|
| Spotlight Contacts | Inbound photographer listing and manual industry discovery | Check free listing; no assumed harvesting rights | https://app.spotlight.com/contacts-info/ |
| Casting Directors Association | Manual member research | Directory access visible; bulk reuse not authorised by this document | https://castingdirectorsassociation.com/directory |
| Personal Managers' Association | Historical candidate names | May 2024 list is stale; recheck each agency | https://thepma.com/wp-content/uploads/2024/06/List-of-PMA-Members-2024.pdf |
| Actors Pro Expo London | Organiser partnership/event tracking | 27 Feb 2027 official listing; monitor specific page | https://www.actorsproexpo.com/london-2027 |
| Greenhouse Job Board API | Published company vacancies | Public GET; board token per employer; comply with documented terms/limits | https://docs.greenhouse.io/job-board |
| Lever Postings API | Published company vacancies | Published per site, no universal search | https://github.com/lever/postings-api |
| Companies House | Company identity and filings | API key required; not an employee roster | https://developer.company-information.service.gov.uk/ |
| Brave Search API | Discover source pages | Metered API; snippets must be verified at origin | https://brave.com/search/api/ |
| Google Search Console | Own-site inbound attribution | OAuth authorization required from property owner | https://developers.google.com/webmaster-tools/v1/how-tos/authorizing |
| Backstage / Mandy / StarNow | Possible actor signals | **Excluded from automation**: Backstage prohibits automated scraping | https://www.backstage.com/terms-of-service/ |
| LinkedIn | Company and hiring context | **Excluded from unauthorised automation** | https://www.linkedin.com/help/linkedin/answer/a1341543 |

## Source verification tiers
1. **Historical candidate**: present in an old list, unverified today.
2. **Source-listed**: a current professional organisation page lists the entity; own website/location may remain unchecked.
3. **Website checked**: own domain and service/location information reviewed, but contact delivery not tested.
4. **Verified for a specific purpose**: independently checked evidence and date, verified source use, relevant location and appropriate contact path.
5. **Excluded or stale**: source blocked, old or irrelevant; no outbound use.

Never call a social-media handle verified until its target and current association have been checked directly.

## Operational policy
Every fetch must record status (including blocked/failed), UTC time, original URL and error. Respect robots directives, rate limits, platform terms, copyrights, privacy requirements and requests to stop processing.
No bulk outreach. Outbound person-level contact details require a documented data-protection basis and a notice/objection workflow. Corporate-subscriber PECR treatment differs from sole traders, and UK GDPR may still apply to named staff even for corporate email.
Respect objections with a protected suppression list and stop future marketing. Configure data retention and deletion separately from suppression records.

Primary regulator sources:
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-be-informed/
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/direct-marketing-guidance/respect-peoples-preferences/
