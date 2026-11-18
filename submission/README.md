# Submission-only facts

The ZIP builder now supports a **package suitable for uploading to the public review portal** before the
reviewer video exists, as permitted by OpenAI's official documentation.
The video is **still required for final MCP review submission**. Do not
commit a completed `metadata.json` if it contains private review details.

The tracked `metadata.template.json` already includes the operator-supplied
name, published legal-page URLs and the verified **non-commerce** behavior.
It deliberately leaves `demo_recording_url: null` because the revised video has not been uploaded. The operator explicitly approved **worldwide availability** on 2026-11-18, represented by `countries: []`.

For final review, copy `metadata.template.json` to the ignored
`submission/metadata.json` and complete:

- confirm the exact registered developer identity is **Lucio Bottacin**;
- confirm the public privacy and terms URLs load correctly;
- add the actual reviewer-accessible demo recording URL once available;
- retain the operator-approved worldwide availability (`countries: []`).
  Do not change this to a regional allowlist without another explicit decision.

The six legal pages were approved, and GitHub Actions deployed the Pages site
successfully on 2026-11-18:
https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44308178741.
The operator's screenshot confirms the homepage renders. Verify each
privacy/terms URL directly before submitting; an external checker was unable
to fetch them. For the domain challenge required later in the MCP connection
flow, see [DOMAIN_VERIFICATION.md](../docs/DOMAIN_VERIFICATION.md).

The website and support links in `plugin/plugin.json` point to the public
repository and its issue tracker. Check both URLs again before submission.
The MCP URL is passed separately to the archive builder and must be a stable,
public HTTPS production endpoint, never a preview or development tunnel.

Build the plugin ZIP using verified details, without inventing a demo URL:

```bash
python scripts/build_plugin_archive.py \
  --mcp-url "https://balneabilidade-sc.enzonic.dev/mcp" \
  --metadata submission/metadata.template.json
```

Or use the manual GitHub Actions workflow **Build plugin package for public review**
to download the generated ZIP without installing Python locally.

The operator reported a **locally prepared** 104.63-second edited real-browser
video on 2026-11-18, but it has not been uploaded, and its reported SHA-256
has not been independently verified. The UI did not expose MCP tool
traces. The three negative review cases therefore remain **INCONCLUSIVE
for non-invocation**, and P3 pagination remains unobservable. See
[REVIEW_VALIDATION.md](../docs/REVIEW_VALIDATION.md).

**Country availability is decided:** on 2026-11-18, the operator explicitly
approved global availability. `countries: []` in the package means there is
no country allowlist restriction. This does **not** mean that the draft
plugin is already publicly listed: OpenAI review and publication are still
pending.

After the corrected demo is uploaded to a reviewer-accessible URL, update
the ignored local metadata file with its real URL. Keep `countries: []`. For
final review, run the strict version:

```bash
python scripts/build_plugin_archive.py \
  --mcp-url "https://balneabilidade-sc.enzonic.dev/mcp" \
  --metadata submission/metadata.json \
  --require-demo
```

The resulting ZIP is an upload candidate, not an approval or publication.
The OpenAI dashboard initially keeps uploaded packages as drafts regardless of ZIP filename. Complete
review requirements before pressing Submit for review. Country targeting has
already been approved as worldwide; it does not authorize submission.
