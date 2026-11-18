# Submission-only facts

## Current publication state — 2026-11-18

- Public plugin source: `LucioB16/balneabilidade-sc-plugin`.
- Current plugin version: `0.1.1`; OpenAI draft is **not submitted or published**.
- Publisher identity: **Lucio Bottacin**, to match verified developer identity.
- Public privacy and terms: linked from `metadata.template.json`.
- **Worldwide availability is operator-approved** (`countries: []`).
- No commerce (`commerce: false`).
- The **v2 reviewer video** (215 s, 1920×1080 H.264) was uploaded to Google
  Drive. Google API confirmed **anyone with the link: reader**, not indexed
  for search:
  <https://drive.google.com/file/d/1THkpgNpv2XjeSzgCV4XlGGR9NPXUob9H/view?usp=drivesdk>.
  **Anonymous playback in an incognito browser still needs checking**.
- Video SHA-256 was independently verified:
  `bb54b7b14e7663d45d4d9355d878706dc3120bc8951936f8b116c142349989dd`.
- **N1–N3 plugin non-invocation remains INCONCLUSIVE**, and P3 ChatGPT
  pagination is not observable. The edited video is not a continuous screen
  capture. See [v2 audit](../docs/VIDEO_AUDIT_V2_20261118.md).
- MCP domain was verified, server configured, five tools discovered and
  scan findings empty in operator-provided OpenAI screenshots.

## Generate the strict final-review ZIP using GitHub Actions

1. Check the demo plays without authentication in an incognito window.
2. Open **Actions → Build plugin package for public review → Run workflow**.
3. Paste the exact reviewer-accessible Google Drive video link into
   `demo_recording_url` and choose branch `main`.
4. After the workflow passes, download the `balneabilidade-sc-package`
   artifact and extract the single `balneabilidade-sc-plugin-0.1.1.zip`
   from it. Do **not** upload the outer Actions artifact ZIP.
5. Upload the plugin ZIP to the **existing OpenAI draft**, not as a new
   plugin, then inspect automated findings and the imported review fields.

The workflow creates an ignored `submission/metadata.json` in the runner
and executes the **strict** archive builder with `--require-demo`. It
checks the URL, worldwide countries, non-commerce declaration, five
positive and three negative test cases, and production MCP URL. It does
**not** send anything to the OpenAI review team or publish the plugin.
Because the workflow input may be visible in GitHub's Actions history,
use only the already shared view-only link, never credentials.

## Alternative local build

Copy the tracked template into the Git-ignored
`submission/metadata.json` and replace `demo_recording_url: null` with
the actual Google Drive video URL, keeping `countries: []`.

```bash
python scripts/build_plugin_archive.py \
  --mcp-url "https://balneabilidade-sc.enzonic.dev/mcp" \
  --metadata submission/metadata.json \
  --require-demo
```

## Final portal checks

OpenAI identity verification, correct legal URLs, no-auth MCP connection,
country availability, eight test cases, reviewer video, release notes,
reviewer credentials if actually required, and policy attestations must
all be reviewed before sending. Six legal files are in `site/` and the
GitHub Pages workflow passed, but independent external fetch of each URL
failed from the verification environment; manually check each public URL.

**Do not claim the negative cases prove absence of MCP tool calls.**
Do not submit for review or publish without the operator's explicit
authorization.
