# Balneabilidade SC — MCP review test evidence

Observed on **2026-11-17 (America/Argentina/Cordoba)** through the connected
**Balneabilidade SC** MCP tools. Source bulletin is **dated 2026-11-13**.
These observations are dated snapshots; later official publications may differ.

## Evidence sources and limits

Two **different kinds of evidence** exist, and must not be conflated.

1. **Direct MCP tool-layer evidence (2026-11-17)**: the five positive scenarios
   were reproduced by calling the public MCP service directly, with named
   tools and explicit parameters. The [GitHub Actions review run
   #44228356588](https://github.com/LucioB16/balneabilidade-sc-plugin/actions/runs/44228356588)
   passed those direct checks. The dated table below preserves that evidence.
2. **ChatGPT Web browser-run report (2026-11-18)**: the operator relayed the
   output of a separate **DeepSeek Harness + browser-use** session. The prompts
   were entered through the actual authenticated ChatGPT Web interface.
   Its observations are documented separately below **as reported by the
   operator**, not independently audited by this repository update.

**Critical observability limitation:** ChatGPT did not expose tool names or
tool-call cards. Conversation backend inspection was unavailable
(`conversation_inaccessible`, HTTP 404), and the plugin MCP server does not
expose request access logs. Therefore the browser-run response text **cannot
prove** which MCP tools were used, whether all history pages were fetched, or
that any of N1–N3 invoked **no** plugin tool. Tool attribution for the
positive browser-run scenarios is **indirect**.

The originally edited **v1 MP4** was independently inspected: see
[VIDEO_AUDIT_20261118.md](VIDEO_AUDIT_20261118.md). On 2026-11-18
the operator uploaded a revised **v2 MP4**, and the file itself was
independently checked (215 s, H.264, full decode PASS, exact SHA-256 match).
The new video fixes the overlapping caption and includes P5's first failed
attempt and retry, as documented in the
[version 2 audit](VIDEO_AUDIT_V2_20261118.md). Both versions are composites
of actual browser frames/events, **not continuous screen captures**.
Source event files were not independently inspected and **no
reviewer-accessible video URL has been supplied**.

All bathing-water information is **dated published IMA/SC sampling**, not
real-time measurements or a safety guarantee.

## Positive cases — dated tool-layer evidence

| Case | Input / calls executed | Observed result | Layer |
| --- | --- | --- | --- |
| P1 — Perequê | \`search_beaches("Perequê", municipality="Porto Belo")\`; \`get_bathing_status(beach="Praia de Perequê", municipality="Porto Belo")\` | Canonical beach found; **3 points, all proper**; sample **2026-11-09**; bulletin **2026-11-13**; no warnings | PASS (tool layer) |
| P2 — Praia Brava | \`get_bathing_status(beach="Praia Brava", municipality="Florianópolis")\` | **4 points**, **1 improper** (\`Ponto 69\`, sampled **2026-11-11**) and 3 proper; bulletin **2026-11-13**; no warnings | PASS (tool layer) |
| P3 — Campeche 2025 | \`search_beaches("Campeche", municipality="Florianópolis")\`; \`get_bathing_history(beach="Praia do Campeche", from_date="2025-01-01", to_date="2025-12-31")\` with three 50-row paginated requests | Canonical name resolved; **145 records** across **5 points** and **3 pages**: **116 proper, 29 improper**, date range **2025-01-02** through **2025-12-29**; year listed as available, no warnings | PASS (tool layer) |
| P4 — Zimbros | \`get_bathing_status(beach="Praia de Zimbros", municipality="Bombinhas")\` | **2 points**, **1 improper** (\`Ponto 09\`, sampled **2026-11-09**) and 1 proper; bulletin **2026-11-13**; no warnings | PASS (tool layer) |
| P5 — Garopaba | \`search_beaches("Praia de Garopaba", municipality="Garopaba")\`; \`get_bathing_status(beach="Praia de Garopaba", municipality="Garopaba")\` | Canonical beach found; **2 points, both proper**, bulletin **2026-11-13**; no warnings | PASS (tool layer) |

The extra features **\`get_sampling_points\`** and **\`get_bulletin_page\`**
were exercised separately: Perequê returned 3 identified locations, and
page 1 of the 2026-11-13 bulletin rendered successfully. Five distinct tool
types were exercised. The archived review video should demonstrate these
features as well.

### Corrections discovered

- The user-facing phrase **"Praia do Perequê"** is reasonable colloquial
  input but a literal catalog query for \`Praia do Perequê\` returned **no
  matches**. \`search_beaches("Perequê", municipality="Porto Belo")\`
  resolves the official name **Praia de Perequê**. Therefore P1's expected
  tool arguments were corrected *without changing the user's natural prompt*.
- The call \`get_bathing_history(beach="Campeche", ...)\` failed with
  \`no beach matched 'Campeche'\`. Searching \`Campeche\` first resolves the
  canonical **Praia do Campeche**. P3 now explicitly includes
  \`search_beaches\` and pagination via \`next_cursor\`.
- **Do not claim a passed ChatGPT prompt test from a successful raw MCP tool
  call.** The LLM may choose different tools/parameters or omit pagination
  unless verified in the real client.

## ChatGPT Web browser-run — operator report (2026-11-18)

Environment as reported: DeepSeek Harness Desktop `0.2.2-rc.1`,
`browser-use 1.0.6`, `browser-harness 0.1.13`, Edge 157 guest profile,
MCP stdio `browser-use --cli-mcp`. The operator authenticated manually
and selected Balneabilidade SC with the `@` menu; no browser cookies,
tokens or credentials were extracted.

The exact **five positive and three negative** prompts were taken unchanged
from `plugin/plugin.json`. The following statuses refer to **observable
response content**, not independently proven plugin-call traces.

| Case | Browser-run report | Status and unresolved criterion |
| --- | --- | --- |
| P1 — Perequê | 3/3 proper sampling points; report 53 dated 2026-11-13; samples dated 2026-11-09; stated not real-time | **PASS (answer content)**; plugin attribution indirect |
| P2 — Praia Brava | 1 improper of 4, Ponto 69 by the river mouth; sample 2026-11-11; no whole-beach generalization | **PASS (answer content)**; plugin attribution indirect |
| P3 — Campeche 2025 | 145 samples, 5 points, 29 sampling dates, 116 proper / 29 improper, from 2025-01-02 to 2025-12-29 | **PASS (answer content); INCONCLUSIVE (pagination)**: reaching an empty `next_cursor` not observable |
| P4 — Zimbros | Answered in pt-BR; Ponto 09 improper / Ponto 10 proper; samples 2026-11-09, bulletin 2026-11-13 | **PASS (answer content)**; plugin attribution indirect |
| P5 — Garopaba, attempt 1 | Answer was in **Spanish** despite an English prompt | **FAIL (language)** — preserved, not overwritten |
| P5 — Garopaba, attempt 2 | Retry answered in **English**; two proper points, bulletin 2026-11-13, samples 2026-11-10 | **PASS on retry (answer content)**; initial failure remains recorded |
| N1 — Ubatuba / São Paulo | Answered in pt-BR using CETESB data dated 2026-11-12 and noted that São Paulo is handled by CETESB, not IMA/SC | **INCONCLUSIVE (MCP non-invocation)**; other-source response does not prove no MCP call |
| N2 — Waves in Itapoá | Responded with forecast data attributed to Surfnerd and INMET, not bathing-water samples | **INCONCLUSIVE (MCP non-invocation)**; tool use not observable |
| N3 — Perequê parking / showers | Answered the **English** prompt in **Spanish**, citing web information; free parking and public showers were **not independently confirmed** | **INCONCLUSIVE (MCP non-invocation)**; also review language and unsupported-amenity risk |

For N1–N3, **never claim “PASS: did not invoke MCP.”** The expected
no-tool-selection behavior is **unverified**. The browser-run reported
non-plugin content but could not establish the underlying tool trace.

### Local video and evidence manifest (reported, not uploaded)

- Video: `outputs/edited/balneabilidade-sc-walkthrough.mp4`
- Reported format: 104.63 seconds, 1920×1080, H.264; sequence P1–P5 then N1–N3.
- Reported SHA-256 (video only):
  `8D6B60D954C495189614A2981B55FE662AA7796140FB915223D2AF3E56D3450A`
- Per-case clips: `outputs/edited/clips/P1.mp4` through `N3.mp4`
  (reportedly 12.6–13.4 seconds each).
- Machine-local evidence: `outputs/manifest.json` (media and frame/event
  hashes), `outputs/results.json`, `outputs/REVIEW_REPORT.md`.
- Prepared publication files **not uploaded**:
  `outputs/publication/PUBLICATION_CHECKLIST.md`,
  `outputs/publication/metadata.pending.json` (video URL and countries
  unresolved) and `outputs/publication/SHA256SUMS.txt`.
- Video construction: compilation of **real UI frames/events**, **not a
  continuous screen recording**. The reporter says account name/avatar were
  redacted in every included frame; the first P1 frame showing the sidebar
  was excluded. The **v1 MP4 checksum was independently verified**. The corrected **v2**
  MP4 has now also been examined; its hash matches the operator's new
  report and sampled frames show improved presentation with masking.
  Neither media audit is an exhaustive frame-by-frame privacy clearance.
  See [v1 audit](VIDEO_AUDIT_20261118.md) and
  [v2 audit](VIDEO_AUDIT_V2_20261118.md).
- **No video URL, video upload, public media share or review submission.**
  A local filename is not a reviewer-accessible URL.

The OpenAI reviewer needs to understand the editing/observability
limitations. Current official documentation requires a demonstration video
with an accessible URL, but does **not explicitly certify that composites
satisfy review**. Do not assert acceptance before reviewer confirmation.

### How to close the inconclusive criteria

If a definitive no-plugin-use claim is important, rerun N1–N3 while
recording observable **server-side tool-call metadata** (such as tool names
and timestamps, without private prompt contents) for the isolated test
window. Preserve privacy and avoid logging sensitive user data. Likewise,
verify the P3 MCP pagination trace or keep it **INCONCLUSIVE**. The pending
review can be submitted transparently without inventing evidence, but the
reviewer may request a clearer recording or tool-level proof.

## Reproducibility

Run a serial, one-shot live MCP **positive-tool** suite:

~~~sh
python -m scripts.review_cases --timeout 120 --output review-evidence.json
~~~

Or manually run the GitHub Actions workflow:
**Actions → Manual five positive MCP review checks → Run workflow**.
Its run creates a downloadable \`review-tool-evidence\` JSON artifact.

It deliberately does not test negative cases by calling a tool: a
"should not call" scenario is a decision of the ChatGPT model, not an MCP
server response. The 2026-11-18 real-browser run is documented above,
but MCP non-invocation remains inconclusive for N1–N3. See the
[walkthrough](REVIEW_DEMO.md) and preserve this distinction in review notes.

The workflow is opt-in only; it does not probe the host on a schedule.
Keep calls sequential to respect the free-tier service and the process-level
admission guard. If remote traffic starts failing, do not repeatedly rerun
without investigating the failure.

## Sources

- Official IMA/SC portal: https://balneabilidade.ima.sc.gov.br/
- Recorded review prompt inventory: \`plugin/plugin.json\`,
  \`extensions.com.openai.review.test_cases\`
- OpenAI submission requirements:
  https://developers.openai.com/plugins/deploy/submission
- OpenAI ChatGPT plugin testing:
  https://developers.openai.com/plugins/deploy/connect-chatgpt
