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
- Privacy and terms pages in pt-BR, English and es-AR were **approved by the
  operator on 2026-11-18**. Draft banners and noindex metadata have been
  removed in PR #4. A manual-only GitHub Pages deployment workflow is
  prepared, but the pages are **not yet deployed or HTTPS-verified**.
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
- All five tools were invoked in the connected ChatGPT integration. The five
  positive review scenarios were also manually exercised at MCP tool level,
  including complete 2025 pagination for Campeche (145 records). A manual
  GitHub Actions review run [#44228356588](https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44228356588)
  passed all five tool-layer cases and uploaded review-tool-evidence.zip.
  See [review evidence](REVIEW_VALIDATION.md). Model-level tool selection and
  three negative no-tool scenarios still require a real ChatGPT recorded review;
  no reviewer video exists yet. See [recording guide](REVIEW_DEMO.md).
- The operator approved the public privacy and terms pages on 2026-11-18,
  but GitHub Pages publishing and URL checks are **not yet complete**.
  The operator's screenshot records Enzonic's permission and no-retention
  statement. The technical categories of transient processing or independent
  network providers were not detailed. The OpenAI individual verification
  screen shows Approved; reviewer-accessible recording, selected countries
  and commerce declaration still need completion. The operator supplied the
  public name Lucio Bottacin and privacy contact luciobotacin@gmail.com.
- No public submission ZIP has been generated with those verified facts, and no
  submission, directory approval or listing has occurred.
- A private custom MCP connection is **not** a publicly listed ChatGPT/Codex plugin.

## Next steps

1. Record Enzonic's written approval and no-retention statement (done in
   the legal review checklist); review the final legal text, attribution and
   contact information before publishing. See [legal review](LEGAL_REVIEW.md).
2. Merge the approved legal PR; configure GitHub Pages to deploy from
   GitHub Actions, manually run the Pages workflow and verify all six
   HTTPS URLs before using them in submission metadata.
3. Continue resource/abuse testing without flooding the shared free host;
   complete publisher verification and a reviewer-accessible demonstration.
4. Run the five positive and three negative prompts through ChatGPT, record
   tool selection and user-visible answers, upload a reviewer-accessible demo
   video, then build and check the single-plugin ZIP.
5. Complete the publisher and domain verification, and submit for directory review.

See [`ENZONIC.md`](ENZONIC.md) for the deployment runbook and
[`submission/README.md`](../submission/README.md) for submission-only facts.
