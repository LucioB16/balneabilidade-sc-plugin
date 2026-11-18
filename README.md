# Balneabilidade SC

ChatGPT and Codex plugin source for checking IMA/SC's published bathing-water
results at monitored beaches in Santa Catarina, Brazil. It reuses the Python
provider and five MCP tools from
[`balneabilidade-sc-mcp`](https://github.com/LucioB16/balneabilidade-sc-mcp)
through a pinned dependency; this repository holds the remote deployment,
plugin package, CI, and publication materials.

> Results are dated published measurements, not real-time readings or a safety
> guarantee. IMA/SC is the official data source. This independent project is
> not developed, operated, or endorsed by the agency.

## What it can do

- Find monitored beaches and ask for a municipality when names are ambiguous.
- Return every sampling point separately, including sample and bulletin dates,
  source, freshness, and the provider's classification.
- Show dated history for a beach or point over a selected date range.
- Return a bulletin page as an image when a vision-capable client needs to
  inspect an unreadable row; the server does not invent parsed results.
- Answer naturally in Rioplatense Spanish, Brazilian Portuguese, and English.

The server preserves `proper`, `improper`, `mixed`, `partial`, `unknown`, and
stale/unverified states from the MCP contract. It does not collapse point-level
results into a claim that an entire beach is suitable.

## Example questions

- “¿Está apta para bañarse Praia do Perequê, en Porto Belo?”
- “¿Qué puntos de Praia Brava, en Florianópolis, están impropios?”
- “Mostrame el historial de balneabilidad de Campeche durante 2025.”
- “Qual é a condição publicada mais recente da Praia de Zimbros, em Bombinhas?”
- “What is the latest published result for Praia de Garopaba?”

## Current release state

A remote Python MCP server is deployed on Enzonic's free Python hosting at
[`https://balneabilidade-sc.enzonic.dev/mcp`](https://balneabilidade-sc.enzonic.dev/mcp). On 2026-11-15, it passed
MCP initialization, tool discovery, and live IMA/SC lookups from a custom
ChatGPT MCP integration. All five tools were invoked from ChatGPT.

**This is an operational validation, not a production-readiness or uptime
guarantee.** The public directory listing has not been submitted or approved.
See [`docs/PUBLICATION.md`](docs/PUBLICATION.md) for the remaining requirements.

The live Enzonic deployment currently uses Python 3.12, the repository's
`main.py` entry point, and the exact upstream package revision in
`requirements.txt`. For reproducible setup and caveats, see
[`docs/ENZONIC.md`](docs/ENZONIC.md).

## Run the remote server locally

Build the Docker image and bind it only to loopback for local testing:

```bash
docker build -t balneabilidade-sc-plugin .
docker run --rm -p 127.0.0.1:8000:8000 \
  -e BALNEABILIDADE_ALLOWED_HOSTS='127.0.0.1,127.0.0.1:*,localhost,localhost:*' \
  -e BALNEABILIDADE_ALLOWED_ORIGINS='http://127.0.0.1:*,http://localhost:*' \
  balneabilidade-sc-plugin
```

The MCP endpoint is `http://127.0.0.1:8000/mcp`. This local address is for
development only; it is not included in the distributable plugin manifest.
See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) before selecting a public host.

## Licenses and data

The plugin code is MIT licensed. IMA/SC publishes the source data at
<https://balneabilidade.ima.sc.gov.br/>. The source MCP repository records that
no data-reuse license was confirmed; the plugin fetches official source files
at runtime and does not commit or redistribute IMA PDFs, CSV exports, or bulk
datasets. Attribution requirements are documented in the MCP repository.

This project does not claim an affiliation with IMA/SC. For verified support,
use [GitHub Issues](https://github.com/LucioB16/balneabilidade-sc-plugin/issues).

## Repository contents

- `plugin/plugin.json`: listing text, translations, icon references, and draft
  review cases.
- `scripts/build_plugin_archive.py`: produces a single-plugin ZIP only after a
  production MCP URL and verified submission facts are supplied.
- `Dockerfile`, `requirements.txt`, `main.py` and `guard.py`: Docker and Enzonic
  entry points using the pinned MCP package, with process-level request
  admission controls. The operator confirmed both Python files in Enzonic;
  no separate live threshold-trigger test has yet been recorded.
- `tests/` and `.github/workflows/ci.yml`: offline manifest and real MCP
  handshake validation against the pinned server.
- `docs/`: Enzonic runbook, data-handling facts, publication status, and
  [legal-page review checklist](docs/LEGAL_REVIEW.md).
- `site/`: approved and published privacy/terms pages in pt-BR, en and es-AR,
  deployed via GitHub Pages on 2026-11-18.
- `docs/DOMAIN_VERIFICATION.md`: OpenAI MCP-host challenge workflow;
  the challenge route is implemented but not yet deployed to Enzonic.
- `scripts/check_remote_mcp.py`: opt-in external HTTPS/MCP health check for
  operator-controlled restart validation.

The submission archive uses the public production MCP URL, not a preview or
development tunnel. It can now produce an uploadable **draft** with the
approved legal URLs and the documented non-commerce declaration, while
leaving the demo and country targeting unspecified until those decisions are
available. Final review still requires the real video and completed settings.

## Listing wording clarification (0.1.1)

The listing and the es-AR/pt-BR subtitles now describe **bathing-water results**
without calling the plugin itself “official”. The source data comes from
IMA/SC, but Balneabilidade SC is an **independent, unaffiliated plugin**.
Version 0.1.1 only changes public metadata and release notes; the remotely
hosted MCP endpoint and its tools are unchanged.
