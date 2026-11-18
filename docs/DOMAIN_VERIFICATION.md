# OpenAI domain verification for Enzonic MCP hosting

Source: https://developers.openai.com/plugins/deploy/submission
(see "Domain verification details").

## What OpenAI verifies

OpenAI issues a **specific text token** during MCP connection in the developer
portal. That token must be served verbatim at the URL shown by the portal:

`https://balneabilidade-sc.enzonic.dev/.well-known/openai-apps-challenge`

The challenge is **not** hosted at the GitHub Pages legal website; that has
a different domain. Do not invent, reuse, or commit a challenge token.

## What this PR prepares

A small optional ASGI endpoint in `main.py` answers `GET` and `HEAD`
on `/.well-known/openai-apps-challenge` without touching the MCP `/mcp`
transport or its process-local admission guard.

- When `OPENAI_APPS_CHALLENGE_TOKEN` is **unset**, GET returns HTTP 404.
- When set, GET returns HTTP 200 with the **exact token as text/plain**, no
  JSON, HTML, newline, or additional tokens; caching is disabled.
- Other HTTP methods return HTTP 405.
- Existing MCP calls and non-HTTP ASGI lifespan are passed to the original app.

## Activation — after the portal provides a token

1. Upload the plugin draft ZIP to https://platform.openai.com/plugins and
   select the verified **Individual** developer identity.
2. Go to the new plugin draft's **MCPs** tab → **Connect**. Obtain the actual
   domain-verification token and challenge URL displayed by OpenAI.
3. In Enzonic, back up and deploy the updated repository `main.py` together
   with the existing `guard.py`. **Do not update the Python entry point
   without confirming both files.**
4. In Enzonic Startup environment settings, set
   `OPENAI_APPS_CHALLENGE_TOKEN` to the exact challenge token provided by
   OpenAI (no extra quotes, newline or whitespace).
5. Restart Enzonic once and confirm Uvicorn has started normally.
6. Open the exact challenge URL and verify that the **response body matches
   the token byte-for-byte**. Do not paste the token into a GitHub issue.
7. In the OpenAI portal, complete **Verify domain** / **Connect** and wait
   for the MCP tool scan to finish.
8. Re-run `Manual remote MCP smoke check` or the one-shot MCP client tests.
   Confirm all five tools continue to work.
9. After verification, preserve the challenge token while required by the
   platform; do not rotate/remove it without checking OpenAI's rules.

## Known limitations

- GitHub Pages deployment does not deploy `main.py` to Enzonic. Changes to
  this repo do not automatically update the running instance.
- The verified identity page does not by itself verify the **MCP domain**.
- This change only prepares the challenge route; no token or production
  deployment is performed by this PR.
- The free-host acceptable-use confirmation applies to the current read-only
  data MCP service. No availability or load guarantee was provided.
