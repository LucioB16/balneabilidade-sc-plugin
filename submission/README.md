# Submission-only facts

The ZIP builder now supports a **package suitable for uploading to the public review portal** before the
reviewer video exists, as permitted by OpenAI's official documentation.
The video is **still required for final MCP review submission**. Do not
commit a completed `metadata.json` if it contains private review details.

The tracked `metadata.template.json` already includes the operator-supplied
name, published legal-page URLs and the verified **non-commerce** behavior.
It deliberately leaves `demo_recording_url: null` and `countries: null`.

For final review, copy `metadata.template.json` to the ignored
`submission/metadata.json` and complete:

- confirm the exact registered developer identity is **Lucio Bottacin**;
- confirm the public privacy and terms URLs load correctly;
- add the actual reviewer-accessible demo recording URL once available;
- choose country availability deliberately: set `countries: []` only if
  unrestricted availability is intended, use an explicit allowlist otherwise,
  or omit with `null` while undecided.

The six legal pages were approved, and GitHub Actions deployed the Pages site
successfully on 2026-11-18:
https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44308178741.
The operator's screenshot confirms the homepage renders. Verify each
privacy/terms URL directly before submitting; an external checker was unable
to fetch them. For the domain challenge required later in the MCP connection
flow, see [DOMAIN_VERIFICATION.md](../docs/DOMAIN_VERIFICATION.md).

The website and support links in `plugin/plugin.json` point to the public
repository and its issue tracker. Check both URLs again before submission.
The MCP URL is passed separately to the archive builder and must be a stable,
public HTTPS production endpoint, never a preview or development tunnel.

Build the plugin ZIP using verified details, without inventing a demo URL:

```bash
python scripts/build_plugin_archive.py \
  --mcp-url "https://balneabilidade-sc.enzonic.dev/mcp" \
  --metadata submission/metadata.template.json
```

Or use the manual GitHub Actions workflow **Build plugin package for public review**
to download the generated ZIP without installing Python locally.

After recording the demo, add its real URL and choose the countries in your
ignored local metadata file. For final review, run the strict version:

```bash
python scripts/build_plugin_archive.py \
  --mcp-url "https://balneabilidade-sc.enzonic.dev/mcp" \
  --metadata submission/metadata.json \
  --require-demo
```

The resulting ZIP is an upload candidate, not an approval or publication.
The OpenAI dashboard initially keeps uploaded packages as drafts regardless of ZIP filename. Complete
review requirements before pressing Submit for review. Leave country targeting
unset until the intended availability is explicitly chosen.
