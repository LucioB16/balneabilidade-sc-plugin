# Enzonic deployment runbook

Verified at: 2026-11-15, based on the actual free Python instance and
external MCP tool calls. No admin credential or token belongs in this file.

This runbook documents a **tested existing deployment**, not a guarantee that
Enzonic will always offer capacity, permit every use case, or keep its free
plan and domain unchanged.

## Live endpoint and runtime

- Public Streamable HTTP MCP: <https://balneabilidade-sc.enzonic.dev/mcp>
- Hostname: `balneabilidade-sc.enzonic.dev` (not a tunnel).
- Runtime type: Enzonic **Web o app → Continuar de todos modos → Python**,
  rather than the separate serverless Enzonic Deploy product.
- Selected plan: **Gratis / Sin tarjeta**, advertised as always-on.
- Provisioned resources observed in the UI: **512 MiB RAM**, **1 GiB disk**.
  The UI chose an available free node and initially queued the request.
- Runtime: **Python 3.12**; Python 3.12.16 appeared in the actual log.
- Entry point: `main.py`; `requirements.txt` at repository root.
- Git repository field: <https://github.com/LucioB16/balneabilidade-sc-plugin>,
  branch `main`; "User Uploaded Files" was enabled.
- The public hostname was attached to the assigned server's principal port.
  The assigned port was `28982` **at the time of the test only**; never
  hardcode this number.

The original live instance was provisioned with a placeholder `main.py`
and an empty `requirements.txt`, despite a repository address being set
in Startup. Those two files were manually corrected through Enzonic's
file manager. Git synchronization on redeploy **has not yet been tested**.

## Files and immutable dependency

The entry point, guard, and dependency file live at the repository root.
Deploy `main.py` and `guard.py` together; the guarded entry point imports
the second file. Git synchronization on the live host remains unverified.

- `main.py`: starts the existing upstream ASGI `/mcp` application through
  the `guard.py` admission limiter, keeping the source provider unchanged.
  **This new wrapper is not yet active in the existing Enzonic container.**
