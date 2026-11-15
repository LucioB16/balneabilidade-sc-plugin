# Publication readiness

Last checked: 2026-11-15.

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
- Earlier CI passed five tests, including an offline Streamable HTTP initialization
  and tool-discovery handshake. These are pre-change results; this change needs
  a fresh CI run before merge.
- The archive builder rejects placeholder and non-HTTPS submission values and
  requires missing publication metadata to be completed deliberately.

## Still outstanding / not verified

- Availability and stability over time, behavior under concurrent calls, memory
  peaks, restarts and potential free-host sleep or suspension have **not** been
  load-tested. An observed always-on label is not a contractual uptime guarantee.
- Rate limiting at public ingress and protection against abusive requests are not
  yet verified. The IMA request pace is per process; keep one replica unless
  global upstream throttling and shared caching are added.
- Enzonic's terms for this specific publicly accessible API use, capacity
  guarantees, billing/overage behavior, exact log retention, and country-specific
  eligibility have not all been independently verified.
- Enzonic's `/tmp/balneabilidade` cache is ephemeral; persistence across restarts
  is not verified. The currently observed deployment was configured through the
  hosting panel; a fresh Git-based redeploy from this repository is not yet tested.
- All five tools were invoked in the ChatGPT integration, but the full set of
  five positive and three negative review cases has not been evaluated end to end
  as a recorded review suite.
- No public privacy policy page, terms-of-service page, reviewer-accessible demo
  recording, verified publisher identity, selected country availability, or
  truthful commerce declaration has been supplied.
- No public submission ZIP has been generated with those verified facts, and no
  submission, directory approval or listing has occurred.
- A private custom MCP connection is **not** a publicly listed ChatGPT/Codex plugin.

## Next steps

1. Review/merge the Enzonic reproducibility changes and verify the CI job.
2. Validate recovery after a restart, actual free-plan resource and egress
   limits, and ingress rate limiting; review Enzonic's applicable terms.
3. Prepare accurate public privacy and terms pages, publisher verification,
   a reviewer-accessible recording, and the publication declarations.
4. Run all review cases in ChatGPT, then build and check the single-plugin ZIP.
5. Complete the publisher and domain verification, and submit for directory review.

See [`ENZONIC.md`](ENZONIC.md) for the deployment runbook and
[`submission/README.md`](../submission/README.md) for submission-only facts.
