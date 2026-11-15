# Hosting and deployment

The HTTP transport lives in the original Python MCP package. This repository
adds a container entry point and pins the source repository to an immutable
commit; it does not copy the IMA provider or its parsing logic.

## Architecture choices

| Option | Reuse and operations | Decision |
| --- | --- | --- |
| Sites via Plugin Creator | The Site MCP runtime is a JavaScript/Worker environment. The existing provider is Python; porting or proxying it there adds code and operational components. | Not selected for this Python MCP. |
| Vercel Python Functions | Python/ASGI functions can host an MCP route, but per-instance `/tmp` caches and request pacing are ephemeral. Hobby usage is restricted to personal, non-commercial use; current account plan and intended-use eligibility have not been confirmed. | Possible only after those limits and route behavior are verified. |
| Persistent container host or user-operated server | Runs the existing Starlette/uvicorn entry point, supports a persistent cache, and can keep one process-level IMA pacing queue. | Best fit for code reuse; host and cost remain unselected pending authorization. |

The container is portable across hosts. We have not registered a new hosting
service, selected a paid plan, created a public deployment, or claimed an
endpoint is production-ready. A stable public directory listing needs a
reachable HTTPS MCP URL.

## Local container check

```bash
docker build -t balneabilidade-sc-plugin .
docker run --rm -p 127.0.0.1:8000:8000 \
  -e BALNEABILIDADE_ALLOWED_HOSTS='127.0.0.1,127.0.0.1:*,localhost,localhost:*' \
  -e BALNEABILIDADE_ALLOWED_ORIGINS='http://127.0.0.1:*,http://localhost:*' \
  balneabilidade-sc-plugin
```

The local endpoint is `http://127.0.0.1:8000/mcp`. Do not put that address in
`mcp.json` for distribution. Verify MCP initialization, `tools/list`, and live
tool calls from the connected ChatGPT plugin after deploying to the chosen
host.

## Production environment

Terminate TLS at the host's HTTPS ingress and expose `/mcp`. Set:

- `BALNEABILIDADE_ALLOWED_HOSTS` to the exact stable public hostname and,
  if needed, the matching `:*` form for a proxy that sends a port.
- `BALNEABILIDADE_ALLOWED_ORIGINS` to exact HTTPS origins only when browser
  requests with an `Origin` header are expected.
- `BALNEABILIDADE_CACHE_DIR` to persistent writable storage if the host
  supports it. Cache entries contain public IMA source data, not chat history.
- `PORT` only if the host does not provide it automatically; the app defaults
  to `8000`.

The MCP server is read-only and stateless, but the upstream HTTP request pace is
per process. Use ingress rate limits and keep one replica until a shared cache
and global IMA limiter exist. The application disables access logging and logs
tool error types without request bodies; the chosen host may have separate
transport logs and retention.

## Source dependency

`requirements.txt` pins commit
[`fee46b0`](https://github.com/LucioB16/balneabilidade-sc-mcp/commit/fee46b0990fa4a86aa61c89d5564157b1d97782e),
which adds the remote transport to the upstream `main` branch. Keep this
immutable pin until a deliberate dependency update is validated, then rerun the
container and MCP handshake tests.
