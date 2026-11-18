# Balneabilidade SC — MCP review test evidence

Observed on **2026-11-17 (America/Argentina/Cordoba)** through the connected
**Balneabilidade SC** MCP tools. Source bulletin is **dated 2026-11-13**.
These observations are dated snapshots; later official publications may differ.

## Scope and limitations

- **Five positive scenarios: MCP tool-layer checks executed against the live
  Enzonic service.** All five ultimately succeeded using the *canonical*
  identifiers resolved by the IMA/SC catalog.
- **Three negative scenarios: ChatGPT tool-selection checks NOT performed here.**
  A raw MCP tool invocation cannot verify that a language model correctly
  refrains from invoking a plugin for an out-of-scope user request.
- **ChatGPT end-to-end prompt quality / language / tool selection: NOT yet
  verified in a recorded review run.**
- **Video: NOT recorded or uploaded.** The required reviewer-accessible URL
  remains unset. See [REVIEW_DEMO.md](REVIEW_DEMO.md).
- These are tests of functionality, not a guarantee of safety of entering
  the water. IMA/SC values are published samples, not real-time readings.

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

## Negative cases — manual ChatGPT review still needed

| Case | User request | Expected outcome | Actual |
| --- | --- | --- | --- |
| N1 — Outside SC | "Qual é a balneabilidade da Praia Grande em Ubatuba, São Paulo?" | In Portuguese, explain that only beaches monitored in Santa Catarina are available. **Do not invoke MCP.** | PENDING ChatGPT |
| N2 — Waves | "¿Qué altura tendrán las olas mañana en Itapoá?" | Explain that bathing-water sampling is not a wave forecast. **Do not invoke MCP.** | PENDING ChatGPT |
| N3 — Parking | "Is there free parking and a public shower at Praia do Perequê in Porto Belo?" | Do not invent amenities. State that this plugin has no verified facility data. **Do not invoke MCP.** | PENDING ChatGPT |

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
server response. Run N1–N3 in ChatGPT and record the selected tools and user
responses, as described in the [walkthrough](REVIEW_DEMO.md).

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
