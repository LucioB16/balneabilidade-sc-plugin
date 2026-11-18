# Public legal pages — review and deployment checklist

Prepared on **2026-11-17**. These pages are **drafts**, not approved legal
statements or currently accessible public policies.

The independent Balneabilidade SC project uses Enzonic for the public MCP
endpoint, IMA/SC for published bathing-water information, and the proposed
GitHub Pages site for legal pages. OpenAI's [public plugin guidelines]
(https://developers.openai.com/plugins/plugin-guidelines) require a published
privacy policy stating personal-data categories, purposes, recipients,
retention timelines and user controls. The [submission guide]
(https://developers.openai.com/plugins/deploy/submission) requires working
HTTPS privacy and terms URLs for an MCP listing.

## Proposed public URLs (not live until deployment)

- Privacy (pt-BR): https://luciob16.github.io/balneabilidade-sc-plugin/privacy/
- Privacy (en): https://luciob16.github.io/balneabilidade-sc-plugin/privacy/en/
- Privacy (es-AR): https://luciob16.github.io/balneabilidade-sc-plugin/privacy/es/
- Terms (pt-BR): https://luciob16.github.io/balneabilidade-sc-plugin/terms/
- Terms (en): https://luciob16.github.io/balneabilidade-sc-plugin/terms/en/
- Terms (es-AR): https://luciob16.github.io/balneabilidade-sc-plugin/terms/es/

## Facts verified against upstream Python code

- No user-account database, account authentication, payment functionality,
  raw conversation storage or analytics integration in the MCP application.
- MCP input fields are task-specific: beach, municipality, point, date range,
  result limit, bulletin page. Users should not include sensitive information.
- The Python HTTP app disables access logging. MCP tool failures log the
  exception type, not raw MCP input bodies.
- The application caches public IMA/SC source materials, not personal profiles.
  Its TTL configuration: bulletin index **1 hour**, analyses **1 hour**,
  point catalog **24 hours**, current-year CSV **6 hours**, historical-year
  CSV **30 days**, PDF **3650 days**. Cached files are not automatically
  deleted at expiry: expiry means not fresh, not guaranteed erasure.
  The chosen Enzonic `/tmp/balneabilidade` path is ephemeral.
- The host or upstream networks can process connection metadata that this
  application itself does not intentionally log.
- Source attribution: <https://balneabilidade.ima.sc.gov.br/>.
- Enzonic privacy: <https://enzonic.com/legal/privacy>.
- GitHub privacy: <https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement>.

## Blocking questions before publishing or submitting

1. **Service operator (provided):** Lucio Bottacin. The operator gave this
   name for the legal pages. **Not yet verified** against the name registered
   in the OpenAI developer dashboard; check the exact verified legal identity
   before submission.
2. **Direct privacy contact (provided):** luciobotacin@gmail.com.
   The operator provided this address for public display. Verify the mailbox
   is monitored and can receive privacy-related inquiries before publication.
   GitHub Issues remain public and **must not** be used to submit sensitive
   personal information or data-subject requests.
3. **Enzonic technical metadata retention:** obtain its applicable log
   categories, default durations, deletion policy and relevant subprocessors
   for this exact **Python Web o app** product; do not substitute the
   separately marketed *Enzonic Deploy* log-retention table.
4. **Host allowed use:** confirm the free-tier server may operate a public,
   read-only third-party-data MCP service under the current Enzonic AUP.
5. **Law and jurisdiction:** have the operator review applicable privacy
   rules (including Brazil's LGPD if relevant), legal capacity, limitations
   and contact details; translations should be checked for legal consistency.
6. **Data reuse:** verify any attribution/permissions required for the
   official IMA/SC data. A public source does not automatically grant any
   particular reuse license.

## Publication procedure — manual, not automatic

1. Review and resolve every blocking item above with verifiable facts.
2. Update the three privacy pages and three terms pages consistently.
   Replace the draft banners and `noindex,nofollow` metadata on all pages.
   The manual deployment workflow deliberately refuses to publish while
   any legal page is still marked as draft.
3. Merge the legal-site PR into `main`.
4. In GitHub repository **Settings → Pages → Build and deployment**, select
   **GitHub Actions** as the publishing source (if not already enabled).
5. In **Actions → Publish reviewed legal pages → Run workflow**, select
   `main` and run the one-shot deployment. No push trigger exists.
6. Open each public HTTPS URL directly, verify text and TLS, and confirm
   GitHub Pages publishes the new content.
7. Only after the pages are public and correct, populate
   `privacyPolicyURL` and `termsOfServiceURL` in the **ignored**
   `submission/metadata.json`, then build the plugin ZIP.

Until steps 1–6 are complete, **do not add the proposed URLs to the
submission manifest as though they are live** and do not submit the plugin.

## Operator contact supplied (2026-11-17)

The draft pages now identify **Lucio Bottacin** as the service operator and
provide the direct email **luciobotacin@gmail.com** for privacy-related
inquiries. These details were provided by the operator for public display.
This does **not** establish independent verification of legal identity or
of control over the email inbox. The Enzonic logging and allowed-use checks,
legal review, and manual GitHub Pages publication steps remain outstanding.
