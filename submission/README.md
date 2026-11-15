# Submission-only facts

The ZIP builder intentionally stops until these values are supplied and
verified. Do not commit a completed `metadata.json` if it contains private
review details.

Copy `metadata.template.json` to the ignored `submission/metadata.json` and set:

- the exact individual/business name already verified in the OpenAI Platform;
- published HTTPS privacy and terms pages that accurately cover the deployed
  service and its chosen host;
- the verified reviewer-accessible demo recording URL;
- the truthful commerce declaration and description;
- intended country codes, or `[]` only if all available countries are intended.

The website and support links in `plugin/plugin.json` point to the public
repository and its issue tracker. Check both URLs again before submission.
The MCP URL is passed separately to the archive builder and must be a stable,
public HTTPS production endpoint, never a preview or development tunnel.

Run the builder only after deployment, policy pages, identity, countries,
commerce details and demo are ready:

```bash
python scripts/build_plugin_archive.py \
  --mcp-url "https://YOUR-STABLE-HOST/mcp" \
  --metadata submission/metadata.json
```

The placeholder above is documentation only and is rejected by the builder.
The resulting ZIP is an upload candidate, not a submission or approval.
