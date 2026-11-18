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
- Enzonic privacy: <https://enzonic.com/legal/privacy>. The public
  [Enzonic privacy policy](https://enzonic.com/es/legal/privacy) describes
  potential technical processing, including console logs, latency and network
  diagnostics. In a **2026-11-18 email response supplied by the operator**,
  admin@enzonic.com replied to the two questions about hosting this public,
  read-only MCP on the free Python plan and log retention: **“Yes to all of
  your questions :D Enjoy!”** and, in a follow-up, **“Data is not retained.”**
  This is written provider confirmation that the use is allowed and that the
  provider reports no data retention, **not an itemized logging inventory**.
  Its scope regarding transient processing and independent network
  subprocessors was not detailed. The application separately caches public
  IMA/SC documents. Do not equate these things or claim no data ever passes
  through the provider. Keep the operator's screenshot of this email in the
  internal review evidence; the repo does not contain the original email.
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
3. **Enzonic support response received (2026-11-18):** the operator supplied
   an email screenshot where admin@enzonic.com confirms this specific public
   read-only MCP use is permitted under the free Python plan and states
   “Data is not retained.” Record these facts with attribution. The exact
   categories of transient technical processing and independent network
   providers' practices were not specified; do not extrapolate the response
   into a guarantee of no processing or no third-party logging.
4. **Hosting acceptable-use inquiry:** ANSWERED in writing for this particular
   service, according to the operator-provided email. No general exemption
   from future policy changes or limits has been granted.
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
of control over the email inbox. The Enzonic usage/retention inquiry has received an affirmative response.
The operator still needs to review the final text, applicable law/data reuse,
and the manual GitHub Pages publication steps.
