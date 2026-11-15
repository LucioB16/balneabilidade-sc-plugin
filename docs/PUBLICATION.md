# Publication readiness

Last checked: 2026-11-15.

## Completed

- Public, separate repository: <https://github.com/LucioB16/balneabilidade-sc-plugin>.
- The remote Streamable HTTP implementation is merged in the upstream MCP
  repository at [commit `fee46b0`](https://github.com/LucioB16/balneabilidade-sc-mcp/commit/fee46b0990fa4a86aa61c89d5564157b1d97782e).
- Package listing copy, icon, Spanish/Portuguese translations, five positive
  and three negative MCP test cases, Dockerfile, tests, and CI are in this repo.
- Plugin checks pass in CI: 5 tests pass, including a real Streamable HTTP
  initialization and tool-discovery handshake against the pinned MCP package;
  the multi-stage Docker image also builds. See [the green run](https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/43663372049).
- The upstream MCP suite passes 75 offline tests, Ruff, formatting, mypy, and
  package build; the merged commit check is [green](https://github.com/LucioB16/balneabilidade-sc-mcp/actions/runs/43663289434).
- The package generator validates the expected review metadata and refuses
  placeholder, local, or non-HTTPS URLs.

## Not completed or not verified

- The plugin pins the immutable upstream commit `fee46b0`.
- No production container has been deployed. There is no stable public MCP URL
  yet and therefore no distributable `mcp.json`.
- No private ChatGPT plugin has been created or connected. We cannot test the
  integrated ChatGPT flow before a real endpoint exists.
- The five positive and three negative cases are drafts; none have run in
  connected ChatGPT.
- A public privacy page, terms page, reviewer-accessible recording, verified
  publisher identity, country selection, and commerce declaration are not
  supplied. No legal statements or URLs have been invented.
- The plugin has not been submitted for review or published in the shared
  ChatGPT/Codex directory.

See [`submission/README.md`](../submission/README.md) for the exact metadata
required to build the final ZIP. Creating a ZIP or a private plugin is not the
same as submitting it for review or publishing it.
