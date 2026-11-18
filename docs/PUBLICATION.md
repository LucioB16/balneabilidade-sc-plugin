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
- The **v1** 104.63-second MP4 was independently reviewed and its
  SHA-256 verified; see [v1 audit](VIDEO_AUDIT_20261118.md).
  The operator then uploaded **v2**, and its **215-second** MP4
  (1920×1080 H.264, no audio; **3,413,718 bytes**) was independently
  decoded and checked. SHA-256
  `bb54b7b14e7663d45d4d9355d878706dc3120bc8951936f8b116c142349989dd`
  **exactly matches** the reported hash. V2 removes obstructing captions,
  shows P5's first language failure and successful retry, and explicitly
  retains P3 and N1–N3 observability limits. See
  [v2 video audit](VIDEO_AUDIT_V2_20261118.md). Both videos are edited
  composites of real frames/events rather than continuous screen captures.
  Source files were not independently inspected, and masking was visually
  sampled, not frame-by-frame certified. **No public reviewer video URL
  exists**; do not mark the evidence as uploaded.
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
- The operator uploaded the independently verified v2 MP4 to Google Drive:
  <https://drive.google.com/file/d/1THkpgNpv2XjeSzgCV4XlGGR9NPXUob9H/view?usp=drivesdk>.
  Google Drive metadata confirms `anyone:reader` access with search
  discoverability disabled. **Independent incognito playback remains
  unverified**. Review policy attestations and draft submission are pending.
  Worldwide availability was explicitly approved (`countries: []`).
- The manual **Build plugin package for public review** GitHub Actions
  workflow accepts a real reviewer video URL, creates ignored metadata
  in the runner and builds with `--require-demo`. It verifies contents
  and returns an artifact; it never submits to OpenAI.
  No submission, directory approval or listing has occurred.
- A private custom MCP connection is **not** a publicly listed ChatGPT/Codex plugin.

## Remaining steps before review submission

1. **Reviewer video:** v2 MP4 is uploaded and has confirmed
   `anyone:reader` permissions. Verify playback in an incognito window;
   check final masking, disclose that the footage is edited rather than
   continuous, and preserve the P3/N1–N3 evidence limitations.
2. **Country availability:** confirmed worldwide, `countries: []`.
3. **Legal pages and metadata:** confirm the six published legal URLs load,
   publisher identity `Lucio Bottacin`, `commerce: false`, correct
   translations, and the real reviewer video URL. The tracked template
   deliberately leaves the video URL null; only ignored metadata or
   a workflow run should include it.
4. **Strict ZIP:** run GitHub Actions → **Build plugin package for public
   review**, input the real video URL and choose `main`. Download the
   artifact, extract the actual `balneabilidade-sc-plugin-0.1.1.zip`,
   and upload that plugin ZIP to the **existing** OpenAI draft. Check
   imported fields and scan findings. Alternatively run the local
   `build_plugin_archive.py` command with `--require-demo`.

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
