# Publication readiness

Last checked: 2026-11-18.

## Completed and externally observed

- Public, separate source repository: <https://github.com/LucioB16/balneabilidade-sc-plugin>.
- The Python Streamable HTTP transport is merged in the upstream MCP repository
  at immutable commit [`fee46b0`](https://github.com/LucioB16/balneabilidade-sc-mcp/commit/fee46b0990fa4a86aa61c89d5564157b1d97782e).
- An Enzonic free-tier Python 3.12 instance runs Uvicorn and the upstream MCP app,
  using the `main.py` entry point and a ZIP-installed pinned dependency.
- Public HTTPS endpoint: <https://balneabilidade-sc.enzonic.dev/mcp>. HTTPS and the MCP
  handshake were confirmed from Windows PowerShell and an authenticated ChatGPT
  session on 2026-11-15. The URL is not a temporary tunnel or preview.
- PowerShell tests returned valid `initialize`, `tools/list` (five tools), and
  `tools/call` results for `search_beaches` and `get_bathing_status`.
  The latter fetched and processed IMA/SC report 53, dated 2026-11-13,
  for Praia de Perequê (Porto Belo), returning three sampling points.
- The newly created *private custom MCP integration* in ChatGPT successfully
  invoked all five tools: `search_beaches`, `get_sampling_points`,
  `get_bathing_status`, `get_bathing_history`, and `get_bulletin_page`.
  The last returned a rendered PNG page from the official bulletin.
- Package listing copy, icon, Spanish/Portuguese translations, five draft
  positive cases, three draft negative cases, Dockerfile, tests and CI exist.
- PRs #1–#3 were merged and passed CI; `main.py` and `guard.py` were
  independently confirmed by the operator in Enzonic. External GitHub Actions
  smoke run [#44224201321](https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44224201321)
  passed initialize, tool list and a real IMA/SC status call on 2026-11-17
  (America/Argentina/Cordoba). A transient earlier HTTP 403 is no longer
  reproduced; its root cause was not conclusively identified.
- Privacy and terms pages in pt-BR, English and es-AR were approved on
  2026-11-18 and published via GitHub Pages workflow
  [#44308178741](https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44308178741).
  The operator's screenshot shows the homepage rendering correctly; the
  six individual legal URLs have not been independently fetched here.
- The archive builder rejects placeholder and non-HTTPS submission values and
  requires missing publication metadata to be completed deliberately.

## Still outstanding / not verified

- Availability and stability over time, behavior under concurrent calls, memory
  peaks, restarts and potential free-host sleep or suspension have **not** been
  load-tested. An observed always-on label is not a contractual uptime guarantee.
- The operator confirmed the guarded `main.py` and `guard.py` files on Enzonic;
  a post-restart functional MCP check passed. Reaching the live admission
  thresholds (429/413/503) has not been safely tested against the public server.
  Edge-layer rate limiting and per-client isolation remain unverified.
  IMA request pacing is per process; keep one replica until shared limits exist.
- On 2026-11-18, the operator provided a screenshot of an Enzonic support
  email confirming the public read-only MCP use on the free plan and stating
  **“Data is not retained.”** This is provider-supplied confirmation, not an
  itemized declaration about transient processing or other network providers.
  Capacity guarantees, billing/overage and country-specific eligibility
  remain unverified.
- Enzonic's `/tmp/balneabilidade` cache is ephemeral; persistence across restarts
  is not verified. The currently observed deployment was configured through the
  hosting panel; a fresh Git-based redeploy from this repository is not yet tested.
- Direct MCP tests passed all five positive scenarios; the
  [manual review workflow #44228356588](https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44228356588)
  generated JSON evidence, including complete server-side pagination for
  Campeche 2025 (145 records). The operator separately **reported** a
  DeepSeek Harness/browser-use run of all eight exact prompts inside
  ChatGPT Web on 2026-11-18. Answer content passed P1, P2 and P4;
  P3 content passed but browser-side pagination remained **INCONCLUSIVE**;
  P5 **failed English language on the first attempt** and passed on retry.
  N1–N3 are all **INCONCLUSIVE for plugin non-invocation** due to no
  observable tool traces. See [detailed review evidence](REVIEW_VALIDATION.md).
- The operator reports a locally edited 104.63-second H.264 video
  (`outputs/edited/balneabilidade-sc-walkthrough.mp4`, SHA-256
  `8D6B60D954C495189614A2981B55FE662AA7796140FB915223D2AF3E56D3450A`).
  It is a composition of real frames/events, **not a continuous capture**.
  The uploaded MP4 was independently inspected on 2026-11-18; its SHA-256
  exactly matched the reported value, and the complete video decoded
  successfully. It has editorial flaws and cannot prove non-invocation or
  complete pagination; see [video audit](VIDEO_AUDIT_20261118.md).
  The original frame/event manifest was not inspected and redactions were
  sampled rather than checked frame by frame. No public video URL exists.
  Do not mark the reviewer recording as uploaded.
- The operator approved and published the public legal pages on 2026-11-18.
  GitHub Pages deployment [#44308178741](https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44308178741)
  passed, and the operator showed the rendered homepage. All six individual
  HTTPS URLs still require direct verification; a web retrieval attempt on
  2026-11-18 could not reach them, which is not proof of their unavailability.
- Enzonic confirmed use of the read-only public MCP on the free host and
  answered “Data is not retained,” without an itemized processing inventory.
  The operator provided individual OpenAI verification approval.
  `developerName` is **Lucio Bottacin**; the privacy contact is
  `luciobotacin@gmail.com`; `review.commerce=false` accurately describes
  the read-only, no-payment plugin. Confirm dashboard values before review.
- The OpenAI Platform plugin is currently **version 0.1.1 in draft**,
  with the neutral subtitle. The operator-provided OpenAI screenshots show
  the Enzonic **MCP domain verified**, the server **Configured**, five tools
  discovered and **no MCP scan findings**. These steps are completed,
  not pending as in earlier checklists.
- **Not yet supplied:** accessible reviewer video URL and deliberate
  publication country selection. The edited video exists locally according
  to the reporter but was not uploaded. Review details and policy
  attestations have not been completed, and nothing was submitted.
- A manual plugin ZIP build workflow is available. The initial ZIP can
  omit the video and country allowlist under the official schema; final
  review still requires an accessible video and deliberate country targeting.
  No submission, directory approval or listing has occurred.
- A private custom MCP connection is **not** a publicly listed ChatGPT/Codex plugin.

## Remaining steps before review submission

1. **Reviewer video:** upload the existing real-browser composite to a
   reviewer-accessible, read-only URL; check playback in an unauthenticated
   incognito session. Disclose that the video is edited/composited rather
   than a continuous recording; assess whether an additional continuous
   capture is needed. Keep the reported video SHA-256 for comparison; verify
   the corrected export's actual hash and redactions before uploading.
   The current file's SHA-256 has been independently verified, but a revised
   version will have a different hash. See
   [independent video audit](VIDEO_AUDIT_20261118.md).
   Do not invent `demo_recording_url`.
2. **Country availability:** operator decision is pending. **Recommendation:
   `countries: []` for worldwide availability**, because beaches in Santa
   Catarina are relevant to international travelers and the tool supports
   Spanish, Portuguese and English. According to OpenAI, an empty list
   explicitly removes country restrictions; `null`/omission leaves
   targeting unchanged. **Do not assign worldwide availability without
   the operator's choice.** An explicit uppercase ISO-style allowlist is
   valid if regional targeting is preferred.
3. **Metadata:** confirm `developerName: "Lucio Bottacin"`, the live
   privacy and terms HTTPS URLs, and `commerce: false`. Populate the
   ignored `submission/metadata.json` with the *actual* video URL and
   chosen `countries` once known. Keep missing values null until then.
4. **Strict ZIP:** build with
   `python scripts/build_plugin_archive.py --mcp-url "https://balneabilidade-sc.enzonic.dev/mcp" --metadata submission/metadata.json --require-demo`.
   Review generated archive contents. If updating fields already imported
   to OpenAI, upload the new version to the **existing** plugin.
5. **Portal review:** domain verification and all five tool scans are
   **already completed**. Add the video URL in **Review information**,
   verify the five positive / three negative case descriptions, enter
   reviewer credentials **only if needed** (none for this no-auth MCP),
   complete truthful attestations and select **Submit for review**
   **only with explicit operator authorization**.
6. **Publication:** wait for OpenAI's review decision, then request explicit
   authorization before publishing. A configured/draft plugin is not a
   public directory listing.

**No upload, submission, release or publication action is authorized by
this documentation-only update.**

See [`ENZONIC.md`](ENZONIC.md) for the deployment runbook and
[`submission/README.md`](../submission/README.md) for submission-only facts.
