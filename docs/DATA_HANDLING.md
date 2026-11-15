# Data-handling facts for policy drafting

This is an implementation description, not a privacy policy or terms of
service. Do not submit it as a legal document without reviewing the choices and
practices of the selected host.

## Verified behavior in the code

- The MCP server has no user account, database, analytics integration, or
  conversation-history store.
- Tool inputs identify a beach, municipality, sampling point, date range, or
  bulletin page. The provider uses those inputs to search the IMA/SC catalog or
  request the public IMA/SC portal data needed for the result.
- The provider's TTL cache stores catalog, bulletin, analysis, and history
  source data from IMA/SC. It does not store ChatGPT conversations. Cache
  location and persistence are controlled by `BALNEABILIDADE_CACHE_DIR` and
  the chosen host.
- The application does not log MCP request bodies. On a tool failure it logs
  only the exception type. The Uvicorn entry point disables its access log.
- Enzonic hosts the current public MCP endpoint and may separately record
  network, access, and operational metadata. The provider's actual log retention,
  visibility, and data-processing terms have not been verified for this deployment.
  The app-level Uvicorn access log remains disabled.
- IMA/SC is the official data source; the project is independent and does not
  represent agency endorsement.

## Facts still needed for a public policy

Before publication, the operator must review and state Enzonic's
logging/retention settings, how support requests are handled, and the applicable
terms and contact details. The repository does not publish or link a privacy
policy or terms page yet.