- `requirements.txt`: installs the `mcp` extra from the ZIP for the immutable
  [upstream commit `fee46b0`](https://github.com/LucioB16/balneabilidade-sc-mcp/commit/fee46b0990fa4a86aa61c89d5564157b1d97782e),
  plus Uvicorn. This is the **same source version** as the prior Git URL and
  does not require the `git` executable in the hosting container.

No provider source code, private credential, data export or chat transcript
is copied into this repository.

## Enzonic Startup settings

In the server's **Arranque** page use:

| Setting | Value |
| --- | --- |
| Software | `Python` |
| Runtime image | `Python 3.12` |
| Main File / `MAIN_FILE` | `main.py` |
| Git Repository Address | `https://github.com/LucioB16/balneabilidade-sc-plugin` |
| Git Branch | `main` |
| Additional Packages | Leave empty |
| User Uploaded Files | Enabled |
| `BALNEABILIDADE_ALLOWED_HOSTS` | `balneabilidade-sc.enzonic.dev` |
| `BALNEABILIDADE_CACHE_DIR` | `/tmp/balneabilidade` |

Enzonic's generated startup wrapper was observed to do the equivalent of:

```sh
export PORT="${SERVER_PORT}"
python3 -m pip install --no-cache-dir -r requirements.txt
python3 -u main.py
```

The real wrapper additionally detects dependency changes and may skip an
unchanged successful installation. **Do not overwrite the entire startup
command with these illustrative lines**. Enzonic sets `SERVER_PORT` itself.
The upstream server reads `PORT` (default 8000), binds `0.0.0.0`, and
serves Streamable HTTP on `/mcp`.

`BALNEABILIDADE_ALLOWED_HOSTS` is a strict allowed-host list for DNS
rebinding protection. Set it only to real, expected public hostnames; do not
use `*` or disable the protection. Server-to-server requests that omit
`Origin` work without extra configuration; if a browser-based client needs
to send an `Origin` header, configure an exact
`BALNEABILIDADE_ALLOWED_ORIGINS` allowlist after checking the origin.

`/tmp/balneabilidade` is a writable **ephemeral** TTL cache. The current
deployment does not guarantee cache survival across container restarts.
A persistent volume and global IMA pacing would require separate verification.

## Deployment / recovery checklist

1. Provision the **free** Python runtime and assign a non-temporary HTTPS
   `*.enzonic.dev` domain. Do not upgrade or attach billing to follow this runbook.
2. Verify the Enzonic file manager shows this repository's `main.py`,
   `guard.py` and nonempty `requirements.txt`. If missing, copy their
   tracked contents together. Do not assume the Git address cloned correctly.
   **Do not update `main.py` without `guard.py`: it will fail to import.**
3. Review the Startup variables, including exact hostname and `SERVER_PORT`
   (provider assigned), and preserve Enzonic's managed startup wrapper.
4. Start the server. The first installation can take longer while downloading
   PyMuPDF and the other Python wheels.
5. In logs verify `Successfully installed`,
   `StreamableHTTP session manager started`,
   `Application startup complete.` and
   `Uvicorn running on http://0.0.0.0:<assigned-port>`.
6. Confirm HTTPS and `/mcp` from an **external** MCP client. A browser GET
   may display SSE keepalive `: ping` messages but alone does not confirm
   JSON-RPC tool calls.
7. Test `initialize`, `tools/list`, and at least one `tools/call` against
   IMA/SC before using the endpoint with ChatGPT or Codex.
8. After any update or runtime restart, re-run the health and source checks.
   Automatic source refresh from GitHub and recovery after a full restart are
   still **unverified** for this host.

## External functional checks observed

On 2026-11-15 Windows PowerShell successfully ran:

- `initialize` → JSON-RPC result with MCP capabilities.
- `tools/list` → all five named tools.
- `search_beaches` for Perequê in Porto Belo → one match, three points.
- `get_bathing_status` → IMA/SC bulletin 53 of 2026-11-13,
  three distinct points and matching dated source attribution.

Then a **private ChatGPT custom MCP integration** exercised all five tools,
including CSV history and a rendered PNG bulletin page. These results
establish functional connectivity at the time of testing, not service uptime
or suitability for unbounded public traffic.

Windows PowerShell **5.1** needs special care with accented inputs. For
`Invoke-RestMethod`, send explicit UTF-8 bytes instead of passing a JSON
string to `-Body`:

```powershell
$uri = "https://balneabilidade-sc.enzonic.dev/mcp"
$headers = @{ Accept = "application/json, text/event-stream" }
$request = @{
    jsonrpc = "2.0"
    id = 1
    method = "initialize"
    params = @{
        protocolVersion = "2025-11-25"
        capabilities = @{}
        clientInfo = @{ name = "enzonic-check"; version = "1.0" }
    }
} | ConvertTo-Json -Depth 10
$bytes = [Text.Encoding]::UTF8.GetBytes($request)
Invoke-RestMethod -Uri $uri -Method Post -Headers $headers `
    -ContentType "application/json; charset=utf-8" -Body $bytes
```

A parser error for `Perequê` was eliminated by sending UTF-8 bytes. For
correctly displaying accented response text on old Windows PowerShell,
decode the raw response stream as UTF-8 instead of relying on default
console decoding.

## Proposed app-level abuse limits (not yet deployed)

The guarded entry point now in this repository applies a **per-process**
global admission budget to \`GET /mcp\` and \`POST /mcp\`:

| Control | Default |
| --- | --- |
| Admissions per 60-second sliding window | 40 |
| Concurrent POST requests | 2 |
| Open GET SSE streams | 8 |
| Maximum POST body (including chunked) | 256 KiB |
| Maximum time to receive a POST body | 15 seconds |

Over-limit responses are HTTP 429 (rate), 503 (concurrency), 413 (body size)
or 408 (body deadline). All thresholds were chosen for a 512 MiB instance
and must be reevaluated using real peak memory measurements.

This is not an edge firewall or per-user quota. Enzonic is behind a proxy,
so the guard intentionally ignores unverified client IP headers such as
\`X-Forwarded-For\`. A malicious user could monopolize the shared budget.
It also does not globally control IMA/SC traffic across multiple replicas,
protect against all L7 abuse, or guarantee high availability. Maintain a
single process until a shared limiter/cache is implemented.

**No active Enzonic settings were changed by the code update.**
To activate it, deploy the *pair* of files \`main.py\` and \`guard.py\`,
then restart once in the hosting panel. Keep a backup of the prior \`main.py\`
to roll back immediately if ChatGPT clients fail. The remote MCP endpoint
and \`BALNEABILIDADE_ALLOWED_HOSTS\` setting do not change.

## Restart / recovery validation procedure (still pending)

The Enzonic dashboard has a manual **Reiniciar** control and console.
No authenticated panel control was available during this review, so a
real restart has **not** been performed or falsely declared successful.

1. Note the current uptime and RAM, and confirm the endpoint works.
2. Trigger **Reiniciar** in Enzonic when an interruption is acceptable.
3. Review logs for \`StreamableHTTP session manager started\`,
   \`Application startup complete.\` and the listening \`PORT\`.
4. From the repository root on Windows, macOS, Linux, or the manual
   GitHub Actions workflow "Manual remote MCP smoke check", run:

   \`\`\`sh
   python scripts/check_remote_mcp.py --timeout 120 --check-source
   \`\`\`

5. Confirm \`initialize\`, \`tools/list\` and the IMA/SC sample call all pass,
   then execute a tool from the private ChatGPT MCP integration.
6. Record recovery time, peak RAM, whether \`/tmp\` cache survives, and
   whether the host downloads dependencies or source anew. Restart once more
   if you need to confirm reproducibility.

The workflow runs **only when manually dispatched**: it is not a persistent
monitor, does not probe continuously and does not attempt to keep free
hosting awake.

## Production risks still unresolved

- No contractual SLA, verified availability window or guaranteed free
  capacity. Queueing was observed at provisioning time.
- Rate limiting for public unauthenticated MCP requests has not been
  established. The IMA client throttles outbound requests **per process**,
  not across replicas; keep a single replica.
- Cache is ephemeral; cold cache may repeatedly download official PDFs/CSVs.
- Concurrent request performance, peak RAM / CPU / disk and restart recovery
  remain untested.
- Enzonic's applicable terms for this specific public API, upstream egress
  restrictions, logs / retention, and abuse controls must be checked before
  directory submission.
- A stable domain and working HTTPS in the browser do not replace required
  publisher/domain verification for public plugin listing.

See [`PUBLICATION.md`](PUBLICATION.md) for the publishing checklist and
[`DATA_HANDLING.md`](DATA_HANDLING.md) for factual inputs to future policies.
