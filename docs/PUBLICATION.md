# Publication readiness

Last checked: 2026-11-17.

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
- Draft privacy and terms pages in pt-BR, English and es-AR, plus a manual-only
  GitHub Pages deployment workflow, are prepared in a dedicated legal PR.
  They are **not yet published or approved as legal statements**.
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
- Enzonic's terms for this specific publicly accessible API use, capacity
  guarantees, billing/overage behavior, exact log retention, and country-specific
  eligibility have not all been independently verified.
- Enzonic's `/tmp/balneabilidade` cache is ephemeral; persistence across restarts
  is not verified. The currently observed deployment was configured through the
  hosting panel; a fresh Git-based redeploy from this repository is not yet tested.
- All five tools were invoked in the ChatGPT integration, but the full set of
  five positive and three negative review cases has not been evaluated end to end
  as a recorded review suite.
- The public policy and terms pages are **drafts only**, not yet deployed.
  Enzonic's technical log categories and retention period, a confidential
  privacy contact, publisher identity, reviewer-accessible recording, selected
  country availability and commerce declaration still need verification.
- No public submission ZIP has been generated with those verified facts, and no
  submission, directory approval or listing has occurred.
- A private custom MCP connection is **not** a publicly listed ChatGPT/Codex plugin.

## Next steps

1. Confirm Enzonic's technical log retention and acceptable-use policy for
   this deployment; supply publisher legal identity and a private contact
   channel. Complete the [legal review checklist](LEGAL_REVIEW.md).
2. Approve the translations, remove draft banners and disable noindex; deploy
   GitHub Pages manually and verify all six live URLs.
3. Continue resource/abuse testing without flooding the shared free host;
   complete publisher verification and a reviewer-accessible demonstration.
4. Run all review cases in ChatGPT, then build and check the single-plugin ZIP.
5. Complete the publisher and domain verification, and submit for directory review.

See [`ENZONIC.md`](ENZONIC.md) for the deployment runbook and
[`submission/README.md`](../submission/README.md) for submission-only facts.
