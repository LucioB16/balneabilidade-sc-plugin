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

The public GitHub repository and package source are being prepared. The Python
MCP implementation is in the separate repository. No production endpoint has
been deployed, no private ChatGPT plugin has been created, and this project is
not yet listed in the public ChatGPT/Codex directory. See
[`docs/PUBLICATION.md`](docs/PUBLICATION.md) for the verified state and remaining
requirements.

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
- `Dockerfile` and `requirements.txt`: deployable Python/ASGI server wrapper
  pinned to an immutable MCP source commit.
- `tests/` and `.github/workflows/ci.yml`: offline manifest and real MCP
  handshake validation against the pinned server.
- `docs/`: hosting comparison, data-handling facts, and publication status.

The submission archive deliberately does not use an example, preview, or
development URL. The builder requires real policy URLs, a verified publisher
identity, country selection, commerce declaration, and an accessible recorded
demo before it creates an upload candidate.
